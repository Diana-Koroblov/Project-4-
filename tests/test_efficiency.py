"""Unit tests for the token-efficiency comparison (Phase 6.2)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hw4 import efficiency
from hw4.efficiency import (
    BASELINE_NODE,
    GUIDED_NODE,
    GUIDED_READS,
    _reduction,
    _totals,
    build_token_log,
    compare,
    record_guided,
)
from hw4.tools.token_tracker import TokenTracker


class TestReductionHelper:
    def test_zero_baseline_is_zero(self):
        assert _reduction(0, 0) == 0.0

    def test_half(self):
        assert _reduction(100, 50) == 0.5


class TestTotals:
    def test_filters_by_node(self):
        entries = [
            {"node": "a", "tokens_in": 10, "tokens_out": 1, "files_read": ["x"]},
            {"node": "b", "tokens_in": 5, "tokens_out": 2, "files_read": ["y", "z"]},
        ]
        totals = _totals(entries, "a")
        assert totals == {
            "calls": 1,
            "tokens_in": 10,
            "tokens_out": 1,
            "tokens": 11,
            "files": 1,
        }


class TestRecordGuided:
    def test_records_one_entry_per_phase(self):
        tracker = record_guided(TokenTracker())
        entries = tracker.entries
        assert len(entries) == len(GUIDED_READS)
        assert all(e["node"] == GUIDED_NODE for e in entries)
        assert all(e["tokens_in"] > 0 for e in entries)


class TestBuildTokenLog:
    def test_contains_both_modes(self):
        tracker = build_token_log()
        nodes = {e["node"] for e in tracker.entries}
        assert nodes == {BASELINE_NODE, GUIDED_NODE}
        # Two phases per mode.
        assert len(tracker.entries) == 2 * len(GUIDED_READS)


class TestCompare:
    def test_guided_reads_fewer_tokens_and_files(self):
        result = compare()
        assert result["guided"]["tokens_in"] < result["baseline"]["tokens_in"]
        assert result["guided"]["files"] < result["baseline"]["files"]

    def test_meets_70_percent_input_reduction_kpi(self):
        """Regression guard on the headline DoD: >70% input-token reduction."""
        assert compare()["input_reduction"] > 0.70


class TestEfficiencyMain:
    def test_main_writes_token_log(self, tmp_path, monkeypatch, capsys):
        # Redirect the output path and inject a prebuilt tracker so main() does
        # no real file I/O beyond writing the log.
        fake = TokenTracker()
        fake.record("polygons", BASELINE_NODE, 1000, 100, ["a", "b"])
        fake.record("polygons", GUIDED_NODE, 200, 100, ["a"])
        monkeypatch.setattr(efficiency, "REPO_ROOT", tmp_path)
        monkeypatch.setattr(efficiency, "build_token_log", lambda: fake)
        efficiency.main()
        assert (tmp_path / "results" / "token_log.jsonl").exists()
        assert "reduction" in capsys.readouterr().out
