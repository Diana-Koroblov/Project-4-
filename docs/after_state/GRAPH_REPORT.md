# Graph Report - broken-python  (2026-06-16)

## Corpus Check
- 7 files · ~1,748 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 35 nodes · 30 edges · 12 communities (6 shown, 6 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `aec2f8ec`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]

## God Nodes (most connected - your core abstractions)
1. `Polygon` - 8 edges
2. `Shape` - 6 edges
3. `Maths Quiz` - 4 edges
4. `Abstract base class for drawable 2-D shapes.` - 1 edges
5. `Return the perimeter of the shape.` - 1 edges
6. `A regular polygon with ``sides`` edges, each ``length`` units long.` - 1 edges
7. `Sum of the interior angles: (n - 2) * 180.` - 1 edges
8. `Single interior angle of a regular polygon: (n - 2) * 180 / n.` - 1 edges
9. `Perimeter: number of sides times the edge length.` - 1 edges
10. `Draw the polygon with the turtle, turning 360/n degrees per edge.` - 1 edges

## Surprising Connections (you probably didn't know these)
- `Polygon` --inherits--> `Shape`  [EXTRACTED]
  polygons/polygons.py → polygons/polygons.py  _Bridges community 0 → community 4_

## Import Cycles
- None detected.

## Communities (12 total, 6 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.33
Nodes (4): ABC, Return the perimeter of the shape., Abstract base class for drawable 2-D shapes., Shape

### Community 1 - "Community 1"
Cohesion: 0.40
Nodes (4): Introduction, Maths Quiz, Objectives, The Files

## Knowledge Gaps
- **4 isolated node(s):** `broken-python`, `Introduction`, `Objectives`, `The Files`
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Polygon` connect `Community 4` to `Community 0`, `Community 5`, `Community 6`, `Community 7`, `Community 8`?**
  _High betweenness centrality (0.198) - this node is a cross-community bridge._
- **Why does `Shape` connect `Community 0` to `Community 4`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **What connects `Abstract base class for drawable 2-D shapes.`, `Return the perimeter of the shape.`, `A regular polygon with ``sides`` edges, each ``length`` units long.` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._