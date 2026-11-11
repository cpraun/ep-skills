"""Eval suite for the check-art-83-epc skill.

Each scenario under cases/ is generated against the model, then checked by the
deterministic gates (gates.run_gates) — structure, scope discipline, and
forbidden-phrase rules drawn straight from SKILL.md. Hard-fail; each failure
names the rule it violated.

The gates check that the output is a well-shaped sufficiency assessment (or, when
the mandatory description is missing, that the skill asks for it rather than
assessing claims alone) and stays in scope; they do not judge whether a given
issue was correctly rated — that stays with the reviewing attorney.
"""

from skilltest import gate_test

# Skill-specific gate configuration (see gates.run_gates).
GATE_PROFILE = {
    "skill": "check-art-83-epc",
    "structure": {
        # §Output format — the assessment title, the per-claim issue table, or the
        # "no issues" line a fully-enabled claim produces.
        "sufficiency assessment": (
            r"sufficiency of disclosure assessment"
            r"|\|\s*issue\s*#\s*\|"
            r"|no sufficiency issues identified"
        ),
    },
    # No universally-safe drift phrase (the skill legitimately names Art. 84 / support
    # when declaring them out of scope), so drift is left to scenario `forbidden` lists.
    "drift": [],
}

test_gates = gate_test(__file__, GATE_PROFILE)
