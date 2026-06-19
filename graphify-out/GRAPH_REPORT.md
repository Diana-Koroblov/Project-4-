# Graph Report - Project-4-  (2026-06-19)

## Corpus Check
- 106 files · ~60,170 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1038 nodes · 1400 edges · 76 communities (61 shown, 15 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 196 edges (avg confidence: 0.67)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a8ecbe53`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]

## God Nodes (most connected - your core abstractions)
1. `OrphanDetector` - 31 edges
2. `BaselineAgent` - 24 edges
3. `GraphifySDK` - 24 edges
4. `SlidingWindowRateLimiter` - 22 edges
5. `MathQuiz` - 21 edges
6. `OverflowQueue` - 20 edges
7. `Graph-Driven Sequential Debugging System` - 19 edges
8. `GroqLoggingCallback` - 17 edges
9. `Polygon` - 15 edges
10. `GatekeptChatModel` - 15 edges

## Surprising Connections (you probably didn't know these)
- `AgentState` --uses--> `AgentState`  [INFERRED]
  tests/test_graph.py → src/hw4/state.py
- `main()` --calls--> `GraphifySDK`  [INFERRED]
  main.py → src/hw4/sdk/core.py
- `main()` --calls--> `GraphifySDK`  [INFERRED]
  run_live_agent.py → src/hw4/sdk/core.py
- `TestMathQuizAnswerCorrectness` --uses--> `MathQuiz`  [INFERRED]
  tests/test_mathsquiz.py → src/broken-python/mathsquiz/mathsquiz.py
- `TestMathQuizAnswerValidation` --uses--> `MathQuiz`  [INFERRED]
  tests/test_mathsquiz.py → src/broken-python/mathsquiz/mathsquiz.py

## Import Cycles
- None detected.

## Communities (76 total, 15 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (28): System prompt for Subagent Alpha — the Polygons-domain specialist.  Enforces str, System prompt for Subagent Beta — the Math Quiz-domain specialist.  Enforces str, Bounded FIFO overflow queue for the API gatekeeper (§5.3).  When the rate limite, Thread-safe sliding-window rate limiter (requests/min and tokens/min).  Enforces, BaselineAgent, estimate_tokens(), main(), modeled_output_tokens() (+20 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (25): load_threshold(), main(), OrphanDetector, OrphanNode, Extension: Orphan Node Detector (Phase 7).  Scans a Graphify ``graph.json`` (rea, One-paragraph guidance summarising the detected orphans., CLI entry point; see the module docstring for usage., A poorly-connected graph node flagged by the detector. (+17 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (24): BaseMessage, Exception, Any, Exception, _BadRequest, _FakeModel, Offline tests for the Groq tool_use_failed repair shim (no network)., Minimal stand-in: returns a canned message, never raises. (+16 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (21): _basic_fallback(), configure_logging(), _ensure_log_dirs(), GroqLoggingCallback, _model_name(), _preview(), Centralised logging + LLM-call instrumentation for API debugging.  * :func:`conf, Logs LLM request / response / error for post-mortem debugging. (+13 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (19): ABC, Polygon, Return the perimeter of the shape., A regular polygon with ``sides`` edges, each ``length`` units long., Sum of the interior angles: (n - 2) * 180., Single interior angle of a regular polygon: (n - 2) * 180 / n., Perimeter: number of sides times the edge length., Draw the polygon with the turtle, turning 360/n degrees per edge. (+11 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (42): 0.1 Base Repository & Graph Products, 0.2 Obsidian Vault & Reverse-Engineering Deliverables, 1.1 Repository & Environment Genesis, 1.2 Guidelines Compliance — Structural Scaffolding, 1.3 LLM Provider Configuration, 1.4 Before-State Snapshot Lock, 2.1 AgentState Schema, 2.2 Graph Nodes (+34 more)

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (28): RepairResult, GraphifySDK, Facade over graph orchestration, efficiency research, and graph analysis., Return the configured (gatekept) LLM, building it once on first use., Compile and return the multi-agent StateGraph., Return the Mermaid diagram of the compiled graph., Run the full Router->Alpha->Gatekeeper->Beta repair; return its result., Deterministic baseline-vs-guided token comparison. (+20 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (38): Agent Tools & Guardrails, Agent Workflow (LangGraph), AgentState Schema, Architectural Decision Record (ADR-001): LangGraph over CrewAI, Architectural Visualizations, Base Repository & Rationale, Before / After, Block Schema (Before State) (+30 more)

### Community 8 - "Community 8"
Cohesion: 0.09
Nodes (22): ApiGatekeeper, estimate_tokens(), GatekeptChatModel, Route a chat model's API calls through the :class:`ApiGatekeeper`.  :func:`wrap_, Rough pre-call token estimate (tokens ≈ chars / 4) used for accounting., Proxy delegating to ``inner`` but submitting ``invoke`` to the gatekeeper., Bind tools on the inner model, keeping the result gatekept., Bind runtime kwargs (e.g. max_tokens) while staying gatekept.          Without t (+14 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (15): Path, Unit tests for the surgical agent tools and TokenTracker (Phase 3)., TestFileIO, TestReadObsidianPage, TestTokenTracker, Tool: sandboxed read/write of source files.  Both operations are confined to the, Resolve ``path`` and confirm it falls inside the allowed source root.      Raise, Return the UTF-8 contents of a file inside ``src/broken-python/``.      Raises: (+7 more)

### Community 10 - "Community 10"
Cohesion: 0.06
Nodes (30): Entry Format, Phase 0 — Knowledge Base & Reverse Engineering, Phase 1 — Environment Setup, Phase 2 — LangGraph Orchestration, Phase 3 — Agent Toolset, Phase 4 — Subagent Alpha (Polygons), Phase 5 — Subagent Beta (Math Quiz), Phase 6 — Analysis & Reporting (+22 more)

### Community 11 - "Community 11"
Cohesion: 0.09
Nodes (23): BaseCallbackHandler, BaselineAgent, _baseline_prompt(), _guided_prompt(), _invoke(), main(), Live token-efficiency measurement — REAL Groq usage, not a chars/4 estimate.  Th, One Groq call with a couple of backoff retries on a rate-limit (413/429). (+15 more)

### Community 12 - "Community 12"
Cohesion: 0.11
Nodes (20): build_token_log(), compare(), main(), Token-efficiency comparison: naive baseline vs. graph-guided agent.  Builds a si, Record the guided agent's per-phase targeted reads onto ``tracker``., Populate one tracker with baseline + guided records for every phase., Return baseline vs. guided totals and the token-reduction ratios., _read() (+12 more)

### Community 13 - "Community 13"
Cohesion: 0.13
Nodes (18): RateLimitConfig, Immutable rate-limit settings for a single API provider., ApiGatekeeper, BackpressureError, get_gatekeeper(), _is_retryable(), Central API gatekeeper (§5.1) — the sole entry point for external calls.  Every, Return the process-wide gatekeeper for ``provider`` (built once, reused). (+10 more)

### Community 14 - "Community 14"
Cohesion: 0.11
Nodes (17): Bug 10 — Only 6 of the promised 10 questions, Bug 11 — Every question mislabelled "Question 1", Bug 1 — `Object` as the base class, Bug 2 — `new Polygon(...)` instantiation, Bug 3 — Hardcoded angle table (only 3- and 4-sided polygons correct), Bug 4 — Turtle loop hardcoded to a hexagon, Bug 5 — Python-2 `print` statements, Bug 6 — Assignment (`=`) used for comparison (+9 more)

### Community 15 - "Community 15"
Cohesion: 0.24
Nodes (12): Rolling-window limiter over request count and token volume., SlidingWindowRateLimiter, FakeClock, Tests for the sliding-window rate limiter., Manually advanced monotonic clock for deterministic window tests., test_requests_per_minute_ceiling(), test_retry_after_falls_back_to_window_for_unfittable_request(), test_retry_after_reports_request_window() (+4 more)

### Community 16 - "Community 16"
Cohesion: 0.17
Nodes (11): OverflowQueue, Thread-safe FIFO queue with a hard depth cap and backpressure logging., RateLimitConfig, Logger, Logger, Tests for the bounded FIFO overflow queue and its backpressure alert., test_enqueue_until_full_then_backpressure(), test_fifo_peek_and_remove() (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.27
Nodes (12): _config(), FakeClock, _gatekeeper(), Tests for the central ApiGatekeeper: rate limiting, queue, drain, retries., test_backpressure_raises_when_queue_full(), test_fast_path_executes_immediately(), test_non_retryable_error_raised_without_retry(), test_oversized_request_rejected() (+4 more)

### Community 18 - "Community 18"
Cohesion: 0.13
Nodes (14): 1. Mechanism Overview, 2. Problem Statement, 3. Theoretical Background, 4.1 Inputs / Outputs, 4.2 Operations (per `submit`), 4.3 Configuration (§5.2 — never hardcoded), 4.4 Integration Point (§5.1 — no bypass), 4. Functional Requirements (+6 more)

### Community 19 - "Community 19"
Cohesion: 0.14
Nodes (13): Communities (12 total, 6 thin omitted), Community 0 - "Community 0", Community 1 - "Community 1", Community Hubs (Navigation), Corpus Check, God Nodes (most connected - your core abstractions), Graph Freshness, Graph Report - broken-python  (2026-06-16) (+5 more)

### Community 20 - "Community 20"
Cohesion: 0.14
Nodes (13): Communities (6 total, 1 thin omitted), Community 1 - "Community 1", Community 4 - "Community 4", Community Hubs (Navigation), Corpus Check, God Nodes (most connected - your core abstractions), Graph Freshness, Graph Report - broken-python  (2026-06-15) (+5 more)

### Community 21 - "Community 21"
Cohesion: 0.24
Nodes (12): load_rate_limit_config(), Load API rate-limit settings from ``config/rate_limits.json``.  Per §5.2, every, Read ``path`` and return the :class:`RateLimitConfig` for ``provider``.      Rai, Tests for loading rate-limit configuration (§5.2: limits from config)., The repo's real config must define limits for the providers we ship., test_committed_config_has_required_providers(), test_loads_provider_section(), test_missing_file_raises() (+4 more)

### Community 22 - "Community 22"
Cohesion: 0.14
Nodes (13): Communities (6 total, 1 thin omitted), Community 1 - "Community 1", Community 4 - "Community 4", Community Hubs (Navigation), Corpus Check, God Nodes (most connected - your core abstractions), Graph Freshness, Graph Report - broken-python  (2026-06-15) (+5 more)

### Community 23 - "Community 23"
Cohesion: 0.14
Nodes (8): Original expected 126., Original expected 668., Original expected 77., Original expected 60., Verify every default question has the right product., Original expected 55., Original expected 49., TestMathQuizAnswerCorrectness

### Community 24 - "Community 24"
Cohesion: 0.17
Nodes (11): make_alpha_node(), Return the SubagentAlpha node bound to the Polygons toolset.      Runs one LLM t, make_beta_node(), build_graph(), Compile and return the sequential StateGraph.      Accepts an optional llm overr, BaseChatModel, BaseChatModel, BaseChatModel (+3 more)

### Community 25 - "Community 25"
Cohesion: 0.15
Nodes (12): 1. Project Context & Goal, 2. Functional Requirements & Orchestration Workflow, 3. KPIs & Acceptance Criteria, 4. Assumptions, Dependencies & Out-of-Scope, Agent Toolset (Guardrails), Architectural Guardrails: "Zero Edge" Domain Isolation, Assumptions, Code & Architecture Standards (+4 more)

### Community 26 - "Community 26"
Cohesion: 0.21
Nodes (10): _alpha_route(), _beta_route(), _has_tool_calls(), Assemble and compile the sequential multi-agent StateGraph.  This is the orchest, Loop through AlphaTools while Alpha is calling tools, else hand off to the Gatek, Loop through BetaTools while Beta is calling tools, else finish., main(), Print the compiled graph's Mermaid diagram (delegates to the SDK). (+2 more)

### Community 27 - "Community 27"
Cohesion: 0.20
Nodes (8): AgentState, gatekeeper_node(), Gatekeeper: logs Alpha completions, purges messages, advances to mathsquiz phase, Master Router: reads the Obsidian index and seeds initial agent state., router_node(), AgentState, AgentState, TypedDict

### Community 28 - "Community 28"
Cohesion: 0.17
Nodes (11): 1. Project Goals, 2. Architectural Visualizations (Reverse Engineering), 3. Architectural Decision Records (ADR), 4. Repository Structure (current state), 5. Agent Workflow Implementation, ADR 001: Choice of Orchestration Framework, ADR 002: Central API Gatekeeper for All External Calls, ADR 003: SDK Layer as the Sole Entry Point (+3 more)

### Community 29 - "Community 29"
Cohesion: 0.17
Nodes (11): 1. Mechanism Overview, 2. Problem Statement, 3.1 Graph Topology, 3.2 AgentState Schema, 3.3 Router Node, 3.4 Gatekeeper Node (see also PRD_gatekeeper.md), 3.5 Entry Point, 3. Functional Requirements (+3 more)

### Community 30 - "Community 30"
Cohesion: 0.17
Nodes (11): 1. Mechanism Overview, 2. Problem Statement, 3. Before-State Findings, 4.1 Data Model, 4.2 Detector Class Interface, 4.3 CLI Entry Point, 4.4 Report Format (`results/orphan_report.md`), 4. Functional Requirements (+3 more)

### Community 31 - "Community 31"
Cohesion: 0.23
Nodes (6): MathQuiz, A small command-line times-tables quiz.  Consolidated, object-oriented rewrite, A ten-question multiplication quiz that tracks the player's score., Test display_result output for each score band., score 8–9 → 'really well'., TestMathQuizResult

### Community 32 - "Community 32"
Cohesion: 0.17
Nodes (5): Test correct answer checking via check_answer., Input from the terminal arrives as a string., Regression: non-numeric input must not raise., Regression: original used '=' instead of '=='., TestMathQuizAnswerValidation

### Community 33 - "Community 33"
Cohesion: 0.26
Nodes (5): TestExtractNodeContent, extract_node_content(), _load_nodes(), Tool: extract the source backing a single graph node.  Resolves a node id from `, Return the raw source of the file backing ``node_id``.      Args:         node_i

### Community 34 - "Community 34"
Cohesion: 0.18
Nodes (6): AIMessage, Dry-run smoke tests for the LangGraph orchestration pipeline.  Uses FakeListChat, draw_mermaid() output includes all five expected node identifiers., A subagent tool call is routed to the ToolNode and yields a ToolMessage., TestGraphCompilation, TestToolInvocation

### Community 35 - "Community 35"
Cohesion: 0.18
Nodes (10): 1. Mechanism Overview, 2. Problem Statement, 3.1 Inputs, 3.2 Operations (in order), 3.3 Outputs, 3.4 Guarantees, 3. Functional Requirements, 4. Zero-Edge Domain Isolation Protocol (+2 more)

### Community 36 - "Community 36"
Cohesion: 0.18
Nodes (10): 1. Mechanism Overview, 2. Problem Statement, 3.1 Interface, 3.2 Resolution Logic, 3.3 Guardrails, 3.4 Caching, 3. Functional Requirements, 4. Non-Functional Requirements (+2 more)

### Community 37 - "Community 37"
Cohesion: 0.18
Nodes (10): 1. Mechanism Overview, 2. Problem Statement, 3.1 Tracked Metrics (per call), 3.2 Interface, 3.3 Baseline Comparison, 3.4 Integration Point, 3. Functional Requirements, 4. Non-Functional Requirements (+2 more)

### Community 38 - "Community 38"
Cohesion: 0.24
Nodes (7): _initial_state(), AgentState, After a full run the current_phase must be 'mathsquiz' (set by Gatekeeper)., Router, Alpha, Gatekeeper, and Beta each leave their marker in completed_tasks., After the full run only Beta's single message remains (Alpha's was purged)., Router seeds token_log with at least one entry., TestGraphTraversal

### Community 39 - "Community 39"
Cohesion: 0.20
Nodes (9): 1. What is the actual architecture, and what wasn't obvious at first glance?, 2. Which components/modules/classes/functions are the most central?, 3. Where are the complexity hotspots, mixed responsibility, or "God Nodes"?, 4. How do you extract a block schema and OOP schema when docs are sparse?, 5. How did you identify the bug, what was the root cause, and what steps led there?, 6. What was the advantage of the graph + Obsidian navigation vs. linear reading?, 7. How did the graph-guided agent save tokens / reduce unnecessary reads?, 8. What improvements, extensions, or agent mechanisms would you add? (+1 more)

### Community 40 - "Community 40"
Cohesion: 0.20
Nodes (9): (a) Total tokens in / out, per phase, (b) Files / text units read, (c) Iterations / investigation rounds, Conclusion, (d) Quality / speed of reaching the root cause, Methodology & Reproducibility, Results — the four §5.5 metrics, Thesis (+1 more)

### Community 41 - "Community 41"
Cohesion: 0.20
Nodes (9): 1. What is the actual architecture, and what wasn't obvious at first glance?, 2. Which components/modules/classes/functions are the most central?, 3. Where are the complexity hotspots, mixed responsibility, or "God Nodes"?, 4. How do you extract a block schema and OOP schema when docs are sparse?, 5. How did you identify the bug, what was the root cause, and what steps led there?, 6. What was the advantage of the graph + Obsidian navigation vs. linear reading?, 7. How did the graph-guided agent save tokens / reduce unnecessary reads?, 8. What improvements, extensions, or agent mechanisms would you add? (+1 more)

### Community 42 - "Community 42"
Cohesion: 0.20
Nodes (5): Unit tests for the consolidated Math Quiz system (Phase 5).  Targets src/broke, Test MathQuiz class instantiation., Assignment expects exactly 10 questions., Constructor accepts an explicit question list., TestMathQuizInit

### Community 43 - "Community 43"
Cohesion: 0.22
Nodes (8): 1. Token efficiency — MEASURED, 2. A real rate-limit finding the model could not show, 3. Live end-to-end agent — now completes (tool_use_failed repaired), Bottom line, Live Groq Results — Measured, Not Modeled, Measured live run — before-state broken code, real repair, The fix: a tool-call repair shim, The limitation that was blocking it

### Community 44 - "Community 44"
Cohesion: 0.22
Nodes (8): Conclusion — the consolidated `mathsquiz.py` supersedes all three, Evolution summary, Math Quiz — Step File Evolution Analysis, Purpose, Step 1 — `mathsquiz-step1.py`: "make it work", Step 2 — `mathsquiz-step2.py`: "remove repetition with functions", Step 3 — `mathsquiz-step3.py`: "generate questions dynamically", The starting point — `mathsquiz.py` (original, broken)

### Community 45 - "Community 45"
Cohesion: 0.25
Nodes (4): Drop entries older than the window (caller holds the lock)., Record a call of ``tokens`` size if both ceilings allow it., Seconds until a call of ``tokens`` size could be admitted (0 if now)., When enough buffered tokens age out to fit ``tokens`` (holds lock).

### Community 46 - "Community 46"
Cohesion: 0.25
Nodes (4): Return ``True`` if ``answer`` equals the product of ``question``.          ``a, Pose one question to the player and update the score in place., Ask every question in order, then show the result; return the score., Print the closing message based on the final score.

### Community 47 - "Community 47"
Cohesion: 0.29
Nodes (4): Append ``item`` in FIFO order; return ``False`` (alert) when full., Return the head item without removing it (``None`` if empty)., Remove the first occurrence of ``item`` if present., Any

### Community 48 - "Community 48"
Cohesion: 0.29
Nodes (6): Headline numbers, Knowledge Delta — Before vs. After Graph, Math Quiz — code consolidated, graph snapshot pending, Orphans — unchanged count, shifted composition, Polygons — God Functions eliminated, OOP nodes added, Summary

### Community 50 - "Community 50"
Cohesion: 0.33
Nodes (5): Before / After (post-refactoring), Graphic Mapping, Navigation and Investigation Paths, Research & Investigation, System Index - Broken Python

### Community 51 - "Community 51"
Cohesion: 0.40
Nodes (4): Math Quiz System — Before State, OOP Schema — Before State, Polygons System — Before State, Target Architecture — After Remediation

### Community 52 - "Community 52"
Cohesion: 0.40
Nodes (4): Introduction, Maths Quiz, Objectives, The Files

### Community 53 - "Community 53"
Cohesion: 0.40
Nodes (4): Orphan Node Report, Orphan Nodes, Recommendations, Summary

## Knowledge Gaps
- **262 isolated node(s):** `Logger`, `Any`, `Path`, `BaseChatModel`, `Exception` (+257 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphifySDK` connect `Community 6` to `Community 1`, `Community 26`, `Community 11`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `AIMessage` connect `Community 34` to `Community 2`, `Community 6`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `OrphanDetector` connect `Community 1` to `Community 6`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `OrphanDetector` (e.g. with `OrphanNode` and `RepairResult`) actually correct?**
  _`OrphanDetector` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `BaselineAgent` (e.g. with `BaselineAgent` and `TokenTracker`) actually correct?**
  _`BaselineAgent` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `GraphifySDK` (e.g. with `main()` and `main()`) actually correct?**
  _`GraphifySDK` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `SlidingWindowRateLimiter` (e.g. with `ApiGatekeeper` and `.__init__()`) actually correct?**
  _`SlidingWindowRateLimiter` has 15 INFERRED edges - model-reasoned connections that need verification._