"""Dry-run smoke tests for the LangGraph orchestration pipeline.

Uses FakeListChatModel so no real API key is required.
"""

import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel

from hw4.state import AgentState


def _initial_state() -> AgentState:
    return {
        "current_phase": "",
        "messages": [],
        "errors": [],
        "completed_tasks": [],
        "token_log": [],
    }


@pytest.fixture
def fake_llm():
    return FakeListChatModel(responses=["Polygons analysis done.", "Math Quiz analysis done."])


@pytest.fixture
def app(fake_llm):
    from main import build_graph
    return build_graph(llm=fake_llm)


class TestGraphCompilation:
    def test_mermaid_contains_all_nodes(self, app):
        """draw_mermaid() output includes all five expected node identifiers."""
        mermaid = app.get_graph().draw_mermaid()
        for name in ("Router", "SubagentAlpha", "Gatekeeper", "SubagentBeta"):
            assert name in mermaid, f"Node '{name}' missing from Mermaid output"


class TestGraphTraversal:
    def test_final_phase_is_mathsquiz(self, app):
        """After a full run the current_phase must be 'mathsquiz' (set by Gatekeeper)."""
        result = app.invoke(_initial_state())
        assert result["current_phase"] == "mathsquiz"

    def test_all_completed_task_markers_present(self, app):
        """Router, Alpha, Gatekeeper, and Beta each leave their marker in completed_tasks."""
        result = app.invoke(_initial_state())
        tasks = result["completed_tasks"]
        assert "alpha:polygons:complete" in tasks
        assert "phase:polygons:complete" in tasks
        assert "beta:mathsquiz:complete" in tasks

    def test_gatekeeper_clears_alpha_messages(self, app):
        """After the full run only Beta's single message remains (Alpha's was purged)."""
        result = app.invoke(_initial_state())
        assert len(result["messages"]) == 1
        assert result["messages"][0].content == "Math Quiz analysis done."

    def test_token_log_seeded_by_router(self, app):
        """Router seeds token_log with at least one entry."""
        result = app.invoke(_initial_state())
        assert len(result["token_log"]) >= 1
        assert result["token_log"][0]["event"] == "router_loaded_index"
