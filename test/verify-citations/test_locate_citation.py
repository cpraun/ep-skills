"""Deterministic tests for the verify-citations skill's locator (no model call).

Runs skills/misc/verify-citations/scripts/locate_citation.py on every citation listed
in cases/*/citations.yaml, against the source documents in that case's sources/
folder, and checks the reported status (and, where given, where the quote was
actually found). See cases/README.md for how to add your own case with your own
PDF and Word documents.

Requires poppler (and tesseract for scanned PDFs) and python-docx; entries whose
tools are missing are skipped.
"""

import functools
import pathlib
import shutil
import sys

import pytest
import yaml

from skilltest import skill_dir_for

SKILL_DIR = skill_dir_for(__file__)   # -> <repo>/skills/misc/verify-citations
sys.path.insert(0, str(SKILL_DIR / "scripts"))
import locate_citation as lc  # noqa: E402

CASES_DIR = pathlib.Path(__file__).parent / "cases"


def _entries():
    for case in sorted(p for p in CASES_DIR.iterdir() if (p / "citations.yaml").is_file()):
        for entry in yaml.safe_load((case / "citations.yaml").read_text(encoding="utf-8")) or []:
            yield pytest.param(case, entry, id=f"{case.name}/{entry['id']}")


@functools.lru_cache(maxsize=None)
def _segments(path, lang):
    # Read each source once per test run (OCR is slow).
    return lc.read_segments(path, lang)


def _skip_if_tools_missing(source):
    suffix = source.suffix.lower()
    if suffix == ".pdf" and shutil.which("pdftotext") is None:
        pytest.skip("poppler not installed")
    if suffix == ".docx":
        pytest.importorskip("docx")


@pytest.mark.parametrize("case, entry", list(_entries()))
def test_citation(case, entry):
    source = case / "sources" / entry["source"]
    assert source.is_file(), f"source not found: {source}"
    _skip_if_tools_missing(source)
    lang = entry.get("lang", "eng")
    try:
        segs = _segments(source, lang)
    except SystemExit as e:          # pdf_extract exits with an install hint
        pytest.skip(str(e))
    result = lc.locate(source, entry["quote"], entry.get("cited"), lang, segs=segs)

    detail = f"\n  quote: {entry['quote']!r}\n  result: {result}"
    assert result["status"] == entry["expect"], f"status {result['status']!r}, expected {entry['expect']!r}{detail}"
    if "found_at" in entry:
        want = entry["found_at"]
        assert any(all(f.get(k) == v for k, v in want.items()) for f in result["found"]), (
            f"not found at {want}{detail}")
