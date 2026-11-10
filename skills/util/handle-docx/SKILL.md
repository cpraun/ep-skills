---
name: handle-docx
description: >-
  Read, create, edit and format Word (.docx) files while preserving fonts, styles, tracked changes and OpenXML markup; uses your template.docx or a sample. Use only when the user refers to a Word file (.docx) or gives one as input, or asks for a Word file as output.
---
# Docx

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

Create and edit Word (`.docx`) files with `python-docx` and `lxml`, preserving fonts, run formatting, structure and OpenXML (`w:`) markup. Helpers are in `scripts/docx_helper.py`.

**The original file's formatting governs.** When changing a Word file, or creating one from another Word file, keep its styles, fonts, numbering, margins, headers and footers. Format every addition like the surrounding text (same paragraph style, same run formatting), remove only the content concerned, and never restyle or "clean up" parts the task does not concern.

## Opening a document

- **Editing an existing file:** `docx.Document(input_path)`.
- **New file based on another Word file:** load that file, not the template, and save under a new name.
- **New file from scratch:** use, in this order, a template path from the user; `assets/template.docx` (the user's own template, git-ignored); `assets/template-sample.docx`. `load_document()` implements this order. If `template.docx` is missing, say once that the sample was used and that a customised template can be added (see `assets/CUSTOMIZE.txt`).

## Editing

- **Never assign `paragraph.text`** on formatted paragraphs: it destroys the runs and their formatting. Replace text inside `run.text`; for text spanning several runs, use `replace_text_in_paragraph`.
- Traverse body paragraphs, table cells (including nested tables) and every section's headers and footers.
- Use named styles (`style="Heading 1"`) rather than direct formatting, if the style exists (check `[s.name for s in doc.styles]`; otherwise fall back to `"Normal"`). To copy a run's formatting, deep-copy its `<w:rPr>`.
- A header with `is_linked_to_previous = True` also changes earlier sections; unlink it to target one section.
- For cell shading, borders, keep-with-next or page breaks, and for **any tracked change** (e.g., claim amendments shown with markup), read `references/openxml-and-tracked-changes.md`.

## Reading

Report the text **with all tracked changes applied** (insertions in, deletions out): use `read_text_with_changes_applied(doc)` or `accepted_text(paragraph)`, never `paragraph.text`, which drops inserted text. If `has_tracked_changes(doc)` is true, say so once. If the user asks for the original version or the changes themselves, report those instead.

## Saving and verifying

Save to a new or temporary path before overwriting an original. Then re-open the saved file, and check the target strings and the paragraph and table counts with `read_text_with_changes_applied`.
