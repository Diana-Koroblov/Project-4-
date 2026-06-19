# PRD: LangGraph Orchestration Engine

## 1. Mechanism Overview
The LangGraph Orchestration Engine is the central control plane of the project. It defines a **StateGraph** with a strict sequential execution order, coordinates all subagents, and enforces token-efficient context management via the Gatekeeper node.

## 2. Problem Statement
A naive monolithic agent that reads the entire repository produces massive, noisy context windows and suffers from the "Lost in the Middle" problem — relevant information gets buried between irrelevant tokens. The orchestration engine solves this by decomposing the repair workflow into isolated phases, each with a clean, purpose-built context.

## 3. Functional Requirements

### 3.1 Graph Topology
The compiled graph MUST follow this exact sequential order with no conditional branching:
```
START → Router → SubagentAlpha → Gatekeeper → SubagentBeta → END
```

### 3.2 AgentState Schema
State (`src/hw4/state.py`) must carry:
| Field | Type | Purpose |
|---|---|---|
| `current_phase` | `str` | Active phase name (`"polygons"` / `"mathsquiz"`) |
| `messages` | `list` | LLM message history (purged by Gatekeeper) |
| `errors` | `list` | Accumulated error log |
| `completed_tasks` | `list` | Completed task identifiers |
| `token_log` | `list` | Per-call token metrics |

### 3.3 Router Node
- Reads `obsidian/index.md`
- Seeds `AgentState` with empty lists and `current_phase = "polygons"`
- Routes execution to SubagentAlpha

### 3.4 Gatekeeper Node (see also PRD_gatekeeper.md)
- Logs `completed_tasks` from Alpha's run
- **Hard-purges** the `messages` list
- Sets `current_phase = "mathsquiz"`

### 3.5 Entry Point
Graph assembly lives in `src/hw4/graph.py` (`build_graph(llm=None)`) and is reached through the SDK (`GraphifySDK.build_graph()` / `run_repair()`). `build_graph` accepts an optional `llm` override so tests substitute a `FakeListChatModel` for the real LLM; `main.py` is a thin controller that prints the compiled graph's Mermaid diagram and re-exports `build_graph` for back-compat.

## 4. Non-Functional Requirements
- Graph compilation must succeed in < 2 seconds (no network calls at import time)
- All values (model name, token budget, max iterations) loaded from `config/setup.json`
- Zero hardcoded strings beyond the node names in the graph topology

## 5. Acceptance Criteria
- [ ] `graph.get_graph().draw_mermaid()` output matches the planned topology
- [ ] Dry-run smoke test traverses all 5 nodes in order without errors
- [ ] `AgentState.messages` is empty after Gatekeeper runs
- [ ] Token log entries appear for every LLM call
