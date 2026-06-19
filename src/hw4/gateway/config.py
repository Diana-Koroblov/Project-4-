"""Load API rate-limit settings from ``config/rate_limits.json``.

Per §5.2, every rate limit is read from configuration — never hardcoded in
source. This module turns one provider's JSON section into an immutable
:class:`RateLimitConfig` that the gatekeeper consumes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from hw4.constants import CONFIG_RATE_LIMITS_PATH, DEFAULT_POLL_INTERVAL_SECONDS


@dataclass(frozen=True)
class RateLimitConfig:
    """Immutable rate-limit settings for a single API provider."""

    provider: str
    requests_per_minute: int
    tokens_per_minute: int
    max_retries: int
    retry_backoff_seconds: float
    queue_max_size: int
    poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS


def load_rate_limit_config(
    provider: str, path: str = CONFIG_RATE_LIMITS_PATH
) -> RateLimitConfig:
    """Read ``path`` and return the :class:`RateLimitConfig` for ``provider``.

    Raises:
        FileNotFoundError: if the config file is missing.
        KeyError: if ``provider`` has no section in the config.
    """
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(
            f"Rate-limit config not found: {config_path}. "
            "It must exist so no rate limits are hardcoded in source."
        )
    data = json.loads(config_path.read_text(encoding="utf-8"))
    if provider not in data:
        raise KeyError(f"No rate limits configured for provider {provider!r} in {config_path}")

    section = data[provider]
    return RateLimitConfig(
        provider=provider,
        requests_per_minute=int(section["requests_per_minute"]),
        tokens_per_minute=int(section["tokens_per_minute"]),
        max_retries=int(section.get("max_retries", 0)),
        retry_backoff_seconds=float(section.get("retry_backoff_seconds", 0.0)),
        queue_max_size=int(section["queue_max_size"]),
        poll_interval=float(
            section.get("poll_interval_seconds", DEFAULT_POLL_INTERVAL_SECONDS)
        ),
    )
