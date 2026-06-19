# PRD: Token Tracker

## 1. Mechanism Overview
The `TokenTracker` class (`src/hw4/tools/token_tracker.py`) wraps every LLM call and records per-call token metrics. It is the primary instrument for proving the >70% token reduction KPI against the naive baseline.

## 2. Problem Statement
Without structured token logging, the efficiency claim ("graph-guided agents use 70%+ fewer tokens than naive whole-repo reads") is unverifiable. The Token Tracker makes every LLM interaction auditable, enabling the efficiency report in `reports/efficiency_report.md`.

## 3. Functional Requirements

### 3.1 Tracked Metrics (per call)
| Field | Type | Description |
|---|---|---|
| `phase` | `str` | `"polygons"` or `"mathsquiz"` |
| `node` | `str` | Graph node name that triggered the call |
| `tokens_in` | `int` | Prompt tokens consumed |
| `tokens_out` | `int` | Completion tokens generated |
| `files_read` | `list[str]` | File paths read before the call |
| `timestamp` | `str` | ISO-8601 timestamp |

### 3.2 Interface
```python
class TokenTracker:
    def record(self, phase: str, node: str, tokens_in: int,
               tokens_out: int, files_read: list[str]) -> None: ...
    def get_summary(self) -> dict: ...          # totals per phase + grand total
    def save_log(self, path: str) -> None: ...  # writes JSON to path
```

### 3.3 Baseline Comparison
`TokenTracker.get_summary()` must include a `"vs_baseline"` key populated after `src/hw4/baseline_agent.py` runs, showing percentage reduction.

### 3.4 Integration Point
`TokenTracker` is instantiated once in `main.py` and passed into each node via `AgentState.token_log`. It is NOT a LangGraph tool (not bound to the LLM) — it is infrastructure.

## 4. Non-Functional Requirements
- Thread-safe log appending (use `threading.Lock`)
- Log file format: newline-delimited JSON (one record per line)
- Must not add latency > 1ms per call

## 5. Acceptance Criteria
- [ ] `tracker.get_summary()["total_tokens_in"]` equals sum of all recorded `tokens_in`
- [ ] `tracker.save_log("results/token_log.jsonl")` produces a valid JSONL file
- [ ] Unit tests in `tests/test_tools.py` cover happy path, empty log, and save/load round-trip
