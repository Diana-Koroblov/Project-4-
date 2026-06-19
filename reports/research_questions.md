# Research Questions — Findings Report

This report answers the 8 understanding-and-research questions mandated by the
assignment (§4), drawn from the reverse-engineering and debugging of
[`martinpeck/broken-python`](https://github.com/martinpeck/broken-python). The
same answers appear in the [README](../README.md) and in the Obsidian vault at
[`obsidian/research_questions.md`](../obsidian/research_questions.md); this copy
links to the supporting reports and schemas.

| # | Question | Primary evidence |
|---|----------|------------------|
| 1 | Actual architecture | [`obsidian/GRAPH_REPORT.md`](../obsidian/GRAPH_REPORT.md) |
| 2 | Most central components | [`obsidian/GRAPH_REPORT.md`](../obsidian/GRAPH_REPORT.md) (God Nodes) |
| 3 | Complexity hotspots / God Nodes | [`docs/oop_schema.md`](../docs/oop_schema.md) |
| 4 | Extracting schemas from sparse docs | [`docs/block_schema.md`](../docs/block_schema.md) |
| 5 | Bug identification & root cause | [`reports/bug_analysis.md`](bug_analysis.md) |
| 6 | Graph vs. linear reading | [`reports/efficiency_report.md`](efficiency_report.md) |
| 7 | Token savings mechanism | [`reports/efficiency_live_results.md`](efficiency_live_results.md) |
| 8 | Future improvements / extensions | [`docs/PRD_orphan_detector.md`](../docs/PRD_orphan_detector.md) |

---

## 1. What is the actual architecture, and what wasn't obvious at first glance?
Two **completely independent** systems share a single repository with **no imports
between them**. What was not obvious initially: `mathsquiz.py` is **not** a "final"
version — it is itself broken, and the `mathsquiz-step1..3.py` files are **not**
scaffolding toward it but separate incomplete attempts. Graphify identified
6 communities, with Polygons and Math Quiz isolated from each other (see
[`obsidian/GRAPH_REPORT.md`](../obsidian/GRAPH_REPORT.md)).

## 2. Which components/modules/classes/functions are the most central?
Per the Graphify God Nodes report: `Polygon` (4 edges) and `Maths Quiz` (4 edges)
are the two highest-centrality nodes. Within the Polygons system,
`calc_polygon_details()` is the critical God Function bridging user input to
output.

## 3. Where are the complexity hotspots, mixed responsibility, or "God Nodes"?
- `calc_polygon_details()` — handles both calculation **and** object instantiation
  outside the class.
- `draw_polygon()` — owns drawing logic that belongs inside `Polygon`.
- `mathsquiz.py` — a single flat script handling all quiz logic with no structure.

See the before-state class diagram in [`docs/oop_schema.md`](../docs/oop_schema.md).

## 4. How do you extract a block schema and OOP schema when docs are sparse?
By running Graphify to generate `graph.json` and `GRAPH_REPORT.md`, then manually
tracing call flows and class definitions. The Mermaid diagrams in
[`docs/block_schema.md`](../docs/block_schema.md) and
[`docs/oop_schema.md`](../docs/oop_schema.md) were produced this way — not from
docs, but from reverse-reading the code structure.

## 5. How did you identify the bug, what was the root cause, and what steps led there?
The agent navigated via `index.md` → `hot_polygons.md`, which explicitly listed
the known suspects. Root causes:
- **Polygons:** `Object` (capital O) as base class → `NameError`; `new Polygon(...)`
  → `SyntaxError`; hardcoded angles/loop.
- **Math Quiz:** Python 2 `print` statement; `=` used for comparison; `else if`
  instead of `elif`; wrong expected answers; score never incremented.

Full investigation trail with graph-node references: [`reports/bug_analysis.md`](bug_analysis.md).

## 6. What was the advantage of the graph + Obsidian navigation vs. linear reading?
Linear reading of all files (including 3 redundant step files) would expose the
agent to ~400 lines of noise before reaching relevant code. The graph-guided path
(`index.md` → hot page → single target file) required reading only ~70 lines of
directly relevant content — a reduction of **over 80%** in context loaded per
investigation phase. Quantified in [`reports/efficiency_report.md`](efficiency_report.md).

## 7. How did the graph-guided agent save tokens / reduce unnecessary reads?
The `hot_*.md` pages **pre-filter**: they identify the exact file and the exact bug
category before the agent touches any source. Subagent Alpha never loaded Math Quiz
content; Subagent Beta never loaded Polygons content; the Gatekeeper node wiped
state between phases. Measured **70.7% input-token reduction** on real Groq calls —
[`reports/efficiency_live_results.md`](efficiency_live_results.md).

## 8. What improvements, extensions, or agent mechanisms would you add?
- **Centrality-ranked suspect list:** score nodes by betweenness centrality ×
  proximity to failing tests.
- **Dynamic git diff** generated from `graph.json` to show exactly which edges
  change after a fix.
- **Orphan node detector:** auto-document nodes with ≤1 connection (4 found:
  `Introduction`, `Objectives`, `The Files`, `MIT License`) — *built* as the
  Phase 7 extension ([`docs/PRD_orphan_detector.md`](../docs/PRD_orphan_detector.md)).
- **Impact report:** given a changed node, traverse outbound edges to predict what
  breaks.
