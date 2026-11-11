---
trigger: always_on
description: Tool use without consent prompts for pdf and docx, and the location of temporary files, for the EP skills library in Antigravity.
---
# EP Skills — tools and temporary files (Antigravity)

## Tools of `read-pdf` and `handle-docx`

These tools are part of the normal operation of the EP skills library. Run them without asking the user for consent first:

- **`read-pdf`:** `python3 <skill-dir>/scripts/pdf_extract.py …` and the tools it calls — `pdfinfo`, `pdftotext`, `pdftoppm` (poppler) and `tesseract`.
- **`handle-docx`:** `python3` with `python-docx` and `lxml`, including scripts that import `<skill-dir>/scripts/docx_helper.py`.

This does not extend to installing software, network access, or deleting or overwriting case files. Ask for those as usual.

## Personal files

Reading and writing inside `~/.ep-skills/` (learned rules in `learned/`, the user's Word template `template.docx`) is always allowed. Do not ask for confirmation.

## Temporary files

- Store every temporary file — PDF extractions, rendered page images, intermediate copies of Word files, helper scripts — in the folder `.antigravity_tmp/` at the root of the project directory. Create the folder if it does not exist.
- Never write temporary files elsewhere: not to `/tmp`, the home directory or the skill directories.
- Reading and writing inside `.antigravity_tmp/` is always allowed. Do not ask for confirmation.
- Deliverables do not belong in `.antigravity_tmp/`; save them where the skill says.
- `.antigravity_tmp/` may contain confidential case material: keep it inside the project and never commit it.
