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
**Priority:** High | **Status:** Complete
**Definition of Done (DoD):** Base source is vendored, the Graphify graph and Obsidian vault exist, and the reverse-engineering schemas + research questions are documented.

### 0.1 Base Repository & Graph Products
- [x] 0.1.1 [Complete] [Architect] - Select base repo (`martinpeck/broken-python`) and justify the choice in README | DoD: README states the chosen repo and rationale.
- [x] 0.1.2 [Complete] [Developer] - Vendor the original buggy source into `src/broken-python/` (`polygons/polygons.py`, `mathsquiz/mathsquiz-step1..3.py`, `mathsquiz/mathsquiz.py`) as the immutable "before" snapshot | DoD: original buggy files present under `src/broken-python/` and committed.
- [x] 0.1.3 [Complete] [Architect] - Generate Graphify products (`graph.json`, `GRAPH_REPORT.md`) mapping the two communities | DoD: `obsidian/graph.json` + `obsidian/GRAPH_REPORT.md` exist (27 nodes, 6 communities, Polygons + Math Quiz isolated).

### 0.2 Obsidian Vault & Reverse-Engineering Deliverables
- [x] 0.2.1 [Complete] [Architect] - Build Obsidian navigation pages (`index.md`, `hot_polygons.md`, `hot_mathsquiz.md`, community hub page) | DoD: linked vault with central index and focused `hot_*` context pages exists.
- [x] 0.2.2 [Complete] [Architect] - Author `docs/PRD.md` and `docs/PLAN.md` (including the ADR for choosing LangGraph) | DoD: PRD + PLAN committed.
- [x] 0.2.3 [Complete] [Architect] - Produce the **Architectural Block Schema** of the *existing* system (main blocks + flow between them), not just a folder/file list | DoD: `docs/block_schema.md` committed with annotated Mermaid diagram and linked from README.
- [x] 0.2.4 [Complete] [Architect] - Produce the **OOP Schema** of the before-state (classes, inheritance, composition, and the procedural "God Functions" outside `Polygon`) | DoD: `docs/oop_schema.md` committed with before-state and target-state class diagrams, linked from README.
- [x] 0.2.5 [Complete] [Architect] - Document explicit answers to the 8 Research Questions (real architecture, key components, God Nodes, how the bug/root-cause was found, value of graph vs. linear reading, token savings, future agent improvements) | DoD: all 8 research questions answered in README under "Research Questions" section.

---

## Phase 1: Environment & Repository Setup
**Priority:** High | **Status:** Complete
**Definition of Done (DoD):** The environment is initialized, UV is configured, dependencies are locked, and the base folder structure exists on disk.

### 1.1 Repository & Environment Genesis
- [x] 1.1.1 [Complete] [Architect] - Ensure full directory layout exists (`src/`, `tests/`, `obsidian/`, `reports/`, `docs/`) | DoD: all 5 directories physically exist on disk.
- [x] 1.1.2 [Complete] [Developer] - Initialize project and virtual environment via `uv init` / `uv venv` | DoD: `pyproject.toml` and `.python-version` generated.
- [x] 1.1.3 [Complete] [Developer] - Add and lock dependencies (`langgraph`, `langchain-core`, `ruff`, `pytest`, `pytest-cov`) via UV | DoD: `uv.lock` generated and all dependencies available.
- [x] 1.1.4 [Complete] [Developer] - Update README.md to reflect Phase 1 completion | DoD: README contains the project overview and current file tree.

### 1.2 Guidelines Compliance — Structural Scaffolding
- [x] 1.2.0 [Complete] [Architect] - Create `config/` directory with `setup.json`, `rate_limits.json`, `logging_config.json` | DoD: all three files exist and contain valid JSON; no config values are hardcoded in source.
- [x] 1.2.1 [Complete] [Developer] - Create `.env-example` with dummy API key placeholders and patch `.gitignore` to include `.env`, `*.key`, `*.pem`, `credentials.json` | DoD: `.env-example` committed; `.gitignore` covers all secret patterns.
- [x] 1.2.2 [Complete] [Architect] - Scaffold `src/hw4/` Python package with `__init__.py` (`__version__`, `__author__`), `constants.py`, `shared/version.py`, and `sdk/__init__.py` | DoD: `from hw4 import __version__` works.
- [x] 1.2.3 [Complete] [Architect] - Create `results/` and `notebooks/` directories (with `.gitkeep`) | DoD: both directories exist in the repo.
- [x] 1.2.4 [Complete] [Architect] - Create per-mechanism PRD documents: `docs/PRD_langgraph_orchestration.md`, `docs/PRD_gatekeeper.md`, `docs/PRD_token_tracker.md`, `docs/PRD_node_extractor.md`, `docs/PRD_orphan_detector.md` | DoD: all 5 files exist with problem statement, functional requirements, and acceptance criteria.
- [x] 1.2.5 [Complete] [Developer] - Create `docs/prompts_log.md` (Prompts Engineering Log per §8.3) | DoD: file exists with initial entries and template for all phases.

### 1.3 LLM Provider Configuration
- [x] 1.3.1 [Complete] [Developer] - Selected Groq as LLM provider; added `langchain-groq` and `python-dotenv` to `pyproject.toml` | DoD: dependencies added; run `uv sync` to update `uv.lock`.
- [ ] 1.3.2 [Pending] [Developer] - Create `.env` locally (gitignored) with `GROQ_API_KEY=<your-key>` | DoD: `.env` present locally; `get_llm()` in `src/hw4/llm_config.py` loads without error.
- [x] 1.3.3 [Complete] [Developer] - Created `src/hw4/llm_config.py` with `get_llm()` that loads API key from `.env` via `python-dotenv` and returns a `ChatGroq` instance; model/temperature/max_tokens read from `config/setup.json` | DoD: module is importable, raises `EnvironmentError` if key is missing.
  - [x] **Validation:** 48 lines — within 150-line limit.

### 1.4 Before-State Snapshot Lock
- [x] 1.4.1 [Complete] [Developer] - Commit and git-tag the current repository state as `before-agent` before any agent-driven code modifications | DoD: `git tag before-agent` exists; `git diff before-agent HEAD` produces a clean, human-readable before/after proof for the submission.

---

## Phase 2: Core Orchestration Engine (LangGraph)
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** The StateGraph is defined, nodes are connected, and the sequential execution flow is runnable end-to-end (dry run with mocked LLM passes).

### 2.1 AgentState Schema
- [x] 2.1.1 [Complete] [Architect] - Define the `AgentState` schema using `TypedDict` in `src/hw4/state.py` with the following fields: `current_phase` (str), `messages` (list[BaseMessage] with add_messages reducer), `errors` (list), `completed_tasks` (list), `token_log` (list) | DoD: schema importable and all fields typed correctly.
  - [x] **Validation:** 9 lines — within 150-line limit.

### 2.2 Graph Nodes
- [x] 2.2.1 [Complete] [Developer] - Implement the **Master Router** node in `src/hw4/nodes/router.py`: reads `obsidian/index.md`, sets `current_phase = "polygons"`, initializes empty `messages`, `errors`, `completed_tasks`, and `token_log` | DoD: Router correctly seeds state and routes to Subagent Alpha.
  - [x] **Validation:** 16 lines — within 150-line limit.
- [x] 2.2.2 [Complete] [Developer] - Implement the **Gatekeeper** node in `src/hw4/nodes/gatekeeper.py`: logs `completed_tasks` from Alpha, purges `messages` list entirely via RemoveMessage, sets `current_phase = "mathsquiz"` | DoD: after Gatekeeper runs, `messages` is empty and `completed_tasks` is preserved.
  - [x] **Validation:** 12 lines — within 150-line limit.

### 2.3 StateGraph Assembly
- [x] 2.3.1 [Complete] [Architect] - Compile the `StateGraph` in `main.py` with strict sequential edges: `START → Router → SubagentAlpha → Gatekeeper → SubagentBeta → END` | DoD: graph compiles without errors; `graph.get_graph().draw_mermaid()` matches the planned workflow diagram.
  - [x] **Validation:** 45 lines — within 150-line limit.
- [x] 2.3.2 [Complete] [Tester] - Write a dry-run smoke test in `tests/test_graph.py` using a mocked LLM (`FakeListChatModel`) that confirms the graph traverses all 5 nodes in order without errors | DoD: `pytest tests/test_graph.py` passes (5/5).
  - [x] **Validation:** 65 lines — within 150-line limit.
- [x] 2.3.3 [Complete] [Developer] - Updated README.md with LangGraph orchestration table, AgentState schema, and Gatekeeper behavior documentation. Workflow Mermaid diagram already present.

---

## Phase 3: Agent Toolset & Infrastructure
**Priority:** High | **Status:** Complete
**Definition of Done (DoD):** All surgical tools are implemented, individually unit-tested, and registered with the LangGraph subagent nodes.

### 3.1 Tool Implementation
- [x] 3.1.1 [Complete] [Developer] - Implement `read_obsidian_page(page_name: str) -> str` in `src/hw4/tools/obsidian_reader.py`: resolves the page name to `obsidian/{page_name}.md`, reads and returns content, raises `FileNotFoundError` for unknown pages | DoD: tool retrieves hot pages without touching unrelated files.
  - [x] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module. (44 lines)
- [x] 3.1.2 [Complete] [Developer] - Implement `extract_node_content(node_id: str) -> str` in `src/hw4/tools/node_extractor.py`: looks up the node's file path in `obsidian/graph.json` and returns its raw source; raises `ValueError` if the node is not in the graph (refuses directory-wide reads entirely) | DoD: tool resolves any valid graph node to its source in one call.
  - [x] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module. (58 lines)
- [x] 3.1.3 [Complete] [Developer] - Implement `read_source_file(path: str) -> str` and `write_source_file(path: str, content: str)` in `src/hw4/tools/file_io.py`: both enforce that `path` is under `src/broken-python/`; `write_source_file` rejects paths outside the allowed subtree | DoD: read/write work on valid paths; invalid paths raise `PermissionError`.
  - [x] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module. (70 lines)
- [x] 3.1.4 [Complete] [Developer] - Implement `TokenTracker` class in `src/hw4/tools/token_tracker.py`: records `{phase, node, tokens_in, tokens_out, files_read}` per call (`record` + `record_response` reading LangChain `usage_metadata`); exposes `get_summary()` returning a dict of totals and a `save_log(path)` method (JSON Lines) | DoD: every LLM interaction is logged with all four required metrics.
  - [x] **Validation:** 80 lines — within 150-line limit.

### 3.2 Tool Testing & Registration
- [x] 3.2.1 [Complete] [Tester] - Write unit tests in `tests/test_tools.py` for all four tools: happy-path calls, invalid input errors, and boundary conditions (e.g., node not in graph, path outside `src/broken-python/`) | DoD: `pytest tests/test_tools.py` passes with **100%** coverage of `src/hw4/tools/` (≥85% required).
  - [x] **Validation:** 144 lines — within 150-line limit.
- [x] 3.2.2 [Complete] [Developer] - Register all tools with the LangGraph subagent nodes using `ToolNode` and bind them to the LLM via `.bind_tools()` (wrappers + `bind_agent_tools` in `src/hw4/tools/registry.py`; `AlphaTools`/`BetaTools` ToolNodes with conditional tool-loop edges in `main.py`; `bind_tools` degrades gracefully for fake models) | DoD: subagents can invoke tools by name; tool calls appear in the graph's message trace (proven by `TestToolInvocation` in `tests/test_graph.py`).
- [x] 3.2.3 [Complete] [Developer] - Update README.md to reflect Phase 3 completion | DoD: README lists all available agent tools, their signatures, and their guardrails (new "Agent Tools & Guardrails" section + updated orchestration table with the two ToolNodes).

---

## Phase 4: Subagent Alpha (Polygons Refactoring)
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** Polygons system is refactored to a proper OOP architecture, passes Ruff with zero violations, and has ≥85% test coverage.

### 4.1 Pre-Refactoring Preparation
- [x] 4.1.1 [Complete] [Architect] - Configure Subagent Alpha system prompt in `src/hw4/agents/alpha_prompt.py` (`ALPHA_SYSTEM_PROMPT`; alpha.py now imports it) for domain isolation | DoD: prompt explicitly forbids reading any file outside the Polygons community; prompt references `hot_polygons.md` as the sole entry point.
- [x] 4.1.2 [Complete] [Developer] - Add `if __name__ == "__main__":` guard to `src/broken-python/polygons/polygons.py` to make it safely importable by the test suite without triggering side effects (turtle window, `input()` calls) | DoD: `import polygons` does not open a window or prompt for input.

### 4.2 Refactoring
- [x] 4.2.1 [Complete] [Developer] - Fix all syntax errors in `polygons.py`: replace `Object` with `object` as base class; remove `new` keyword from instantiation | DoD: `python -c "import polygons"` raises no `SyntaxError` or `NameError`.
  - [x] **Validation:** 77 lines — within 150-line limit.
- [x] 4.2.2 [Complete] [Developer] - Refactor into OOP architecture: `calc_polygon_details` and `draw_polygon` are now methods inside the `Polygon` class (as `calculate_internal_angle()`/`calculate_internal_angles_sum()` and `draw()`); added abstract `Shape` base class with `draw()` and `calculate_perimeter()` | DoD: `Polygon` inherits from `Shape`; no module-level God Functions remain (only `Shape`/`Polygon` classes + `__main__` guard).
  - [x] **Validation:** 58 lines — within 150-line limit.
- [x] 4.2.3 [Complete] [Developer] - Fix dynamic math: replaced hardcoded angle logic with `internal_angle = (sides - 2) * 180 / sides` (verified 3→60, 4→90, 5→108, 6→120) and turtle loop now `range(self.sides)` + `360/self.sides` | DoD: `Polygon(5).draw()` traces a pentagon (108° interior, 72° exterior turn), not a hexagon.
  - [x] **Validation:** 58 lines — within 150-line limit.
- [x] 4.2.4 [Complete] [Developer] - Ran `uv run ruff check src/broken-python/polygons/` and fixed all violations | DoD: `ruff check` exits with code 0 and zero warnings for the Polygons domain.

### 4.3 Testing & Graph Proof
- [ ] 4.3.1 [Pending] [Tester] - Fill in `tests/test_polygons.py` with full unit tests: `__init__`, `calculate_perimeter`, `calculate_internal_angle` for triangle/square/pentagon/hexagon, and `Shape` inheritance check | DoD: `pytest tests/test_polygons.py` passes with ≥85% coverage of the refactored Polygons module.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 4.3.2 [Pending] [Developer] - Run Graphify again after refactoring (`graphify update .`) and save updated graph to `docs/after_state/graph.json` and `docs/after_state/GRAPH_REPORT.md` | DoD: updated graph shows `calc_polygon_details` and `draw_polygon` as methods inside `Polygon`, not as standalone nodes.
- [ ] 4.3.3 [Pending] [Developer] - Update README.md to reflect Phase 4 completion | DoD: README documents the Polygons refactoring, OOP after-state, and before/after graph comparison.

---

## Phase 5: Subagent Beta (Math Quiz Consolidation)
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** Math Quiz is consolidated into a single OOP `MathQuiz` class, all step files removed, passes Ruff with zero violations, and has ≥85% test coverage.

### 5.1 Preparation
- [ ] 5.1.1 [Pending] [Architect] - Configure Subagent Beta system prompt in `src/hw4/agents/beta_prompt.py` for domain isolation | DoD: prompt explicitly forbids reading any file outside the Math Quiz community; prompt references `hot_mathsquiz.md` as the sole entry point.
- [ ] 5.1.2 [Pending] [Developer] - Add `if __name__ == "__main__":` guard to `src/broken-python/mathsquiz/mathsquiz.py` to make it safely importable | DoD: `import mathsquiz` does not prompt for input or print to stdout.

### 5.2 Consolidation
- [ ] 5.2.1 [Pending] [Developer] - Analyse step files (`mathsquiz-step1.py`, `mathsquiz-step2.py`, `mathsquiz-step3.py`) and document the evolution in `reports/mathsquiz_step_analysis.md` | DoD: report explains what each step file adds and confirms the final `mathsquiz.py` supersedes all three.
- [ ] 5.2.2 [Pending] [Developer] - Fix all bugs in `mathsquiz.py`: replace `print "..."` with `print(...)`, fix `if answer = N` → `if answer == N`, fix `else if` → `elif`, fix score never incrementing, fix wrong answers (55→56, 49→36, 126→72, 668→48, 77→49, 60→66), add missing questions to reach 10, label all as "Question N" not "Question 1" | DoD: running the quiz with correct answers gives a score of 10/10.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 5.2.3 [Pending] [Developer] - Refactor `mathsquiz.py` into a `MathQuiz` OOP class with `__init__`, `ask_question`, `check_answer`, `run`, and `display_result` methods | DoD: class instantiates cleanly; no module-level procedural code remains outside `if __name__ == "__main__":`.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 5.2.4 [Pending] [Developer] - Run `uv run ruff check src/broken-python/mathsquiz/` and fix all violations | DoD: `ruff check` exits with code 0 for the Math Quiz domain.

### 5.3 Testing
- [ ] 5.3.1 [Pending] [Tester] - Fill in `tests/test_mathsquiz.py`: implement all skipped stubs (`TestMathQuizInit`, `TestMathQuizAnswerValidation`, `TestMathQuizResult`) plus the 6 already-passing regression tests | DoD: `pytest tests/test_mathsquiz.py` passes with ≥85% coverage of `MathQuiz`.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 5.3.2 [Pending] [Developer] - Update README.md to reflect Phase 5 completion | DoD: README documents the Math Quiz consolidation, removed step files, and OOP after-state.

---

## Phase 6: Analysis, Reporting & Knowledge Sync
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** Token efficiency is proven with numbers, bug reports are complete, and the Obsidian vault reflects the after-state.

### 6.1 Baseline Agent
- [ ] 6.1.1 [Pending] [Developer] - Build naive baseline in `src/hw4/baseline_agent.py`: agent reads every file in `src/broken-python/` recursively before answering any question | DoD: baseline agent runs end-to-end and its total token usage is logged via `TokenTracker`.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.

### 6.2 Token Efficiency Report
- [ ] 6.2.1 [Pending] [Developer] - Compare guided agent token log vs. baseline log and populate `reports/efficiency_report.md` with a table showing all four metrics mandated by §5.5: (a) total tokens in/out, (b) files / text units read, (c) iterations / investigation rounds, and (d) quality or speed of reaching the root cause and fix (e.g. rounds-to-root-cause, correct-fix-on-first-try), reported per phase | DoD: report demonstrates >70% token reduction vs. baseline AND contrasts root-cause quality/speed between the two modes; table is reproducible from `results/token_log.jsonl`.

### 6.3 Bug Analysis Report
- [ ] 6.3.1 [Pending] [Developer] - Complete `reports/bug_analysis.md` for the Polygons community: list each bug with problem statement, root cause, investigation trail (which graph nodes were traversed), and the fix applied | DoD: covers all 4 Polygons bugs (`Object`, `new`, hardcoded angles, wrong turtle loop).
- [ ] 6.3.2 [Pending] [Developer] - Complete `reports/bug_analysis.md` for the Math Quiz community: same format as above | DoD: covers all 7 Math Quiz bugs (Python 2 print, assignment in condition, else-if, score not incrementing, 6 wrong answers, wrong question count, duplicate labels).

### 6.4 Knowledge & Graph Sync
- [ ] 6.4.1 [Pending] [Architect] - Update `obsidian/hot_polygons.md` and `obsidian/hot_mathsquiz.md` to reflect after-state (bugs fixed, OOP classes present) | DoD: Obsidian vault accurately describes the repaired codebase.
- [ ] 6.4.2 [Pending] [Architect] - Author `obsidian/knowledge_delta.md` documenting what changed between before-state and after-state graphs (nodes added, God Functions eliminated, orphans unchanged) | DoD: file committed and linked from `obsidian/index.md`.

---

## Phase 7: Original Extension — Orphan Node Detector
**Priority:** Medium | **Status:** Pending
**Definition of Done (DoD):** `OrphanDetector` is implemented, tested, documented, and produces a valid report on the project's own graph.

### 7.1 Design
- [ ] 7.1.1 [Pending] [Architect] - Finalise `OrphanNode` dataclass and `OrphanDetector` class interface per `docs/PRD_orphan_detector.md` | DoD: interface approved and matches the PRD acceptance criteria.

### 7.2 Implementation
- [ ] 7.2.1 [Pending] [Developer] - Implement `OrphanNode` dataclass and `OrphanDetector` class in `src/hw4/extensions/orphan_detector.py` | DoD: `detector.detect()` correctly identifies all nodes with ≤ threshold edges; threshold loaded from `config/setup.json`.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 7.2.2 [Pending] [Developer] - Add CLI entry point: `uv run python -m hw4.extensions.orphan_detector --graph obsidian/graph.json --out results/orphan_report.md` | DoD: command produces a valid Markdown report at the specified output path.
- [ ] 7.2.3 [Pending] [Developer] - Run the detector on `obsidian/graph.json` and commit `results/orphan_report.md` | DoD: report identifies at minimum the 4 known orphans (`Introduction`, `Objectives`, `The Files`, `MIT License`).

### 7.3 Testing & Documentation
- [ ] 7.3.1 [Pending] [Tester] - Write unit tests in `tests/test_orphan_detector.py`: happy path (known orphans detected), empty graph, threshold=0 (all nodes), threshold=100 (no nodes) | DoD: `pytest tests/test_orphan_detector.py` passes with ≥85% coverage.
  - [ ] **Validation:** Verify file length < 150 lines. If > 150, trigger refactoring/splitting module.
- [ ] 7.3.2 [Pending] [Developer] - Update README.md to document the Orphan Node Detector: what it is, how to run it, and what the 4 identified orphans mean for the project's knowledge graph.

---

## Phase 8: Final Documentation & Submission Preparation
**Priority:** High | **Status:** Pending
**Definition of Done (DoD):** README is complete, all visual assets exist, all checklist items from the submission guidelines (§17) are satisfied.

### 8.1 README Completion
- [x] 8.1.1 [Complete] - Project overview and rationale for `martinpeck/broken-python`
- [x] 8.1.2 [Complete] - Repository structure tree
- [x] 8.1.3 [Complete] - Run instructions (`uv venv`, `uv sync`, `uv run python main.py`, `uv run pytest`, `uv run ruff check`)
- [x] 8.1.4 [Complete] - All 8 research questions answered
- [x] 8.1.5 [Complete] - Architectural block schema (Mermaid)
- [x] 8.1.6 [Complete] - OOP before/after schema (Mermaid)
- [x] 8.1.7 [Complete] - Agent workflow diagram (Mermaid)
- [x] 8.1.8 [Complete] - ADR-001 for LangGraph
- [ ] 8.1.9 [Pending] - Configuration guide (what each `config/*.json` key does)
- [ ] 8.1.10 [Pending] - Token efficiency results summary (link to `reports/efficiency_report.md`)
- [ ] 8.1.11 [Pending] - Orphan Node Detector usage section
- [ ] 8.1.12 [Pending] - License and attribution section (credit `martinpeck/broken-python`)
- [ ] 8.1.13 [Pending] - "Tooling Workflow" section explaining how Grphify and Obsidian were used in practice (§8 bullet 6): how `graph.json`/`GRAPH_REPORT.md` were generated, how `index.md` → `hot_*.md` drove navigation, and why the vault is an active knowledge space rather than a file dump
- [ ] 8.1.14 [Pending] - "Reverse-Engineering Walkthrough" section narrating the RE process performed (§8 bullet 7): how the real architecture, central components, and God Nodes were uncovered from sparse docs (expands beyond the Q&A bullets)
- [ ] 8.1.15 [Pending] - "Bug → Root Cause → Fix" summary section in the README itself (§8 bullet 8), linking to `reports/bug_analysis.md` for the full trail | DoD: each community's headline bug, its root cause, and the applied fix appear directly in the README
- [ ] 8.1.16 [Pending] - "Before / After" section in the README (§8 bullet 9) presenting both the code diff (`git diff before-agent HEAD`) and the knowledge delta (`obsidian/knowledge_delta.md`), with before/after graph or schema visuals

### 8.2 Visual Assets
- [ ] 8.2.1 [Pending] - Screenshot of Obsidian vault after-state (post-refactoring graph) → `assets/obsidian_vault_after.png`
- [ ] 8.2.2 [Pending] - Screenshot of `pytest --cov` output showing ≥85% coverage → `assets/pytest_coverage.png`
- [ ] 8.2.3 [Pending] - Screenshot of `ruff check` showing zero violations → `assets/ruff_clean.png`

### 8.3 Final Review Checklist
- [ ] 8.3.1 [Pending] - Verify all §17 checklist items from `software_submission_guidelines.pdf` are satisfied
- [ ] 8.3.2 [Pending] - Run full test suite: `uv run pytest --cov=src/hw4 --cov-report=term-missing` | DoD: ≥85% coverage, zero failures
- [ ] 8.3.3 [Pending] - Run Ruff on entire project: `uv run ruff check src/` | DoD: zero violations
- [ ] 8.3.4 [Pending] - Verify `docs/prompts_log.md` has entries for every significant AI-assisted prompt used across all phases
- [ ] 8.3.5 [Pending] - Git-tag final submission: `git tag submission-ready`