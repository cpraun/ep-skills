"""Eval suite for the check-art-54-epc skill.

Each scenario under cases/ is generated against the model, then checked by the
deterministic gates (gates.run_gates) — structure, scope discipline, and
forbidden-phrase rules drawn straight from SKILL.md. Hard-fail; each failure
names the rule it violated.
"""

from skilltest import gate_test

# Skill-specific gate configuration (see gates.run_gates).
GATE_PROFILE = {
    "skill": "check-art-54-epc",
    "structure": {
        # §Output format — the mandated five-column novelty table.
        "feature table": r"\|\s*Feature\s*\|\s*Claim wording\s*\|\s*D1 disclosure\s*\|\s*Citation\s*\|\s*Assessment\s*\|",
        # Step 5 — a conclusion line per claim.
        "conclusion line": r"\*\*\s*conclusion",
    },
    # Step 6 cross-check — no inventive-step reasoning (Art. 56 drift).
    "drift": [
        "obvious to combine",
        "obviously combine",
        "straightforward to modify",
        "would arrive at",
        "obvious modification",
    ],
}

test_gates = gate_test(__file__, GATE_PROFILE)
