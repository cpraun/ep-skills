"""Deterministic tests for the handle-docx skill's helper script (no model call).

Unlike the eval suites, these exercise real code: skills/util/handle-docx/scripts/
docx_helper.py, on real .docx files built in a temporary directory. They check the
skill's two guarantees that can be verified mechanically:

- template selection — the user's template (~/.ep-skills/template.docx) if present,
  else template-sample.docx, else a blank document (SKILL.md "Opening a document");
- formatting preservation — replacements and insertions keep the run formatting
  of the original text (SKILL.md guiding principle and "Editing").

Free and offline; requires python-docx (skipped otherwise).
"""

import sys

import pytest

from skilltest import skill_dir_for

docx = pytest.importorskip("docx")

SKILL_DIR = skill_dir_for(__file__)   # -> <repo>/skills/util/handle-docx
sys.path.insert(0, str(SKILL_DIR / "scripts"))
import docx_helper as h  # noqa: E402

from docx.enum.style import WD_STYLE_TYPE  # noqa: E402
from docx.shared import Pt  # noqa: E402

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _marked_doc(path, marker_text):
    """A document whose only paragraph says `marker_text` — to tell templates apart."""
    d = docx.Document()
    d.add_paragraph(marker_text)
    d.save(path)
    return path


# --- Template selection (SKILL.md "Opening a document") -------------------------------------

def test_shipped_sample_template_exists_and_is_empty():
    sample = SKILL_DIR / "assets" / "template-sample.docx"
    assert sample.is_file(), "assets/template-sample.docx must ship with the skill"
    d = docx.Document(sample)
    assert not any(p.text.strip() for p in d.paragraphs), (
        "the sample template must be empty: its text would appear in every new document"
    )
    assert not d.core_properties.author and not d.core_properties.subject, (
        "the sample template must carry no author/subject metadata"
    )


def test_customize_note_ships_with_the_skill():
    assert (SKILL_DIR / "assets" / "CUSTOMIZE.txt").is_file()


def test_user_template_is_preferred(tmp_path):
    user = _marked_doc(tmp_path / "template.docx", "USER TEMPLATE")
    _marked_doc(tmp_path / "template-sample.docx", "SAMPLE TEMPLATE")
    d = h.load_document(user_template=str(user), template_dir=str(tmp_path))
    assert d.paragraphs[0].text == "USER TEMPLATE"


def test_sample_template_is_the_fallback(tmp_path):
    _marked_doc(tmp_path / "template-sample.docx", "SAMPLE TEMPLATE")
    d = h.load_document(user_template=str(tmp_path / "none.docx"), template_dir=str(tmp_path))
    assert d.paragraphs[0].text == "SAMPLE TEMPLATE"


def test_blank_document_when_no_template(tmp_path):
    d = h.load_document(user_template=str(tmp_path / "none.docx"), template_dir=str(tmp_path))
    assert not any(p.text for p in d.paragraphs)


def test_existing_input_file_beats_any_template(tmp_path):
    user = _marked_doc(tmp_path / "template.docx", "USER TEMPLATE")
    src = _marked_doc(tmp_path / "letter.docx", "ORIGINAL LETTER")
    d = h.load_document(input_path=str(src), user_template=str(user), template_dir=str(tmp_path))
    assert d.paragraphs[0].text == "ORIGINAL LETTER"


def test_default_template_dir_is_the_skills_assets(tmp_path, monkeypatch):
    # Independent of the current working directory.
    monkeypatch.chdir(tmp_path)
    d = h.load_document()
    assert d is not None


# --- Formatting preservation (guiding principle, "Editing") ----------------------

def _split_run_paragraph(doc):
    """'Our Ref.: [FILE NUMBER] dated today' with the placeholder split over three
    runs, the first bold 12 pt — as Word's spellchecker typically leaves it."""
    p = doc.add_paragraph()
    a = p.add_run("Our Ref.: [FILE")
    a.bold = True
    a.font.size = Pt(12)
    b = p.add_run(" NUM")
    b.italic = True
    p.add_run("BER] dated today")
    return p


def test_cross_run_replacement_keeps_text_and_first_run_formatting(tmp_path):
    d = docx.Document()
    p = _split_run_paragraph(d)
    assert h.replace_text_in_paragraph(p, "[FILE NUMBER]", "STW 001")
    assert p.text == "Our Ref.: STW 001 dated today"
    # The replacement lands in the first run and inherits its formatting.
    assert "STW 001" in p.runs[0].text
    assert p.runs[0].bold is True and p.runs[0].font.size == Pt(12)
    # Round-trip through a saved file.
    out = tmp_path / "out.docx"
    d.save(out)
    p2 = docx.Document(out).paragraphs[0]
    assert p2.text == "Our Ref.: STW 001 dated today"
    assert p2.runs[0].bold is True


def test_single_run_replacement_keeps_run_formatting():
    d = docx.Document()
    p = d.add_paragraph()
    r = p.add_run("Dear [NAME],")
    r.italic = True
    assert h.replace_text_in_paragraph(p, "[NAME]", "Ms Example")
    assert p.text == "Dear Ms Example,"
    assert p.runs[0].italic is True


def test_replacement_leaves_unrelated_paragraph_untouched():
    d = docx.Document()
    other = d.add_paragraph()
    o = other.add_run("Unrelated text")
    o.bold = True
    p = d.add_paragraph("[X]")
    assert h.replace_text_in_paragraph(p, "[X]", "Y")
    assert not h.replace_text_in_paragraph(other, "[X]", "Y")
    assert other.text == "Unrelated text" and other.runs[0].bold is True


def test_paragraph_style_is_kept():
    d = docx.Document()
    p = d.add_paragraph("[TITLE]", style="Heading 1")
    h.replace_text_in_paragraph(p, "[TITLE]", "Response to the Communication")
    assert p.style.name == "Heading 1"


def test_replace_everywhere_covers_tables_headers_and_footers():
    d = docx.Document()
    d.add_paragraph("Body [APP]")
    d.add_table(rows=1, cols=1).cell(0, 0).paragraphs[0].add_run("Cell [APP]")
    sec = d.sections[0]
    sec.header.paragraphs[0].add_run("Header [APP]")
    sec.footer.paragraphs[0].add_run("Footer [APP]")
    count = h.replace_text_everywhere(d, {"[APP]": "EP 0000000"})
    assert count == 4
    texts = [p.text for p in h.iter_all_paragraphs(d)]
    assert "Body EP 0000000" in texts
    assert "Cell EP 0000000" in texts
    assert "Header EP 0000000" in texts
    assert "Footer EP 0000000" in texts
    assert not any("[APP]" in t for t in texts)


def test_tracked_insertion_inherits_formatting_of_last_run():
    d = docx.Document()
    p = d.add_paragraph()
    r = p.add_run("Claim 1 is amended")
    r.bold = True
    r.font.size = Pt(11)
    h.add_tracked_insertion(p, " to recite feature X.", author="Test")
    ins = p._p.find(f"{W_NS}ins")
    assert ins is not None and ins.get(f"{W_NS}author") == "Test"
    rpr = ins.find(f"{W_NS}r/{W_NS}rPr")
    assert rpr is not None and rpr.find(f"{W_NS}b") is not None, (
        "the inserted text must carry the formatting of the surrounding run"
    )
    assert ins.find(f"{W_NS}r/{W_NS}t").text == " to recite feature X."


def test_cell_shading_sets_fill():
    d = docx.Document()
    cell = d.add_table(rows=1, cols=1).cell(0, 0)
    h.set_cell_shading(cell, "#D9E1F2")
    shd = cell._tc.tcPr.find(f"{W_NS}shd")
    assert shd is not None and shd.get(f"{W_NS}fill") == "D9E1F2"


def test_editing_an_existing_file_keeps_its_styles(tmp_path):
    # A document "based on another Word file": its custom style must survive an edit.
    src = tmp_path / "original.docx"
    d = docx.Document()
    style = d.styles.add_style("FirmBody", WD_STYLE_TYPE.PARAGRAPH)
    style.font.size = Pt(13)
    d.add_paragraph("Reply by [DATE].", style="FirmBody")
    d.save(src)

    edited = h.load_document(input_path=str(src))
    h.replace_text_everywhere(edited, {"[DATE]": "1 March 2027"})
    out = tmp_path / "edited.docx"
    edited.save(out)

    p = docx.Document(out).paragraphs[0]
    assert p.text == "Reply by 1 March 2027."
    assert p.style.name == "FirmBody" and p.style.font.size == Pt(13)
