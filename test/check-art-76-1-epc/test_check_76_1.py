"""Eval suite for the check-art-76-1-epc skill.

Each scenario under cases/ is generated against the model, then checked by the
deterministic gates (gates.run_gates) — structure, scope discipline, and
forbidden-phrase rules drawn straight from SKILL.md. Hard-fail; each failure
names the rule it violated.

The gates check that the output is a well-shaped divisional-basis assessment (a
feature table plus a conclusion) — or, when the parent as filed is missing or was
supplied only as a granted patent, that the skill asks for the as-filed text
rather than assessing. They do not judge whether COMPLIES / DOES NOT COMPLY is the
correct verdict — that stays with the reviewing attorney.
"""

from skilltest import gate_test

# Skill-specific gate configuration (see gates.run_gates).
GATE_PROFILE = {
    "skill": "check-art-76-1-epc",
    "structure": {
        # §Output format — the mandated feature/basis table ...
        "basis table": r"\|\s*Feature\s*\|\s*Claim wording\s*\|\s*Basis in earlier application\s*\|\s*Citation\s*\|\s*Assessment\s*\|",
        # ... and a per-claim conclusion.
        "conclusion line": r"\*\*\s*conclusion",
    },
    # Workflow step 5 cross-check — no inventive-step reasoning (Art. 56 drift).
    "drift": [
        "obvious to combine",
        "obviously combine",
        "straightforward to modify",
        "would arrive at",
        "obvious modification",
    ],
}

test_gates = gate_test(__file__, GATE_PROFILE)
