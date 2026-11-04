"""Tests of the util-docx helpers on a document authored and saved in Microsoft Word.

fixtures/test-sample.docx is a fictitious patent application saved by Word 16,
with tracked changes in the claims made the way Word records them: insertions,
deletions, a moved claim step (move ranges and a deleted paragraph mark), a
formatting change, plus a hyperlink and a table elsewhere. It tests what the
python-docx-built documents in the other suites cannot: Word's own markup.

- Reading: the text with all changes applied, checked against fixed expected claim
  wording and, where installed, against pandoc's independent reading.
- Writing: new redlines added on top of Word's existing ones remain valid —
  pandoc's accept view shows all changes, its reject view the original.

Manual check in Word (not automatable here): set UTIL_DOCX_OUTPUT_DIR to a folder,
run this file, and open the written `test-sample-amended.docx` in Word to confirm
the redlines display as Word's own.

Free and offline; requires python-docx (skipped otherwise).
"""

import os
import pathlib
import shutil
import subprocess
import sys
import zipfile

import pytest

from skilltest import skill_dir_for

docx = pytest.importorskip("docx")

SKILL_DIR = skill_dir_for(__file__)   # -> <repo>/skills/util-docx
sys.path.insert(0, str(SKILL_DIR / "scripts"))
import docx_helper as h  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "test-sample.docx"
PANDOC = shutil.which("pandoc")
needs_pandoc = pytest.mark.skipif(PANDOC is None, reason="pandoc not installed")

# The claims as they read with all tracked changes accepted.
ACCEPTED_CLAIM_1 = [
    "1.\tA computer-implemented method for balancing the processing load in a wireless sensor "
    "network (1) comprising a plurality of sensor nodes (10) and a gateway (20), the method comprising:",
    "(a)\teach sensor node (10) periodically determining a load value (L) indicative of its current "
    "processing utilisation;",
    "(b)\teach sensor node (10) transmitting the load value (L) to the gateway (20) via a wireless link;",
    "(c)\tthe gateway (20) comparing the load value (L) with a threshold value (T); and",
    "(d)\tthe gateway (20) reassigning at least one processing task from a sensor node (10) whose "
    "load value (L) exceeds the threshold value (T) to a neighbouring sensor node (10);",
    "characterised in that the threshold value (T) is adapted in dependence on the remaining battery "
    "capacity (B) of the sensor nodes (10).",
]
ACCEPTED_CLAIM_2 = ("2.\tThe method according to claim 1, wherein the threshold value (T) is reduced "
                    "as the remaining battery capacity (B) decreases.")


def _pandoc(path, mode):
    out = subprocess.run(
        [PANDOC, f"--track-changes={mode}", "-t", "plain", "--wrap=none", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    # Drop pandoc's plain-text table borders (lines of '-', '+', '|', '=').
    return " ".join(w for w in out.split() if w.strip("-+|=:"))


def _words(text):
    # Same normalisation as _pandoc: our table-cell separators ('|') are dropped too.
    return " ".join(w for w in text.split() if w.strip("-+|=:"))


def _lines():
    return h.read_text_with_changes_applied(docx.Document(FIXTURE)).split("\n")


def _claims_block(lines):
    start = lines.index("Claims") + 1
    return lines[start:lines.index("Abstract")]


# --- The fixture is what it claims to be ---------------------------------------

def test_fixture_was_saved_by_word_and_carries_its_markup():
    with zipfile.ZipFile(FIXTURE) as z:
        assert "Microsoft" in z.read("docProps/app.xml").decode()
        xml = z.read("word/document.xml").decode()
    for tag in ("w:ins", "w:del", "w:delText", "w:moveFrom", "w:moveTo",
                "w:moveFromRangeStart", "w:rPrChange", "w:hyperlink", "w:tbl"):
        assert f"<{tag}" in xml, f"fixture no longer contains <{tag}>"


# --- Reading ---------------------------------------------------------------------

def test_tracked_changes_are_detected():
    assert h.has_tracked_changes(docx.Document(FIXTURE))


def test_claims_read_with_all_changes_applied():
    claims = _claims_block(_lines())
    assert claims[:6] == ACCEPTED_CLAIM_1
    assert claims[6] == ACCEPTED_CLAIM_2


def test_moved_step_leaves_no_empty_line():
    # Step (b) was moved by Word; its old position has a deleted paragraph mark
    # and must merge away, not leave an empty line.
    assert "" not in _claims_block(_lines())


def test_python_docx_paragraph_text_misses_the_amendments():
    # Why the skill must not read with paragraph.text: on Word's markup it drops
    # inserted text, e.g. "…is adapted ." instead of the amended clause.
    texts = [p.text for p in docx.Document(FIXTURE).paragraphs]
    assert "characterised in that the threshold value (T) is adapted ." in texts
    assert ACCEPTED_CLAIM_1[5] not in texts


@needs_pandoc
def test_reader_agrees_with_pandoc_on_the_whole_document():
    assert _words("\n".join(_lines())) == _pandoc(FIXTURE, "accept")


# --- Writing on top of Word's markup ---------------------------------------------

def _amend(tmp_path):
    d = docx.Document(FIXTURE)
    claim3 = next(p for p in d.paragraphs if h.accepted_text(p).startswith("3.\t"))
    assert h.add_tracked_replacement(claim3, "between 1 s and 60 s", "between 5 s and 30 s",
                                     author="Test")
    out = tmp_path / "test-sample-amended.docx"
    d.save(out)
    return out


def test_new_redline_ids_do_not_clash_with_words(tmp_path):
    out = _amend(tmp_path)
    with zipfile.ZipFile(out) as z:
        root = docx.oxml.parse_xml(z.read("word/document.xml"))
    revision_tags = {f"{W}{t}" for t in ("ins", "del", "moveFrom", "moveTo", "rPrChange", "pPrChange")}
    ids = [e.get(f"{W}id") for e in root.iter() if e.tag in revision_tags]
    assert len(ids) == len(set(ids)), "revision ids must be unique across Word's and ours"


def test_new_redline_reads_as_amended(tmp_path):
    out = _amend(tmp_path)
    claims = _claims_block(h.read_text_with_changes_applied(docx.Document(out)).split("\n"))
    assert claims[7] == ("3.\tThe method according to claim 1 or 2, wherein the load value (L) is "
                         "transmitted at a transmission interval (Δt) of between 5 s and 30 s.")
    assert claims[:6] == ACCEPTED_CLAIM_1, "Word's earlier changes must be unaffected"


@needs_pandoc
def test_pandoc_accept_and_reject_after_adding_redlines(tmp_path):
    out = _amend(tmp_path)
    accepted, rejected = _pandoc(out, "accept"), _pandoc(out, "reject")
    assert "between 5 s and 30 s" in accepted and "between 1 s and 60 s" not in accepted
    assert "via a wireless link" in accepted                      # Word's change still accepted
    assert rejected == _pandoc(FIXTURE, "reject")                 # rejecting all = the original


def test_search_does_not_match_across_a_hyperlink():
    # [0003] reads "…searched via <hyperlink>Espacenet</hyperlink>) discloses…".
    d = docx.Document(FIXTURE)
    p = next(p for p in d.paragraphs if h.accepted_text(p).startswith("[0003]"))
    before = p._p.xml
    assert h.add_tracked_deletion(p, "via ) discloses") is None
    assert h.add_tracked_deletion(p, "Espacenet") is None   # inside the hyperlink: not supported
    assert p._p.xml == before


def test_write_amended_copy_for_manual_check_in_word(tmp_path):
    target = os.environ.get("UTIL_DOCX_OUTPUT_DIR")
    if not target:
        pytest.skip("set UTIL_DOCX_OUTPUT_DIR to write a copy for opening in Word")
    out = _amend(tmp_path)
    dest = pathlib.Path(target) / out.name
    shutil.copy(out, dest)
    print(f"\nWritten for manual check in Word: {dest}")


def test_redline_spanning_a_tab_in_a_word_run(tmp_path):
    # Word keeps "<tab>A gateway…" in one run after "4."; the redline must split it.
    d = docx.Document(FIXTURE)
    claim4 = next(p for p in d.paragraphs if h.accepted_text(p).startswith("4.\t"))
    assert h.add_tracked_replacement(claim4, "4.\tA gateway", "4.\tAn edge gateway")
    out = tmp_path / "tab.docx"
    d.save(out)
    claim4 = next(p for p in docx.Document(out).paragraphs if h.accepted_text(p).startswith("4."))
    assert h.accepted_text(claim4).startswith("4.\tAn edge gateway (20) for a wireless sensor network")
    if PANDOC:
        assert _pandoc(out, "reject") == _pandoc(FIXTURE, "reject")
