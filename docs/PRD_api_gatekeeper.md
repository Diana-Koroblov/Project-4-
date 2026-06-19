# PRD: Central API Gatekeeper & Rate Limiting

> **Disambiguation.** This document covers the **API Gatekeeper** (`src/hw4/gateway/`),
> the rate-limiting front door for all external API calls (§5 of the requirements).
> It is **not** the *Gatekeeper node* (`src/hw4/nodes/gatekeeper.py`, see
> [`PRD_gatekeeper.md`](PRD_gatekeeper.md)), which is an in-graph context-reset
> step. The two share a name by coincidence of domain vocabulary only.

## 1. Mechanism Overview
The API Gatekeeper is the single, central choke point through which every
outbound call to an external LLM provider (Groq) must pass. It enforces
config-driven rate limits before each call, parks overflow in a bounded FIFO
queue and drains it as the rate window resets, retries transient failures with
exponential backoff, and logs every admission and outcome for monitoring.

Implementation (one concern per file, all ≤ 150 LOC):

| File | Class / function | Concern |
|---|---|---|
| `src/hw4/gateway/config.py` | `RateLimitConfig`, `load_rate_limit_config()` | Read limits from `config/rate_limits.json` |
| `src/hw4/gateway/rate_limiter.py` | `SlidingWindowRateLimiter` | Enforce RPM + TPM over a rolling window |
| `src/hw4/gateway/overflow_queue.py` | `OverflowQueue` | Bounded FIFO + backpressure alert |
| `src/hw4/gateway/gatekeeper.py` | `ApiGatekeeper`, `get_gatekeeper()` | Orchestrate admit → drain → retry → log |
| `src/hw4/gateway/llm_proxy.py` | `GatekeptChatModel`, `wrap_with_gatekeeper()` | Route a chat model's calls through the gatekeeper |

## 2. Problem Statement
Free-tier Groq enforces hard per-minute ceilings on both **requests** (RPM) and
**tokens** (TPM). A multi-agent run that fires calls in a tight tool loop will,
without governance, burst past those ceilings and receive `429 Too Many
Requests` / `413` errors that crash a phase mid-repair. Equally, scattering rate
logic across call sites would duplicate code (violating §4.2 OOP/DRY) and make
it impossible to guarantee that *no* call bypasses the limits (§5.1). A single
gatekeeper makes the ceiling enforceable, the overflow recoverable, and the call
stream auditable.

## 3. Theoretical Background
**Rate limiting — sliding-window log.** We track the timestamps of recent
admissions in a deque and admit a new call only if, within the trailing window
`W = 60 s`, both the request count and the summed token volume stay under their
ceilings:

```
admit(t, k)  ⇔  |{r ∈ R : r > t − W}| < RPM   ∧   Σ{ tok(τ) : τ > t − W } + k ≤ TPM
```

where `R` is the set of recent request times and `k` the estimated tokens of the
new call. When a call cannot be admitted, the **reset time** is the moment the
oldest blocking entry ages out of the window — `retry_after()` returns
`oldest + W − t`. This is the classic sliding-window-log algorithm: exact (no
boundary bursting) at the cost of `O(window-occupancy)` memory, which is
negligible at our call volume.

**Backoff.** Transient failures are retried after `b · 2^a` seconds for attempt
`a` (exponential backoff), bounding load on an already-stressed endpoint.

**Queueing.** Overflow is buffered FIFO so admission order equals arrival order
(fairness), with a hard depth cap so an overloaded producer triggers
backpressure instead of unbounded memory growth (a bounded-buffer producer/
consumer).

## 4. Functional Requirements

### 4.1 Inputs / Outputs
| Surface | Input | Output |
|---|---|---|
| `load_rate_limit_config(provider, path)` | provider name, config path | `RateLimitConfig` (RPM, TPM, retries, backoff, queue size, poll) |
| `SlidingWindowRateLimiter.try_acquire(tokens)` | int tokens | `bool` (admitted / not) |
| `SlidingWindowRateLimiter.retry_after(tokens)` | int tokens | `float` seconds until admissible (`0.0` if now) |
| `OverflowQueue.enqueue(item)` | any | `bool` (`False` + alert when full) |
| `ApiGatekeeper.submit(fn, *args, estimated_tokens, **kwargs)` | callable + args | result of `fn`, or raises `BackpressureError` / re-raises a non-retryable error |
| `wrap_with_gatekeeper(model, provider)` | chat model | `GatekeptChatModel` proxy |

### 4.2 Operations (per `submit`)
1. Reject up front if `estimated_tokens > TPM` (un-servable in any window).
2. Enqueue a FIFO ticket; if the queue is full, log a backpressure alert and
   raise `BackpressureError`.
3. Drain: while this ticket is not the head **or** the limiter denies it, sleep
   `min(retry_after, poll_interval)` and re-check — this is the window-reset
   drain.
4. On admission, dequeue the ticket and run `fn` with retries: retry only
   *transient* errors (HTTP 429/503, timeouts) up to `max_retries` with
   exponential backoff; re-raise everything else immediately.
5. Log every admission, success, retry, and failure to the `hw4.gateway` logger.

### 4.3 Configuration (§5.2 — never hardcoded)
All limits are read from `config/rate_limits.json`, keyed by provider:
```json
{ "groq": { "requests_per_minute": 30, "tokens_per_minute": 6000,
            "max_retries": 3, "retry_backoff_seconds": 2, "queue_max_size": 100 } }
```
`poll_interval_seconds` is optional (defaults via `DEFAULT_POLL_INTERVAL_SECONDS`).

### 4.4 Integration Point (§5.1 — no bypass)
`hw4.llm_config.get_llm()` wraps the single `ChatGroq` instance with
`wrap_with_gatekeeper(...)`. Because `ChatGroq` is constructed nowhere else, and
the proxy keeps both `bind_tools(...)` **and** `bind(...)` results gatekept,
every real Groq call — in the agent tool loop and in `live_efficiency.py` —
flows through the gatekeeper. Test doubles injected via `build_graph(llm=fake)`
are not wrapped, so the suite runs offline and fast.

## 5. Non-Functional Requirements & Performance Metrics
- **Thread safety:** limiter, queue, and the gatekeeper registry each guard
  shared state with a `threading.Lock` (§15.2).
- **Monitoring:** `hw4.gateway` is a child of the `hw4` logger, so every record
  reaches `results/agent.log` (§5.1 "all API calls are logged").
- **Latency budget:** an admitted fast-path call adds only two lock-guarded
  deque scans (`O(window occupancy)`) — target < 1 ms of gatekeeper overhead.
- **Determinism in tests:** `clock` and `sleep` are injectable so window/drain
  behaviour is tested without wall-clock waits (dependency injection, §16.2).

## 6. Constraints & Limitations
- Token counts are **estimated pre-call** (`tokens ≈ chars / 4`); the limiter is
  conservative, not exact to the provider's tokenizer.
- A single request whose estimate exceeds TPM is rejected by design — it can
  never fit one window. The committed groq `tokens_per_minute` (6000, free tier)
  must be raised in config to match a higher paid tier.
- Enforcement is per-process (one gatekeeper per provider via `get_gatekeeper`);
  it does not coordinate limits across multiple processes/hosts.

## 7. Alternatives Considered
| Decision | Alternatives | Choice & rationale |
|---|---|---|
| Rate algorithm | Fixed-window counter; token bucket; **sliding-window log** | Sliding-window log: exact, no fixed-window boundary bursts; memory cost is trivial at our volume. |
| Overflow behaviour | Reject immediately; drop-oldest (`deque(maxlen=)`); **bounded FIFO + block-drain** | §5.3 mandates queueing, not rejection; FIFO preserves fairness; a hard cap yields backpressure instead of unbounded growth. |
| Interception point | Monkeypatch `ChatGroq`; gate inside `invoke_with_repair`; **proxy at `get_llm()`** | Proxy wraps only the real model, so fakes bypass the gatekeeper (no shared-window slowdown in tests) while every real call is mediated. |
| Retry scope | Retry all exceptions; **retry transient only** | Retrying a `tool_use_failed` (HTTP 400) would waste calls and delay the repair layer; only 429/503/timeouts are transient. |

## 8. Success Criteria
- [x] Every external API call passes through `ApiGatekeeper` (proxy keeps
      `bind`/`bind_tools` gatekept; only `ChatGroq` site is wrapped).
- [x] Rate limits read from `config/rate_limits.json`; nothing hardcoded.
- [x] Overflow is queued FIFO with a config-driven depth cap and a backpressure
      alert when full; queue drains as the window resets.
- [x] Transient failures retried with exponential backoff; non-transient errors
      surface unchanged.
- [x] Gateway activity logged to `results/agent.log`.
- [x] 100 % statement coverage of `src/hw4/gateway/`; `ruff check` clean; all
      files ≤ 150 LOC.

## 9. Test Scenarios
Covered by `tests/test_gateway_*.py`:

| Scenario | Test | Expectation |
|---|---|---|
| Provider section loaded; defaults applied | `test_gateway_config.py` | RPM/TPM/queue parsed; `poll_interval` default; committed config has groq + openai |
| Missing file / unknown provider | `test_gateway_config.py` | `FileNotFoundError` / `KeyError` |
| RPM ceiling, then window reset | `test_gateway_rate_limiter.py` | 3rd call denied; admitted after `+60 s` |
| TPM ceiling boundary | `test_gateway_rate_limiter.py` | `800+300` denied, `800+200` admitted |
| `retry_after` for request/token/unfittable | `test_gateway_rate_limiter.py` | correct reset seconds; full window for oversize |
| Queue fills → backpressure | `test_gateway_queue.py` | `enqueue` returns `False` + warning logged |
| FIFO peek/remove ordering | `test_gateway_queue.py` | head advances in arrival order |
| Fast path admits immediately | `test_gateway_gatekeeper.py` | no sleep |
| Rate-limited call waits then drains | `test_gateway_gatekeeper.py` | total sleep ≥ one window |
| Backpressure on full queue | `test_gateway_gatekeeper.py` | `BackpressureError` |
| Oversize request | `test_gateway_gatekeeper.py` | `ValueError` (cannot ever admit) |
| Transient retry (timeout / HTTP 429) then success | `test_gateway_gatekeeper.py` | retried with backoff, then returns |
| Non-transient error / max-retries exhausted | `test_gateway_gatekeeper.py` | re-raised; bounded attempt count |
| Singleton per provider | `test_gateway_gatekeeper.py` | same instance returned |
| Proxy `invoke` / `bind` / `bind_tools` stay gatekept | `test_gateway_proxy.py` | calls routed through gatekeeper; token estimate correct |
