"""Tests for the public SDK facade (§4.1 — all operations via GraphifySDK)."""

import json

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models.fake_chat_models import (
    FakeListChatModel,
    FakeMessagesListChatModel,
)
from langchain_core.messages import AIMessage

from hw4.sdk import DEFAULT_SEED, GraphifySDK, RepairResult, __version__

_GRAPH = {
    "nodes": [
        {"id": "a", "label": "A"},
        {"id": "b", "label": "B"},
        {"id": "lonely", "label": "Lonely"},
    ],
    "links": [{"source": "a", "target": "b"}],
}


def _fake_repair_llm():
    tool_call = {
        "name": "read_obsidian_page",
        "args": {"page_name": "hot_polygons"},
        "id": "call_1",
        "type": "tool_call",
    }
    return FakeMessagesListChatModel(
        responses=[
            AIMessage(content="", tool_calls=[tool_call]),  # Alpha -> AlphaTools
            AIMessage(content="alpha done"),  # Alpha -> Gatekeeper
            AIMessage(content="beta done"),  # Beta  -> END
        ]
    )


def test_exports_version_and_seed():
    assert __version__ == "1.00"
    assert "investigation" in DEFAULT_SEED


def test_build_graph_with_injected_llm():
    sdk = GraphifySDK(llm=FakeListChatModel(responses=["x", "y"]))
    mermaid = sdk.graph_diagram()
    for name in ("Router", "SubagentAlpha", "Gatekeeper", "SubagentBeta"):
        assert name in mermaid


def test_run_repair_collects_structured_result():
    sdk = GraphifySDK(llm=_fake_repair_llm())
    result = sdk.run_repair()
    assert isinstance(result, RepairResult)
    # Tool call collected exactly once despite appearing in several snapshots.
    assert result.tool_calls == ["read_obsidian_page"]
    assert result.current_phase == "mathsquiz"
    assert "beta:mathsquiz:complete" in result.completed_tasks
    assert "phase:polygons:complete" in result.completed_tasks
    assert result.final_message == "beta done"


def test_run_repair_without_tool_calls():
    sdk = GraphifySDK(llm=FakeListChatModel(responses=["alpha done", "beta done"]))
    result = sdk.run_repair(seed="go")
    assert result.tool_calls == []
    assert "alpha:polygons:complete" in result.completed_tasks


def test_run_repair_threads_callbacks_through():
    """A callback passed to the controller is wired into the stream config."""

    class RecordingHandler(BaseCallbackHandler):
        def __init__(self):
            self.starts = 0

        def on_chat_model_start(self, *args, **kwargs):
            self.starts += 1

        def on_llm_start(self, *args, **kwargs):
            self.starts += 1

    handler = RecordingHandler()
    sdk = GraphifySDK(llm=FakeListChatModel(responses=["alpha done", "beta done"]))
    result = sdk.run_repair(callbacks=[handler])
    assert result.current_phase == "mathsquiz"
    assert handler.starts >= 1  # the handler observed at least one LLM call


def test_get_llm_uses_override_without_calling_provider(monkeypatch):
    import hw4.llm_config as llm_config

    def _boom():
        raise AssertionError("get_llm() must not be called when an llm is injected")

    monkeypatch.setattr(llm_config, "get_llm", _boom)
    sdk = GraphifySDK(llm="sentinel-model")
    assert sdk.get_llm() == "sentinel-model"


def test_get_llm_builds_once_and_caches(monkeypatch):
    calls = {"n": 0}

    def _fake_get_llm():
        calls["n"] += 1
        return "built-llm"

    monkeypatch.setattr("hw4.llm_config.get_llm", _fake_get_llm)
    sdk = GraphifySDK()
    assert sdk.get_llm() == "built-llm"
    assert sdk.get_llm() == "built-llm"
    assert calls["n"] == 1  # built once, then cached


def test_compare_efficiency_returns_reductions():
    stats = GraphifySDK().compare_efficiency()
    assert stats["input_reduction"] > 0
    assert stats["baseline"]["tokens_in"] > stats["guided"]["tokens_in"]


def test_detect_and_report_orphans(tmp_path):
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(_GRAPH), encoding="utf-8")
    out_path = tmp_path / "orphans.md"

    sdk = GraphifySDK()
    orphans = sdk.detect_orphans(str(graph_path), threshold=1)
    labels = {o.label for o in orphans}
    assert "Lonely" in labels  # 0 edges

    count = sdk.report_orphans(str(graph_path), str(out_path), threshold=1)
    assert count == len(orphans)
    assert out_path.exists()
    assert "Orphan Node Report" in out_path.read_text(encoding="utf-8")


def test_repair_result_defaults():
    result = RepairResult()
    assert result.completed_tasks == []
    assert result.tool_calls == []
    assert result.current_phase is None
