"""Tests for the sliding-window rate limiter."""

from hw4.gateway.rate_limiter import SlidingWindowRateLimiter


class FakeClock:
    """Manually advanced monotonic clock for deterministic window tests."""

    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t

    def advance(self, dt):
        self.t += dt


def test_requests_per_minute_ceiling():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(2, 10_000, clock=clock)
    assert limiter.try_acquire(1) is True
    assert limiter.try_acquire(1) is True
    assert limiter.try_acquire(1) is False  # RPM=2 reached


def test_window_resets_after_60s():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(1, 10_000, clock=clock)
    assert limiter.try_acquire(1) is True
    assert limiter.try_acquire(1) is False
    clock.advance(60.1)
    assert limiter.try_acquire(1) is True  # oldest request aged out


def test_tokens_per_minute_ceiling():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(100, 1000, clock=clock)
    assert limiter.try_acquire(800) is True
    assert limiter.try_acquire(300) is False  # 800+300 > 1000
    assert limiter.try_acquire(200) is True  # 800+200 == 1000 fits


def test_retry_after_zero_when_capacity_free():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(5, 10_000, clock=clock)
    assert limiter.retry_after(1) == 0.0


def test_retry_after_reports_request_window():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(1, 10_000, clock=clock)
    limiter.try_acquire(1)
    clock.advance(20)
    assert limiter.retry_after(1) == 40.0  # 0 + 60 - 20


def test_retry_after_reports_token_window():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(100, 1000, clock=clock)
    limiter.try_acquire(900)
    clock.advance(10)
    # Need 900+200-1000 = 100 tokens to free; the 900-token entry ages out at 60.
    assert limiter.retry_after(200) == 50.0


def test_retry_after_falls_back_to_window_for_unfittable_request():
    # A request larger than the whole TPM budget can never fit; the limiter
    # reports a full window rather than looping forever (gatekeeper guards this).
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(100, 1000, clock=clock)
    assert limiter.retry_after(5000) == 60.0
