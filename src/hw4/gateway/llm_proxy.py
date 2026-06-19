"""Route a chat model's API calls through the :class:`ApiGatekeeper`.

:func:`wrap_with_gatekeeper` returns a thin proxy whose ``invoke`` (and the
``invoke`` of any tool-bound child it produces) is submitted to the gatekeeper.
This is how §5.1's "no direct API calls that bypass the gatekeeper" is enforced
for the real Groq model while leaving test doubles untouched.
"""

from __future__ import annotations

from typing import Any

from hw4.constants import CHARS_PER_TOKEN, CONFIG_RATE_LIMITS_PATH
from hw4.gateway.gatekeeper import ApiGatekeeper, get_gatekeeper


def estimate_tokens(messages: Any) -> int:
    """Rough pre-call token estimate (tokens ≈ chars / 4) used for accounting."""
    try:
        text = " ".join(str(getattr(m, "content", m)) for m in messages)
    except TypeError:
        text = str(messages)
    return max(1, len(text) // CHARS_PER_TOKEN)


class GatekeptChatModel:
    """Proxy delegating to ``inner`` but submitting ``invoke`` to the gatekeeper."""

    def __init__(self, inner: Any, gatekeeper: ApiGatekeeper, provider: str) -> None:
        self._inner = inner
        self._gatekeeper = gatekeeper
        self._provider = provider

    def bind_tools(self, tools: Any, **kwargs: Any) -> "GatekeptChatModel":
        """Bind tools on the inner model, keeping the result gatekept."""
        bound = self._inner.bind_tools(tools, **kwargs)
        return GatekeptChatModel(bound, self._gatekeeper, self._provider)

    def bind(self, **kwargs: Any) -> "GatekeptChatModel":
        """Bind runtime kwargs (e.g. max_tokens) while staying gatekept.

        Without this, ``.bind()`` would fall through to the inner model and
        return an un-gatekept runnable whose ``invoke`` bypasses §5.1.
        """
        return GatekeptChatModel(self._inner.bind(**kwargs), self._gatekeeper, self._provider)

    def invoke(self, input: Any, config: Any = None, **kwargs: Any) -> Any:
        """Submit the underlying ``invoke`` through the gatekeeper."""
        tokens = estimate_tokens(input)
        return self._gatekeeper.submit(
            self._inner.invoke, input, config, estimated_tokens=tokens, **kwargs
        )

    def __getattr__(self, name: str) -> Any:
        # Delegate everything else (e.g. model metadata) to the wrapped model.
        return getattr(self._inner, name)


def wrap_with_gatekeeper(
    model: Any, provider: str, *, path: str = CONFIG_RATE_LIMITS_PATH
) -> GatekeptChatModel:
    """Wrap ``model`` so all its API calls pass through ``provider``'s gatekeeper."""
    return GatekeptChatModel(model, get_gatekeeper(provider, path=path), provider)
