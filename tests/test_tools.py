"""Unit tests for the surgical agent tools and TokenTracker (Phase 3)."""

import json

import pytest

from hw4.tools import (
    TokenTracker,
    extract_node_content,
    file_io,
    node_extractor,
    read_obsidian_page,
    read_source_file,
    write_source_file,
)


class TestReadObsidianPage:
    def test_happy_path(self):
        assert read_obsidian_page("hot_polygons").strip()

    def test_md_suffix_tolerated(self):
        assert read_obsidian_page("index.md") == read_obsidian_page("index")

    def test_missing_page_raises(self):
        with pytest.raises(FileNotFoundError):
            read_obsidian_page("definitely_missing_page")

    def test_empty_name_raises(self):
        with pytest.raises(ValueError):
            read_obsidian_page("   ")

    @pytest.mark.parametrize("bad", ["../secret", "sub/page", "..", "a\\b"])
    def test_traversal_raises(self, bad):
        with pytest.raises(ValueError):
            read_obsidian_page(bad)


class TestExtractNodeContent:
    def test_happy_path(self):
        # any node maps to its backing source file; assert on a stable file-level marker
        content = extract_node_content("polygons_polygons")
        assert "class Polygon" in content

    def test_unknown_node_raises(self):
        with pytest.raises(ValueError):
            extract_node_content("no_such_node")

    def test_empty_node_id_raises(self):
        with pytest.raises(ValueError):
            extract_node_content("")

    def test_node_without_source_file_raises(self):
        # the 'object' node is an external symbol with an empty source_file
        with pytest.raises(ValueError):
            extract_node_content("object")

    def test_missing_source_file_raises(self, monkeypatch, tmp_path):
        monkeypatch.setattr(node_extractor, "_SOURCE_ROOT", tmp_path)
        with pytest.raises(FileNotFoundError):
            extract_node_content("polygons_polygons_calc_polygon_details")

    def test_missing_graph_raises(self, monkeypatch, tmp_path):
        monkeypatch.setattr(node_extractor, "_GRAPH_PATH", tmp_path / "nope.json")
        with pytest.raises(FileNotFoundError):
            extract_node_content("polygons_polygons")


class TestFileIO:
    @pytest.fixture
    def sandbox(self, monkeypatch, tmp_path):
        root = (tmp_path / "broken-python").resolve()
        root.mkdir()
        monkeypatch.setattr(file_io, "_ALLOWED_ROOT", root)
        return root

    def test_write_then_read_roundtrip(self, sandbox):
        target = str(sandbox / "polygons" / "p.py")
        write_source_file(target, "x = 1\n")
        assert read_source_file(target) == "x = 1\n"

    def test_read_missing_raises(self, sandbox):
        with pytest.raises(FileNotFoundError):
            read_source_file(str(sandbox / "missing.py"))

    def test_read_outside_sandbox_raises(self, sandbox, tmp_path):
        with pytest.raises(PermissionError):
            read_source_file(str(tmp_path / "evil.py"))

    def test_write_outside_sandbox_raises(self, sandbox, tmp_path):
        with pytest.raises(PermissionError):
            write_source_file(str(tmp_path / "evil.py"), "bad")

    def test_traversal_escape_raises(self, sandbox):
        with pytest.raises(PermissionError):
            write_source_file(str(sandbox / ".." / "evil.py"), "bad")

    def test_empty_path_raises(self, sandbox):
        with pytest.raises(ValueError):
            read_source_file("")

    def test_relative_path_resolves_against_real_root(self):
        # exercises the non-absolute branch against the real vendored tree
        content = read_source_file("src/broken-python/polygons/polygons.py")
        assert "class Polygon" in content


class TestTokenTracker:
    def test_record_and_summary(self):
        t = TokenTracker()
        t.record("polygons", "alpha", 100, 20, ["a.py", "b.py"])
        t.record("mathsquiz", "beta", 50, 10, ["c.py"])
        s = t.get_summary()
        assert s["total_calls"] == 2
        assert s["total_tokens_in"] == 150
        assert s["total_tokens_out"] == 30
        assert s["total_tokens"] == 180
        assert s["total_files_read"] == 3

    def test_record_response_reads_usage_metadata(self):
        t = TokenTracker()

        class _Resp:
            usage_metadata = {"input_tokens": 7, "output_tokens": 3}

        t.record_response("polygons", "alpha", _Resp(), ["x.py"])
        entry = t.entries[0]
        assert entry["tokens_in"] == 7
        assert entry["tokens_out"] == 3
        assert entry["files_read"] == ["x.py"]

    def test_record_response_without_usage_defaults_to_zero(self):
        t = TokenTracker()
        t.record_response("p", "n", object())
        assert t.entries[0]["tokens_in"] == 0
        assert t.entries[0]["tokens_out"] == 0

    def test_save_log_writes_jsonl(self, tmp_path):
        t = TokenTracker()
        t.record("p", "n", 1, 2, ["f.py"])
        out = tmp_path / "logs" / "token_log.jsonl"
        t.save_log(str(out))
        lines = out.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        assert json.loads(lines[0])["tokens_in"] == 1
