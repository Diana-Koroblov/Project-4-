# Hot Context — Polygons System (After-State ✅ RESOLVED)

**Status:** Refactored and verified — this page describes the *repaired* codebase.
**Domain isolation:** still scoped SOLELY to `polygons/`; do not touch `mathsquiz/`.

**File:** [`polygons.py`](../src/broken-python/polygons/polygons.py)

**Architecture now (OOP):**
* `Shape(ABC)` — abstract base declaring `draw()` + `calculate_perimeter()`.
* `Polygon(Shape)` — encapsulates state (`sides`, `length`) and all behaviour as methods: `calculate_internal_angle()`, `calculate_internal_angles_sum()`, `calculate_perimeter()`, `draw()`.
* No module-level "God Functions" remain (`calc_polygon_details`/`draw_polygon` are gone); runnable code lives only under `if __name__ == "__main__"`.

**Bugs fixed (4):**
1. `Object` base class → inherits real `Shape(ABC)` (no undefined `Object`).
2. `new Polygon(...)` → idiomatic `Polygon(...)`.
3. Hardcoded angle table → formula `(n-2)*180/n` (3→60, 4→90, 5→108, 6→120).
4. Turtle loop hardcoded to a hexagon → `range(self.sides)` turning `360/self.sides`.

**Full trail:** [Bug Analysis](../reports/bug_analysis.md) · graph delta: [[knowledge_delta]].
