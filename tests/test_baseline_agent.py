"""Unit tests for the naive baseline agent (Phase 6.1)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hw4.baseline_agent import (
    QUESTIONS,
    BaselineAgent,
    estimate_tokens,
    modeled_output_tokens,
)
from hw4.constants import PHASE_POLYGONS
from hw4.tools.token_tracker import TokenTracker


class TestEstimateTokens:
    def test_empty_string_is_at_least_one(self):
        assert estimate_tokens("") == 1

    def test_four_chars_per_token(self):
        assert estimate_tokens("a" * 4) == 1
        assert estimate_tokens("a" * 5) == 2
        assert estimate_tokens("a" * 40) == 10

    def test_deterministic(self):
        text = "the quick brown fox" * 7
        assert estimate_tokens(text) == estimate_tokens(text)


class TestModeledOutputTokens:
    def test_real_phase_returns_positive(self):
        assert modeled_output_tokens(PHASE_POLYGONS) > 0

    def test_unknown_phase_falls_back_to_question_estimate(self):
        # No fix file and no question -> empty string estimate (1).
        assert modeled_output_tokens("does-not-exist") == 1


def _make_tree(root: Path) -> None:
    """A miniature broken-python tree: two text files, one binary, one cache."""
    (root / "polygons").mkdir(parents=True)
    (root / "mathsquiz").mkdir(parents=True)
    (root / "polygons" / "polygons.py").write_text("class Polygon: pass\n", encoding="utf-8")
    (root / "mathsquiz" / "mathsquiz.py").write_text("print('hi')\n", encoding="utf-8")
    (root / "README.md").write_text("# noise\n", encoding="utf-8")
    # Binary file that is not valid UTF-8 -> must be skipped, not crash.
    (root / "logo.bin").write_bytes(b"\xff\xfe\x00\x01")
    # __pycache__ must be ignored entirely.
    (root / "polygons" / "__pycache__").mkdir()
    (root / "polygons" / "__pycache__" / "polygons.cpython-312.pyc").write_bytes(b"\x00")


class TestBaselineAgent:
    def test_gather_files_skips_pycache(self, tmp_path):
        _make_tree(tmp_path)
        agent = BaselineAgent(source_root=tmp_path)
        names = {p.name for p in agent.gather_files()}
        assert "polygons.py" in names
        assert "polygons.cpython-312.pyc" not in names

    def test_read_all_skips_binary(self, tmp_path):
        _make_tree(tmp_path)
        agent = BaselineAgent(source_root=tmp_path)
        contents = agent.read_all()
        assert any(name.endswith("polygons.py") for name in contents)
        assert all(not name.endswith("logo.bin") for name in contents)

    def test_read_all_uses_relative_labels(self, tmp_path):
        _make_tree(tmp_path)
        agent = BaselineAgent(source_root=tmp_path)
        # No absolute paths leak into the log labels.
        assert all(not Path(name).is_absolute() for name in agent.read_all())

    def test_answer_records_one_entry(self, tmp_path):
        _make_tree(tmp_path)
        tracker = TokenTracker()
        agent = BaselineAgent(source_root=tmp_path, tracker=tracker)
        entry = agent.answer(PHASE_POLYGONS, "fix it")
        assert entry["node"] == "baseline:read_all"
        assert entry["tokens_in"] > 0
        assert len(entry["files_read"]) == 3  # 2 .py + 1 .md (binary/cache excluded)

    def test_run_records_one_entry_per_question(self, tmp_path):
        _make_tree(tmp_path)
        agent = BaselineAgent(source_root=tmp_path)
        tracker = agent.run()
        assert tracker.get_summary()["total_calls"] == len(QUESTIONS)

    def test_default_source_root_points_at_vendored_tree(self):
        agent = BaselineAgent()
        assert agent.source_root.name == "broken-python"


class TestBaselineMain:
    def test_main_writes_log(self, tmp_path, monkeypatch):
        import hw4.baseline_agent as mod

        monkeypatch.setattr(mod, "REPO_ROOT", tmp_path)
        _make_tree(tmp_path / "src" / "broken-python")
        # FIX_FILES were resolved at import time against the real repo; that is
        # fine - modeled_output_tokens falls back gracefully if they are absent.
        mod.main()
        assert (tmp_path / "results" / "baseline_token_log.jsonl").exists()
