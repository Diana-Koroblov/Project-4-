"""Extension: Orphan Node Detector (Phase 7).

Scans a Graphify ``graph.json`` (read-only) and reports nodes with ``<= threshold``
edges - "orphans" a graph-guided agent cannot navigate to or from (dead docs, stub
code, poorly cross-referenced files). The threshold is config-driven:
``config/setup.json`` -> ``extensions.orphan_detector.max_edge_threshold`` (with
``config/setup.example.json`` as fallback). See ``docs/PRD_orphan_detector.md``.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from hw4.constants import CONFIG_SETUP_EXAMPLE_PATH, CONFIG_SETUP_PATH, DEFAULT_ORPHAN_THRESHOLD

DEFAULT_GRAPH_PATH = "obsidian/graph.json"
DEFAULT_REPORT_PATH = "results/orphan_report.md"


@dataclass
class OrphanNode:
    """A poorly-connected graph node flagged by the detector."""

    node_id: str
    label: str
    edge_count: int
    file: str | None  # mapped source file, if any
    reason: str  # "isolated" (0 edges) or "weakly_connected" (>=1 edge)


def load_threshold() -> int:
    """Return ``max_edge_threshold`` from setup.json (example file as fallback)."""
    for path in (CONFIG_SETUP_PATH, CONFIG_SETUP_EXAMPLE_PATH):
        cfg_path = Path(path)
        if cfg_path.exists():
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            ext = cfg.get("extensions", {}).get("orphan_detector", {})
            return int(ext.get("max_edge_threshold", DEFAULT_ORPHAN_THRESHOLD))
    return DEFAULT_ORPHAN_THRESHOLD


class OrphanDetector:
    """Detect and report orphan nodes in a Graphify graph."""

    def __init__(self, graph_path: str, threshold: int | None = None) -> None:
        self.graph_path = Path(graph_path)
        # ``None`` => config-driven default; an explicit int overrides config.
        self.threshold = load_threshold() if threshold is None else threshold

    def _load_graph(self) -> dict:
        if not self.graph_path.exists():
            raise FileNotFoundError(f"Graph file not found: {self.graph_path}")
        return json.loads(self.graph_path.read_text(encoding="utf-8"))

    def _scan(self) -> tuple[list[OrphanNode], int]:
        """Single read-only pass returning (orphans, total_node_count)."""
        graph = self._load_graph()
        nodes = graph.get("nodes", [])
        degree: Counter[str] = Counter()
        for link in graph.get("links", []):  # one pass over undirected edges
            for endpoint in (link.get("source"), link.get("target")):
                if endpoint is not None:
                    degree[endpoint] += 1

        orphans: list[OrphanNode] = []
        for node in nodes:  # one pass over nodes -> linear in nodes + edges
            node_id = node.get("id", "")
            edge_count = degree.get(node_id, 0)
            if edge_count <= self.threshold:
                orphans.append(
                    OrphanNode(
                        node_id=node_id,
                        label=node.get("label", node_id),
                        edge_count=edge_count,
                        file=(node.get("source_file") or "").strip() or None,
                        reason="isolated" if edge_count == 0 else "weakly_connected",
                    )
                )
        orphans.sort(key=lambda o: (o.edge_count, o.label or "", o.node_id or ""))
        return orphans, len(nodes)

    def detect(self) -> list[OrphanNode]:
        """Return every node with ``<= threshold`` edges."""
        return self._scan()[0]

    def report(self, output_path: str) -> None:
        """Write a Markdown orphan report to ``output_path``."""
        orphans, total = self._scan()
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(self._render(orphans, total), encoding="utf-8")

    def _render(self, orphans: list[OrphanNode], total: int) -> str:
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        head = [
            "# Orphan Node Report",
            f"Generated: {timestamp}",
            f"Graph: {self.graph_path.as_posix()}",
            f"Threshold: <= {self.threshold} edge(s)",
            "",
            "## Summary",
            f"- Total nodes: {total}",
            f"- Orphan nodes detected: {len(orphans)}",
            "",
            "## Orphan Nodes",
            "| Node | Edges | Reason | File |",
            "|------|-------|--------|------|",
        ]
        rows = [
            f"| {o.label} | {o.edge_count} | {o.reason} | {o.file or '(none)'} |"
            for o in orphans
        ]
        tail = ["", "## Recommendations", "", _recommendation(orphans)]
        return "\n".join(head + rows + tail) + "\n"


def _recommendation(orphans: list[OrphanNode]) -> str:
    """One-paragraph guidance summarising the detected orphans."""
    if not orphans:
        return "No orphans at this threshold - the graph is well connected."
    isolated = sum(1 for o in orphans if o.reason == "isolated")
    weak = len(orphans) - isolated
    return (
        f"- {isolated} isolated node(s) with 0 edges: dead docs/code or missing "
        "links - wire them into the graph or remove them.\n"
        f"- {weak} weakly-connected node(s): review whether they deserve more "
        "cross-references to become navigable by the graph-guided agent."
    )


def main(argv: list[str] | None = None) -> None:
    """CLI entry point; see the module docstring for usage."""
    parser = argparse.ArgumentParser(description="Detect orphan nodes in a Graphify graph.")
    parser.add_argument("--graph", default=DEFAULT_GRAPH_PATH, help="Path to graph.json")
    parser.add_argument("--out", default=DEFAULT_REPORT_PATH, help="Output Markdown path")
    parser.add_argument("--threshold", type=int, default=None, help="Override config threshold")
    args = parser.parse_args(argv)
    detector = OrphanDetector(args.graph, threshold=args.threshold)
    detector.report(args.out)
    count = len(detector.detect())
    print(f"Wrote {args.out}: {count} orphan(s) at threshold <= {detector.threshold}.")


if __name__ == "__main__":
    main()
