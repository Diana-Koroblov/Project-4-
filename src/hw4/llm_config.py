"""LLM provider configuration.

Loads the Groq API key from .env and returns a configured
ChatGroq instance. Model name and parameters are read from
config/setup.json — nothing is hardcoded here.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from hw4.constants import CONFIG_SETUP_PATH


def _load_config() -> dict:
    """Read config/setup.json and return the llm section."""
    config_path = Path(CONFIG_SETUP_PATH)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with config_path.open() as f:
        return json.load(f)["llm"]


def get_llm() -> ChatGroq:
    """Return a configured ChatGroq instance.

    Reads GROQ_API_KEY from the .env file.
    Reads model, temperature, and max_tokens from config/setup.json.

    Raises:
        EnvironmentError: If GROQ_API_KEY is not set.
        FileNotFoundError: If config/setup.json is missing.
    """
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. "
            "Copy .env-example to .env and add your key."
        )

    cfg = _load_config()

    return ChatGroq(
        api_key=api_key,
        model=cfg["model"],
        temperature=cfg["temperature"],
        max_tokens=cfg["max_tokens"],
    )
