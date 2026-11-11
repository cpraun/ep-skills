"""Eval suite for the check-art-84-epc skill.

Each scenario under cases/ is generated against the model, then checked by the
deterministic gates (gates.run_gates) — structure, scope discipline, and
forbidden-phrase rules drawn straight from SKILL.md. Hard-fail; each failure
names the rule it violated.

The gates check that the output is a well-shaped clarity assessment and stays in
scope; they do not judge whether a given issue was correctly rated High/Medium/Low
— that stays with the reviewing attorney.
"""

from skilltest import gate_test

# Skill-specific gate configuration (see gates.run_gates).
GATE_PROFILE = {
    "skill": "check-art-84-epc",
    "structure": {
        # §Output format — the assessment title, the per-claim issue table, or the
        # "no issues" line a clean claim produces. Any one of them means the skill
        # produced its assessment rather than doing something else.
        "clarity assessment": (
            r"clarity and conciseness assessment"
            r"|\|\s*issue\s*#\s*\|"
            r"|no clarity or conciseness issues identified"
        ),
    },
    # No universally-safe drift phrase (the skill legitimately names Art. 83 / support
    # when declaring them out of scope), so drift is left to scenario `forbidden` lists.
    "drift": [],
}

test_gates = gate_test(__file__, GATE_PROFILE)
