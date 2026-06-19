"""Tests for the GatekeptChatModel proxy and token estimation."""

from langchain_core.messages import HumanMessage

from hw4.gateway.llm_proxy import GatekeptChatModel, estimate_tokens, wrap_with_gatekeeper


class FakeGatekeeper:
    """Records submissions and just runs the function (no rate limiting)."""

    def __init__(self):
        self.calls = []

    def submit(self, fn, *args, estimated_tokens, **kwargs):
        self.calls.append(estimated_tokens)
        return fn(*args, **kwargs)


class FakeModel:
    """Minimal chat-model stand-in supporting invoke and bind_tools."""

    def __init__(self, name="fake"):
        self.name = name
        self.bound = None

    def invoke(self, messages, config=None, **kwargs):
        return f"echo:{messages}"

    def bind_tools(self, tools, **kwargs):
        self.bound = tools
        return FakeModel(name="bound")

    def bind(self, **kwargs):
        return FakeModel(name="bound-kwargs")


def test_estimate_tokens_from_messages():
    msgs = [HumanMessage(content="a" * 40)]
    assert estimate_tokens(msgs) == 10  # 40 chars / 4


def test_estimate_tokens_minimum_one():
    assert estimate_tokens([]) == 1


def test_estimate_tokens_handles_non_iterable():
    # A non-iterable input (e.g. a stray scalar) must not crash estimation.
    assert estimate_tokens(12345) == 1


def test_invoke_routes_through_gatekeeper():
    gk = FakeGatekeeper()
    proxy = GatekeptChatModel(FakeModel(), gk, "groq")
    out = proxy.invoke([HumanMessage(content="hello world")])
    assert out.startswith("echo:")
    assert len(gk.calls) == 1  # exactly one gated submission


def test_bind_tools_returns_gatekept_wrapper():
    gk = FakeGatekeeper()
    proxy = GatekeptChatModel(FakeModel(), gk, "groq")
    bound = proxy.bind_tools(["tool_a"])
    assert isinstance(bound, GatekeptChatModel)
    # The bound child still routes through the same gatekeeper.
    bound.invoke([HumanMessage(content="x")])
    assert len(gk.calls) == 1


def test_bind_keeps_result_gatekept():
    # `.bind(max_tokens=...)` (used by live_efficiency) must stay gatekept so the
    # bound model's invoke does not bypass the gatekeeper (§5.1).
    gk = FakeGatekeeper()
    proxy = GatekeptChatModel(FakeModel(), gk, "groq")
    bound = proxy.bind(max_tokens=512)
    assert isinstance(bound, GatekeptChatModel)
    bound.invoke([HumanMessage(content="x")])
    assert len(gk.calls) == 1


def test_getattr_delegates_to_inner():
    proxy = GatekeptChatModel(FakeModel(name="inner"), FakeGatekeeper(), "groq")
    assert proxy.name == "inner"


def test_wrap_with_gatekeeper_uses_real_config():
    proxy = wrap_with_gatekeeper(FakeModel(), "groq")
    assert isinstance(proxy, GatekeptChatModel)
    # Routing a call should not raise with the committed groq limits.
    assert proxy.invoke([HumanMessage(content="hi")]).startswith("echo:")
