# Product Requirements Document (PRD): Sequential Graph-Driven Debugging & Context Engineering

## 1. Project Context & Goal
The **Broken Python** project is a multi-component legacy codebase containing two distinct, unrelated systems:
1.  **Polygons System:** A Turtle-based graphics library suffering from syntax corruption, procedural "God Functions", and architectural debt (lack of OOP encapsulation).
2.  **Math Quiz System:** A terminal-based educational tool heavily cluttered with redundant "step" files and duplicated logic.

**Strategic Goal:** Instead of building a monolithic agent prone to the **"Lost in the Middle"** problem, this project demonstrates advanced **Context Engineering** and **Multi-Agent Orchestration**. The goal is to deploy a Master Router Agent that spawns isolated Subagents to perform a full-system repair. By utilizing strict memory isolation, Graph-driven navigation (`graph.json`), and targeted Obsidian context pages (`hot_*.md`), we aim to achieve maximum Token Efficiency.

## 2. Functional Requirements & Orchestration Workflow

### Multi-Agent Sequential Execution Model
To maintain a clean context window and high signal-to-noise ratio, the orchestration must follow a strict lifecycle:

* **Phase 1: Polygons Remediation (Subagent Alpha)**
    * **Context:** Master Agent reads `index.md` and routes Subagent Alpha to `hot_polygons.md`.
    * **Task:** Refactor `polygons.py` into a proper Object-Oriented Architecture (encapsulating calculations and drawing inside the `Polygon` class) and fix syntax errors.
    * **Validation:** Run `graphify update .` to capture the new architectural graph (verifying the elimination of procedural "TODO" nodes).
* **Phase 2: Mandatory Context Reset (Compaction/Subagent Termination)**
    * **Action:** The Master Agent explicitly terminates Subagent Alpha or performs a complete memory wipe.
    * **Purpose:** Ensure zero residual "noise" or vector contamination from the Polygons system persists in the active context window.
* **Phase 3: Math Quiz Remediation (Subagent Beta)**
    * **Context:** Master Agent spawns a fresh Subagent Beta and routes it to `hot_mathsquiz.md`.
    * **Task:** Consolidate the fragmented execution flow from `step1`-`step3` into a single, clean `mathsquiz.py` implementation.

### Agent Toolset (Guardrails)
The subagents are restricted to the following surgical tools:
* **Navigation Reader:** Specialized tool for reading structured navigation pages (`index.md`, `hot_polygons.md`, `hot_mathsquiz.md`).
* **Node Content Extractor:** Tool for pulling raw content for a single specific node or file identified in the graph.
* **Forbidden Action:** Naive folder scanning or directory-wide recursive reading is strictly prohibited. The agents must rely on the graph edges.

## 3. KPIs & Acceptance Criteria

### Efficiency & Signal
* **Token Efficiency:** Achieve >70% reduction in token consumption compared to a naive agent reading the entire repository.
* **Signal-to-Noise Ratio:** Zero cross-contamination between components. Quiz-related code must never enter the context window of Subagent Alpha, and vice-versa.

### Code & Architecture Standards
* **Graph Before/After Proof:** The updated `graph.json` must clearly show the transition from procedural nodes to encapsulated OOP structures (specifically in the Polygons community).
* **Linter Compliance:** The final codebase must have **zero violations** when checked with the **Ruff** linter.
* **Test Coverage (TDD):** Repaired modules must be accompanied by unit tests reaching at least **85% test coverage**.

## 4. Assumptions, Dependencies & Out-of-Scope

### Assumptions
* **Graph Communities:** The initial `graphify` run correctly identifies the Polygons and Math Quiz systems as separate, unrelated communities.
* **Navigation Map:** `index.md` serves as the primary router for the Master Agent.

### Out-of-Scope
* **Free Scanning:** Reading or searching for files not explicitly defined in the `graph.json` or the relevant "hot" navigation pages.
* **Inter-component Integration:** The agent will not attempt to merge or link the Polygons and Math Quiz systems, as they are intentionally separated domains.