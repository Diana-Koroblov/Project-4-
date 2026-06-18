"""Repair Groq ``tool_use_failed`` errors into well-formed tool calls.

The Llama models on Groq sometimes serialize a tool call in their raw
``<function=NAME{...json...}</function>`` syntax instead of the structured
``tool_calls`` the server expects. Groq then rejects the generation with a 400
``tool_use_failed`` error whose body carries the offending text under
``error.failed_generation``.

This module parses that payload back into proper ``tool_calls`` and re-emits it as
an ``AIMessage`` so the LangGraph tool loop proceeds exactly as if the model had
formatted the call correctly. It is inert for any model that already returns
structured tool calls (e.g. the fakes used in tests), because it only activates
when an ``invoke`` raises an exception whose body is a ``tool_use_failed`` error.
"""

from __future__ import annotations

import json
import re
from typing import Any
from uuid import uuid4

from langchain_core.messages import AIMessage, BaseMessage

# Matches the start of a Llama function tag and captures the tool name. The
# argument JSON object that follows is extracted separately by a brace scan so
# that braces inside string values (e.g. an f-string in written source) are safe.
_FUNCTION_RE = re.compile(r"<(?:function=|\|python_tag\|>?)\s*([\w.\-]+)?")


def _extract_json_object(text: str, start: int) -> tuple[str, int] | None:
    """Return the balanced ``{...}`` substring beginning at/after ``start``.

    Scans respecting double-quoted strings and backslash escapes so that braces
    inside string values do not end the object early. Returns ``(json, end)`` or
    ``None`` if no balanced object is found.
    """
    open_idx = text.find("{", start)
    if open_idx == -1:
        return None
    depth = 0
    in_string = False
    escaped = False
    for i in range(open_idx, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[open_idx : i + 1], i + 1
    return None


def _loads_lenient(blob: str) -> dict[str, Any] | None:
    """Parse ``blob`` as JSON, with a small fallback for Python-ish literals."""
    try:
        return json.loads(blob)
    except json.JSONDecodeError:
        patched = re.sub(r"\bNone\b", "null", blob)
        patched = re.sub(r"\bTrue\b", "true", patched)
        patched = re.sub(r"\bFalse\b", "false", patched)
        try:
            return json.loads(patched)
        except json.JSONDecodeError:
            return None


def parse_tool_calls(failed_generation: str) -> list[dict]:
    """Parse a Groq ``failed_generation`` payload into structured tool calls."""
    tool_calls: list[dict] = []
    for match in _FUNCTION_RE.finditer(failed_generation):
        name = match.group(1)
        extracted = _extract_json_object(failed_generation, match.end())
        if extracted is None:
            continue
        blob, _ = extracted
        args = _loads_lenient(blob)
        if args is None:
            continue
        # The <|python_tag|> form encodes name/args inside the JSON itself.
        if not name and isinstance(args.get("name"), str):
            name = args["name"]
            args = args.get("parameters") or args.get("arguments") or {}
        if not name:
            continue
        tool_calls.append(
            {
                "name": name,
                "args": args,
                "id": f"call_{len(tool_calls)}_{uuid4().hex[:8]}",
                "type": "tool_call",
            }
        )
    return tool_calls


def tool_use_failed_message(exc: Exception) -> AIMessage | None:
    """Build a repaired ``AIMessage`` from a ``tool_use_failed`` exception.

    Returns ``None`` if ``exc`` is not a Groq ``tool_use_failed`` error. If the
    payload cannot be parsed into any tool call, returns an ``AIMessage`` holding
    the raw text so the graph terminates gracefully instead of crashing.
    """
    body = getattr(exc, "body", None)
    if not isinstance(body, dict):
        return None
    error = body.get("error")
    if not isinstance(error, dict) or error.get("code") != "tool_use_failed":
        return None

    failed = error.get("failed_generation") or ""
    tool_calls = parse_tool_calls(failed)
    if tool_calls:
        return AIMessage(content="", tool_calls=tool_calls, id=str(uuid4()))
    return AIMessage(content=failed, id=str(uuid4()))


def invoke_with_repair(model: Any, messages: list[BaseMessage]) -> BaseMessage:
    """Invoke ``model``; on a Groq ``tool_use_failed`` error, repair and return.

    Any other exception is re-raised unchanged.
    """
    try:
        return model.invoke(messages)
    except Exception as exc:  # noqa: BLE001 - only tool_use_failed is handled; rest re-raised
        repaired = tool_use_failed_message(exc)
        if repaired is not None:
            return repaired
        raise
