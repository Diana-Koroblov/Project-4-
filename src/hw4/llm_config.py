"""LLM provider configuration.

Reads provider, model, and parameters from config/setup.json.
Reads the API key from .env. Supports: groq, gemini.
Nothing is hardcoded — swap providers by editing setup.json only.
"""

import json
import os
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

from hw4.constants import CONFIG_SETUP_PATH


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


def get_llm() -> Union["ChatGroq", "ChatGoogleGenerativeAI"]:  # noqa: F821
    """Return a configured LLM instance based on config/setup.json.

    Supported providers: groq, gemini.

    Raises:
        EnvironmentError: If the required API key is not set.
        FileNotFoundError: If config/setup.json is missing.
        ValueError: If the provider in setup.json is not supported.
    """
    load_dotenv()
    cfg = _load_config()
    provider = cfg["provider"]

    if provider == "groq":
        from langchain_groq import ChatGroq

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GROQ_API_KEY is not set. Add it to your .env file."
            )
        return ChatGroq(
            api_key=api_key,
            model=cfg["model"],
            temperature=cfg["temperature"],
            max_tokens=cfg["max_tokens"],
        )

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY is not set. Add it to your .env file."
            )
        return ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=cfg["model"],
            temperature=cfg["temperature"],
            max_output_tokens=cfg["max_tokens"],
        )

    raise ValueError(
        f"Unsupported provider: '{provider}'. "
        "Choose 'groq' or 'gemini' in config/setup.json."
    )
