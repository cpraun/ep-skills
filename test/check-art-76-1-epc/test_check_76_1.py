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

SKILL_DIR = skill_dir_for(__file__)   # -> <repo>/skills/check/check-art-76-1-epc
CASES = discover_cases(__file__)
CASE_IDS = [c.name for c in CASES]

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


@pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
def test_gates(case, request):
    out = generate(read_skill_body(SKILL_DIR), load_input(case))
    show_output(request, case.name, out)
    failures = run_gates(out, load_expected(case), GATE_PROFILE)
    assert not failures, "gate failures:\n  - " + "\n  - ".join(failures)
