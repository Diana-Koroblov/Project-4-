# PRD: Orphan Node Detector (Phase 7 Extension)

## 1. Mechanism Overview
The Orphan Node Detector (`src/extensions/orphan_detector.py`) is the original extension for Phase 7. It scans a Graphify `graph.json` and identifies nodes with ≤1 graph edge — nodes that are effectively isolated from the main knowledge graph ("orphans"). These represent documentation stubs, dead code, or files with no meaningful cross-references.

## 2. Problem Statement
During reverse-engineering, the Graphify graph contains nodes at different connectivity levels. Nodes with zero or one edge are poor navigation targets — the agent cannot "follow the graph" to or from them, making them invisible to a graph-guided agent unless explicitly known. Detecting and reporting orphans helps the developer identify dead documentation and poorly-integrated code before the agent starts.

## 3. Before-State Findings
From the initial `GRAPH_REPORT.md`, 4 orphan nodes have already been identified:
| Node | Edges | Type |
|---|---|---|
| `Introduction` | 0 | Documentation node |
| `Objectives` | 0 | Documentation node |
| `The Files` | 1 | Documentation node |
| `MIT License` | 1 | Documentation node |

## 4. Functional Requirements

### 4.1 Data Model
```python
@dataclass
class OrphanNode:
    node_id: str
    label: str
    edge_count: int
    file: str | None        # mapped file path, if any
    reason: str             # "isolated" (0 edges) or "weakly_connected" (1 edge)
```

### 4.2 Detector Class Interface
```python
class OrphanDetector:
    def __init__(self, graph_path: str, threshold: int = 1) -> None: ...
    def detect(self) -> list[OrphanNode]: ...
    def report(self, output_path: str) -> None: ...   # writes Markdown report
```

- `threshold` loaded from `config/setup.json["extensions"]["orphan_detector"]["max_edge_threshold"]`
- `detect()` must run in O(N) time where N is the number of nodes

### 4.3 CLI Entry Point
```bash
uv run python -m hw4.extensions.orphan_detector --graph obsidian/graph.json --out results/orphan_report.md
```

### 4.4 Report Format (`results/orphan_report.md`)
```markdown
# Orphan Node Report
Generated: <ISO timestamp>
Graph: obsidian/graph.json
Threshold: ≤ 1 edge

## Summary
- Total nodes: N
- Orphan nodes detected: M

## Orphan Nodes
| Node | Edges | Reason | File |
|------|-------|--------|------|
| ... | ... | ... | ... |

## Recommendations
...
```

## 5. Non-Functional Requirements
- Must not modify `graph.json` (read-only)
- Must handle empty graphs without crashing
- `threshold` must be configurable, not hardcoded

## 6. Acceptance Criteria
- [ ] Running detector on `obsidian/graph.json` identifies at least the 4 known orphans
- [ ] `OrphanNode.reason` correctly distinguishes `"isolated"` (0 edges) from `"weakly_connected"` (1 edge)
- [ ] CLI produces `results/orphan_report.md` with valid Markdown
- [ ] ≥ 85% test coverage of `src/extensions/orphan_detector.py` via `pytest-cov`
- [ ] Ruff reports zero violations
