"""Tool: extract the source backing a single graph node.

Resolves a node id from ``obsidian/graph.json`` to the file it lives in and
returns that file's raw source. By keying on the graph it refuses any
directory-wide or speculative reads: only nodes that exist in the dependency
graph can be resolved, and each resolves to exactly one source file.
"""

import json
from pathlib import Path

from hw4.constants import ALLOWED_SOURCE_ROOT

_GRAPH_PATH = Path("obsidian") / "graph.json"
_SOURCE_ROOT = Path(ALLOWED_SOURCE_ROOT)


def _load_nodes() -> list[dict]:
    if not _GRAPH_PATH.exists():
        raise FileNotFoundError(f"Graph file not found: {_GRAPH_PATH}")
    graph = json.loads(_GRAPH_PATH.read_text(encoding="utf-8"))
    return graph.get("nodes", [])


def extract_node_content(node_id: str) -> str:
    """Return the raw source of the file backing ``node_id``.

    Args:
        node_id: A node ``id`` exactly as it appears in ``graph.json``
            (e.g. ``"polygons_polygons_calc_polygon_details"``).

    Returns:
        The full UTF-8 text of the node's ``source_file``.

    Raises:
        ValueError: If ``node_id`` is not present in the graph, or the matched
            node has no concrete ``source_file`` (e.g. external symbols).
        FileNotFoundError: If the resolved source file does not exist on disk.
    """
    if not node_id or not node_id.strip():
        raise ValueError("node_id must be a non-empty string")

    node = next((n for n in _load_nodes() if n.get("id") == node_id), None)
    if node is None:
        raise ValueError(f"Node not in graph: {node_id!r}")

    source_file = (node.get("source_file") or "").strip()
    if not source_file:
        raise ValueError(f"Node {node_id!r} has no resolvable source file")

    source_path = (_SOURCE_ROOT / source_file).resolve()
    allowed = _SOURCE_ROOT.resolve()
    if source_path != allowed and not source_path.is_relative_to(allowed):
        raise PermissionError(
            f"Node {node_id!r} source_file {source_file!r} resolves outside the allowed root"
        )
    if not source_path.exists():
        raise FileNotFoundError(f"Source file for node {node_id!r} not found: {source_path}")

    return source_path.read_text(encoding="utf-8")
