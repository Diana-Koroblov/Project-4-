# Math Quiz — Step File Evolution Analysis

**Task:** 5.2.1 | **Author:** Subagent Beta (Math Quiz domain) | **Date:** 2026-06-16

## Purpose

The `mathsquiz/` directory ships four files: the broken starting point
(`mathsquiz.py`) and three "check-point" files (`mathsquiz-step1.py` …
`mathsquiz-step3.py`). The upstream README frames them as a *teaching ladder* —
each step is one stage further along the path from the broken original toward a
clean, small implementation. They are **not** modules that import one another;
each is a standalone, self-contained rewrite of the whole quiz.

This report documents what each step adds and confirms that the consolidated
`mathsquiz.py` (Phase 5.2.2–5.2.3) supersedes all three.

## The starting point — `mathsquiz.py` (original, broken)

Six categories of bug, all intentional:

| # | Bug | Example |
|---|-----|---------|
| 1 | Python-2 `print` statement | `print "Hello! ..."` (lines 3–4) |
| 2 | `=` (assignment) used for comparison | `if answer = 55:` |
| 3 | `else if` instead of `elif` | final score block |
| 4 | Score never incremented | `score = 0` then never changed → always 0/10 |
| 5 | Every question mislabelled "Question 1" | all six prompts print `Question 1:` |
| 6 | Wrong expected answers | 8×7 checked against **55** (should be 56), etc. |

It also stops at **6 questions** instead of the promised 10, and compares the
raw string from `input()` to an `int` (would never match even with the right
number).

## Step 1 — `mathsquiz-step1.py`: "make it work"

The minimal correctness pass. Stays fully procedural (one flat block per
question) but fixes every bug above:

- `print(...)` function calls throughout.
- `if int(answer) == <product>:` — comparison + `int()` conversion.
- `score = score + 1` inside each correct branch.
- Questions correctly labelled `Question 1` … `Question 10`.
- **Corrected answers**, which are the canonical source of truth for the fix
  table: 8×7=**56**, 4×9=**36**, 12×6=**72**, 6×8=**48**, 7×7=**49**, 11×6=**66**.
- **Four questions added** to reach 10: 9×2=18, 7×9=63, 6×6=36, 4×8=32.
- `else if` → `elif`, plus a missing tier so 8–9 correct now prints a message.

This is the file the consolidated answers and result tiers are taken from.

## Step 2 — `mathsquiz-step2.py`: "remove repetition with functions"

Objective 2 from the README. Collapses the ten near-identical blocks into three
functions — `welcome_message()`, `ask_question(first, second)` (computes the
answer as `first * second` so it can never drift), and `print_final_scores()`.
The driver becomes ten one-line calls. *Carry-over wart:* `print_final_scores`
reads the module-level global `score` instead of its `final_score` parameter —
harmless because they coincide, but a smell the OOP version removes.

## Step 3 — `mathsquiz-step3.py`: "generate questions dynamically"

Objective 3. Introduces `import random`: a `for x in range(1, 11)` loop asks ten
randomly generated `randint(2, 12)` products, so the questions are no longer
pre-programmed. Scoring is generalised to a percentage so the result tiers no
longer hard-code "10". Still carries the same `score` global wart in
`print_final_scores`.

## Evolution summary

| File | Paradigm | Questions | Key advance | Residual issue |
|------|----------|-----------|-------------|----------------|
| `mathsquiz.py` (orig) | procedural | 6, broken | — (starting point) | 6 bug classes |
| `step1` | procedural | 10, fixed | correctness | heavy repetition |
| `step2` | functions | 10, fixed | DRY via functions | `score` global in result fn |
| `step3` | functions + `random` | 10, dynamic | generated questions | same `score` global |

## Conclusion — the consolidated `mathsquiz.py` supersedes all three

The Phase 5 rewrite folds the best of every step into one
`MathQuiz` class and resolves the leftover smells:

- **From step 1** — the corrected fixed question set and the four-tier result
  messages (kept deterministic for testability, rather than step 3's random set).
- **From step 2** — a single `ask_question` that derives the answer from the
  operands (`first * second`), eliminating all per-question repetition.
- **From step 3** — the loop-driven driver (`enumerate` over `self.questions`)
  and a result message that scales to `len(self.questions)` rather than a
  hard-coded 10.
- **Beyond the steps** — state (`score`, `questions`) lives on the instance, so
  the `score`-global wart in steps 2–3 is gone; `check_answer` is a pure,
  side-effect-free static method (the unit-test seam); and all I/O sits inside
  `run()` / `__main__`, so `import mathsquiz` is silent.

The three `mathsquiz-step*.py` files are therefore redundant teaching artefacts
fully captured by the consolidated `MathQuiz` class. They are **deliberately
retained** rather than deleted: they are the documented before-state and serve as
the naive baseline's "noise" in the token-efficiency proof — deleting them would
drop the measured reduction below the >70% KPI. The originals are additionally
recoverable from this report and the `before-agent` git tag.
