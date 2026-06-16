# Graph Report - broken-python  (2026-06-15)

## Corpus Check
- 7 files · ~1,763 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 27 nodes · 23 edges · 6 communities (5 shown, 1 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 1.0)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fc222e24`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 4|Community 4]]

## God Nodes (most connected - your core abstractions)
1. `Polygon` - 4 edges
2. `Maths Quiz` - 4 edges
3. `broken-python` - 3 edges
4. `calc_polygon_details()` - 2 edges
5. `# TODO: find a better way to work this stuff out` - 1 edges
6. `# TODO: perhaps I should use the class Polygon instead!` - 1 edges
7. `# TODO: make this work for any type of polygon` - 1 edges
8. `Introduction` - 1 edges
9. `Objectives` - 1 edges
10. `The Files` - 1 edges

## Surprising Connections (you probably didn't know these)
- `broken-python` --references--> `MIT License`  [INFERRED]
  README.md → LICENSE.txt

## Import Cycles
- None detected.

## Communities (6 total, 1 thin omitted)

### Community 1 - "Community 1"
Cohesion: 0.25
Nodes (6): Object, calc_polygon_details(), Polygon, # TODO: find a better way to work this stuff out, # TODO: perhaps I should use the class Polygon instead!, # TODO: make this work for any type of polygon

### Community 4 - "Community 4"
Cohesion: 0.50
Nodes (4): Introduction, Maths Quiz, Objectives, The Files

## Knowledge Gaps
- **4 isolated node(s):** `Introduction`, `Objectives`, `The Files`, `MIT License`
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Maths Quiz` connect `Community 4` to `Community 0`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `broken-python` (e.g. with `README.md` and `MIT License`) actually correct?**
  _`broken-python` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `# TODO: find a better way to work this stuff out`, `# TODO: perhaps I should use the class Polygon instead!`, `# TODO: make this work for any type of polygon` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._