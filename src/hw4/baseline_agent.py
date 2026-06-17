"""Naive baseline agent — the control group for the token-efficiency proof.

The graph-guided agent (``main.py``) navigates the Obsidian/Graphify map and
reads only the files relevant to the community under investigation. This
baseline does the opposite: before answering any question it ingests the entire
``src/broken-python/`` tree — the classic "stuff the whole repo into the context
window" anti-pattern. Because each question is a separate LLM call that re-sends
the whole context, the cost is paid once per phase. The resulting
:class:`TokenTracker` log is the denominator the guided agent is measured
against in ``reports/efficiency_report.md``.

Token counts use a deterministic ~4-chars-per-token estimate. The *same*
estimator is applied to both modes, so the ratio between them (the >70%
reduction claim) is independent of the estimator's absolute accuracy.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hw4.constants import ALLOWED_SOURCE_ROOT, PHASE_MATHSQUIZ, PHASE_POLYGONS
from hw4.tools.token_tracker import TokenTracker

REPO_ROOT = Path(__file__).resolve().parents[2]
_CHARS_PER_TOKEN = 4

# The two investigation questions a debugging agent must answer — one per community.
QUESTIONS = {
    PHASE_POLYGONS: "Find and fix every bug in the Polygons system.",
    PHASE_MATHSQUIZ: "Find and fix every bug in the Math Quiz system.",
}

# Each phase emits its corrected source file as the fix. Output volume is the
# same whichever way the agent navigated, so both modes model output from these.
FIX_FILES = {
    PHASE_POLYGONS: REPO_ROOT / ALLOWED_SOURCE_ROOT / "polygons" / "polygons.py",
    PHASE_MATHSQUIZ: REPO_ROOT / ALLOWED_SOURCE_ROOT / "mathsquiz" / "mathsquiz.py",
}


def estimate_tokens(text: str) -> int:
    """Deterministic token estimate (~4 chars/token, minimum 1)."""
    return max(1, math.ceil(len(text) / _CHARS_PER_TOKEN))


def modeled_output_tokens(phase: str) -> int:
    """Model the emitted fix as the corrected source file for ``phase``."""
    fix_file = FIX_FILES.get(phase)
    if fix_file is not None and fix_file.exists():
        return estimate_tokens(fix_file.read_text(encoding="utf-8"))
    return estimate_tokens(QUESTIONS.get(phase, ""))


class BaselineAgent:
    """Answers every question by reading the entire source tree first."""

    def __init__(
        self,
        source_root: str | Path | None = None,
        tracker: TokenTracker | None = None,
    ) -> None:
        self.source_root = (
            Path(source_root)
            if source_root is not None
            else REPO_ROOT / ALLOWED_SOURCE_ROOT
        )
        self.tracker = tracker or TokenTracker()

    def gather_files(self) -> list[Path]:
        """Every readable file under the source root, sorted for determinism."""
        return [
            p
            for p in sorted(self.source_root.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts
        ]

    def _rel(self, path: Path) -> str:
        """A portable, repo-relative label for ``path`` (no absolute paths in logs)."""
        for base in (REPO_ROOT, self.source_root.parent, self.source_root):
            try:
                return path.relative_to(base).as_posix()
            except ValueError:
                continue
        return path.name

    def read_all(self) -> dict[str, str]:
        """Decode every file; binary / undecodable files are skipped."""
        contents: dict[str, str] = {}
        for path in self.gather_files():
            try:
                contents[self._rel(path)] = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return contents

    def answer(self, phase: str, question: str) -> dict:
        """Answer one question the naive way and record its token cost."""
        contents = self.read_all()
        context = "\n\n".join(
            f"# FILE: {path}\n{body}" for path, body in contents.items()
        )
        prompt = f"{context}\n\nQUESTION: {question}"
        return self.tracker.record(
            phase=phase,
            node="baseline:read_all",
            tokens_in=estimate_tokens(prompt),
            tokens_out=modeled_output_tokens(phase),
            files_read=list(contents),
        )

    def run(self) -> TokenTracker:
        """Answer every investigation question; return the populated tracker."""
        for phase, question in QUESTIONS.items():
            self.answer(phase, question)
        return self.tracker


def main() -> None:
    agent = BaselineAgent()
    agent.run()
    agent.tracker.save_log(str(REPO_ROOT / "results" / "baseline_token_log.jsonl"))
    print("Baseline agent summary:")
    for key, value in agent.tracker.get_summary().items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
