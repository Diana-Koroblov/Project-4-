# Live Groq Results — Measured, Not Modeled

**Date:** 2026-06-18 | **Model:** `llama-3.3-70b-versatile` (Groq, free tier)
**Source data:** [`results/token_log_live.jsonl`](../results/token_log_live.jsonl)
**Reproduce:** `uv run python src/hw4/live_efficiency.py`

This report records results from **real Groq API calls**, to complement the
modeled estimate in [`efficiency_report.md`](efficiency_report.md) (which used a
deterministic ~4-chars/token estimator because the build sandbox had no network).
Here the token counts are the exact values Groq's tokenizer returned in
`response.usage_metadata`.

## 1. Token efficiency — MEASURED

Each phase sent two contexts to Groq with the same question: the **graph-guided**
reads (entry page + the one targeted source file) vs. the **naive baseline**
(the entire `src/broken-python/` tree). Identical methodology to `efficiency.py`,
but real tokens.

| Phase | Mode | Real input tokens | File-loads |
|-------|------|------------------:|-----------:|
| Polygons | Baseline | 3,827 | 9 |
| Polygons | **Guided** | **1,065** | 3 |
| Math Quiz | Baseline | 3,827 | 9 |
| Math Quiz | **Guided** | **1,177** | 2 |
| **TOTAL** | Baseline | **7,654** | 18 |
| **TOTAL** | **Guided** | **2,242** | 5 |

- **Measured input-token reduction: 70.7%** (7,654 → 2,242).
  - Polygons: **72.2%**, Math Quiz: **69.2%**.
- The modeled report claimed **70.9%**. Real Groq tokenization came in at
  **70.7%** — the estimate was accurate to within 0.2 points, so the modeled
  proof was sound; this run confirms it against the live API.

*(Output tokens were capped at 512/call only to fit the free-tier rate limit;
output is not part of the efficiency thesis, which is about input/context tokens.)*

## 2. A real rate-limit finding the model could not show

On the first attempt the **baseline** whole-tree call was **rejected by Groq with
HTTP 413**: at the default `max_tokens=8192` reservation it requested 12,019
tokens against the free-tier ceiling of 12,000 tokens/minute. The **guided** call
(smaller context) fit and succeeded. In other words, the naive whole-repo prompt
is so large it does not even fit the free-tier budget once a normal completion is
reserved — a concrete, real-world cost of the anti-pattern that a chars/4 estimate
can never surface. The measurement script now caps the reservation and paces calls
to stay inside the window.

## 3. Live end-to-end agent — now completes (tool_use_failed repaired)

### The limitation that was blocking it

The configured `llama-3.3-70b-versatile` deterministically emits Llama's raw
`<function=read_obsidian_page{...}</function>` tool-call syntax, which Groq's
server-side parser rejects with a 400 `tool_use_failed` (confirmed at temps
0.0 / 0.4 / 0.7; `openai/gpt-oss-20b` also failed on a later turn and
`moonshotai/kimi-k2-instruct` is 404 on this account). This — not just the
no-network sandbox — is why the loop could not previously run.

### The fix: a tool-call repair shim

[`src/hw4/tools/tool_call_repair.py`](../src/hw4/tools/tool_call_repair.py)
(`invoke_with_repair`, wired into the Alpha/Beta nodes) catches the
`tool_use_failed` error, parses the `failed_generation` payload back into a
well-formed `AIMessage(tool_calls=...)` (using a balanced-brace scan so a
`write_source_file` content arg with `{`/`}` is preserved), and returns it so the
graph's ToolNode executes the call exactly as intended. It activates **only** on
`tool_use_failed`, so it is inert for any correctly-formatting model and for the
fake-model unit tests. Covered by `tests/test_tool_call_repair.py` (100%).

### Measured live run — before-state broken code, real repair

`uv run python run_live_agent.py` was run against the **before-agent** broken
source (re-injected via git), then the after-state was restored.

| Result | Value |
|--------|-------|
| Graph traversal | **Completed to END** — `completed_tasks = [alpha:polygons:complete, phase:polygons:complete, beta:mathsquiz:complete]`, `current_phase = mathsquiz` |
| Tools actually invoked | `read_obsidian_page`, `read_source_file`, `write_source_file` (real `ToolMessage`s in the trace) |
| Real repair landed | Agent rewrote `polygons.py` (`class Polygon` — no `Object`/`new`, dynamic `(n-2)*180/n`, `range(self.sides)` turning `360/self.sides`) and `mathsquiz.py` (Python-3 `print`, `int(answer) == first*second`, score increments, 10 questions). Both `py_compile`-clean; **zero** known bug markers remain. |
| Proof | [`results/live_agent_fix.diff`](../results/live_agent_fix.diff) (broken → agent fix), plus `results/live_fix_polygons.py` / `results/live_fix_mathsquiz.py` |
| Measured tokens | 17,587 input / 1,082 output across the **successfully-returned** turns ([`results/live_agent_token_log.jsonl`](../results/live_agent_token_log.jsonl)) |

**Caveat on the token figure.** `usage_metadata` is only available for turns Groq
returns successfully; the `tool_use_failed` turns the shim repairs still consumed
Groq input tokens that are *not* captured here, so 17,587 is a **lower bound** on
true usage. The agent also took several retry turns per file (Llama re-emitting
the malformed format), making this autonomous loop markedly more token-hungry than
the single-shot contexts measured in §1 — a fair, real-world cost of running a
brittle-tool-calling model end-to-end.

### Bottom line

Both halves are now proven on live Groq: the **token-efficiency thesis** (§1,
70.7% measured) *and* the **autonomous tool loop** (§3) — the agent navigates via
its Obsidian/graph tools and repairs the broken code end-to-end. The remaining
quality gap is the model itself: a Groq model with native structured tool-calling
would remove the retry overhead the repair shim currently absorbs.
