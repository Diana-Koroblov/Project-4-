# Project TODO List: Sequential Graph-Driven Debugging Agent

## Assignment Context (EX04 — Reverse Engineering, Debugging & Token-Efficient Agentic AI)
Reverse-engineer an unfamiliar Python codebase (**martinpeck/broken-python**), represent it as a **Graphify** knowledge graph and an **Obsidian** vault, then run a **graph-guided LangGraph agent** to investigate, fix, and explain its bugs — and **prove token savings** versus a naive whole-repo read.

**Required deliverables (must each map to a task below):** full Python solution · CrewAI/LangGraph agent workflow · Graphify products (`graph.json`, `GRAPH_REPORT.md`) · full Obsidian vault (`index.md` + `hot_*.md` + linked pages) · bug-analysis report (problem, root cause, investigation trail, fix) · token-efficiency report (baseline vs. guided: tokens, files read, iterations, quality) · architectural **block schema** · **OOP schema** · before/after proof (code + knowledge) · ≥1 original extension · rich README with diagrams/screenshots/run instructions.

## Global Mandate: Code Modularity & QA Protocol
Every Python (.py) file created or modified in this project is subject to a 3-step continuous refactoring and verification protocol:
1. **Implementation:** Write and implement the required logic fully.
2. **Size Verification & Refactoring:** Check the file length. If the logic causes the file to exceed 150 lines of code, pause and refactor by extracting components (e.g., functions, classes, mixins) into separate modules.
3. **Quality Assurance:** Enforce 0 Ruff violations and ensure >= 85% test coverage via `pytest-cov`.
*Note: Documentation (.md) and configuration files are exempt from this 3-step sequence.*

---

## Phase 0: Knowledge-Base & Reverse-Engineering Foundation
**Priority:** High | **Status:** In Progress
**Definition of Done (DoD):** Base source is vendored, the Graphify graph and Obsidian vault exist, and the reverse-engineering schemas + research questions are documented.

### 0.1 Base Repository & Graph Products
- [x] 0.1.1 [Complete] [Architect] - Select base repo (`martinpeck/broken-python`) and justify the choice in README | DoD: README states the chosen repo and rationale.
- [ ] 0.1.2 [Pending] [Developer] - Vendor the original buggy source into `src/` (`polygons/polygons.py`, `mathsquiz/mathsquiz-step1..3.py`, `mathsquiz/mathsquiz.py`) as the immutable "before" snapshot | DoD: original buggy files present under `src/` and committed (currently `src/` is empty).
- [x] 0.1.3 [Complete] [Architect] - Generate Graphify products (`graph.json`, `GRAPH_REPORT.md`) mapping the two communities | DoD: `obsidian/graph.json` + `obsidian/GRAPH_REPORT.md` exist (27 nodes, 6 communities, Polygons + Math Quiz isolated).

### 0.2 Obsidian Vault & Reverse-Engineering Deliverables
- [x] 0.2.1 [Complete] [Architect] - Build Obsidian navigation pages (`index.md`, `hot_polygons.md`, `hot_mathsquiz.md`, community hub page) | DoD: linked vault with central index and focused `hot_*` context pages exists.
- [x] 0.2.2 [Complete] [Architect] - Author `docs/PRD.md` and `docs/PLAN.md` (including the ADR for choosing LangGraph) | DoD: PRD + PLAN committed.
- [ ] 0.2.3 [Pending] [Architect] - Produce the **Architectural Block Schema** of the *existing* system (main blocks + flow between them), not just a folder/file list | DoD: block diagram committed under `obsidian/` or `reports/` and linked from README.
- [ ] 0.2.4 [Pending] [Architect] - Produce the **OOP Schema** of the before-state (classes, inheritance, composition, and the procedural "God Functions" outside `Polygon`) | DoD: OOP class diagram committed and linked from README.
- [ ] 0.2.5 [Pending] [Architect] - Document explicit answers to the 8 Research Questions (real architecture, key components, God Nodes, how the bug/root-cause was found, value of graph vs. linear reading, token savings, future agent improvements) | DoD: each research question is addressed in README and/or Obsidian.

---

## Phase 1: Environment & Repository Setup
**Priority:** High | **Status:** In Progress
**Definition of Done (DoD):** The environment is initialized, UV is configured, dependencies are locked, and the base folder structure exists on disk.

### 1.1 Repository & Environment Genesis
- [ ] 1.1.1 [Pending] [Architect] - Ensure full directory layout exists (`src/`, `tests/`, `obsidian/`, `reports/`, `docs/`) | DoD: all 5 directories physically exist on disk (currently `tests/` and `reports/` are missing).
- [x] 1.1.2 [Complete] [Developer] - Initialize project and virtual environment via `uv init` / `uv venv` | DoD: `pyproject.toml` and `.python-version` generated.
- [ ] 1.1.3 [Pending] [Developer] - Add and lock dependencies (`langgraph`, `langchain-core`, `ruff`, `pytest`, `pytest-cov`) via UV | DoD: `uv.lock` generated and dependencies available (currently `pyproject.toml` has `dependencies = []`).
- [ ] 1.1.4 [Pending] [Developer] - Update README.md to reflect Phase 1 completion | DoD: README contains the project overview and current file tree.

---

## Phase 2: Core Orchestration Engine (LangGraph)
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** The StateGraph is defined, nodes are connected, and the sequential execution flow is runnable.

### 2.1 LangGraph Framework Construction
- [ ] 2.1.1 [Pending] [Architect] - Define the `AgentState` schema using `TypedDict` in `src/state.py` | DoD: State contains `current_phase`, `messages`, `errors`, and `completed_tasks`.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 2.1.2 [Pending] [Developer] - Implement the Master Router node to read `index.md` and direct initial state | DoD: Router correctly identifies the Polygons community as the first task.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 2.1.3 [Pending] [Developer] - Implement the Gatekeeper node for context compaction | DoD: Gatekeeper successfully purges `messages` history while preserving `completed_tasks`.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 2.1.4 [Pending] [Architect] - Compile the `StateGraph` with strict sequential edges (`START -> Router -> Alpha -> Gatekeeper -> Beta -> END`) | DoD: The graph compiles without errors and follows the planned path.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 2.1.5 [Pending] [Developer] - Update README.md to reflect Phase 2 completion | DoD: README documents the LangGraph orchestration and Gatekeeper behavior.

---

## Phase 3: Agent Toolset & Infrastructure
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** Surgical tools for Obsidian reading, file operations, and token tracking are fully functional.

### 3.1 Surgical Tool Development
- [ ] 3.1.1 [Pending] [Developer] - Implement `read_obsidian_page` for surgical context retrieval | DoD: Tool retrieves content from `hot_*.md` without reading unrelated files.
- [ ] 3.1.2 [Pending] [Developer] - Implement a Node Content Extractor that pulls a single node/file identified in `graph.json` (no recursive folder scanning) | DoD: Tool returns one node's source on demand and refuses directory-wide reads.
- [ ] 3.1.3 [Pending] [Developer] - Implement standard file I/O operations (`read_source_file`, `write_source_file`) | DoD: Tool allows the agent to read and modify specific files in `src/`.
- [ ] 3.1.4 [Pending] [Developer] - Implement the Token Tracker/Logger utility | DoD: Every agent interaction is logged with token-consumption and files-read metrics.
- [ ] 3.1.5 [Pending] [Developer] - Update README.md to reflect Phase 3 completion | DoD: README lists all available agent tools and their guardrails.

---

## Phase 4: Subagent Alpha (Polygons Refactoring)
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** Polygons system is refactored to an OOP architecture with 85% test coverage.

### 4.1 Polygons Remediation Lifecycle
- [ ] 4.1.1 [Pending] [Architect] - Configure Subagent Alpha system prompt for domain isolation | DoD: Prompt forbids interaction with any files outside the Polygons community.
- [ ] 4.1.2 [Pending] [Developer] - Refactor `polygons.py` into a proper OOP architecture (`Shape` -> `Polygon`) | DoD: Inheritance is established and calculations are encapsulated.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 4.1.3 [Pending] [Developer] - Remediate syntax corruption and "God Functions" (`Object`->`object`, `new` keyword, hardcoded 3/4-side angles, fixed hexagon turtle loop) | DoD: dynamic per-side math; drawing/calculation encapsulated in `Polygon`.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 4.1.4 [Pending] [Tester] - Implement unit tests for Polygons in `tests/test_polygons.py` | DoD: Pytest report shows >= 85% coverage for the Polygons domain.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 4.1.5 [Pending] [Developer] - Update README.md to reflect Phase 4 completion | DoD: README includes the refactored OOP class diagram for Polygons.

---

## Phase 5: Subagent Beta (Math Quiz Consolidation)
**Priority:** Medium | **Status:** Pending
**Definition of Done (DoD):** Math Quiz logic is consolidated into a single file with 85% test coverage.

### 5.1 Math Quiz Remediation Lifecycle
- [ ] 5.1.1 [Pending] [Architect] - Configure Subagent Beta system prompt for domain isolation | DoD: Prompt forbids interaction with any files outside the Math Quiz community.
- [ ] 5.1.2 [Pending] [Developer] - Consolidate logic from `mathsquiz-step1.py`, `step2.py`, and `step3.py` into `src/mathsquiz/mathsquiz.py` | DoD: A unified, functional quiz engine is produced.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 5.1.3 [Pending] [Developer] - Remove redundant step files and clean up the mathsquiz directory | DoD: Only the consolidated engine and necessary assets remain.
- [ ] 5.1.4 [Pending] [Tester] - Implement unit tests for Math Quiz in `tests/test_mathsquiz.py` | DoD: Pytest report shows >= 85% coverage for the Math Quiz domain.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 5.1.5 [Pending] [Developer] - Update README.md to reflect Phase 5 completion | DoD: README documents the consolidation of quiz logic and the resulting file structure.

---

## Phase 6: Bug Analysis, Token-Savings Proof & Knowledge Sync
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** A measured baseline-vs-guided comparison and a full bug-analysis report exist, and the updated graph proves the before/after architecture change.

### 6.1 Investigation Proof & Reporting
- [ ] 6.1.1 [Pending] [Tester] - Execute the **naive baseline** run (agent/workflow over raw whole-repo files, no graph guidance) and capture: tokens consumed, files/units read, iterations, time-to-root-cause | DoD: baseline metrics logged under `reports/`.
- [ ] 6.1.2 [Pending] [Tester] - Execute the **graph-guided** run (via `graph.json`, `index.md`, `hot_*.md`) capturing the same four metrics | DoD: guided metrics logged under `reports/`.
- [ ] 6.1.3 [Pending] [Developer] - Write the **Bug Analysis Report** in `reports/bug_analysis.md` (problem description, root cause, investigation trail, the fix, and how success was verified) for both communities | DoD: report covers the Polygons and Math Quiz fixes.
- [ ] 6.1.4 [Pending] [Developer] - Compile the **Token Efficiency Report** in `reports/efficiency_report.md` (baseline vs. guided comparison table) | DoD: report confirms > 70% token savings with the four required metrics.
- [ ] 6.1.5 [Pending] [Architect] - Regenerate the graph (`graphify update src/`) for the after-state proof | DoD: new `graph.json` reflects the OOP structure (procedural/TODO God-Function nodes eliminated).
- [ ] 6.1.6 [Pending] [Architect] - Document the **before/after knowledge delta** (which Obsidian pages, nodes, links, and insights were added/changed) and final-sync `index.md` + `PRD.md` to "Complete" | DoD: knowledge before/after is explicit in the vault.

---

## Phase 7: Original Extension (Assignment §5.6 — Mandatory)
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** At least one original analysis/feature beyond the minimum requirements is implemented and documented.

### 7.1 Original Initiative
- [ ] 7.1.1 [Pending] [Architect] - Choose and implement ≥1 original extension. Candidates: rank suspect nodes by centrality/proximity to failing tests · generate a dynamic git diff from `graph.json`/`hot.md` · detect orphan nodes and auto-document them · flag mixed-responsibility nodes and propose refactoring · before/after architecture comparison · "impact report" (what breaks if class/function X changes) | DoD: the extension runs and is documented in README.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.

---

## Phase 8: Final README & Submission Package
**Priority:** Medium | **Status:** Pending
**Definition of Done (DoD):** A rich, externally-readable README ties together every deliverable.

### 8.1 README & Visuals
- [ ] 8.1.1 [Pending] [Developer] - Assemble the final README per assignment §8: repo choice + rationale, bug/problem, research questions, extracted architecture, agent workflow, Graphify+Obsidian usage, reverse-engineering walkthrough, root cause + fix, before/after, token efficiency, original extensions, and clear run instructions | DoD: an external reader can follow the full process.
- [ ] 8.1.2 [Pending] [Developer] - Embed visual elements (screenshots, block schema, OOP schema, flow/Graph diagrams) | DoD: README includes the required diagrams and screenshots.
