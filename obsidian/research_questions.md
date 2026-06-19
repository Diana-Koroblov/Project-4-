# Research Questions — Investigation Log

The 8 understanding-and-research questions required by the assignment (§4),
answered from the actual investigation of `martinpeck/broken-python`. This is the
Obsidian-vault copy; the same answers appear in the [README](../README.md) and in
[`reports/research_questions.md`](../reports/research_questions.md).

Navigation context for these answers: [[index]] → [[hot_polygons]] /
[[hot_mathsquiz]] → [[GRAPH_REPORT]] → [[knowledge_delta]].

---

### 1. What is the actual architecture, and what wasn't obvious at first glance?
Two **completely independent** systems share a single repository with **no imports
between them**. What was not obvious initially: `mathsquiz.py` is **not** a "final"
version — it is itself broken, and the `mathsquiz-step1..3.py` files are **not**
scaffolding toward it but separate incomplete attempts. Graphify identified
6 communities, with Polygons and Math Quiz isolated from each other (see
[[GRAPH_REPORT]]).

### 2. Which components/modules/classes/functions are the most central?
Per the Graphify God Nodes report: `Polygon` (4 edges) and `Maths Quiz` (4 edges)
are the two highest-centrality nodes. Within the Polygons system,
`calc_polygon_details()` is the critical God Function bridging user input to
output. Full suspect list on [[hot_polygons]].

### 3. Where are the complexity hotspots, mixed responsibility, or "God Nodes"?
- `calc_polygon_details()` — handles both calculation **and** object instantiation
  outside the class.
- `draw_polygon()` — owns drawing logic that belongs inside `Polygon`.
- `mathsquiz.py` — a single flat script handling all quiz logic with no structure.

### 4. How do you extract a block schema and OOP schema when docs are sparse?
By running Graphify to generate `graph.json` and [[GRAPH_REPORT]], then manually
tracing call flows and class definitions. The Mermaid diagrams in
[`docs/block_schema.md`](../docs/block_schema.md) and
[`docs/oop_schema.md`](../docs/oop_schema.md) were produced this way — not from
docs, but from reverse-reading the code structure.

### 5. How did you identify the bug, what was the root cause, and what steps led there?
The agent navigated via [[index]] → [[hot_polygons]], which explicitly listed the
known suspects. Root causes:
- **Polygons:** `Object` (capital O) as base class → `NameError`; `new Polygon(...)`
  → `SyntaxError`; hardcoded angles/loop.
- **Math Quiz:** Python 2 `print` statement; `=` used for comparison; `else if`
  instead of `elif`; wrong expected answers; score never incremented.

Full investigation trail: [`reports/bug_analysis.md`](../reports/bug_analysis.md).

### 6. What was the advantage of the graph + Obsidian navigation vs. linear reading?
Linear reading of all files (including 3 redundant step files) would expose the
agent to ~400 lines of noise before reaching relevant code. The graph-guided path
([[index]] → hot page → single target file) required reading only ~70 lines of
directly relevant content — a reduction of **over 80%** in context loaded per
investigation phase.

### 7. How did the graph-guided agent save tokens / reduce unnecessary reads?
The `hot_*.md` pages **pre-filter**: they identify the exact file and the exact bug
category before the agent touches any source. Subagent Alpha never loaded Math Quiz
content; Subagent Beta never loaded Polygons content; the Gatekeeper node wiped
state between phases. Measured **70.7% input-token reduction** —
[`reports/efficiency_report.md`](../reports/efficiency_report.md) (modeled) and
[`reports/efficiency_live_results.md`](../reports/efficiency_live_results.md)
(real Groq).

### 8. What improvements, extensions, or agent mechanisms would you add?
- **Centrality-ranked suspect list:** score nodes by betweenness centrality ×
  proximity to failing tests.
- **Dynamic git diff** generated from `graph.json` to show exactly which edges
  change after a fix.
- **Orphan node detector:** auto-document nodes with ≤1 connection (19 found,
  incl. 4 notable documentation orphans: `Introduction`, `Objectives`, `The Files`,
  `MIT License`) — *built* as the Phase 7 extension.
- **Impact report:** given a changed node, traverse outbound edges to predict what
  breaks.
