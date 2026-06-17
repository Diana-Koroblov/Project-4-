"""Token-efficiency comparison: naive baseline vs. graph-guided agent.

Builds a single ``results/token_log.jsonl`` containing one record per phase for
each mode, then derives the comparison consumed by
``reports/efficiency_report.md``. The guided records mirror the guided agent's
documented reading pattern — the Obsidian entry page(s) plus the single targeted
source file per community — rather than the whole tree. The same deterministic
token estimator is used for both modes (see ``baseline_agent.estimate_tokens``),
so the reduction ratio is reproducible from the log alone.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hw4.baseline_agent import (
    QUESTIONS,
    REPO_ROOT,
    BaselineAgent,
    estimate_tokens,
    modeled_output_tokens,
)
from hw4.constants import PHASE_MATHSQUIZ, PHASE_POLYGONS
from hw4.tools.token_tracker import TokenTracker

BASELINE_NODE = "baseline:read_all"
GUIDED_NODE = "guided:targeted"

# Exactly the files the guided agent loads per phase: entry page(s) + the single
# targeted source file. ``index.md`` is read once (router), attributed to the
# first phase; the Gatekeeper wipes context before the Math Quiz phase.
GUIDED_READS = {
    PHASE_POLYGONS: [
        "obsidian/index.md",
        "obsidian/hot_polygons.md",
        "src/broken-python/polygons/polygons.py",
    ],
    PHASE_MATHSQUIZ: [
        "obsidian/hot_mathsquiz.md",
        "src/broken-python/mathsquiz/mathsquiz.py",
    ],
}


def _read(rel_path: str) -> str:
    return (REPO_ROOT / rel_path).read_text(encoding="utf-8")


def record_guided(tracker: TokenTracker) -> TokenTracker:
    """Record the guided agent's per-phase targeted reads onto ``tracker``."""
    for phase, paths in GUIDED_READS.items():
        context = "\n\n".join(f"# FILE: {p}\n{_read(p)}" for p in paths)
        prompt = f"{context}\n\nQUESTION: {QUESTIONS[phase]}"
        tracker.record(
            phase=phase,
            node=GUIDED_NODE,
            tokens_in=estimate_tokens(prompt),
            tokens_out=modeled_output_tokens(phase),
            files_read=list(paths),
        )
    return tracker


def build_token_log() -> TokenTracker:
    """Populate one tracker with baseline + guided records for every phase."""
    tracker = TokenTracker()
    BaselineAgent(tracker=tracker).run()
    record_guided(tracker)
    return tracker


def _totals(entries: list[dict], node: str) -> dict:
    rows = [e for e in entries if e["node"] == node]
    tokens_in = sum(e["tokens_in"] for e in rows)
    tokens_out = sum(e["tokens_out"] for e in rows)
    return {
        "calls": len(rows),
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "tokens": tokens_in + tokens_out,
        "files": sum(len(e["files_read"]) for e in rows),
    }


def _reduction(baseline: int, guided: int) -> float:
    return 1 - (guided / baseline) if baseline else 0.0


def compare(tracker: TokenTracker | None = None) -> dict:
    """Return baseline vs. guided totals and the token-reduction ratios."""
    tracker = tracker or build_token_log()
    entries = tracker.entries
    baseline = _totals(entries, BASELINE_NODE)
    guided = _totals(entries, GUIDED_NODE)
    return {
        "baseline": baseline,
        "guided": guided,
        "input_reduction": _reduction(baseline["tokens_in"], guided["tokens_in"]),
        "total_reduction": _reduction(baseline["tokens"], guided["tokens"]),
    }


def main() -> None:
    tracker = build_token_log()
    tracker.save_log(str(REPO_ROOT / "results" / "token_log.jsonl"))
    result = compare(tracker)
    print(f"Baseline tokens_in: {result['baseline']['tokens_in']}")
    print(f"Guided   tokens_in: {result['guided']['tokens_in']}")
    print(f"Baseline files read: {result['baseline']['files']}")
    print(f"Guided   files read: {result['guided']['files']}")
    print(f"Input-token reduction: {result['input_reduction']:.1%}")
    print(f"Total-token reduction: {result['total_reduction']:.1%}")


if __name__ == "__main__":
    main()
