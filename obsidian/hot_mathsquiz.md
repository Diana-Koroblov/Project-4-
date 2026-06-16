# Hot Context - Math Quiz Bug Investigation

**Supervisory Directive for AI Agent:**
This investigation focuses SOLELY on the `mathsquiz/` component. **DO NOT** attempt to read, parse, or interact with any files in the `polygons/` directory during this phase.

**Main Suspects (Relevant Files):**
* `src/broken-python/mathsquiz/mathsquiz.py` (Single Source of Truth)
* `src/broken-python/mathsquiz/mathsquiz-step1.py` through `step3.py` (Legacy clutter)

**Problem Description:**
The Math Quiz system contains logical inconsistencies and legacy "step" files that heavily clutter the namespace and create code duplication. The execution flow is fragmented.

**Refactoring Objectives:**
* **Consolidation:** Analyze the overlapping methods across the step files and consolidate the logic into a single, functional, bug-free implementation in `src/broken-python/mathsquiz/mathsquiz.py`.
* **Clean-up:** Identify redundant files and suggest their removal to clean the graph.
* **Validation:** Implement standard unit tests to validate the quiz flow.
* Ensure zero cross-contamination with the Polygons system.