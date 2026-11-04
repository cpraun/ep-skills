"""Eval suite for the check-art-123-2-epc skill.

Each scenario under cases/ is generated against the model, then checked by the
deterministic gates (gates.run_gates) — structure, scope discipline, and
forbidden-phrase rules drawn straight from SKILL.md. Hard-fail; each failure
names the rule it violated.

The gates check that the output is well-shaped (a finding is reached) and in
scope; they do not judge whether COMPLIANT / NON-COMPLIANT is the *correct*
verdict — that stays with the reviewing attorney.
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

SKILL_DIR = skill_dir_for(__file__)   # -> <repo>/skills/check-art-123-2-epc
CASES = discover_cases(__file__)
CASE_IDS = [c.name for c in CASES]

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


@pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
def test_gates(case, request):
    out = generate(read_skill_body(SKILL_DIR), load_input(case))
    show_output(request, case.name, out)
    failures = run_gates(out, load_expected(case), GATE_PROFILE)
    assert not failures, "gate failures:\n  - " + "\n  - ".join(failures)
