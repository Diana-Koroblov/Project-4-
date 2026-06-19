"""Tests for loading rate-limit configuration (§5.2: limits from config)."""

import json

import pytest

from hw4.gateway.config import RateLimitConfig, load_rate_limit_config

_SAMPLE = {
    "groq": {
        "requests_per_minute": 30,
        "tokens_per_minute": 6000,
        "max_retries": 3,
        "retry_backoff_seconds": 2,
        "queue_max_size": 100,
    }
}


def _write(tmp_path, data):
    path = tmp_path / "rate_limits.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


def test_loads_provider_section(tmp_path):
    cfg = load_rate_limit_config("groq", _write(tmp_path, _SAMPLE))
    assert isinstance(cfg, RateLimitConfig)
    assert cfg.requests_per_minute == 30
    assert cfg.tokens_per_minute == 6000
    assert cfg.max_retries == 3
    assert cfg.queue_max_size == 100


def test_poll_interval_has_default(tmp_path):
    cfg = load_rate_limit_config("groq", _write(tmp_path, _SAMPLE))
    assert cfg.poll_interval > 0


def test_poll_interval_read_from_config(tmp_path):
    data = {"groq": {**_SAMPLE["groq"], "poll_interval_seconds": 1.5}}
    cfg = load_rate_limit_config("groq", _write(tmp_path, data))
    assert cfg.poll_interval == 1.5


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_rate_limit_config("groq", str(tmp_path / "absent.json"))


def test_unknown_provider_raises(tmp_path):
    with pytest.raises(KeyError):
        load_rate_limit_config("openai", _write(tmp_path, _SAMPLE))


def test_committed_config_has_required_providers():
    """The repo's real config must define limits for the providers we ship."""
    for provider in ("groq", "openai"):
        cfg = load_rate_limit_config(provider)
        assert cfg.requests_per_minute > 0
        assert cfg.tokens_per_minute > 0
