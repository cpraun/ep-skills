"""Deterministic tests for the read-pdf skill's extractor (no model call).

Runs skills/util/read-pdf/scripts/pdf_extract.py on the fictitious fixtures in
fixtures/ — the same two-page document as a text PDF, as a scanned (image-only)
PDF, and mixed (page 1 text, page 2 scanned) — and checks the guarantees the
skill's citations rest on:

- every line carries a page:line key, counted per page, blank lines excluded;
- paragraph tags ([0010]) and claim numbers (1.) are recognised, and
  continuation lines are attributed to their paragraph (`para_ctx`);
- pages without a text layer are OCR'd automatically, and OCR yields the same
  text as the text layer (up to dash variants);
- page selection, --info, --json and --ocr behave as documented.

Requires poppler (pdfinfo, pdftotext, pdftoppm); OCR tests also need tesseract.
Skipped where the tools are missing.
"""

import json
import pathlib
import shutil
import subprocess
import sys

import pytest

from skilltest import skill_dir_for

SKILL_DIR = skill_dir_for(__file__)   # -> <repo>/skills/util/read-pdf
SCRIPT = SKILL_DIR / "scripts" / "pdf_extract.py"
FIX = pathlib.Path(__file__).parent / "fixtures"
TEXT, SCANNED, MIXED = FIX / "text.pdf", FIX / "scanned.pdf", FIX / "mixed.pdf"

pytestmark = pytest.mark.skipif(shutil.which("pdftotext") is None, reason="poppler not installed")
needs_ocr = pytest.mark.skipif(shutil.which("tesseract") is None, reason="tesseract not installed")


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                          check=True, capture_output=True, text=True).stdout


def as_json(pdf, *args):
    return json.loads(run(pdf, "--json", *args))


def lines_of(doc, page):
    return [ln["text"] for ln in doc["pages"][page - 1]["lines"]]


def dashes(text):
    return text.replace("—", "–")


# --- Text layer: locations ------------------------------------------------------

def test_page_line_keys_are_per_page_and_skip_blank_lines():
    out = run(TEXT).splitlines()
    assert out[0] == "=== Page 1 of 2 (text) ==="
    assert out[1].startswith("1:01 ")
    assert "=== Page 2 of 2 (text) ===" in out
    assert out[out.index("=== Page 2 of 2 (text) ===") + 1].startswith("2:01 ")
    # Page 1 has 9 drawn lines, 2 of them blank -> 7 numbered lines.
    assert len(as_json(TEXT)["pages"][0]["lines"]) == 7


def test_line_text_is_verbatim_including_curly_quotes_and_hyphenation():
    p1 = lines_of(as_json(TEXT), 1)
    assert p1[3] == "(6). The term “closure member” denotes any element com-"
    assert p1[4] == "prising a sealing surface."


def test_paragraph_tags_and_continuation_lines():
    doc = as_json(TEXT)
    p1 = doc["pages"][0]["lines"]
    assert p1[1]["para"] == "[0010]"
    assert p1[2]["para"] is None and p1[2]["para_ctx"] == "[0010]"
    assert p1[5]["para"] == "[0011]"


def test_claim_numbers_are_tagged():
    p2 = as_json(TEXT)["pages"][1]["lines"]
    tags = [ln["para"] for ln in p2]
    assert "1." in tags and "2." in tags
    claim2 = next(ln for ln in p2 if ln["para"] == "2.")
    assert claim2["text"].startswith("2. The valve assembly according to claim 1")


def test_text_format_shows_tag_column():
    out = run(TEXT)
    assert "1:02 [0010]  [0010] A valve assembly" in out
    assert "1:03         closure member (4)" in out


# --- Page selection, info, JSON ---------------------------------------------------

def test_page_selection():
    doc = as_json(TEXT, "-p", "2")
    assert [pg["page"] for pg in doc["pages"]] == [2]
    assert doc["pages_total"] == 2
    assert [pg["page"] for pg in as_json(TEXT, "-p", "1-2")["pages"]] == [1, 2]


def test_info_reports_pages_needing_ocr():
    assert run(TEXT, "--info").strip().endswith("Pages without text layer (need OCR): none")
    assert run(MIXED, "--info").strip().endswith("Pages without text layer (need OCR): [2]")
    assert run(SCANNED, "--info").strip().endswith("Pages without text layer (need OCR): [1, 2]")


def test_json_structure():
    doc = as_json(TEXT)
    assert set(doc) == {"file", "pages_total", "pages"}
    pg = doc["pages"][0]
    assert set(pg) == {"page", "source", "lines"} and pg["source"] == "text"
    assert set(pg["lines"][0]) == {"text", "para", "para_ctx"}


# --- OCR ------------------------------------------------------------------------

@needs_ocr
def test_scanned_pdf_is_ocrd_with_same_text_and_locations():
    text, scanned = as_json(TEXT), as_json(SCANNED)
    assert [pg["source"] for pg in scanned["pages"]] == ["ocr", "ocr"]
    for page in (1, 2):
        assert [dashes(t) for t in lines_of(scanned, page)] == [dashes(t) for t in lines_of(text, page)]
    assert scanned["pages"][0]["lines"][1]["para"] == "[0010]"


@needs_ocr
def test_mixed_pdf_uses_text_layer_and_ocr_per_page():
    doc = as_json(MIXED)
    assert [pg["source"] for pg in doc["pages"]] == ["text", "ocr"]
    assert lines_of(doc, 2) == lines_of(as_json(TEXT), 2)


@needs_ocr
def test_forced_ocr_on_a_text_pdf():
    doc = as_json(TEXT, "--ocr", "-p", "2")
    assert doc["pages"][0]["source"] == "ocr"
    assert lines_of(doc, 1) == lines_of(as_json(TEXT, "-p", "2"), 1)
