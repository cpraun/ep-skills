"""Model seam for the skill test harness.

Everything that couples the tests to a specific LLM lives in this one file. The
harness can run each skill against either **Gemini** (default) or **Claude**,
selected by the MODEL_PROVIDER environment variable; the gates and the per-skill
suites never see the provider.

Both provider SDKs are imported lazily inside their branch, so a machine that
only ever uses one provider needs only that provider's SDK installed, and
collecting the tests requires neither.

Environment (set in test/env.sh):
    MODEL_PROVIDER      gemini (default) | claude
    # Gemini:
    GEMINI_API_KEY      (or GOOGLE_API_KEY)
    GEMINI_MODEL        default gemini-2.5-pro
    # Claude:
    ANTHROPIC_API_KEY
    ANTHROPIC_MODEL     default claude-opus-5
    ANTHROPIC_MAX_TOKENS  default 16000
"""

import os
from functools import lru_cache


def _provider():
    return os.environ.get("MODEL_PROVIDER", "gemini").strip().lower()


# --- Gemini (Google) --------------------------------------------------------
# Verify the current model id at https://ai.google.dev/gemini-api/docs/models
# before relying on this. Override without editing code via GEMINI_MODEL.
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")


@lru_cache(maxsize=1)
def _gemini_client():
    from google import genai

    # Reads GEMINI_API_KEY (or GOOGLE_API_KEY) from the environment.
    return genai.Client()


def _generate_gemini(skill_body, user_input):
    from google.genai import types

    response = _gemini_client().models.generate_content(
        model=GEMINI_MODEL,
        contents=user_input,
        config=types.GenerateContentConfig(system_instruction=skill_body),
    )
    return response.text


# --- Claude (Anthropic) -----------------------------------------------------
# Verify the current model id at
# https://platform.claude.com/docs/en/about-claude/models/overview
# Override without editing code via ANTHROPIC_MODEL.
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")
# max_tokens caps thinking + response together on current Claude models; 16000
# is a safe non-streaming default. Do NOT set temperature/top_p — current models
# reject them.
ANTHROPIC_MAX_TOKENS = int(os.environ.get("ANTHROPIC_MAX_TOKENS", "16000"))


@lru_cache(maxsize=1)
def _anthropic_client():
    import anthropic

    # Reads ANTHROPIC_API_KEY from the environment.
    return anthropic.Anthropic()


def _generate_claude(skill_body, user_input):
    message = _anthropic_client().messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=ANTHROPIC_MAX_TOKENS,
        system=skill_body,
        messages=[{"role": "user", "content": user_input}],
    )
    # content is a list of blocks; concatenate the text blocks (skips any
    # thinking blocks, which are empty by default on current models).
    return "".join(block.text for block in message.content if block.type == "text")


def generate(skill_body, user_input):
    """Run a skill against the configured provider: its SKILL.md body as system
    context, the user input as the turn. Returns the model's text response."""
    provider = _provider()
    if provider in ("gemini", "google"):
        return _generate_gemini(skill_body, user_input)
    if provider in ("claude", "anthropic"):
        return _generate_claude(skill_body, user_input)
    raise ValueError(
        f"Unknown MODEL_PROVIDER={provider!r}; set it to 'gemini' or 'claude' in test/env.sh."
    )
