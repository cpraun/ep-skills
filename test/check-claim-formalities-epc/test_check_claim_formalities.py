"""Eval suite for the check-claim-formalities-epc skill.

Each scenario under cases/ is generated against the model, then checked by the
deterministic gates (gates.run_gates) — structure, scope discipline, and
forbidden-phrase rules drawn straight from SKILL.md. Hard-fail; each failure
names the rule it violated.

Formalities are mechanical, so these scenarios are unusually gate-friendly: the
gate confirms the skill produced its formalities assessment and stayed in scope
(pushing substantive clarity out to /check-art-84-epc). It does not grade whether
every individual defect was spotted — that stays with the reviewing attorney.
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

SKILL_DIR = skill_dir_for(__file__)   # -> <repo>/skills/claims/check-claim-formalities-epc
CASES = discover_cases(__file__)
CASE_IDS = [c.name for c in CASES]

# Skill-specific gate configuration (see gates.run_gates).
GATE_PROFILE = {
    "skill": "check-claim-formalities-epc",
    "structure": {
        # §Output format — the assessment title, the per-claim issue table, or the
        # "no formal issues" line a clean claim set produces.
        "formalities assessment": (
            r"claim formalities assessment"
            r"|\|\s*issue\s*#\s*\|"
            r"|no formal issues identified"
        ),
    },
    # Substantive-clarity terms are named legitimately when the skill declares them
    # out of scope, so drift is left to scenario `forbidden` lists.
    "drift": [],
}


@pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
def test_gates(case, request):
    out = generate(read_skill_body(SKILL_DIR), load_input(case))
    show_output(request, case.name, out)
    failures = run_gates(out, load_expected(case), GATE_PROFILE)
    assert not failures, "gate failures:\n  - " + "\n  - ".join(failures)
