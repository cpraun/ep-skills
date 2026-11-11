"""Eval suite for the check-art-123-2-epc skill.

Each scenario under cases/ is generated against the model, then checked by the
deterministic gates (gates.run_gates) — structure, scope discipline, and
forbidden-phrase rules drawn straight from SKILL.md. Hard-fail; each failure
names the rule it violated.

The gates check that the output is well-shaped (a finding is reached) and in
scope; they do not judge whether COMPLIANT / NON-COMPLIANT is the *correct*
verdict — that stays with the reviewing attorney.
"""

from skilltest import gate_test

# Skill-specific gate configuration (see gates.run_gates).
GATE_PROFILE = {
    "skill": "check-art-123-2-epc",
    "structure": {
        # §Output Format — the assessment ends in a Finding with one of the three
        # verdicts. Requiring the verdict token confirms a conclusion was reached.
        "finding verdict": r"COMPLIANT|NON[\s-]?COMPLIANT|UNCERTAIN",
    },
    # No universally-safe drift phrase here (e.g. "inventive step" legitimately
    # appears in the G 1/03 disclaimer conditions), so drift is left to
    # scenario-specific `forbidden` lists.
    "drift": [],
}

test_gates = gate_test(__file__, GATE_PROFILE)
