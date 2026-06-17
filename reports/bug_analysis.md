# Bug Analysis Report — broken-python

**Tasks:** 6.3.1 (Polygons) · 6.3.2 (Math Quiz) | **Date:** 2026-06-17
**Subject:** `martinpeck/broken-python`, vendored under [`src/broken-python/`](../src/broken-python/)
**Before-state proof:** `git show before-agent:<path>` · **After-state:** working tree at `HEAD`

## Summary

Two independent communities were reverse-engineered from the
[Graphify](../obsidian/graph.json) knowledge graph and repaired by two
domain-isolated subagents (Alpha → Polygons, Beta → Math Quiz). **11 bugs** were
found and fixed in total: **4** in Polygons and **7** in Math Quiz. Every fix was
located by traversing the graph from the Obsidian entry pages
([`index.md`](../obsidian/index.md) → [`hot_polygons.md`](../obsidian/hot_polygons.md) /
[`hot_mathsquiz.md`](../obsidian/hot_mathsquiz.md)) to the single suspect source
file — never by scanning the whole repository (see
[`efficiency_report.md`](./efficiency_report.md) for the 71% token saving this
produced).

| # | Community | Bug | Class | Status |
|---|-----------|-----|-------|--------|
| 1 | Polygons | `Object` base class | `NameError` | ✅ Fixed |
| 2 | Polygons | `new Polygon(...)` instantiation | `SyntaxError` | ✅ Fixed |
| 3 | Polygons | Hardcoded angle table | Logic | ✅ Fixed |
| 4 | Polygons | Turtle loop fixed to a hexagon | Logic | ✅ Fixed |
| 5 | Math Quiz | Python-2 `print` statements | `SyntaxError` | ✅ Fixed |
| 6 | Math Quiz | `=` used for comparison | `SyntaxError` | ✅ Fixed |
| 7 | Math Quiz | `else if` instead of `elif` | `SyntaxError` | ✅ Fixed |
| 8 | Math Quiz | Score never incremented | Logic | ✅ Fixed |
| 9 | Math Quiz | 6 wrong expected answers | Logic | ✅ Fixed |
| 10 | Math Quiz | Only 6 of the promised 10 questions | Logic | ✅ Fixed |
| 11 | Math Quiz | Every question mislabelled "Question 1" | Logic | ✅ Fixed |

## How the investigation was driven (the graph trail)

The agent never opened the repository blind. For each community it:

1. Read [`obsidian/index.md`](../obsidian/index.md) to learn the two communities exist and must be investigated **sequentially** (with a context reset between them).
2. Opened the community's `hot_*.md` page, which names the **single** suspect file.
3. Resolved graph nodes to source via the surgical tools `read_obsidian_page` → `extract_node_content` / `read_source_file`, then applied the fix with `write_source_file`.

The graph node IDs cited below come from [`obsidian/graph.json`](../obsidian/graph.json)
(before-state, commit `fc222e24`).

---

# Part 1 — Polygons community

**Suspect file:** [`src/broken-python/polygons/polygons.py`](../src/broken-python/polygons/polygons.py)
**Graph community:** Community 1 — nodes `polygons.py`, `Polygon`, `Object`,
`.__init__()`, `calc_polygon_details()`, `draw_polygon()`, plus three `# TODO`
rationale nodes.

### Bug 1 — `Object` as the base class

- **Problem statement:** The module would not import: `class Polygon(Object):` raised `NameError: name 'Object' is not defined`.
- **Root cause:** Python's universal base class is the lowercase built-in `object`; `Object` (capital O, Java/C# style) is not defined in Python.
- **Investigation trail:** Graph edge `polygons_polygons_polygon --inherits--> object`. The `Object` node had an **empty `source_file`** — a tell-tale that it was an unresolved/external symbol, not a real class in the repo. That dangling inheritance edge pointed straight at the broken base class.
- **Fix applied:** During the OOP refactor the class now inherits a real abstract base: `class Polygon(Shape)`, where `Shape(ABC)` is defined in-file. This removes the undefined `Object` entirely. See [polygons.py:17](../src/broken-python/polygons/polygons.py#L17).

### Bug 2 — `new Polygon(...)` instantiation

- **Problem statement:** Even after Bug 1, the file raised `SyntaxError` at `poly = new Polygon(sides, ...)`.
- **Root cause:** Python has no `new` keyword; objects are created by calling the class directly (`Polygon(...)`). `new` is C++/Java/JavaScript syntax.
- **Investigation trail:** Node `calc_polygon_details()` with edge `calc_polygon_details() --calls--> Polygon` (at L29). Reading that God Function's body exposed the illegal `new` token at the call site.
- **Fix applied:** The `calc_polygon_details()` God Function that contained the `new` call was eliminated entirely (see Bug 3); the surviving instantiation in the `__main__` guard is the idiomatic `polygon = Polygon(sides)`. See [polygons.py:48](../src/broken-python/polygons/polygons.py#L48).

### Bug 3 — Hardcoded angle table (only 3- and 4-sided polygons correct)

- **Problem statement:** `calc_polygon_details()` returned correct angles only for triangles and squares; every other polygon got the placeholder values `internal_angles_sum = 1000`, `internal_angles = 200`.
- **Root cause:** The angle logic was a literal `if sides == 3 / elif sides == 4 / else` lookup table instead of the general formula. The author even flagged it: the rationale node `# TODO: find a better way to work this stuff out` (L18) is attached to this file.
- **Investigation trail:** Three rationale nodes (`# TODO: find a better way…`, `# TODO: perhaps I should use the class Polygon instead!`, `# TODO: make this work for any type of polygon`) all have `rationale_for --> polygons.py` edges — the graph surfaced the author's own admissions of incomplete logic as first-class nodes, pinpointing the defect before the code was even read.
- **Fix applied:** Replaced the table with the closed-form regular-polygon formulae, now encapsulated as `Polygon` methods:
  - `calculate_internal_angles_sum()` → `(sides - 2) * 180`
  - `calculate_internal_angle()` → `(sides - 2) * 180 / sides`
  - Verified: 3→60°, 4→90°, 5→108°, 6→120°. See [polygons.py:24-30](../src/broken-python/polygons/polygons.py#L24-L30).

### Bug 4 — Turtle loop hardcoded to a hexagon

- **Problem statement:** `Polygon(5).draw()` (or any side count) always drew a **hexagon**, ignoring the user's input.
- **Root cause:** `draw_polygon()` looped `for i in range(0, 6)` and turned `t.right(60)` — both constants for a 6-sided shape — instead of using the polygon's own `sides`. The `# TODO: make this work for any type of polygon` rationale node (L50) marks exactly this block.
- **Investigation trail:** Node `draw_polygon()` (edge `polygons.py --contains--> draw_polygon()` at L41). Reading the function body revealed the two hardcoded `6`/`60` constants and the rationale TODO attached at L50.
- **Fix applied:** Drawing is now a `Polygon.draw()` method that loops `for _ in range(self.sides)` and turns `t.right(360 / self.sides)` (exterior angle), so a pentagon traces 5 edges with 72° turns. See [polygons.py:36-43](../src/broken-python/polygons/polygons.py#L36-L43).

**Architectural outcome:** the two module-level "God Functions"
(`calc_polygon_details`, `draw_polygon`) were dissolved into methods of a
`Polygon` class that now inherits an abstract `Shape(ABC)` base
(`draw()` + `calculate_perimeter()` abstract methods). No procedural code remains
outside the `if __name__ == "__main__"` guard.

---

# Part 2 — Math Quiz community

**Suspect file:** [`src/broken-python/mathsquiz/mathsquiz.py`](../src/broken-python/mathsquiz/mathsquiz.py)
**Graph community:** Community 0/4 — the README sub-sections `Maths Quiz`,
`Introduction`, `Objectives`, `The Files`, plus the opaque `mathsquiz.py` node.
**Note:** because the original file was **Python-2 source**, Graphify's AST parser
could not descend into it — `mathsquiz.py` appears as a *single, childless node*
(no functions extracted). That opacity was itself the first signal that the file
would not even parse under Python 3. The three legacy `mathsquiz-step*.py` files
*did* parse and appear as separate communities; their evolution is analysed in
[`mathsquiz_step_analysis.md`](./mathsquiz_step_analysis.md), which confirms the
consolidated `mathsquiz.py` supersedes all three.

### Bug 5 — Python-2 `print` statements

- **Problem statement:** The file raised `SyntaxError` on the very first line: `print "Hello! ..."`.
- **Root cause:** In Python 3 `print` is a function; the Python-2 statement form `print "..."` is a syntax error.
- **Investigation trail:** Childless `mathsquiz.py` node (no AST children) ⇒ file does not parse ⇒ open raw source via `read_source_file`; the leading `print "…"` lines are the first defect.
- **Fix applied:** All output uses the `print(...)` function form, e.g. [mathsquiz.py:54-55](../src/broken-python/mathsquiz/mathsquiz.py#L54-L55).

### Bug 6 — Assignment (`=`) used for comparison

- **Problem statement:** `if answer = 55:` raised `SyntaxError` (and would have been an assignment, not a test, even if allowed). The same defect appeared in the final-score block (`else if score = 10:`).
- **Root cause:** Equality testing requires `==`; `=` is assignment. Additionally `answer` came from `input()` as a **string**, so it would never equal an `int` without conversion.
- **Investigation trail:** Raw source scan of the six question blocks; every `if answer = <n>:` line is the same defect repeated.
- **Fix applied:** Comparison is centralised in `MathQuiz.check_answer()`, which converts and compares: `int(answer) == first * second`, guarded against non-numeric input. See [mathsquiz.py:38-49](../src/broken-python/mathsquiz/mathsquiz.py#L38-L49).

### Bug 7 — `else if` instead of `elif`

- **Problem statement:** The score-summary cascade used `else if score < 8:` / `else if score = 10:`, a `SyntaxError` in Python.
- **Root cause:** Python spells the construct `elif`; `else if` is C/Java/JavaScript syntax.
- **Investigation trail:** Raw source of the final `print the final scores` block.
- **Fix applied:** Rewritten as a proper `if / elif / elif / else` ladder in `display_result()`. See [mathsquiz.py:78-85](../src/broken-python/mathsquiz/mathsquiz.py#L78-L85).

### Bug 8 — Score never incremented

- **Problem statement:** Even with every answer correct, the program always reported `0 points out of a possible 10`.
- **Root cause:** `score = 0` was initialised but **never increased** — the "Correct!" branch printed a message and did nothing else.
- **Investigation trail:** Raw source — each correct branch contained only `print("Correct!")`, with no `score = score + 1`.
- **Fix applied:** `ask_question()` does `self.score += 1` on a correct answer; `run()` returns the final score (now verifiably 10/10 with correct input). See [mathsquiz.py:57-59](../src/broken-python/mathsquiz/mathsquiz.py#L57-L59).

### Bug 9 — Six wrong expected answers

- **Problem statement:** Every hardcoded "correct" answer was actually wrong, so a perfect player would still score 0.
- **Root cause:** The expected values were typos / unrelated numbers, not the products:

  | Question | In code (wrong) | Correct product |
  |----------|-----------------|-----------------|
  | 8 × 7 | 55 | **56** |
  | 4 × 9 | 49 | **36** |
  | 12 × 6 | 126 | **72** |
  | 6 × 8 | 668 | **48** |
  | 7 × 7 | 77 | **49** |
  | 11 × 6 | 60 | **66** |

- **Investigation trail:** Raw source — compared each prompt's operands against its hardcoded answer.
- **Fix applied:** Answers are no longer hardcoded at all. Questions are stored as `(first, second)` operand pairs in `MathQuiz.QUESTIONS`, and the correct answer is computed as `first * second` — they can never drift out of sync with the prompt again. See [mathsquiz.py:21-32](../src/broken-python/mathsquiz/mathsquiz.py#L21-L32) and [mathsquiz.py:45-47](../src/broken-python/mathsquiz/mathsquiz.py#L45-L47).

### Bug 10 — Only 6 of the promised 10 questions

- **Problem statement:** The intro says "I'm going to ask you 10 maths questions" and the summary says "out of a possible 10", but only 6 questions were implemented.
- **Root cause:** Four question blocks were simply missing (the file ended after question 6).
- **Investigation trail:** Raw source — counted the question blocks (6) against the advertised total (10).
- **Fix applied:** `QUESTIONS` now holds **10** operand pairs; the summary uses `len(self.questions)` rather than a hardcoded `10`, so the promised count and the actual count are guaranteed equal. See [mathsquiz.py:21-32](../src/broken-python/mathsquiz/mathsquiz.py#L21-L32) and [mathsquiz.py:75-77](../src/broken-python/mathsquiz/mathsquiz.py#L75-L77).

### Bug 11 — Every question mislabelled "Question 1"

- **Problem statement:** All six blocks printed `print("Question 1:")`, so the player never knew which question they were on.
- **Root cause:** Copy-paste — the label literal was never updated per block.
- **Investigation trail:** Raw source — identical `Question 1:` literal in every block.
- **Fix applied:** Numbering is generated by `enumerate(self.questions, start=1)` and printed as `f"Question {number}:"`, so labels are always correct and self-maintaining. See [mathsquiz.py:51-54](../src/broken-python/mathsquiz/mathsquiz.py#L51-L54) and [mathsquiz.py:68](../src/broken-python/mathsquiz/mathsquiz.py#L68).

**Architectural outcome:** the procedural script (and the three legacy step
files) collapsed into a single OOP `MathQuiz` class with `__init__`,
`check_answer`, `ask_question`, `run`, and `display_result`. Data (the questions)
is separated from behaviour, and the previously duplicated bugs (wrong answers,
"Question 1", manual `== 10`) are now structurally impossible.

---

## Statistics

- **Total bugs identified:** 11 (Polygons 4 · Math Quiz 7)
- **Total bugs fixed:** 11 (100%)
- **Categories:** `SyntaxError` / parse failures — 5 (`Object`, `new`, Python-2 `print`, `=`-as-comparison, `else if`); logic / correctness — 6 (hardcoded angles, hexagon loop, score never incremented, 6 wrong answers, 6-of-10 questions, duplicate labels).
- **Verification:** `polygons.py` and `mathsquiz.py` import cleanly, pass `ruff check` with zero violations, and are covered by [`tests/test_polygons.py`](../tests/test_polygons.py) (17 tests) and [`tests/test_mathsquiz.py`](../tests/test_mathsquiz.py) (21 tests).
- **Knowledge proof:** the structural before→after change is recorded in [`obsidian/knowledge_delta.md`](../obsidian/knowledge_delta.md).
