# Hot Context - Polygons System Investigation

**Supervisory Directive for AI Agent:**
This investigation focuses SOLELY on the `polygons/` component. **DO NOT** attempt to read, parse, or interact with any files in the `mathsquiz/` directory during this phase.

**Main Suspects (Relevant Files):**
* `polygons.py`

**Problem Description:**
The Polygons system suffers from syntax errors, architectural debt, and severe OOP violations:
1. **Syntax Errors:** Incorrect inheritance (`Object` instead of `object`) and Java-style instantiation (`new Polygon`).
2. **OOP Violations:** Procedural code acting as a "God Function". `calc_polygon_details` and `draw_polygon` are isolated outside the `Polygon` class, completely ignoring state encapsulation.
3. **Hardcoded Logic:** Angle calculations are hardcoded only for 3 and 4 sides, failing for any generic polygon.
4. **Broken Dynamic Drawing:** The turtle loop is fixed to `range(0, 6)` with a `60` degree angle, forcing it to draw a hexagon regardless of user input.

**Refactoring Objectives:**
* Fix all syntax and compilation errors.
* Refactor the system into a proper Object-Oriented architecture: encapsulate calculation and drawing methods inside the `Polygon` class.
* Implement dynamic mathematical calculations for any number of sides.
* Ensure zero cross-contamination with the Math Quiz system.