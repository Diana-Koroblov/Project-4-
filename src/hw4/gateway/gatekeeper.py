"""Central API gatekeeper (§5.1) — the sole entry point for external calls.

Every outbound API call is submitted here. The gatekeeper enforces the
configured rate limits before each call, parks overflow in a bounded FIFO queue
and drains it as the rate window resets, retries transient failures with
exponential backoff, and logs every admission/outcome for monitoring.
"""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable
from typing import Any

from hw4.constants import CONFIG_RATE_LIMITS_PATH, GATEWAY_LOGGER_NAME
from hw4.gateway.config import RateLimitConfig, load_rate_limit_config
from hw4.gateway.overflow_queue import OverflowQueue
from hw4.gateway.rate_limiter import SlidingWindowRateLimiter


class BackpressureError(RuntimeError):
    """Raised when the overflow queue is full and no admission can be granted."""


def _is_retryable(exc: Exception) -> bool:
    """Transient errors (429/503, timeouts) are retried; 4xx like 400 are not."""
    status = getattr(exc, "status_code", None)
    if status in (429, 503):
        return True
    if isinstance(exc, (ConnectionError, TimeoutError)):
        return True
    text = str(exc).lower()
    return "rate limit" in text or "rate_limit" in text or "timeout" in text


class ApiGatekeeper:
    """Rate-limited, queued, retrying front door for one provider's API."""

    def __init__(
        self,
        config: RateLimitConfig,
        *,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
        logger: logging.Logger | None = None,
    ) -> None:
        self._cfg = config
        self._sleep = sleep
        self._logger = logger or logging.getLogger(GATEWAY_LOGGER_NAME)
        self._limiter = SlidingWindowRateLimiter(
            config.requests_per_minute, config.tokens_per_minute, clock=clock
        )
        self._queue = OverflowQueue(config.queue_max_size, logger=self._logger)

    def submit(self, fn: Callable[..., Any], *args: Any, estimated_tokens: int, **kwargs: Any) -> Any:
        """Admit (waiting if rate-limited), then run ``fn`` with retries."""
        if estimated_tokens > self._cfg.tokens_per_minute:
            raise ValueError(
                f"Request needs ~{estimated_tokens} tokens, exceeding the "
                f"{self._cfg.tokens_per_minute} tokens/min ceiling; cannot ever admit."
            )
        self._await_capacity(estimated_tokens)
        return self._call_with_retries(fn, args, kwargs)

    def _await_capacity(self, tokens: int) -> None:
        """Queue this call and block until the limiter grants it (FIFO drain)."""
        ticket = object()
        if not self._queue.enqueue(ticket):
            raise BackpressureError("API gateway queue is full; shed load and retry later.")
        try:
            while not (self._queue.peek() is ticket and self._limiter.try_acquire(tokens)):
                wait = self._limiter.retry_after(tokens)
                nap = self._cfg.poll_interval if wait <= 0 else min(wait, self._cfg.poll_interval)
                self._sleep(nap)
            self._logger.info(
                "Gateway admit | provider=%s | tokens~%d | queued=%d",
                self._cfg.provider, tokens, len(self._queue),
            )
        finally:
            self._queue.remove(ticket)

    def _call_with_retries(self, fn: Callable[..., Any], args: tuple, kwargs: dict) -> Any:
        """Run ``fn``, retrying only transient errors up to ``max_retries``."""
        for attempt in range(self._cfg.max_retries + 1):
            try:
                result = fn(*args, **kwargs)
                self._logger.info("Gateway call ok | provider=%s | attempt=%d", self._cfg.provider, attempt + 1)
                return result
            except Exception as exc:  # noqa: BLE001 - re-raised below unless retryable
                if not _is_retryable(exc) or attempt >= self._cfg.max_retries:
                    self._logger.error("Gateway call failed | attempt=%d | %s", attempt + 1, exc)
                    raise
                backoff = self._cfg.retry_backoff_seconds * (2**attempt)
                self._logger.warning(
                    "Gateway retry | attempt=%d | backoff=%.1fs | %s", attempt + 1, backoff, exc
                )
                self._sleep(backoff)


_GATEKEEPERS: dict[str, ApiGatekeeper] = {}
_REGISTRY_LOCK = threading.Lock()


def get_gatekeeper(provider: str, *, path: str = CONFIG_RATE_LIMITS_PATH) -> ApiGatekeeper:
    """Return the process-wide gatekeeper for ``provider`` (built once, reused)."""
    with _REGISTRY_LOCK:
        gatekeeper = _GATEKEEPERS.get(provider)
        if gatekeeper is None:
            gatekeeper = ApiGatekeeper(load_rate_limit_config(provider, path))
            _GATEKEEPERS[provider] = gatekeeper
        return gatekeeper
