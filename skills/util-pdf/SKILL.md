---
name: util-pdf
description: >-
  Read PDF files, text-based or scanned (OCR), via local Homebrew tools, with page:line and paragraph locations for exact citations. Use only when the user refers to a PDF file (.pdf) or gives one as input, to read, quote or cite it. Read-only; never creates or edits PDFs.
---

# PDF reading with exact locations

<!-- protocol:begin -->
## Working protocol

- You draft; the attorney decides. Never go faster than the attorney can verify.
- State the assumptions that change the result (claim interpretation, D-document identity, effective date, applicable rule version) under "Assumptions:". Omit the heading if there are none.
- Do not fill gaps by guessing. Ask for the missing document or fact. Never invent prior art, claim text, passages, dates or citations.
- Do not agree by default. If an argument is weak, an amendment lacks basis, or a request is out of scope, say so and give the better option.
- Do only what this skill covers. Do not change files the task does not name.
- Write short sentences with direct verbs and no filler. Use one term for one concept throughout; never vary terms for style. Templates, quoted text and translations keep their own wording.
- This skill's output format takes precedence over this protocol.
<!-- protocol:end -->

Whenever a task involves a PDF, extract its text with `scripts/pdf_extract.py` and work from that output. Every line gets a location, so every quotation can cite page, line and paragraph. Do not read a PDF by other means (screenshots, `pdftotext` without page/line keys) when a citation may be needed.

The skill is read-only: it never creates, edits, merges, splits, fills or signs a PDF, and it does not handle password-protected PDFs — say so in one sentence if asked.

**Requirements** (macOS/Linux via Homebrew): `poppler` (`pdfinfo`, `pdftotext`, `pdftoppm`), `tesseract` plus `tesseract-lang` for non-English OCR, and `python3`. If a tool is missing, the script names the `brew install` command; tell the user rather than switching tools silently.

## Workflow

1. **Inspect:** `python3 <skill-dir>/scripts/pdf_extract.py FILE.pdf --info` — page count, metadata, and which pages have no text layer. For a large document, choose the pages to extract from this.
2. **Extract:**

   ```
   python3 <skill-dir>/scripts/pdf_extract.py FILE.pdf                 # whole document
   python3 <skill-dir>/scripts/pdf_extract.py FILE.pdf -p 3-7,12       # selected pages
   python3 <skill-dir>/scripts/pdf_extract.py FILE.pdf --lang deu+eng  # OCR language(s)
   python3 <skill-dir>/scripts/pdf_extract.py FILE.pdf --ocr           # force OCR (bad text layer)
   python3 <skill-dir>/scripts/pdf_extract.py FILE.pdf --json          # structured output
   ```

   Pages without a usable text layer are OCR'd automatically; the page header says `(text)` or `(ocr)`. For German or French documents pass `--lang deu` / `--lang fra` — the default English OCR garbles umlauts and accents. Save long extractions to a scratch file and read the relevant parts. If a page is `(ocr)`, read `references/ocr.md` in this skill's directory before quoting from it.

   ```
   === Page 3 of 12 (text) ===
   3:01 [0012]  [0012] The housing 10 is made of aluminium and
   3:02         carries a temperature sensor 12.
   ```

   `3:02` is PDF page 3, line 2 (blank lines not counted). The tag column shows the paragraph (`[0012]`, `(12)`) or claim number (`1.`) a line starts with; in `--json`, `para_ctx` gives the paragraph of each line. The text is verbatim.
3. **Cite** with the most specific location the document offers:
   1. **Paragraph number** where the document has them: `D1, [0012]`, or `D1, [0012], page 3, lines 1–2` for a spot in a long paragraph.
   2. **Page and line** otherwise: `D2, page 3, lines 1–2` — the printed page number if it differs from the PDF page and both are known (`page 7 (PDF p. 9)`); otherwise say it is the PDF page.
   3. **Column and line** for column-numbered documents: `col. 4, lines 12–18`.

   Quote the words relied on verbatim, in the original language. Never cite a location you have not seen in the extraction.
