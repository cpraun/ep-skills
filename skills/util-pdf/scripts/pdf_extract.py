#!/usr/bin/env python3
"""
Extract text from a PDF with a location for every line, so that citations can
name page, line and (where present) paragraph number.

Uses the Poppler command-line tools (pdfinfo, pdftotext, pdftoppm) and, for
pages without a text layer, Tesseract OCR. Read-only: the PDF is never modified.

Output (text mode, default) — one line of the document per output line:

    === Page 3 of 12 (text) ===
    3:01 [0012]  The housing 10 is made of aluminium and ...
    3:02         carries a temperature sensor 12.

    <page>:<line> is the citation key. The paragraph tag (e.g. [0012]) is
    repeated on the line where it starts and left blank for continuation lines.

Usage:
    pdf_extract.py FILE.pdf                  # whole document
    pdf_extract.py FILE.pdf -p 3-5,9         # selected pages
    pdf_extract.py FILE.pdf --json           # machine-readable output
    pdf_extract.py FILE.pdf --ocr            # force OCR on every page
    pdf_extract.py FILE.pdf --lang deu+eng   # OCR languages (tesseract codes)
    pdf_extract.py FILE.pdf --info           # page count, metadata, text/scan status
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PARA_RE = re.compile(r"^\s*(\[\d{3,5}\]|\(\d{1,4}\)|\d{1,4}\.)\s+")
# Minimum number of word characters on a page for its text layer to be trusted.
MIN_TEXT_CHARS = 20


def run(cmd):
    return subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True).stdout


def require(tool, formula):
    if shutil.which(tool) is None:
        sys.exit(f"'{tool}' not found. Install it with: brew install {formula}")


def page_count(pdf):
    for line in run(["pdfinfo", str(pdf)]).splitlines():
        if line.startswith("Pages:"):
            return int(line.split()[1])
    sys.exit("pdfinfo did not report a page count")


def pdf_info(pdf):
    return run(["pdfinfo", str(pdf)])


def parse_pages(spec, n):
    if not spec:
        return list(range(1, n + 1))
    pages = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        lo, hi = int(a), int(b or a)
        pages.extend(range(lo, hi + 1))
    return [p for p in pages if 1 <= p <= n]


def text_layer(pdf, page):
    return run(["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(pdf), "-"])


def ocr_page(pdf, page, lang, dpi, tmp):
    require("tesseract", "tesseract")
    prefix = Path(tmp) / f"p{page}"
    run(["pdftoppm", "-r", str(dpi), "-f", str(page), "-l", str(page), "-gray", "-png", str(pdf), str(prefix)])
    png = next(Path(tmp).glob(f"p{page}-*.png"))
    return run(["tesseract", str(png), "-", "-l", lang, "--psm", "4"])


def split_lines(raw):
    """Non-empty lines; 'para' is the tag a line starts with, 'para_ctx' the
    most recent tag seen (the paragraph a continuation line belongs to)."""
    lines = []
    para = None
    for ln in raw.splitlines():
        if not ln.strip():
            continue
        m = PARA_RE.match(ln)
        if m:
            para = m.group(1)
        lines.append({"text": ln.rstrip(), "para": m.group(1) if m else None, "para_ctx": para})
    return lines


def extract(pdf, pages, force_ocr, lang, dpi):
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        for p in pages:
            raw = "" if force_ocr else text_layer(pdf, p)
            source = "text"
            if len(re.findall(r"\w", raw)) < MIN_TEXT_CHARS:
                raw = ocr_page(pdf, p, lang, dpi, tmp)
                source = "ocr"
            out.append({"page": p, "source": source, "lines": split_lines(raw)})
    return out


def render_text(pages, total):
    buf = []
    for pg in pages:
        buf.append(f"=== Page {pg['page']} of {total} ({pg['source']}) ===")
        for i, ln in enumerate(pg["lines"], 1):
            tag = f"{ln['para']:<8}" if ln["para"] else " " * 8
            buf.append(f"{pg['page']}:{i:02d} {tag}{ln['text']}")
        buf.append("")
    return "\n".join(buf)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("-p", "--pages", help="page selection, e.g. 1-3,7")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    ap.add_argument("--ocr", action="store_true", help="OCR every page, ignore the text layer")
    ap.add_argument("--lang", default="eng", help="tesseract language(s), e.g. eng, deu, deu+eng")
    ap.add_argument("--dpi", type=int, default=300, help="rasterisation resolution for OCR")
    ap.add_argument("--info", action="store_true", help="print pdfinfo and per-page text/scan status, then exit")
    a = ap.parse_args()

    require("pdfinfo", "poppler")
    if not a.pdf.is_file():
        sys.exit(f"not a file: {a.pdf}")

    n = page_count(a.pdf)
    pages = parse_pages(a.pages, n)

    if a.info:
        print(pdf_info(a.pdf).rstrip())
        scanned = [p for p in pages if len(re.findall(r"\w", text_layer(a.pdf, p))) < MIN_TEXT_CHARS]
        print(f"Pages without text layer (need OCR): {scanned or 'none'}")
        return

    result = extract(a.pdf, pages, a.ocr, a.lang, a.dpi)
    if a.json:
        json.dump({"file": str(a.pdf), "pages_total": n, "pages": result}, sys.stdout, ensure_ascii=False, indent=1)
    else:
        print(render_text(result, n))


if __name__ == "__main__":
    main()
