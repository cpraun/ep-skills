"""Deterministic tests for redlines (tracked changes) in the handle-docx skill (no model call).

Two guarantees, both from references/openxml-and-tracked-changes.md and SKILL.md "Reading":

- **Writing redlines.** Insertions, deletions and replacements are recorded as real
  Word revision markup (<w:ins>, <w:del>/<w:delText>) with unique ids, author and
  date, keeping the formatting of the text concerned — so that accepting all
  changes gives the revised text and rejecting all gives the original.
- **Reading redlines.** A reader sees the text with all changes applied (inserted
  and moved-to text in, deleted and moved-from text out) — not python-docx's
  `paragraph.text`, which drops inserted text altogether.

Where pandoc is installed, its independent reading of the saved file
(`--track-changes=accept|reject`) is used as a cross-check that the markup is
genuine Word markup and not only something our own reader understands.

Free and offline; requires python-docx (skipped otherwise).
"""

import shutil
import subprocess
import sys

import pytest

from skilltest import skill_dir_for

docx = pytest.importorskip("docx")

SKILL_DIR = skill_dir_for(__file__)   # -> <repo>/skills/util/handle-docx
sys.path.insert(0, str(SKILL_DIR / "scripts"))
import docx_helper as h  # noqa: E402

from docx.oxml import parse_xml  # noqa: E402
from docx.oxml.ns import nsdecls  # noqa: E402
from docx.shared import Pt  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
PANDOC = shutil.which("pandoc")
needs_pandoc = pytest.mark.skipif(PANDOC is None, reason="pandoc not installed")

ORIGINAL = "The housing is made of aluminium and comprises a lid."


def _claim_paragraph(doc):
    """ORIGINAL split over three runs; 'aluminium' bold 12 pt."""
    p = doc.add_paragraph()
    p.add_run("The housing is made of ")
    b = p.add_run("aluminium")
    b.bold = True
    b.font.size = Pt(12)
    p.add_run(" and comprises a lid.")
    return p


def _pandoc(path, mode):
    out = subprocess.run(
        [PANDOC, f"--track-changes={mode}", "-t", "plain", "--wrap=none", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    # Drop pandoc's plain-text table borders (lines of '-', '+', '|', '=').
    return " ".join(w for w in out.split() if w.strip("-+|=:"))


def _revisions(p, tag):
    return p._p.findall(f"{W}{tag}")


# --- Writing: the markup itself ------------------------------------------------

def test_deletion_is_real_word_markup():
    d = docx.Document()
    p = _claim_paragraph(d)
    dele = h.add_tracked_deletion(p, "aluminium", author="Attorney")
    assert dele is not None and dele.tag == f"{W}del"
    assert dele.get(f"{W}author") == "Attorney" and dele.get(f"{W}date")
    assert dele.get(f"{W}id", "").isdigit()
    # Deleted text lives in <w:delText>, never in <w:t>, inside the <w:del>.
    assert "".join(t.text for t in dele.iter(f"{W}delText")) == "aluminium"
    assert not list(dele.iter(f"{W}t"))


def test_deletion_keeps_formatting_of_deleted_run():
    d = docx.Document()
    p = _claim_paragraph(d)
    dele = h.add_tracked_deletion(p, "aluminium")
    rpr = dele.find(f"{W}r/{W}rPr")
    assert rpr is not None and rpr.find(f"{W}b") is not None, "bold must survive the deletion"


def test_deletion_mid_run_splits_and_keeps_surrounding_text():
    d = docx.Document()
    p = _claim_paragraph(d)
    h.add_tracked_deletion(p, "made of alumin")   # starts mid-run 1, ends mid-run 2
    assert h.accepted_text(p) == "The housing is ium and comprises a lid."
    # The remaining "ium" is still bold: the split kept the run formatting.
    remaining = [r for r in p._p.findall(f"{W}r") if "ium" in "".join(t.text for t in r.iter(f"{W}t"))]
    assert remaining and remaining[0].find(f"{W}rPr/{W}b") is not None


def test_deletion_of_absent_text_changes_nothing():
    d = docx.Document()
    p = _claim_paragraph(d)
    before = p._p.xml
    assert h.add_tracked_deletion(p, "copper") is None
    assert p._p.xml == before


def test_replacement_is_deletion_followed_by_insertion_with_same_formatting():
    d = docx.Document()
    p = _claim_paragraph(d)
    assert h.add_tracked_replacement(p, "aluminium", "copper")
    dele, ins = _revisions(p, "del"), _revisions(p, "ins")
    assert len(dele) == 1 and len(ins) == 1
    assert dele[0].getnext() is ins[0], "the insertion must directly follow the deletion"
    assert "".join(t.text for t in ins[0].iter(f"{W}t")) == "copper"
    assert ins[0].find(f"{W}r/{W}rPr/{W}b") is not None, "new text takes the old text's formatting"


def test_every_revision_gets_a_unique_id():
    d = docx.Document()
    p = _claim_paragraph(d)
    q = d.add_paragraph("Second paragraph.")
    h.add_tracked_replacement(p, "aluminium", "copper")
    h.add_tracked_deletion(p, " and comprises a lid")
    h.add_tracked_insertion(q, " Added.")
    ids = [e.get(f"{W}id") for e in d.element.body.iter(f"{W}ins", f"{W}del")]
    assert len(ids) == 4 and len(set(ids)) == 4


def test_redlines_survive_save_and_reopen(tmp_path):
    d = docx.Document()
    p = _claim_paragraph(d)
    h.add_tracked_replacement(p, "aluminium", "copper")
    out = tmp_path / "amended.docx"
    d.save(out)
    p2 = docx.Document(out).paragraphs[0]
    assert len(_revisions(p2, "del")) == 1 and len(_revisions(p2, "ins")) == 1
    assert h.accepted_text(p2) == "The housing is made of copper and comprises a lid."


@needs_pandoc
def test_pandoc_accept_and_reject_give_revised_and_original_text(tmp_path):
    d = docx.Document()
    p = _claim_paragraph(d)
    h.add_tracked_replacement(p, "aluminium", "copper")
    h.add_tracked_deletion(p, " and comprises a lid")
    h.add_tracked_insertion(p, " It has a lid.")
    out = tmp_path / "amended.docx"
    d.save(out)
    assert _pandoc(out, "accept") == "The housing is made of copper. It has a lid."
    assert _pandoc(out, "reject") == ORIGINAL


# --- Reading: text with the changes applied -----------------------------------

def _redlined_by_hand():
    """A document whose tracked changes were written as raw Word XML — not by our
    helper — so the reader is tested independently of the writer."""
    d = docx.Document()
    p = d.add_paragraph()
    p._p.append(parse_xml(
        f'<w:r {nsdecls("w")}><w:t xml:space="preserve">A device comprising </w:t></w:r>'))
    p._p.append(parse_xml(
        f'<w:del {nsdecls("w")} w:id="1" w:author="X" w:date="2026-01-01T00:00:00Z">'
        f'<w:r><w:delText>a lever</w:delText></w:r></w:del>'))
    p._p.append(parse_xml(
        f'<w:ins {nsdecls("w")} w:id="2" w:author="X" w:date="2026-01-01T00:00:00Z">'
        f'<w:r><w:rPr><w:b/></w:rPr><w:t>a resilient lever</w:t></w:r></w:ins>'))
    p._p.append(parse_xml(
        f'<w:r {nsdecls("w")}><w:t xml:space="preserve"> and a spring.</w:t></w:r>'))
    q = d.add_paragraph()
    q._p.append(parse_xml(
        f'<w:moveFrom {nsdecls("w")} w:id="3" w:author="X" w:date="2026-01-01T00:00:00Z">'
        f'<w:r><w:t>Moved away. </w:t></w:r></w:moveFrom>'))
    q._p.append(parse_xml(
        f'<w:r {nsdecls("w")}><w:t xml:space="preserve">Kept.</w:t></w:r>'))
    q._p.append(parse_xml(
        f'<w:moveTo {nsdecls("w")} w:id="4" w:author="X" w:date="2026-01-01T00:00:00Z">'
        f'<w:r><w:t xml:space="preserve"> Moved here.</w:t></w:r></w:moveTo>'))
    cell = d.add_table(rows=1, cols=1).cell(0, 0).paragraphs[0]
    cell._p.append(parse_xml(
        f'<w:ins {nsdecls("w")} w:id="5" w:author="X" w:date="2026-01-01T00:00:00Z">'
        f'<w:r><w:t>Inserted in a table</w:t></w:r></w:ins>'))
    return d


def test_reader_shows_text_with_changes_applied():
    d = _redlined_by_hand()
    assert h.accepted_text(d.paragraphs[0]) == "A device comprising a resilient lever and a spring."
    assert h.accepted_text(d.paragraphs[1]) == "Kept. Moved here."


def test_python_docx_paragraph_text_is_not_enough():
    # Documents why the skill must not read with paragraph.text: it drops the
    # inserted text and shows neither version.
    d = _redlined_by_hand()
    assert d.paragraphs[0].text == "A device comprising  and a spring."
    assert d.paragraphs[0].text != h.accepted_text(d.paragraphs[0])


def test_whole_document_reading_includes_tables_in_order():
    d = _redlined_by_hand()
    assert h.read_text_with_changes_applied(d).split("\n") == [
        "A device comprising a resilient lever and a spring.",
        "Kept. Moved here.",
        "Inserted in a table",
    ]


def test_tracked_changes_are_detected():
    assert h.has_tracked_changes(_redlined_by_hand())
    clean = docx.Document()
    clean.add_paragraph("No changes.")
    assert not h.has_tracked_changes(clean)


@needs_pandoc
def test_reader_agrees_with_pandoc(tmp_path):
    d = _redlined_by_hand()
    out = tmp_path / "redlined.docx"
    d.save(out)
    ours = " ".join(h.read_text_with_changes_applied(docx.Document(out)).split())
    assert ours == _pandoc(out, "accept")
