# PRD: Node Content Extractor

## 1. Mechanism Overview
The Node Content Extractor (`src/tools/node_extractor.py`) is a surgical LangGraph tool that allows a subagent to retrieve the source content of a single graph node by ID, without triggering any directory-wide scan. It is the primary mechanism for enforcing the Zero-Edge domain isolation protocol at the tool level.

## 2. Problem Statement
Subagents must not use glob patterns, `os.walk`, or directory reads to find files — doing so is the naive approach that inflates token usage and breaks domain isolation. The extractor provides a node-ID-addressed read that inherently limits the agent to nodes it already knows about from the Obsidian hot-context pages.

## 3. Functional Requirements

### 3.1 Interface
```python
def extract_node_content(node_id: str) -> str:
    """Return raw source for a single graph node.

    Args:
        node_id: A node identifier as it appears in obsidian/graph.json.

    Returns:
        The full text of the file the node maps to.

    Raises:
        ValueError: If node_id is not present in graph.json.
        FileNotFoundError: If the mapped file does not exist on disk.
    """
```

### 3.2 Resolution Logic
1. Load `obsidian/graph.json` (cached after first read)
2. Look up `node_id` in the nodes list; find its `file` attribute
3. Read and return the file contents

### 3.3 Guardrails
- If `node_id` is not in the graph, raise `ValueError` (do not fall back to filesystem search)
- If the resolved path is outside `src/broken-python/`, raise `PermissionError`
- No wildcard lookups — one node ID → one file, deterministically

### 3.4 Caching
The parsed `graph.json` is cached in a module-level dict after the first call; subsequent calls resolve in O(1).

## 4. Non-Functional Requirements
- Graph JSON path loaded from `config/setup.json` (not hardcoded)
- Tool must be registerable with LangGraph's `ToolNode` via `@tool` decorator

## 5. Acceptance Criteria
- [ ] `extract_node_content("Polygon")` returns the content of `polygons.py`
- [ ] `extract_node_content("nonexistent_node")` raises `ValueError`
- [ ] Calling the tool twice with the same ID does not re-read `graph.json` from disk (cache hit)
- [ ] Tests in `tests/test_tools.py` cover all three paths (happy, missing node, outside-path)
