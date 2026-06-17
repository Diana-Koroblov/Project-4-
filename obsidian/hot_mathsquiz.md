# Hot Context — Math Quiz (After-State ✅ RESOLVED)

**Status:** Consolidated and verified — this page describes the *repaired* codebase.
**Scope:** SOLELY `mathsquiz/`; do not touch `polygons/`.

**Canonical file:** [`mathsquiz.py`](../src/broken-python/mathsquiz/mathsquiz.py) — single source of truth; legacy `mathsquiz-step1..3.py` superseded ([step analysis](../reports/mathsquiz_step_analysis.md)).

**Architecture now (OOP):**
* `MathQuiz` class: `__init__`, `check_answer`, `ask_question`, `run`, `display_result`.
* Questions are `(first, second)` pairs in `QUESTIONS`; the answer is computed as `first*second`, so it can't drift from the prompt.
* No procedural code outside `if __name__ == "__main__"`.

**Bugs fixed (7):**
1. Python-2 `print "..."` → `print(...)`.
2. `if answer = N` → `int(answer) == ...` (comparison + str→int).
3. `else if` → `elif`.
4. Score never incremented → `self.score += 1` on correct.
5. Six wrong answers → computed from operands.
6. Only 6 of the promised 10 questions → 10 questions; total uses `len()`.
7. Every block "Question 1" → `enumerate` → "Question N".

**Full trail:** [Bug Analysis](../reports/bug_analysis.md) · graph delta: [[knowledge_delta]].
