# Sample file. Fill in your API keys and set a model provider and the respective model.
# Then rename this file from env_sample.sh to env.sh
#
# Fill in your key below, then load it (from inside test/):  source ./env.sh
# It is meant to be *sourced*, not executed.

# Choose which provider the tests run against: gemini (default) or claude.
export MODEL_PROVIDER="gemini"

# --- Gemini (Google) — used when MODEL_PROVIDER=gemini ---
export GEMINI_API_KEY=""   
export GEMINI_MODEL=""          # e.g. gemini-3.5-flash - verify the current id: https://ai.google.dev/gemini-api/docs/models

# --- Claude (Anthropic) — used when MODEL_PROVIDER=claude ---
export ANTHROPIC_API_KEY=""
export ANTHROPIC_MODEL=""          # e.g. claude-opus-5 - verify the current id: https://platform.claude.com/docs/en/about-claude/models/overview
