"""LLM provider configuration.

Reads provider, model, and parameters from config/setup.json.
Reads the API key from .env. Provider: groq.
Nothing is hardcoded — tune model/params by editing setup.json only.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

from hw4.constants import CONFIG_SETUP_PATH
from hw4.logging_setup import GroqLoggingCallback, configure_logging


def _load_config() -> dict:
    """Read config/setup.json and return the llm section."""
    config_path = Path(CONFIG_SETUP_PATH)
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found: {config_path}. "
            "Copy config/setup.example.json to config/setup.json."
        )
    with config_path.open() as f:
        return json.load(f)["llm"]


def get_llm() -> "ChatGroq":  # noqa: F821
    """Return a configured Groq LLM instance based on config/setup.json.

    Raises:
        EnvironmentError: If GROQ_API_KEY is not set.
        FileNotFoundError: If config/setup.json is missing.
        ValueError: If the provider in setup.json is not 'groq'.
    """
    logger = configure_logging()
    load_dotenv()
    cfg = _load_config()
    provider = cfg["provider"]

    if provider != "groq":
        logger.error("Unsupported provider in config/setup.json: %r", provider)
        raise ValueError(
            f"Unsupported provider: '{provider}'. "
            "Only 'groq' is supported; set provider='groq' in config/setup.json."
        )

    from langchain_groq import ChatGroq

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY is not set; cannot create the Groq LLM.")
        raise EnvironmentError("GROQ_API_KEY is not set. Add it to your .env file.")

    logger.info("Creating Groq LLM | model=%s", cfg["model"])
    return ChatGroq(
        api_key=api_key,
        model=cfg["model"],
        temperature=cfg["temperature"],
        max_tokens=cfg["max_tokens"],
        # Attach the audit callback so every API call is logged to results/agent.log.
        callbacks=[GroqLoggingCallback()],
    )
