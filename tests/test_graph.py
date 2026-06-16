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


class TestToolInvocation:
    def test_tool_calls_execute_and_appear_in_trace(self):
        """A subagent tool call is routed to the ToolNode and yields a ToolMessage."""
        from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
        from langchain_core.messages import AIMessage, ToolMessage

        from main import build_graph

        tool_call = {
            "name": "read_obsidian_page",
            "args": {"page_name": "hot_polygons"},
            "id": "call_1",
            "type": "tool_call",
        }
        responses = [
            AIMessage(content="", tool_calls=[tool_call]),  # Alpha -> AlphaTools
            AIMessage(content="alpha done"),                # Alpha -> Gatekeeper
            AIMessage(content="beta done"),                 # Beta  -> END
        ]
        app = build_graph(llm=FakeMessagesListChatModel(responses=responses))

        tool_messages = [
            msg
            for event in app.stream(_initial_state())
            for update in event.values()
            if isinstance(update, dict)
            for msg in update.get("messages", [])
            if isinstance(msg, ToolMessage)
        ]
        assert tool_messages, "Expected a ToolMessage from the AlphaTools node in the trace"
        assert tool_messages[0].name == "read_obsidian_page"
