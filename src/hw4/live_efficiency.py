"""Live token-efficiency measurement — REAL Groq usage, not a chars/4 estimate.

This is the *measured* counterpart to :mod:`hw4.efficiency`. It sends the same
two contexts per phase — the graph-guided targeted reads vs. the naive whole-tree
read — to the real Groq API and records the input/output token counts the API
actually reports (``response.usage_metadata``). This upgrades the modeled 70.9%
figure to a number measured against a live LLM.

Output: ``results/token_log_live.jsonl`` + a printed reduction summary.
Run:    ``uv run python src/hw4/live_efficiency.py``
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.messages import HumanMessage

from hw4.baseline_agent import QUESTIONS, REPO_ROOT, BaselineAgent
from hw4.efficiency import GUIDED_READS, _read
from hw4.llm_config import get_llm
from hw4.tools.token_tracker import TokenTracker

BASELINE_NODE = "baseline:groq"
GUIDED_NODE = "guided:groq"

# Free-tier Groq is capped at 12,000 tokens/min and counts the completion
# reservation (max_tokens) against that budget. Cap the reservation and pace the
# calls so the rolling window never overflows. The capped output does not affect
# the input-token figure, which is the metric the efficiency thesis turns on.
_MAX_OUTPUT_TOKENS = 512
_PACE_SECONDS = 20


def _invoke(model, prompt: str):
    """One Groq call with a couple of backoff retries on a rate-limit (413/429)."""
    for attempt in range(3):
        try:
            return model.invoke([HumanMessage(content=prompt)])
        except Exception as exc:  # noqa: BLE001 - retry only on rate-limit codes
            if ("413" in str(exc) or "429" in str(exc)) and attempt < 2:
                print(f"    rate-limited, backing off {_PACE_SECONDS}s...", flush=True)
                time.sleep(_PACE_SECONDS)
                continue
            raise


def _guided_prompt(phase: str) -> tuple[str, list[str]]:
    """The graph-guided context: entry page(s) + the single targeted source file."""
    paths = GUIDED_READS[phase]
    context = "\n\n".join(f"# FILE: {p}\n{_read(p)}" for p in paths)
    return f"{context}\n\nQUESTION: {QUESTIONS[phase]}", list(paths)


def _baseline_prompt(phase: str, agent: BaselineAgent) -> tuple[str, list[str]]:
    """The naive context: the entire src/broken-python/ tree, re-sent per phase."""
    contents = agent.read_all()
    context = "\n\n".join(f"# FILE: {p}\n{b}" for p, b in contents.items())
    return f"{context}\n\nQUESTION: {QUESTIONS[phase]}", list(contents)


def _totals(entries: list[dict], node: str) -> dict:
    rows = [e for e in entries if e["node"] == node]
    tokens_in = sum(e["tokens_in"] for e in rows)
    tokens_out = sum(e["tokens_out"] for e in rows)
    files = sum(len(e["files_read"]) for e in rows)
    return {"tokens_in": tokens_in, "tokens_out": tokens_out, "files": files}


def run(llm=None, tracker: TokenTracker | None = None) -> TokenTracker:
    """Send both contexts per phase to Groq and record the real usage."""
    llm = llm or get_llm()
    model = llm.bind(max_tokens=_MAX_OUTPUT_TOKENS)
    tracker = tracker or TokenTracker()
    baseline_agent = BaselineAgent()

    # (node, prompt, files) work items, paced to respect the rolling TPM window.
    jobs = []
    for phase in QUESTIONS:
        g_prompt, g_files = _guided_prompt(phase)
        b_prompt, b_files = _baseline_prompt(phase, baseline_agent)
        jobs.append((phase, GUIDED_NODE, g_prompt, g_files))
        jobs.append((phase, BASELINE_NODE, b_prompt, b_files))

    for i, (phase, node, prompt, files) in enumerate(jobs):
        if i:
            time.sleep(_PACE_SECONDS)
        print(f"[{phase}] {node:<14} -> Groq ({len(files)} files)...", flush=True)
        resp = _invoke(model, prompt)
        rec = tracker.record_response(phase, node, resp, files)
        print(f"    real usage: in={rec['tokens_in']} out={rec['tokens_out']}", flush=True)

    return tracker


def main() -> None:
    tracker = run()
    tracker.save_log(str(REPO_ROOT / "results" / "token_log_live.jsonl"))

    entries = tracker.entries
    base = _totals(entries, BASELINE_NODE)
    guided = _totals(entries, GUIDED_NODE)
    in_red = 1 - guided["tokens_in"] / base["tokens_in"] if base["tokens_in"] else 0.0

    print("\n=== REAL Groq token usage (measured) ===")
    print(f"  Baseline  input tokens : {base['tokens_in']:>6}  (file-loads: {base['files']})")
    print(f"  Guided    input tokens : {guided['tokens_in']:>6}  (file-loads: {guided['files']})")
    print(f"  Baseline  output tokens: {base['tokens_out']:>6}")
    print(f"  Guided    output tokens: {guided['tokens_out']:>6}")
    print(f"  INPUT-TOKEN REDUCTION  : {in_red:.1%}")


if __name__ == "__main__":
    main()
