"""Thin wrapper around the Anthropic API."""
import json
import os
import re

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")
_client = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY is not set. Add it to your .env file.")
        _client = Anthropic()
    return _client


def ask(system: str, user: str, max_tokens: int = 1200, history=None) -> str:
    """Send a prompt to Claude and return the text reply."""
    messages = list(history or []) + [{"role": "user", "content": user}]
    resp = _get_client().messages.create(
        model=MODEL, max_tokens=max_tokens, system=system, messages=messages
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def ask_json(system: str, user: str, max_tokens: int = 2000):
    """Ask for JSON only and parse it safely."""
    text = ask(system + "\nRespond with valid JSON only. No prose, no markdown fences.",
               user, max_tokens)
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(text)
