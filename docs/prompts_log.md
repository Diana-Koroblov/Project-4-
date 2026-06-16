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

## Phase 2 — LangGraph Orchestration (Pending)

*Entries to be added as Phase 2 work proceeds.*

---

## Phase 3 — Agent Toolset (Pending)

*Entries to be added as Phase 3 work proceeds.*

---

## Phase 4 — Subagent Alpha (Pending)

*Entries to be added as Phase 4 work proceeds.*

---

## Phase 5 — Subagent Beta (Pending)

*Entries to be added as Phase 5 work proceeds.*

---

## Phase 6 — Analysis & Reporting (Pending)

*Entries to be added as Phase 6 work proceeds.*

---

## Phase 7 — Orphan Detector Extension (Pending)

*Entries to be added as Phase 7 work proceeds.*

---

## Phase 8 — Final Documentation (Pending)

*Entries to be added as Phase 8 work proceeds.*

---

*Log started: 2025-06-16 | Maintainer: diana | Guidelines reference: §8.3*
