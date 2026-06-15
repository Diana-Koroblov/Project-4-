# Project TODO List: Sequential Graph-Driven Debugging Agent

## Global Mandate: Code Modularity & QA Protocol
Every Python (.py) file created or modified in this project is subject to a 3-step continuous refactoring and verification protocol:
1. **Implementation:** Write and implement the required logic fully.
2. **Size Verification & Refactoring:** Check the file length. If the logic causes the file to exceed 150 lines of code, pause and refactor by extracting components (e.g., functions, classes, mixins) into separate modules.
3. **Quality Assurance:** Enforce 0 Ruff violations and ensure >= 85% test coverage via `pytest-cov`.
*Note: Documentation (.md) and configuration files are exempt from this 3-step sequence.*

---

## Phase 1: Environment & Repository Setup
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** The environment is initialized, UV is configured, dependencies are locked, and the base folder structure exists on disk.

### 1.1 Repository & Environment Genesis
- [ ] 1.1.1 [Pending] [Architect] - Initialize workspace folder directory layout (`src/`, `tests/`, `obsidian/`, `reports/`, `docs/`) | DoD: All 5 directories physically exist on disk.
- [ ] 1.1.2 [Pending] [Developer] - Initialize project and create virtual environment using `uv init` and `uv venv` | DoD: `pyproject.toml` and `.venv` are generated.
- [ ] 1.1.3 [Pending] [Developer] - Install required dependencies (`langgraph`, `ruff`, `pytest`, `pytest-cov`, `langchain-core`) via UV | DoD: `uv.lock` is successfully generated and dependencies are available.
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
- [ ] 3.1.2 [Pending] [Developer] - Implement standard file I/O operations (`read_source_file`, `write_source_file`) | DoD: Tool allows the agent to read and modify specific files in `src/`.
- [ ] 3.1.3 [Pending] [Developer] - Implement the Token Tracker/Logger utility | DoD: Every agent interaction is logged with token consumption metrics.
- [ ] 3.1.4 [Pending] [Developer] - Update README.md to reflect Phase 3 completion | DoD: README lists all available agent tools and their guardrails.

---

## Phase 4: Subagent Alpha (Polygons Refactoring)
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** Polygons system is refactored to an OOP architecture with 85% test coverage.

### 4.1 Polygons Remediation Lifecycle
- [ ] 4.1.1 [Pending] [Architect] - Configure Subagent Alpha system prompt for domain isolation | DoD: Prompt forbids interaction with any files outside the Polygons community.
- [ ] 4.1.2 [Pending] [Developer] - Refactor `polygons.py` into a proper OOP architecture (`Shape` -> `Polygon`) | DoD: Inheritance is established and calculations are encapsulated.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 4.1.3 [Pending] [Developer] - Remediate syntax corruption and "God Functions" | DoD: `new` keywords removed and Turtle drawing logic is modularized.
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

## Phase 6: Final Validation & Knowledge Sync
**Priority:** Low | **Status:** Pending
**Definition of Done (DoD):** Updated graph proof generated and final token efficiency metrics documented.

### 6.1 Project Completion & Reporting
- [ ] 6.1.1 [Pending] [Architect] - Execute `graphify update src/` to generate the final architecture proof | DoD: `graph.json` reflects the new OOP structure.
- [ ] 6.1.2 [Pending] [Developer] - Compile the Token Efficiency Report in `reports/efficiency_report.md` | DoD: Report confirms > 70% token savings compared to naive approach.
- [ ] 6.1.3 [Pending] [Architect] - Perform final sync of Obsidian pages and project documentation | DoD: `index.md` and `PRD.md` are updated with "Complete" status.
