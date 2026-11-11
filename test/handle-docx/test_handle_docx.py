"""Eval suite for the handle-docx skill.

Each scenario under cases/ is generated against the model, then checked by the
deterministic gates (gates.run_gates). The harness is text-only — the model cannot
open or save a Word file here — so these scenarios check the *approach* the skill
makes the model take: python-docx code that keeps the original formatting, loads
the right template, and asks for the file instead of inventing it.

The helper script itself is tested deterministically, without a model call, in
test_docx_helper.py next to this file.
"""

from skilltest import gate_test

GATE_PROFILE = {
    "skill": "handle-docx",
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

test_gates = gate_test(__file__, GATE_PROFILE)
