"""hw4.gateway — central API gatekeeper and rate limiting (§5).

All external API calls flow through :class:`ApiGatekeeper`, which enforces
config-driven rate limits, queues overflow, retries transient failures, and
logs every call. :func:`wrap_with_gatekeeper` attaches it to a chat model.
"""

from hw4.gateway.config import RateLimitConfig, load_rate_limit_config
from hw4.gateway.gatekeeper import ApiGatekeeper, BackpressureError, get_gatekeeper
from hw4.gateway.llm_proxy import GatekeptChatModel, estimate_tokens, wrap_with_gatekeeper
from hw4.gateway.overflow_queue import OverflowQueue
from hw4.gateway.rate_limiter import SlidingWindowRateLimiter

__all__ = [
    "ApiGatekeeper",
    "BackpressureError",
    "GatekeptChatModel",
    "OverflowQueue",
    "RateLimitConfig",
    "SlidingWindowRateLimiter",
    "estimate_tokens",
    "get_gatekeeper",
    "load_rate_limit_config",
    "wrap_with_gatekeeper",
]
