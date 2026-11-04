"""Eval suite for the check-art-54-epc skill.

Each scenario under cases/ is generated against the model, then checked by the
deterministic gates (gates.run_gates) — structure, scope discipline, and
forbidden-phrase rules drawn straight from SKILL.md. Hard-fail; each failure
names the rule it violated.
"""

import pytest

from runner import generate
from gates import run_gates
from skilltest import (
    skill_dir_for,
    read_skill_body,
    discover_cases,
    load_input,
    load_expected,
    show_output,
)

SKILL_DIR = skill_dir_for(__file__)   # -> <repo>/skills/check-art-54-epc
CASES = discover_cases(__file__)
CASE_IDS = [c.name for c in CASES]

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


@pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
def test_gates(case, request):
    out = generate(read_skill_body(SKILL_DIR), load_input(case))
    show_output(request, case.name, out)
    failures = run_gates(out, load_expected(case), GATE_PROFILE)
    assert not failures, "gate failures:\n  - " + "\n  - ".join(failures)
