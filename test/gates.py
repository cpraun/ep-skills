"""Deterministic gates — the harness's only grading step.

Pure string/regex checks over a skill's output. No model calls, stable, hard-fail.
Each check maps to an explicit requirement in the skill's SKILL.md, and each
failure message names the rule it violated so a red test is self-explaining.

The gates are skill-agnostic; the skill-specific bits (its invocation name for the
refusal sentence, the structure markers its output must contain, and the "drift"
phrases it must never emit) come from a *profile* that each per-skill test file
supplies. `run_gates(output, expected, profile)` returns a list of failure
strings (empty == pass). Which checks fire is driven by the `expected.yaml`
fixture, so the same function serves every scenario of every skill.

A profile is a dict:
    {
      "skill": "check-art-54-epc",          # for the "outside the scope of /<skill>" refusal
      "structure": {"<label>": <regex>, …}, # markers required when output is expected
      "drift": ["phrase", …],               # phrases that must never appear
    }
"""

import re

# Words that indicate the skill asked for missing input rather than inventing it.
ASK_WORDS = (
    "provide",
    "supply",
    "paste",
    "attach",
    "passages",
    "text of",
    "originally filed",
    "original disclosure",
    "as filed",
)


def run_gates(output, expected, profile):
    fails = []
    low = output.lower()
    expect_output = expected.get("expect_output", True)

    # --- Structure vs input-discipline ---
    # When the skill's normal assessment is expected, every structure marker must
    # be present. When it is not (a bare request that should be answered by asking
    # for input), no marker may appear — the skill must not fabricate an answer.
    for label, pattern in profile["structure"].items():
        present = bool(re.search(pattern, output, re.IGNORECASE))
        if expect_output and not present:
            fails.append(f"structure: missing {label} ({profile['skill']} output format)")
        if not expect_output and present:
            fails.append(f"input-discipline: produced {label} when required input was absent")

    # --- Asking for missing input ---
    # Implied whenever output is not expected; can also be required alongside a
    # provisional answer (e.g. an assessment that still asks for the missing basis).
    if expected.get("must_ask", not expect_output):
        if not any(w in low for w in ASK_WORDS):
            fails.append("input-discipline: did not ask for the missing input")

    # --- Scope discipline ---
    # The skill must decline the out-of-scope part with an "outside ... scope"
    # statement. Accept any phrasing of that refusal — the model may name the skill
    # command (/check-...), the article ("Art. 76(1) EPC assessment"), or its own
    # subject. The invariant is that it explicitly declined, not the exact wording.
    if expected.get("must_refuse", False):
        if not re.search(r"outside\b[^\n]{0,25}\bscope\b", output, re.IGNORECASE):
            fails.append(
                f"scope: no out-of-scope refusal ('outside ... scope') found — "
                f"the {profile['skill']} skill must decline the out-of-scope request"
            )

    # --- Forbidden phrases: skill-wide drift + scenario-specific ---
    for phrase in list(profile.get("drift", [])) + list(expected.get("forbidden", []) or []):
        if phrase.lower() in low:
            fails.append(f"forbidden: '{phrase}'")

    return fails
