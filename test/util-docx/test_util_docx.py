"""Eval suite for the util-docx skill.

Each scenario under cases/ is generated against the model, then checked by the
deterministic gates (gates.run_gates). The harness is text-only — the model cannot
open or save a Word file here — so these scenarios check the *approach* the skill
makes the model take: python-docx code that keeps the original formatting, loads
the right template, and asks for the file instead of inventing it.

The helper script itself is tested deterministically, without a model call, in
test_docx_helper.py next to this file.
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

SKILL_DIR = skill_dir_for(__file__)   # -> <repo>/skills/util-docx
CASES = discover_cases(__file__)
CASE_IDS = [c.name for c in CASES]

GATE_PROFILE = {
    "skill": "util-docx",
    "structure": {
        # The skill works through python-docx: a normal answer contains code that
        # loads a document with it.
        "python-docx code": r"import docx|from docx\b|docx\.Document\(|load_document\(",
    },
    # "Editing" — assigning paragraph.text destroys run formatting; never acceptable.
    # The trailing space keeps a comparison (`paragraph.text == ...`) from matching.
    # Caveat: the gate is a plain substring check, so it also fires if the model
    # merely *quotes* the warning in prose; read the output before blaming the skill.
    "drift": ["paragraph.text = "],
}


@pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
def test_gates(case, request):
    out = generate(read_skill_body(SKILL_DIR), load_input(case))
    show_output(request, case.name, out)
    failures = run_gates(out, load_expected(case), GATE_PROFILE)
    assert not failures, "gate failures:\n  - " + "\n  - ".join(failures)
