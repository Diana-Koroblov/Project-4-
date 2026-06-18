"""Offline tests for the Groq tool_use_failed repair shim (no network)."""

import json

import pytest
from langchain_core.messages import AIMessage

from hw4.tools.tool_call_repair import (
    invoke_with_repair,
    parse_tool_calls,
    tool_use_failed_message,
)


class _FakeModel:
    """Minimal stand-in: returns a canned message, never raises."""

    def __init__(self, message):
        self._message = message

    def invoke(self, messages):
        return self._message


class _BadRequest(Exception):
    """Stub mirroring groq.BadRequestError: carries a decoded `.body` dict."""

    def __init__(self, body):
        super().__init__("400")
        self.body = body


def _tool_use_failed(failed_generation: str) -> _BadRequest:
    return _BadRequest(
        {"error": {"code": "tool_use_failed", "failed_generation": failed_generation}}
    )


class TestParseToolCalls:
    def test_single_function_tag(self):
        payload = '<function=read_obsidian_page{"page_name": "hot_polygons"}</function>'
        calls = parse_tool_calls(payload)
        assert len(calls) == 1
        assert calls[0]["name"] == "read_obsidian_page"
        assert calls[0]["args"] == {"page_name": "hot_polygons"}
        assert calls[0]["type"] == "tool_call"
        assert calls[0]["id"]

    def test_multiple_function_tags(self):
        payload = (
            '<function=read_obsidian_page{"page_name": "hot_polygons"}</function>'
            '<function=read_source_file{"path": "polygons/polygons.py"}</function>'
        )
        calls = parse_tool_calls(payload)
        assert [c["name"] for c in calls] == ["read_obsidian_page", "read_source_file"]
        # IDs must be unique so ToolMessages map back correctly.
        assert calls[0]["id"] != calls[1]["id"]

    def test_content_with_braces_is_not_truncated(self):
        # write_source_file content contains f-string braces — a non-greedy
        # regex would split the JSON here; the balanced scan must not.
        content = 'print(f"Question {number}: {a} x {b}")\nif x == 1:\n    pass\n'
        payload = "<function=write_source_file" + json.dumps(
            {"path": "mathsquiz/mathsquiz.py", "content": content}
        ) + "</function>"
        calls = parse_tool_calls(payload)
        assert len(calls) == 1
        assert calls[0]["name"] == "write_source_file"
        assert calls[0]["args"]["content"] == content

    def test_python_tag_form(self):
        payload = '<|python_tag|>{"name": "read_source_file", "parameters": {"path": "polygons/polygons.py"}}'
        calls = parse_tool_calls(payload)
        assert len(calls) == 1
        assert calls[0]["name"] == "read_source_file"
        assert calls[0]["args"] == {"path": "polygons/polygons.py"}

    def test_unparseable_payload_yields_no_calls(self):
        assert parse_tool_calls("just some prose, no tool call here") == []

    def test_lenient_parse_of_python_literals(self):
        # Llama sometimes emits Python literals (None/True) instead of JSON.
        payload = '<function=foo{"a": None, "b": True, "c": False}</function>'
        calls = parse_tool_calls(payload)
        assert calls[0]["args"] == {"a": None, "b": True, "c": False}

    def test_function_tag_without_json_is_skipped(self):
        assert parse_tool_calls("<function=foo>no args here") == []

    def test_unbalanced_braces_are_skipped(self):
        assert parse_tool_calls('<function=foo{"a": 1') == []

    def test_unparseable_json_object_is_skipped(self):
        assert parse_tool_calls("<function=foo{not valid json at all}</function>") == []

    def test_python_tag_without_name_is_skipped(self):
        assert parse_tool_calls('<|python_tag|>{"unrelated": "value"}') == []


class TestToolUseFailedMessage:
    def test_repairs_into_tool_calls(self):
        exc = _tool_use_failed('<function=read_obsidian_page{"page_name": "hot_polygons"}</function>')
        msg = tool_use_failed_message(exc)
        assert isinstance(msg, AIMessage)
        assert msg.tool_calls[0]["name"] == "read_obsidian_page"
        assert msg.id

    def test_unparseable_failed_generation_falls_back_to_content(self):
        exc = _tool_use_failed("garbled <function with no json")
        msg = tool_use_failed_message(exc)
        assert isinstance(msg, AIMessage)
        assert not msg.tool_calls
        assert "garbled" in msg.content

    def test_non_tool_use_failed_returns_none(self):
        assert tool_use_failed_message(_BadRequest({"error": {"code": "rate_limit_exceeded"}})) is None

    def test_exception_without_body_returns_none(self):
        assert tool_use_failed_message(ValueError("boom")) is None


class TestInvokeWithRepair:
    def test_passthrough_when_model_succeeds(self):
        expected = AIMessage(content="all good")
        assert invoke_with_repair(_FakeModel(expected), []) is expected

    def test_repairs_on_tool_use_failed(self):
        class _Raises:
            def invoke(self, messages):
                raise _tool_use_failed('<function=read_obsidian_page{"page_name": "hot_polygons"}</function>')

        msg = invoke_with_repair(_Raises(), [])
        assert isinstance(msg, AIMessage)
        assert msg.tool_calls[0]["args"] == {"page_name": "hot_polygons"}

    def test_reraises_other_errors(self):
        class _Raises:
            def invoke(self, messages):
                raise RuntimeError("network down")

        with pytest.raises(RuntimeError, match="network down"):
            invoke_with_repair(_Raises(), [])
