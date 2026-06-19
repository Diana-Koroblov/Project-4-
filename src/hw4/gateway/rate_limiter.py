"""Thread-safe sliding-window rate limiter (requests/min and tokens/min).

Enforces both an RPM and a TPM ceiling over a rolling window. ``try_acquire``
records a call if capacity exists; ``retry_after`` reports how long the caller
must wait for the oldest entries to age out — i.e. when the window resets. All
state is guarded by a lock so multiple worker threads share one limiter safely.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Callable

from hw4.constants import RATE_LIMIT_WINDOW_SECONDS


class SlidingWindowRateLimiter:
    """Rolling-window limiter over request count and token volume."""

    def __init__(
        self,
        requests_per_minute: int,
        tokens_per_minute: int,
        *,
        window: float = RATE_LIMIT_WINDOW_SECONDS,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._rpm = requests_per_minute
        self._tpm = tokens_per_minute
        self._window = window
        self._clock = clock
        self._lock = threading.Lock()
        self._requests: deque[float] = deque()
        self._tokens: deque[tuple[float, int]] = deque()
        self._token_sum = 0

    def _prune(self, now: float) -> None:
        """Drop entries older than the window (caller holds the lock)."""
        cutoff = now - self._window
        while self._requests and self._requests[0] <= cutoff:
            self._requests.popleft()
        while self._tokens and self._tokens[0][0] <= cutoff:
            self._token_sum -= self._tokens.popleft()[1]

    def try_acquire(self, tokens: int) -> bool:
        """Record a call of ``tokens`` size if both ceilings allow it."""
        with self._lock:
            now = self._clock()
            self._prune(now)
            if len(self._requests) >= self._rpm:
                return False
            if self._token_sum + tokens > self._tpm:
                return False
            self._requests.append(now)
            self._tokens.append((now, tokens))
            self._token_sum += tokens
            return True

    def retry_after(self, tokens: int) -> float:
        """Seconds until a call of ``tokens`` size could be admitted (0 if now)."""
        with self._lock:
            now = self._clock()
            self._prune(now)
            waits: list[float] = []
            if len(self._requests) >= self._rpm:
                waits.append(self._requests[0] + self._window - now)
            if self._token_sum + tokens > self._tpm:
                waits.append(self._token_release_wait(now, tokens))
            return max(0.0, max(waits)) if waits else 0.0

    def _token_release_wait(self, now: float, tokens: int) -> float:
        """When enough buffered tokens age out to fit ``tokens`` (holds lock)."""
        needed = self._token_sum + tokens - self._tpm
        freed = 0
        for ts, tk in self._tokens:
            freed += tk
            if freed >= needed:
                return ts + self._window - now
        return self._window
