### System Index - Broken Python

Welcome to the project's knowledge space. This repository contains two independent components.

**Agent Directive:** These are two distinct communities in the graph. The agent MUST investigate them sequentially. It must complete the investigation of one, perform a Context Reset (`/compact`), and only then load the context for the other to maintain high signal-to-noise ratio.

#### Navigation and Investigation Paths

1. **Polygons System:** A system for drawing polygons using the Turtle library in the `polygons/` folder. This is an independent component.
   * To jump to the focused context of the investigation, open the [[hot_polygons]] page.

2. **Math Quiz:** Files in the `mathsquiz/` folder. This is a separate independent component requiring its own investigation path.
   * To jump to the focused context, open the [[hot_mathsquiz]] page.

#### Graphic Mapping
* [[GRAPH_REPORT]] - The automatically generated report that maps the entire system.

#### Before / After (post-refactoring)
* [[knowledge_delta]] - What changed between the before-state and after-state graphs (God Functions eliminated, OOP nodes added, orphans unchanged).
