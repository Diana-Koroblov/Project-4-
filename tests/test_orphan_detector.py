"""Tests for the Orphan Node Detector extension (Phase 7)."""

import json
from pathlib import Path

import pytest

from hw4.extensions import orphan_detector as od
from hw4.extensions.orphan_detector import OrphanDetector, load_threshold, main

REAL_GRAPH = "obsidian/graph.json"
KNOWN_ORPHANS = {"Introduction", "Objectives", "The Files", "MIT License"}


def _write_graph(path: Path, nodes: list, links: list) -> Path:
    path.write_text(json.dumps({"nodes": nodes, "links": links}), encoding="utf-8")
    return path


def _abc_graph(tmp_path: Path) -> Path:
    """A-B connected (degree 1 each); C isolated (degree 0)."""
    nodes = [
        {"id": "a", "label": "A", "source_file": "a.py"},
        {"id": "b", "label": "B", "source_file": ""},
        {"id": "c", "label": "C", "source_file": "c.py"},
    ]
    return _write_graph(tmp_path / "g.json", nodes, [{"source": "a", "target": "b"}])


class TestDetect:
    def test_happy_path_finds_known_orphans(self):
        orphans = OrphanDetector(REAL_GRAPH, threshold=1).detect()
        assert KNOWN_ORPHANS <= {o.label for o in orphans}

    def test_reason_distinguishes_isolated_from_weak(self):
        by_label = {o.label: o for o in OrphanDetector(REAL_GRAPH, threshold=1).detect()}
        assert by_label["mathsquiz-step1.py"].reason == "isolated"
        assert by_label["mathsquiz-step1.py"].edge_count == 0
        assert by_label["MIT License"].reason == "weakly_connected"
        assert by_label["MIT License"].edge_count == 1

    def test_file_mapping_blank_becomes_none(self, tmp_path):
        ids = {o.node_id: o for o in OrphanDetector(str(_abc_graph(tmp_path)), threshold=100).detect()}
        assert ids["c"].file == "c.py"
        assert ids["b"].file is None  # blank source_file maps to None

    def test_empty_graph(self, tmp_path):
        g = _write_graph(tmp_path / "empty.json", [], [])
        assert OrphanDetector(str(g)).detect() == []

    def test_threshold_zero_returns_only_isolated(self, tmp_path):
        ids = {o.node_id for o in OrphanDetector(str(_abc_graph(tmp_path)), threshold=0).detect()}
        assert ids == {"c"}

    def test_threshold_high_returns_all_nodes(self, tmp_path):
        ids = {o.node_id for o in OrphanDetector(str(_abc_graph(tmp_path)), threshold=100).detect()}
        assert ids == {"a", "b", "c"}

    def test_missing_graph_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            OrphanDetector(str(tmp_path / "nope.json"), threshold=1).detect()


class TestThresholdConfig:
    def test_default_is_config_driven(self):
        assert OrphanDetector(REAL_GRAPH).threshold == load_threshold()

    def test_reads_setup_json_first(self, tmp_path, monkeypatch):
        setup = tmp_path / "setup.json"
        payload = {"extensions": {"orphan_detector": {"max_edge_threshold": 5}}}
        setup.write_text(json.dumps(payload), encoding="utf-8")
        monkeypatch.setattr(od, "CONFIG_SETUP_PATH", str(setup))
        assert load_threshold() == 5

    def test_falls_back_to_default_without_config(self, tmp_path, monkeypatch):
        monkeypatch.setattr(od, "CONFIG_SETUP_PATH", str(tmp_path / "x.json"))
        monkeypatch.setattr(od, "CONFIG_SETUP_EXAMPLE_PATH", str(tmp_path / "y.json"))
        monkeypatch.setattr(od, "DEFAULT_ORPHAN_THRESHOLD", 7)
        assert load_threshold() == 7


class TestReport:
    def test_report_writes_valid_markdown(self, tmp_path):
        out = tmp_path / "r.md"
        OrphanDetector(REAL_GRAPH, threshold=1).report(str(out))
        text = out.read_text(encoding="utf-8")
        assert text.startswith("# Orphan Node Report")
        assert "| Node | Edges | Reason | File |" in text
        assert "MIT License" in text
        assert "## Recommendations" in text

    def test_report_empty_graph_recommendation(self, tmp_path):
        g = _write_graph(tmp_path / "e.json", [], [])
        out = tmp_path / "er.md"
        OrphanDetector(str(g)).report(str(out))
        text = out.read_text(encoding="utf-8")
        assert "Total nodes: 0" in text
        assert "well connected" in text

    def test_report_creates_missing_parent_dir(self, tmp_path):
        out = tmp_path / "nested" / "r.md"
        OrphanDetector(REAL_GRAPH, threshold=1).report(str(out))
        assert out.exists()


class TestCli:
    def test_main_writes_report(self, tmp_path):
        out = tmp_path / "cli.md"
        main(["--graph", str(_abc_graph(tmp_path)), "--out", str(out), "--threshold", "100"])
        assert "- Orphan nodes detected: 3" in out.read_text(encoding="utf-8")
