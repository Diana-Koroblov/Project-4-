# Prompts Engineering Log

This document records all significant prompts used with AI assistance during the development of this project, per the software submission guidelines (§8.3). Each entry includes the prompt text, model used, what it produced, and any refinements made.

---

## Entry Format
```
### [PL-NNN] <Short Title>
- **Date:** YYYY-MM-DD
- **Model:** e.g., GPT-4o / Claude 3.5 Sonnet
- **Phase:** Project phase (0–8)
- **Prompt:**
  > <exact prompt text>
- **Output Summary:** What the model produced
- **Refinements:** Any follow-up prompts or manual edits needed
- **Verdict:** Accepted / Accepted with edits / Rejected
```

---

## Phase 0 — Knowledge Base & Reverse Engineering

### [PL-001] Generate Obsidian Navigation Index
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 0
- **Prompt:**
  > Based on the Graphify GRAPH_REPORT.md and graph.json, create an Obsidian index.md file that serves as the master navigation router for a LangGraph agent. The index should summarize the two communities (Polygons and Math Quiz), list God Nodes and Orphan Nodes, and link to hot_polygons.md and hot_mathsquiz.md.
- **Output Summary:** Generated `obsidian/index.md` with community summaries, God Node table, Orphan Node list, and navigation links.
- **Refinements:** Added explicit "Zero-Edge Isolation Protocol" section manually.
- **Verdict:** Accepted with edits

### [PL-002] Generate Hot Context Pages
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 0
- **Prompt:**
  > Create focused Obsidian context pages (hot_polygons.md and hot_mathsquiz.md) for a debugging agent. Each page should include: the key files to read, known bugs to fix, the target OOP architecture, and a step-by-step task list for the subagent.
- **Output Summary:** Generated `obsidian/hot_polygons.md` and `obsidian/hot_mathsquiz.md` with bug lists, target schemas, and task checklists.
- **Refinements:** Fixed a path contradiction in hot_mathsquiz.md (changed `src/mathsquiz/` to `src/broken-python/mathsquiz/`).
- **Verdict:** Accepted with edits

### [PL-003] Generate Architecture Diagrams
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 0
- **Prompt:**
  > Generate a Mermaid block schema and OOP class diagram for the before-state of martinpeck/broken-python. Annotate all known bugs inline. Also produce the target after-state OOP schema with Shape as abstract base.
- **Output Summary:** Generated `docs/block_schema.md` and `docs/oop_schema.md` with annotated Mermaid diagrams.
- **Refinements:** None significant.
- **Verdict:** Accepted

---

## Phase 1 — Environment Setup

### [PL-004] Write Comprehensive README
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 1
- **Prompt:**
  > Write a comprehensive README.md for this project. Include: project overview, rationale for choosing martinpeck/broken-python as base repo, repository structure tree, run instructions using uv only (no pip), answers to all 8 research questions from the assignment, Mermaid block schema, OOP schema before/after, LangGraph workflow diagram, and ADR-001 for choosing LangGraph over CrewAI.
- **Output Summary:** Full README.md rewrite covering all required sections.
- **Refinements:** Research question answers were refined for accuracy.
- **Verdict:** Accepted with edits

---

## Phase 2 — LangGraph Orchestration

### [PL-005] Design AgentState and Graph Topology
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 2
- **Prompt:**
  > Design the LangGraph StateGraph for a two-phase debugging agent. The graph must: (1) start with a Router node that reads obsidian/index.md, (2) route to SubagentAlpha for the Polygons phase, (3) pass through a Gatekeeper node that wipes message history between phases using RemoveMessage, (4) route to SubagentBeta for the Math Quiz phase. Define AgentState as a TypedDict with fields: current_phase, messages (with add_messages reducer), errors, completed_tasks, and token_log.
- **Output Summary:** Generated `src/hw4/state.py`, `src/hw4/nodes/router.py`, `src/hw4/nodes/gatekeeper.py`, and graph wiring in `main.py`.
- **Refinements:** Added the bounded tool-loop conditional edge (checks `tool_calls` on the last message) manually.
- **Verdict:** Accepted with edits

### [PL-006] Implement Gatekeeper Node with RemoveMessage
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 2
- **Prompt:**
  > Implement the Gatekeeper node. It must: (1) append 'phase:polygons:complete' to completed_tasks, (2) issue RemoveMessage ops to hard-purge all Alpha messages, (3) advance current_phase to 'mathsquiz'. Prevents 'Lost in the Middle' contamination. Keep under 150 lines.
- **Output Summary:** Generated `src/hw4/nodes/gatekeeper.py` with RemoveMessage logic and phase transition.
- **Refinements:** None.
- **Verdict:** Accepted

---

## Phase 3 — Agent Toolset

### [PL-007] Implement Obsidian Reader and File I/O Tools
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 3
- **Prompt:**
  > Write a LangChain tool called obsidian_reader that reads Obsidian vault pages from obsidian/. Accept page name without .md extension. Apply zero-edge domain isolation: Alpha may only access polygons pages; Beta may only access mathsquiz pages. Add path traversal guard. Import constants from hw4.constants. Also write a file_io tool that reads/writes source files under ALLOWED_SOURCE_ROOT only. Keep each file under 150 lines.
- **Output Summary:** Generated `src/hw4/tools/obsidian_reader.py` and `src/hw4/tools/file_io.py` with domain allowlisting.
- **Refinements:** Added path traversal guard (resolve against vault root).
- **Verdict:** Accepted with edits

### [PL-008] Implement Token Tracker and Efficiency Reporter
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 3
- **Prompt:**
  > Implement token tracking: (1) log each LLM call's input/output tokens to token_log in AgentState, (2) compute baseline (naive whole-repo read) and guided consumption separately, (3) calculate % reduction and write summary to results/efficiency_report.md. Target KPI: >70% reduction. Split into token_tracker.py and efficiency.py if needed to stay under 150 lines each.
- **Output Summary:** Generated `src/hw4/tools/token_tracker.py` and `src/hw4/efficiency.py`.
- **Refinements:** Split into two files to stay under the line limit.
- **Verdict:** Accepted with edits

---

## Phase 4 — Subagent Alpha (Polygons)

### [PL-009] Implement SubagentAlpha and Fix Polygons Bugs
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 4
- **Prompt:**
  > Implement SubagentAlpha as a LangGraph node. It reads hot_polygons.md via obsidian_reader, then investigates and fixes src/broken-python/polygons/polygons.py. Known bugs: Object as base class (NameError), new Polygon() JS-style constructor, hardcoded angle logic, draw_polygon() outside class. Target OOP: Shape abstract base → Polygon subclass with perimeter(), internal_angle(), draw(). Apply Zero-Edge Isolation: Alpha must not read mathsquiz files. Keep alpha.py under 150 lines.
- **Output Summary:** Generated `src/hw4/agents/alpha.py`, `src/hw4/agents/alpha_prompt.py`, and fixed `src/broken-python/polygons/polygons.py`.
- **Refinements:** Added `__main__` guard to polygons.py manually.
- **Verdict:** Accepted with edits

---

## Phase 5 — Subagent Beta (Math Quiz)

### [PL-010] Implement SubagentBeta and Consolidate Math Quiz
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 5
- **Prompt:**
  > Implement SubagentBeta as a LangGraph node. It consolidates mathsquiz.py from the broken step files. Known bugs: Python 2 print, = instead of == in condition, else if instead of elif, score never increments, wrong expected answers (55→56, 49→36, 126→72, 668→48, 77→49, 60→66), only 6 questions. Target: MathQuiz class with QUESTIONS class constant (10 tuples), check_answer (static), ask_question, run, display_result. Zero-Edge Isolation: Beta must not read polygons files. Keep under 150 lines.
- **Output Summary:** Generated `src/hw4/agents/beta.py`, `src/hw4/agents/beta_prompt.py`, and fixed `src/broken-python/mathsquiz/mathsquiz.py`.
- **Refinements:** Added `if __name__ == '__main__':` guard.
- **Verdict:** Accepted with edits

### [PL-011] Write Math Quiz Unit Tests
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 5
- **Prompt:**
  > Write pytest unit tests for src/broken-python/mathsquiz/mathsquiz.py. Cover: MathQuiz init (score=0, 10 questions, custom questions), check_answer with int/string/wrong/non-numeric inputs, all 6 regression answers, display_result output for all 4 score bands. Use sys.path.insert to import from broken-python. Keep under 150 lines.
- **Output Summary:** Generated `tests/test_mathsquiz.py` with 21 tests across 4 classes.
- **Refinements:** None.
- **Verdict:** Accepted

---

## Phase 6 — Analysis & Reporting

### [PL-012] Generate Token Efficiency Report
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 6
- **Prompt:**
  > Analyze results/token_log.jsonl and results/baseline_token_log.jsonl. Compute: baseline input tokens, guided input tokens, % reduction, file loads baseline vs. guided, KPI pass/fail. Write results/efficiency_report.md with summary table and commentary on which mechanisms drove savings (Gatekeeper, hot pages, zero-edge isolation).
- **Output Summary:** `results/efficiency_report.md` — 70.9% input-token reduction (7,584 → 2,207 tokens), 72.2% fewer file loads. KPI: PASS.
- **Refinements:** Added KPI pass/fail verdict row.
- **Verdict:** Accepted

### [PL-013] Generate Bug Analysis Report
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 6
- **Prompt:**
  > Write reports/bug_analysis.md. For each bug in polygons.py (4) and mathsquiz.py (7): symptom, root cause, investigation trail (which graph nodes/Obsidian pages), before/after code diff. Two sections: Polygons and Math Quiz.
- **Output Summary:** Generated `reports/bug_analysis.md` with full before/after analysis for all 11 bugs.
- **Refinements:** Added investigation trail column referencing specific graph nodes.
- **Verdict:** Accepted with edits

---

## Phase 7 — Orphan Detector Extension

### [PL-014] Implement Orphan Node Detector
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 7
- **Prompt:**
  > Implement an original extension: Orphan Node Detector that scans obsidian/graph.json for nodes with edge count ≤ configurable threshold (default: 1 from hw4.constants.DEFAULT_ORPHAN_THRESHOLD). Load graph.json, count edges per node, identify orphans, write markdown report to results/orphan_report.md. Expose a CLI entry point. Keep under 150 lines.
- **Output Summary:** Generated `src/hw4/extensions/orphan_detector.py` (150 lines) and `results/orphan_report.md` (19 orphans at threshold ≤1).
- **Refinements:** Refactored CLI parsing into a separate function to stay at the line limit.
- **Verdict:** Accepted with edits

---

## Phase 8 — Final Documentation

### [PL-015] Complete Phase 8 README Sections
- **Date:** 2025-06-16
- **Model:** Claude Sonnet
- **Phase:** 8
- **Prompt:**
  > Complete README.md with: Configuration Guide (table of all config/*.json keys), Token Efficiency Results (headline KPI, metric table, link to efficiency_report.md), Tooling Workflow: Graphify + Obsidian (4-step narrative), Reverse-Engineering Walkthrough (3-step narrative), Bug → Root Cause → Fix tables for Polygons and Math Quiz, Before/After section with graph comparison, License & Attribution crediting martinpeck/broken-python (MIT). Use real token numbers from results/ and actual bug lists from reports/.
- **Output Summary:** Added all 7 sections to README.md with real data.
- **Refinements:** Token numbers updated to match actual token_log.jsonl entries.
- **Verdict:** Accepted with edits

---

*Log started: 2025-06-16 | Maintainer: diana | Guidelines reference: §8.3*
