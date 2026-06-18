"""Run the actual LangGraph agent end-to-end against the live Groq API.

Unlike main.py (which only prints the graph) this invokes the compiled graph so
the real subagents reason on Groq, call their tools, and emit fixes. The
tool-call repair shim in the subagent nodes (hw4.tools.tool_call_repair) turns
Groq's `tool_use_failed` responses back into well-formed tool calls, so the
llama-3.3-70b tool loop completes instead of crashing.

A callback meters real token usage across every turn and throttles calls to
respect the free-tier tokens-per-minute window. The caller restores the vendored
source afterwards (the agent's write_source_file tool mutates it).

Run: uv run python run_live_agent.py
"""

import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_groq import ChatGroq

from main import build_graph

MODEL = "llama-3.3-70b-versatile"
MAX_OUTPUT_TOKENS = 2048  # room for a write_source_file content arg on these small files
PACE_SECONDS = 30  # throttle to stay inside the ~12k tokens/min free-tier window
RECURSION_LIMIT = 20
TOKEN_LOG = Path("results") / "live_agent_token_log.jsonl"


class Meter(BaseCallbackHandler):
    """Throttle each LLM call and accumulate real per-call token usage."""

    def __init__(self, pace_seconds: int = PACE_SECONDS) -> None:
        self.records: list[dict] = []
        self._pace = pace_seconds

    def on_llm_start(self, *args, **kwargs) -> None:
        if self.records:
            time.sleep(self._pace)

    def on_llm_end(self, response, **kwargs) -> None:
        try:
            usage = getattr(response.generations[0][0].message, "usage_metadata", None) or {}
        except (AttributeError, IndexError):
            usage = {}
        self.records.append(
            {
                "call": len(self.records) + 1,
                "tokens_in": usage.get("input_tokens", 0),
                "tokens_out": usage.get("output_tokens", 0),
            }
        )

    @property
    def tokens_in(self) -> int:
        return sum(r["tokens_in"] for r in self.records)

    @property
    def tokens_out(self) -> int:
        return sum(r["tokens_out"] for r in self.records)


def main() -> None:
    load_dotenv()
    llm = ChatGroq(
        api_key=os.environ["GROQ_API_KEY"],
        model=MODEL,
        temperature=0.0,
        max_tokens=MAX_OUTPUT_TOKENS,
    )
    app = build_graph(llm=llm)
    meter = Meter()
    seed = HumanMessage(
        content="Begin the investigation. Follow your Obsidian entry page and fix the bugs in your domain."
    )

    print(f"Invoking the live LangGraph agent on Groq (model={MODEL})...\n", flush=True)
    tool_calls_made: list[str] = []
    final: dict = {}
    for state in app.stream(
        {"messages": [seed]},
        stream_mode="values",
        config={"callbacks": [meter], "recursion_limit": RECURSION_LIMIT},
    ):
        final = state
        for msg in state.get("messages", []):
            if isinstance(msg, ToolMessage):
                tool_calls_made.append(msg.name)
            elif isinstance(msg, AIMessage):
                for call in getattr(msg, "tool_calls", None) or []:
                    print(f"  tool call -> {call['name']}({call['args']})", flush=True)

    TOKEN_LOG.parent.mkdir(parents=True, exist_ok=True)
    with TOKEN_LOG.open("w", encoding="utf-8") as fh:
        for rec in meter.records:
            fh.write(json.dumps(rec) + "\n")

    print("\n=== LIVE AGENT RUN (real Groq usage) ===")
    print(f"  LLM calls         : {len(meter.records)}")
    print(f"  Real input tokens : {meter.tokens_in}")
    print(f"  Real output tokens: {meter.tokens_out}")
    print(f"  Tools executed    : {len(set(tool_calls_made))} unique, {len(tool_calls_made)} total")
    print(f"  completed_tasks   : {final.get('completed_tasks')}")
    print(f"  current_phase     : {final.get('current_phase')}")
    last = final.get("messages", [])
    if last:
        preview = (last[-1].content or "")[:400].replace("\n", " ")
        print(f"  final message     : {preview}")


if __name__ == "__main__":
    main()
