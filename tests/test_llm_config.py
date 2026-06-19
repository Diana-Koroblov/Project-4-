"""Unit tests for the Groq-only LLM configuration."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hw4 import llm_config

_GROQ_CFG = {
    "provider": "groq",
    "model": "llama-3.3-70b-versatile",
    "temperature": 0.0,
    "max_tokens": 8192,
}


class TestGetLLM:
    def test_unknown_provider_raises_value_error(self, monkeypatch):
        monkeypatch.setattr(llm_config, "_load_config", lambda: {**_GROQ_CFG, "provider": "gemini"})
        monkeypatch.setenv("GROQ_API_KEY", "x")
        with pytest.raises(ValueError, match="Only 'groq' is supported"):
            llm_config.get_llm()

    def test_missing_key_raises_environment_error(self, monkeypatch):
        monkeypatch.setattr(llm_config, "_load_config", lambda: dict(_GROQ_CFG))
        monkeypatch.setattr(llm_config, "load_dotenv", lambda *a, **k: None)
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        with pytest.raises(EnvironmentError, match="GROQ_API_KEY"):
            llm_config.get_llm()

    def test_groq_happy_path_wraps_in_gatekeeper_with_callback(self, monkeypatch):
        monkeypatch.setattr(llm_config, "_load_config", lambda: dict(_GROQ_CFG))
        monkeypatch.setenv("GROQ_API_KEY", "test-key")
        llm = llm_config.get_llm()
        # §5.1: the model is returned behind the API gatekeeper proxy...
        assert llm.__class__.__name__ == "GatekeptChatModel"
        # ...wrapping a real ChatGroq that still carries the audit callback
        # (delegated through the proxy's __getattr__).
        assert llm._inner.__class__.__name__ == "ChatGroq"
        assert any(
            cb.__class__.__name__ == "GroqLoggingCallback" for cb in (llm.callbacks or [])
        )

    def test_missing_config_file_raises(self, monkeypatch, tmp_path):
        monkeypatch.setattr(llm_config, "CONFIG_SETUP_PATH", str(tmp_path / "nope.json"))
        with pytest.raises(FileNotFoundError, match="Copy config"):
            llm_config._load_config()
