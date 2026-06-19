"""Run the actual LangGraph agent end-to-end against the live Groq API.

Unlike main.py (which only prints the graph) this invokes the compiled graph so
the real subagents reason on Groq, call their tools, and emit fixes. The
tool-call repair shim in the subagent nodes (hw4.tools.tool_call_repair) turns
Groq's `tool_use_failed` responses back into well-formed tool calls, so the
llama-3.3-70b tool loop completes instead of crashing.

This is a thin controller: it builds the gatekept LLM, attaches a token meter,
and delegates the run to GraphifySDK.run_repair. The central API gatekeeper
(hw4.gateway) now paces the calls, so no manual sleep is needed here.

Run: uv run python run_live_agent.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler

from hw4.llm_config import get_llm
from hw4.sdk import GraphifySDK

MAX_OUTPUT_TOKENS = 2048  # room for a write_source_file content arg on these small files
RECURSION_LIMIT = 40  # shared across both phases (Router + Alpha rounds + Gatekeeper + Beta rounds)
TOKEN_LOG = Path("results") / "live_agent_token_log.jsonl"


class Meter(BaseCallbackHandler):
    """Accumulate real per-call token usage across the run."""

    def __init__(self) -> None:
        self.records: list[dict] = []

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
    # Cap output tokens but keep the model gatekept (bind stays behind the gateway).
    llm = get_llm().bind(max_tokens=MAX_OUTPUT_TOKENS)
    sdk = GraphifySDK(llm=llm)
    meter = Meter()

    print("Invoking the live LangGraph agent on Groq (model from config)...\n", flush=True)
    result = sdk.run_repair(recursion_limit=RECURSION_LIMIT, callbacks=[meter])

    TOKEN_LOG.parent.mkdir(parents=True, exist_ok=True)
    with TOKEN_LOG.open("w", encoding="utf-8") as fh:
        for rec in meter.records:
            fh.write(json.dumps(rec) + "\n")

    print("\n=== LIVE AGENT RUN (real Groq usage) ===")
    print(f"  LLM calls         : {len(meter.records)}")
    print(f"  Real input tokens : {meter.tokens_in}")
    print(f"  Real output tokens: {meter.tokens_out}")
    print(f"  Tools executed    : {len(set(result.tool_calls))} unique, {len(result.tool_calls)} total")
    print(f"  completed_tasks   : {result.completed_tasks}")
    print(f"  current_phase     : {result.current_phase}")
    if result.final_message:
        print(f"  final message     : {result.final_message}")


if __name__ == "__main__":
    main()
