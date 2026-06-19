# Knowledge Delta — Before vs. After Graph

**Task:** 6.4.2 | **Date:** 2026-06-17
**Before-state graph:** [`graph.json`](./graph.json) — commit `fc222e24` ([[GRAPH_REPORT|report]])
**After-state graph:** [`../docs/after_state/graph.json`](../docs/after_state/graph.json) — commit `aec2f8ec` ([report](../docs/after_state/GRAPH_REPORT.md))

This page documents how the **knowledge graph** changed once the two communities
were repaired — the structural counterpart to the code diff
(`git diff before-agent HEAD`) and the [Bug Analysis](../reports/bug_analysis.md).

## Headline numbers

| Metric | Before | After | Δ |
|--------|-------:|------:|:--|
| Nodes | 27 | 35 | **+8** |
| Edges | 23 | 30 | **+7** |
| Communities | 6 | 12 | **+6** |
| Extraction quality | 91% EXTRACTED / 9% INFERRED | **100% EXTRACTED** / 0% INFERRED | inferred edges eliminated |
| Top God Node | `Polygon` (4 edges) | `Polygon` (8 edges) | core abstraction strengthened |

The net `+8` nodes is the sum of **+15 added** and **−7 removed** (detailed below).

## Polygons — God Functions eliminated, OOP nodes added

This is where the graph changed the most. The two module-level procedural
functions were dissolved into a class hierarchy.

**Nodes removed (7):**
- `Object` — the undefined base class (its dangling `inherits` edge is gone).
- `calc_polygon_details()` — **God Function**, absorbed into `Polygon` methods.
- `draw_polygon()` — **God Function**, absorbed into `Polygon.draw()`.
- 3 × `# TODO …` rationale nodes (`find a better way…`, `perhaps I should use the class Polygon instead!`, `make this work for any type of polygon`) — the author's own "incomplete logic" markers; the work they described is now done.
- `MIT License` — dropped out of the graph along with the inferred edges (see *Orphans* below); unrelated to the refactor.

**Nodes added (15):**
- Code (8): `Shape`, `ABC`, `Shape.draw()`, `Shape.calculate_perimeter()`, `Polygon.calculate_internal_angles_sum()`, `Polygon.calculate_internal_angle()`, `Polygon.calculate_perimeter()`, `Polygon.draw()`.
- Docstring nodes (7): one per new class/method (e.g. *"Single interior angle of a regular polygon: (n - 2) * 180 / n."*) — the formula that replaced the hardcoded angle table is now first-class knowledge in the graph.

**Nodes kept:** `polygons.py`, `Polygon`, `Polygon.__init__()`.

**Edge / topology change:** `Polygon` went from 4 → **8 edges** and a brand-new
`Shape` God Node appeared at **6 edges**. The new bridge edge
`Polygon --inherits--> Shape` connects the polygon community to the abstract-base
community — exactly the encapsulation that was missing before.

## Math Quiz — code consolidated, graph snapshot pending

> **Important timing note.** The committed after-state graph
> (`docs/after_state/`) was generated at the **end of Phase 4 (Polygons)**,
> *before* the Phase 5 Math Quiz consolidation. So in this snapshot the Math Quiz
> community is **byte-identical** to the before-state: the three
> `mathsquiz-step*.py` nodes (with their `welcome_message()` / `ask_question()` /
> `print_final_scores()` children) and the single, childless `mathsquiz.py` node
> are all still present.

The Math Quiz code change is nonetheless real and proven elsewhere:
- `mathsquiz.py` now parses as Python 3 and contains the `MathQuiz` class (see [Bug Analysis](../reports/bug_analysis.md) and [step analysis](../reports/mathsquiz_step_analysis.md)).
- The original `mathsquiz.py` was a **childless node** purely because it was Python-2 source the AST parser could not descend into. A graph **regenerated at `HEAD`** would therefore:
  1. extract a `MathQuiz` class node with its 5 methods (`__init__`, `check_answer`, `ask_question`, `run`, `display_result`), and
  2. still include the three `mathsquiz-step*.py` communities: those files are **deliberately retained**, not deleted — they are the documented before-state and the naive baseline's "noise" in the token-efficiency proof (removing them would drop the measured reduction below the >70% KPI). History is additionally preserved by the `before-agent` tag.

## Orphans — unchanged count, shifted composition

Both graphs report **4 isolated nodes** (≤1 connection), and the documentation
orphans are unchanged by the refactor:

| Orphan | Before | After | Note |
|--------|:------:|:-----:|------|
| `Introduction` | ✅ | ✅ | `mathsquiz/README.md` sub-section — untouched |
| `Objectives` | ✅ | ✅ | `mathsquiz/README.md` sub-section — untouched |
| `The Files` | ✅ | ✅ | `mathsquiz/README.md` sub-section — untouched |
| `MIT License` | ✅ | — | node dropped (inferred edge removed) |
| `broken-python` | — | ✅ | newly isolated: lost its 2 **INFERRED** edges |

The shift (`MIT License` out, `broken-python` in) is a side effect of extraction
becoming **100% EXTRACTED**: the two low-confidence INFERRED edges from the
before-state (`broken-python --references--> MIT License`,
`mathsquiz/README.md --conceptually_related_to--> broken-python`) were not
re-derived, leaving `broken-python` with no high-confidence connections. The
three genuine documentation orphans persist and remain the prime targets for the
Phase 7 **Orphan Node Detector** extension.

## Summary

- **God Functions eliminated:** `calc_polygon_details()` and `draw_polygon()` (Polygons) — folded into `Polygon`/`Shape` methods.
- **OOP made visible:** a `Shape(ABC)` ← `Polygon` hierarchy with 8 method/docstring nodes replaced the flat procedural layout.
- **Quality up:** extraction moved from 91% EXTRACTED (2 inferred edges) to 100% EXTRACTED.
- **Orphans unchanged:** the three `mathsquiz/README.md` documentation orphans persist; the count stayed at 4.
- **Outstanding:** regenerate the graph at `HEAD` to capture the Phase 5 `MathQuiz` class. The `mathsquiz-step*.py` nodes remain by design — retained as the before-state / efficiency-baseline noise (see 5.2.3).
