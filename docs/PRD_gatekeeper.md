# PRD: Gatekeeper Node

## 1. Mechanism Overview
The Gatekeeper is a deterministic (non-LLM) node in the LangGraph graph. It acts as a hard context boundary between SubagentAlpha (Polygons phase) and SubagentBeta (Math Quiz phase), preventing "Lost in the Middle" contamination.

## 2. Problem Statement
Without a context reset between phases, residual Polygons tokens from SubagentAlpha's conversation history persist in the context window when SubagentBeta starts. This causes the LLM to "look in the middle" — attending to irrelevant Polygons tokens instead of focusing on the Math Quiz. Even a short list of prior messages can reduce recall accuracy significantly on long-context tasks.

## 3. Functional Requirements

### 3.1 Inputs
- `AgentState` with populated `messages`, `completed_tasks`, and `token_log`

### 3.2 Operations (in order)
1. Append a summary entry to `completed_tasks`: `"phase:polygons:complete"`
2. Record the final `messages` length in the token log as `"gatekeeper:purged_messages:<N>"`
3. Replace `state["messages"]` with `[]` (hard purge — no summarization, no compression)
4. Set `state["current_phase"] = "mathsquiz"`

### 3.3 Outputs
- `AgentState` with:
  - `messages = []`
  - `current_phase = "mathsquiz"`
  - `completed_tasks` includes the phase-completion marker
  - `errors` unchanged

### 3.4 Guarantees
- Gatekeeper MUST NOT call any LLM
- Gatekeeper MUST NOT read any file
- Gatekeeper execution time MUST be < 10ms (pure state manipulation)

## 4. Zero-Edge Domain Isolation Protocol
The Gatekeeper is the enforcement mechanism for the Zero-Edge isolation rule:
- Before the Gatekeeper: only Polygons content has ever been in `messages`
- After the Gatekeeper: `messages` is empty — no Polygons content can leak into SubagentBeta's context

## 5. Acceptance Criteria
- [ ] `state["messages"]` is `[]` after `gatekeeper(state)` is called with a non-empty messages list
- [ ] `state["current_phase"]` equals `"mathsquiz"` after the call
- [ ] No LLM calls occur during Gatekeeper execution (verifiable via mock)
- [ ] Gatekeeper is implemented in `src/nodes/gatekeeper.py` in ≤ 50 lines
