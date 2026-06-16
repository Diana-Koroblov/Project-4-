"""TokenTracker — per-call accounting of LLM usage for the efficiency proof.

Records one entry per LLM interaction capturing ``phase``, ``node``,
``tokens_in``, ``tokens_out`` and the ``files_read`` during that turn. The
aggregated summary feeds the baseline-vs-guided comparison in
``reports/efficiency_report.md`` and is persisted to ``results/token_log.jsonl``.
"""

import json
from pathlib import Path
from typing import Any


class TokenTracker:
    """Accumulates token-usage records across an agent run."""

    def __init__(self) -> None:
        self._entries: list[dict[str, Any]] = []

    def record(
        self,
        phase: str,
        node: str,
        tokens_in: int,
        tokens_out: int,
        files_read: list[str] | None = None,
    ) -> dict[str, Any]:
        """Append a single LLM-interaction record and return it."""
        entry = {
            "phase": phase,
            "node": node,
            "tokens_in": int(tokens_in),
            "tokens_out": int(tokens_out),
            "files_read": list(files_read) if files_read else [],
        }
        self._entries.append(entry)
        return entry

    def record_response(
        self,
        phase: str,
        node: str,
        response: Any,
        files_read: list[str] | None = None,
    ) -> dict[str, Any]:
        """Record usage by reading ``usage_metadata`` off a LangChain response.

        Falls back to zero counts when the model does not report usage (e.g. a
        fake model in tests).
        """
        usage = getattr(response, "usage_metadata", None) or {}
        tokens_in = usage.get("input_tokens", 0)
        tokens_out = usage.get("output_tokens", 0)
        return self.record(phase, node, tokens_in, tokens_out, files_read)

    @property
    def entries(self) -> list[dict[str, Any]]:
        """A copy of all recorded entries."""
        return list(self._entries)

    def get_summary(self) -> dict[str, Any]:
        """Return aggregate totals across every recorded interaction."""
        total_in = sum(e["tokens_in"] for e in self._entries)
        total_out = sum(e["tokens_out"] for e in self._entries)
        total_files = sum(len(e["files_read"]) for e in self._entries)
        return {
            "total_calls": len(self._entries),
            "total_tokens_in": total_in,
            "total_tokens_out": total_out,
            "total_tokens": total_in + total_out,
            "total_files_read": total_files,
        }

    def save_log(self, path: str) -> None:
        """Persist every entry as JSON Lines (one record per line)."""
        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as fh:
            for entry in self._entries:
                fh.write(json.dumps(entry) + "\n")
