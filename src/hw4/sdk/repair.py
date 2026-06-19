"""Run the compiled repair graph end-to-end and collect a structured result.

The streaming/collection logic lives here (not in the entry-point script) so the
``run_live_agent.py`` controller is a thin layer that delegates to :mod:`hw4.sdk`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from langchain_core.messages import HumanMessage, ToolMessage

DEFAULT_SEED = (
    "Begin the investigation. Follow your Obsidian entry page and fix the bugs "
    "in your domain."
)
_PREVIEW_CHARS = 400


@dataclass
class RepairResult:
    """Structured outcome of one end-to-end repair run."""

    completed_tasks: list[str] = field(default_factory=list)
    current_phase: str | None = None
    tool_calls: list[str] = field(default_factory=list)
    final_message: str = ""
    state_count: int = 0


def run_repair(
    app: Any,
    seed: str = DEFAULT_SEED,
    *,
    recursion_limit: int = 20,
    callbacks: list | None = None,
) -> RepairResult:
    """Stream ``app`` from a seed message and gather tools, tasks, and final state.

    Uses ``stream_mode="values"`` so the last snapshot carries the reduced final
    state, while tool calls are de-duplicated by message id (the Gatekeeper purge
    means each tool message appears in several snapshots before it is cleared).
    """
    config: dict[str, Any] = {"recursion_limit": recursion_limit}
    if callbacks:
        config["callbacks"] = callbacks

    tool_calls: list[str] = []
    seen: set[str] = set()
    final: dict = {}
    states = 0
    for state in app.stream(
        {"messages": [HumanMessage(content=seed)]}, stream_mode="values", config=config
    ):
        states += 1
        final = state
        for msg in state.get("messages", []):
            if isinstance(msg, ToolMessage) and msg.id not in seen:
                seen.add(msg.id)
                tool_calls.append(msg.name)

    messages = final.get("messages", [])
    preview = (messages[-1].content or "")[:_PREVIEW_CHARS].replace("\n", " ") if messages else ""
    return RepairResult(
        completed_tasks=list(final.get("completed_tasks", [])),
        current_phase=final.get("current_phase"),
        tool_calls=tool_calls,
        final_message=preview,
        state_count=states,
    )
