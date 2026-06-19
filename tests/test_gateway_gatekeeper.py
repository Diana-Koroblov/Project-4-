"""Tests for the central ApiGatekeeper: rate limiting, queue, drain, retries."""

import pytest

from hw4.gateway.config import RateLimitConfig
from hw4.gateway.gatekeeper import ApiGatekeeper, BackpressureError, get_gatekeeper


class FakeClock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t

    def advance(self, dt):
        self.t += dt


def _config(**overrides):
    base = {
        "provider": "test",
        "requests_per_minute": 1,
        "tokens_per_minute": 10_000,
        "max_retries": 2,
        "retry_backoff_seconds": 1.0,
        "queue_max_size": 5,
        "poll_interval": 30.0,
    }
    base.update(overrides)
    return RateLimitConfig(**base)


def _gatekeeper(clock, **overrides):
    sleeps = []

    def sleep(dt):
        sleeps.append(dt)
        clock.advance(dt)

    gk = ApiGatekeeper(_config(**overrides), clock=clock, sleep=sleep)
    return gk, sleeps


def test_fast_path_executes_immediately():
    gk, sleeps = _gatekeeper(FakeClock())
    result = gk.submit(lambda x: x * 2, 21, estimated_tokens=10)
    assert result == 42
    assert sleeps == []  # no waiting needed


def test_rate_limited_call_waits_then_drains():
    clock = FakeClock()
    gk, sleeps = _gatekeeper(clock)
    gk.submit(lambda: "first", estimated_tokens=10)  # uses the only RPM slot
    result = gk.submit(lambda: "second", estimated_tokens=10)
    assert result == "second"
    assert sum(sleeps) >= 60.0  # had to wait a full window for the slot to free


def test_backpressure_raises_when_queue_full(monkeypatch):
    gk, _ = _gatekeeper(FakeClock())
    monkeypatch.setattr(gk._queue, "enqueue", lambda item: False)
    with pytest.raises(BackpressureError):
        gk.submit(lambda: "x", estimated_tokens=10)


def test_oversized_request_rejected():
    gk, _ = _gatekeeper(FakeClock(), tokens_per_minute=100)
    with pytest.raises(ValueError, match="cannot ever admit"):
        gk.submit(lambda: "x", estimated_tokens=500)


def test_retries_transient_error_then_succeeds():
    gk, sleeps = _gatekeeper(FakeClock(), requests_per_minute=100)
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise TimeoutError("temporary network blip")
        return "ok"

    assert gk.submit(flaky, estimated_tokens=10) == "ok"
    assert calls["n"] == 3
    assert len(sleeps) == 2  # two backoffs before the third attempt


def test_retries_on_http_429_status_code():
    gk, sleeps = _gatekeeper(FakeClock(), requests_per_minute=100)
    calls = {"n": 0}

    class RateLimited(Exception):
        status_code = 429

    def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise RateLimited("429 too many requests")
        return "ok"

    assert gk.submit(flaky, estimated_tokens=10) == "ok"
    assert calls["n"] == 2 and len(sleeps) == 1


def test_non_retryable_error_raised_without_retry():
    gk, _ = _gatekeeper(FakeClock(), requests_per_minute=100)
    calls = {"n": 0}

    def bad():
        calls["n"] += 1
        raise ValueError("malformed request")

    with pytest.raises(ValueError, match="malformed"):
        gk.submit(bad, estimated_tokens=10)
    assert calls["n"] == 1  # not retried


def test_retry_gives_up_after_max_retries():
    gk, sleeps = _gatekeeper(FakeClock(), requests_per_minute=100, max_retries=1)
    calls = {"n": 0}

    def always_429():
        calls["n"] += 1
        raise TimeoutError("rate limit")

    with pytest.raises(TimeoutError):
        gk.submit(always_429, estimated_tokens=10)
    assert calls["n"] == 2  # initial + 1 retry
    assert len(sleeps) == 1


def test_get_gatekeeper_is_singleton_per_provider():
    first = get_gatekeeper("groq")
    second = get_gatekeeper("groq")
    assert first is second
