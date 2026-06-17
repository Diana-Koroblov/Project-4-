# Token Efficiency Report — Guided vs. Naive Baseline

**Task:** 6.2.1 | **Date:** 2026-06-17
**Source data:** [`results/token_log.jsonl`](../results/token_log.jsonl) (4 records: 2 modes × 2 phases)

## Thesis

A naive debugging agent answers each question by reading the **entire**
`src/broken-python/` tree into context. The graph-guided agent instead follows
the Obsidian/Graphify map and reads only an entry page plus the **single**
targeted source file for the community under investigation. This report proves
the resulting token savings with measured numbers.

> **Headline result: 70.9% reduction in input (context) tokens** — above the
> §5.4 KPI of >70% — achieved while reading **5 file-loads instead of 18**.

## Methodology & Reproducibility

- **Baseline** ([`src/hw4/baseline_agent.py`](../src/hw4/baseline_agent.py)) recursively reads every file under
  `src/broken-python/` (excluding `__pycache__` and undecodable binaries) and
  re-sends that whole context on each phase's question. This is the
  control-group anti-pattern.
- **Guided** ([`src/hw4/efficiency.py`](../src/hw4/efficiency.py) → `GUIDED_READS`) mirrors the real agent's reading
  pattern: `index.md` + `hot_polygons.md` + `polygons.py` for the Polygons
  phase; `hot_mathsquiz.md` + `mathsquiz.py` for the Math Quiz phase (the
  Gatekeeper wipes context between them, so the index is not re-read).
- **Token counting** is a deterministic ~4-chars-per-token estimate
  (`estimate_tokens`). The **same** estimator is applied to both modes, so the
  *ratio* between them is independent of the estimate's absolute accuracy and is
  byte-for-byte reproducible from the source files.
- **Output tokens** model the emitted fix as the corrected source file for that
  phase. Both modes emit the *same* fix, so output is identical and cancels out
  of the comparison — the savings are entirely on the input/context side.
- **Regenerate:** `uv run python src/hw4/efficiency.py` (rewrites
  `results/token_log.jsonl` and prints the reductions). A regression test
  (`tests/test_efficiency.py::TestCompare::test_meets_70_percent_input_reduction_kpi`)
  fails if the input reduction ever drops to ≤70%.

## Results — the four §5.5 metrics

### (a) Total tokens in / out, per phase

| Phase | Mode | Tokens in | Tokens out | Total |
|-------|------|----------:|-----------:|------:|
| Polygons | Baseline | 3,792 | 445 | 4,237 |
| Polygons | **Guided** | **1,070** | 445 | **1,515** |
| Math Quiz | Baseline | 3,792 | 801 | 4,593 |
| Math Quiz | **Guided** | **1,137** | 801 | **1,938** |
| **TOTAL** | Baseline | **7,584** | 1,246 | **8,830** |
| **TOTAL** | **Guided** | **2,207** | 1,246 | **3,453** |

- **Input-token reduction: 70.9%** (7,584 → 2,207) — Polygons 71.8%, Math Quiz 70.0%.
- **Total-token reduction: 60.9%** (8,830 → 3,453) — lower only because the
  identical emitted fix (output) is counted in both modes; the input figure is
  the meaningful efficiency metric.

### (b) Files / text units read

| Mode | Unique files | File-loads (× phases) | Noise files loaded |
|------|-------------:|----------------------:|--------------------|
| Baseline | 9 | 18 | 8 of 9 per phase: `LICENSE.txt`, `README.md`, `mathsquiz/README.md`, `.gitignore`, **3 redundant `mathsquiz-step*.py`**, + the other community's source |
| **Guided** | 5 | 5 | 0 — only the entry page(s) and the one relevant source file |

**72.2% fewer file-loads** (18 → 5). The baseline cannot tell signal from noise,
so it ingests the MIT licence, two READMEs and the three superseded step files
on *every* question; the guided agent never touches them.

### (c) Iterations / investigation rounds

| Mode | Rounds to reach the target file | Localisation mechanism |
|------|-------------------------------:|------------------------|
| Baseline | 1 monolithic context of 9 files, **no localisation** | none — the model must scan everything and self-filter |
| **Guided** | **1 targeted source read per phase** | the `hot_*.md` page names the suspect file before any source is opened |

The guided agent's bounded tool loop (`read_obsidian_page → extract/read
target → emit fix`) reaches the one relevant file directly. The baseline has no
navigation step, so all filtering happens implicitly inside a context window
padded with ~8× irrelevant material.

### (d) Quality / speed of reaching the root cause

| Dimension | Baseline | Guided |
|-----------|----------|--------|
| Rounds-to-root-cause | High — must locate the bug among 9 files incl. 3 near-duplicate step files | **1** — hot page pre-states the bug categories |
| Correct-fix-on-first-try | At risk — `mathsquiz-step1..3.py` are plausible-but-wrong edit targets; "lost in the middle" over a large context | **High** — only the canonical file is in scope |
| Cross-contamination | Polygons + Math Quiz share one window every turn | **Zero** — Alpha never sees Math Quiz, Beta never sees Polygons (Gatekeeper reset) |

## Conclusion

The graph-guided, community-isolated strategy cuts **input tokens by 70.9%** and
**file-loads by 72.2%** versus the naive whole-repo read, while improving
root-cause localisation (one targeted file per phase vs. nine) and eliminating
cross-domain contamination. The >70% KPI is met and is reproducible from
`results/token_log.jsonl`.

*Note:* the guided figure includes the Obsidian navigation overhead (the
`index.md` / `hot_*.md` pages). Counting source code alone, the guided agent
reads ~70 lines per phase vs. the full tree — an even larger reduction — but the
honest end-to-end figure that includes navigation context is the 70.9% reported
here.
