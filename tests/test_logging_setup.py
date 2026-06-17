"""Unit tests for logging setup and the LLM audit callback."""

import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hw4 import logging_setup
from hw4.logging_setup import (
    GroqLoggingCallback,
    _model_name,
    _preview,
    _usage,
    configure_logging,
)


class _FakeMessage:
    def __init__(self, content, usage_metadata=None):
        self.content = content
        if usage_metadata is not None:
            self.usage_metadata = usage_metadata


class _FakeGeneration:
    def __init__(self, message):
        self.message = message


class _FakeResult:
    def __init__(self, llm_output=None, message=None):
        self.llm_output = llm_output
        self.generations = [[_FakeGeneration(message)]] if message else [[]]


class TestConfigureLogging:
    def test_loads_config_and_creates_log_dir(self, tmp_path):
        log_file = tmp_path / "logs" / "agent.log"
        cfg = {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "filename": str(log_file),
                    "level": "DEBUG",
                }
            },
            "loggers": {"hw4": {"handlers": ["file"], "level": "DEBUG"}},
        }
        cfg_path = tmp_path / "logging_config.json"
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        logger = configure_logging(str(cfg_path), force=True)
        assert logger.name == "hw4"
        assert log_file.parent.exists()

    def test_falls_back_when_config_missing(self, tmp_path):
        logger = configure_logging(str(tmp_path / "nope.json"), force=True)
        assert logger.name == "hw4"  # no exception, returns usable logger

    def test_idempotent_without_force(self, monkeypatch):
        monkeypatch.setattr(logging_setup, "_CONFIGURED", True)
        # Should short-circuit and not raise even with a bogus path.
        assert configure_logging("does-not-exist.json").name == "hw4"


class TestExtractors:
    def test_model_name_from_invocation_params(self):
        name = _model_name({}, {"invocation_params": {"model": "llama-3.3-70b"}})
        assert name == "llama-3.3-70b"

    def test_model_name_fallback_unknown(self):
        assert _model_name(None, {}) == "unknown"

    def test_usage_from_llm_output(self):
        result = _FakeResult(llm_output={"token_usage": {"total_tokens": 42}})
        assert _usage(result) == {"total_tokens": 42}

    def test_usage_from_message_metadata(self):
        msg = _FakeMessage("hi", usage_metadata={"input_tokens": 5})
        assert _usage(_FakeResult(message=msg)) == {"input_tokens": 5}

    def test_usage_empty_when_absent(self):
        assert _usage(_FakeResult(message=_FakeMessage("hi"))) == {}

    def test_preview_truncates(self):
        msg = _FakeMessage("x" * 1000)
        out = _preview([[msg]])
        assert out.endswith("…") and len(out) <= logging_setup._PREVIEW_LIMIT + 1


class TestGroqLoggingCallback:
    def _callback(self):
        logger = logging.getLogger("test_groq_cb")
        logger.setLevel(logging.DEBUG)
        return GroqLoggingCallback(logger=logger), logger

    def test_start_and_end_logged(self, caplog):
        cb, logger = self._callback()
        with caplog.at_level(logging.INFO, logger=logger.name):
            cb.on_chat_model_start(
                {"name": "ChatGroq"},
                [[_FakeMessage("hello")]],
                run_id="r1",
                invocation_params={"model": "llama-3.3-70b"},
            )
            cb.on_llm_end(
                _FakeResult(llm_output={"token_usage": {"total_tokens": 7}}),
                run_id="r1",
            )
        text = caplog.text
        assert "LLM start" in text and "llama-3.3-70b" in text
        assert "LLM ok" in text and "total_tokens" in text

    def test_error_logged_with_traceback(self, caplog):
        cb, logger = self._callback()
        with caplog.at_level(logging.ERROR, logger=logger.name):
            cb.on_llm_error(RuntimeError("rate limit exceeded"), run_id="r2")
        records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert records and "LLM FAILED" in records[0].getMessage()
        assert records[0].exc_info is not None  # traceback captured

    def test_text_model_start_logged(self, caplog):
        cb, logger = self._callback()
        with caplog.at_level(logging.INFO, logger=logger.name):
            cb.on_llm_start(
                {"name": "ChatGroq"},
                ["one prompt"],
                run_id="r3",
                invocation_params={"model_name": "llama-3.1-8b"},
            )
        assert "LLM start" in caplog.text and "llama-3.1-8b" in caplog.text

    def test_elapsed_handles_unknown_run(self):
        cb, _ = self._callback()
        assert cb._elapsed("never-started") == -1.0
