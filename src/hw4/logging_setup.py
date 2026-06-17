"""Centralised logging + LLM-call instrumentation for API debugging.

* :func:`configure_logging` loads ``config/logging_config.json`` via
  ``dictConfig`` so the project shares one rotating file log
  (``results/agent.log``) plus a console handler. It is idempotent and falls
  back to a basic file+console setup if the JSON is missing/invalid, so a
  logging misconfig can never silently hide the errors you are debugging.
* :class:`GroqLoggingCallback` is a LangChain callback that records every LLM
  request, its latency and token usage, and — critically — the full traceback
  for any API failure (rate limits, auth, timeouts). It is attached
  automatically by :func:`hw4.llm_config.get_llm`, so any real Groq call leaves
  an audit trail in ``results/agent.log``.
"""

from __future__ import annotations

import json
import logging
import logging.config
import time
from pathlib import Path
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler

from hw4.constants import CONFIG_LOGGING_PATH

LLM_LOGGER_NAME = "hw4.llm"
_PREVIEW_LIMIT = 500
_CONFIGURED = False


def _ensure_log_dirs(config: dict) -> None:
    """Create parent dirs for every FileHandler ``filename`` ahead of dictConfig."""
    for handler in config.get("handlers", {}).values():
        filename = handler.get("filename")
        if filename:
            Path(filename).parent.mkdir(parents=True, exist_ok=True)


def _basic_fallback() -> None:
    Path("results").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("results/agent.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def configure_logging(
    config_path: str = CONFIG_LOGGING_PATH, *, force: bool = False
) -> logging.Logger:
    """Configure project logging once; return the ``hw4`` logger.

    Safe to call repeatedly — only the first call (or ``force=True``) applies the
    configuration.
    """
    global _CONFIGURED
    if _CONFIGURED and not force:
        return logging.getLogger("hw4")
    try:
        config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        _ensure_log_dirs(config)
        logging.config.dictConfig(config)
    except (OSError, ValueError) as exc:
        _basic_fallback()
        logging.getLogger("hw4").warning(
            "logging_config.json unusable (%s); using basic fallback", exc
        )
    _CONFIGURED = True
    return logging.getLogger("hw4")


def _model_name(serialized: Any, kwargs: dict) -> str:
    params = kwargs.get("invocation_params") or {}
    name = params.get("model") or params.get("model_name")
    if not name and isinstance(serialized, dict):
        name = serialized.get("name") or (serialized.get("kwargs") or {}).get("model")
    return name or "unknown"


def _usage(response: Any) -> dict:
    """Best-effort extraction of token usage from an LLMResult."""
    out = getattr(response, "llm_output", None) or {}
    usage = out.get("token_usage") or out.get("usage")
    if usage:
        return dict(usage)
    try:
        message = response.generations[0][0].message
    except (AttributeError, IndexError):
        return {}
    return dict(getattr(message, "usage_metadata", None) or {})


def _preview(messages: Any) -> str:
    try:
        text = " | ".join(
            str(getattr(m, "content", m)) for batch in messages for m in batch
        )
    except TypeError:
        text = str(messages)
    return text[:_PREVIEW_LIMIT] + ("…" if len(text) > _PREVIEW_LIMIT else "")


class GroqLoggingCallback(BaseCallbackHandler):
    """Logs LLM request / response / error for post-mortem debugging."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger(LLM_LOGGER_NAME)
        self._started_at: dict[Any, float] = {}

    def on_chat_model_start(self, serialized, messages, *, run_id=None, **kwargs):
        self._started_at[run_id] = time.perf_counter()
        n_msgs = sum(len(batch) for batch in messages)
        self.logger.info(
            "LLM start | model=%s | messages=%d | run=%s",
            _model_name(serialized, kwargs), n_msgs, run_id,
        )
        self.logger.debug("LLM prompt preview: %s", _preview(messages))

    def on_llm_start(self, serialized, prompts, *, run_id=None, **kwargs):
        self._started_at[run_id] = time.perf_counter()
        self.logger.info(
            "LLM start | model=%s | prompts=%d | run=%s",
            _model_name(serialized, kwargs), len(prompts), run_id,
        )

    def on_llm_end(self, response, *, run_id=None, **kwargs):
        self.logger.info(
            "LLM ok | run=%s | elapsed=%.3fs | usage=%s",
            run_id, self._elapsed(run_id), _usage(response),
        )

    def on_llm_error(self, error, *, run_id=None, **kwargs):
        self.logger.error(
            "LLM FAILED | run=%s | elapsed=%.3fs | %s: %s",
            run_id, self._elapsed(run_id), type(error).__name__, error,
            exc_info=error,
        )

    def _elapsed(self, run_id) -> float:
        start = self._started_at.pop(run_id, None)
        return time.perf_counter() - start if start is not None else -1.0
