# OpenXML markup and tracked changes

Part of the `util-docx` skill. Read this file when the task needs Word markup that python-docx has no API for, or tracked changes. Implementations are in `scripts/docx_helper.py`.

## OpenXML (`w:` namespace)

Manipulate the underlying `lxml` element (`_element`, `_p`, `_r`, `_tc`) with `docx.oxml.OxmlElement` and `docx.oxml.ns.qn`:

- **Cell shading:** `<w:shd w:val="clear" w:color="auto" w:fill="HEXCODE"/>` in `<w:tcPr>`.
- **Cell borders:** `<w:tcBorders>` in `<w:tcPr>`.
- **Keep with next / page break:** `<w:keepNext/>` or `<w:pageBreakBefore/>` in `<w:pPr>`.

## Tracked changes (revisions, redlines)

Wrap inserted runs in `<w:ins w:id="..." w:author="..." w:date="...">` and deleted text in `<w:del ...><w:r><w:delText>...</w:delText></w:r></w:del>`. Use the helpers rather than hand-built XML: `add_tracked_insertion` (append), `add_tracked_deletion` (first occurrence of a text, even across runs), and `add_tracked_replacement` (deletion immediately followed by insertion, as Word itself records a replacement). They give every revision a unique `w:id`, keep the formatting of the deleted runs, and give the inserted text the formatting of the text it replaces or follows. When the user asks for amendments to be shown as tracked changes (e.g. claim amendments with markup), never edit the text directly — record every change as a revision, so that accepting all changes yields the clean version and rejecting all yields the original. The helpers redline text in ordinary runs, including runs with tabs and line breaks, and number their revisions after all of Word's existing annotations. They refuse — return `None` / `False` and change nothing — when the text lies inside a hyperlink, inside an earlier tracked change, or in a run with a field, drawing or footnote reference; then tell the user which change could not be recorded and that it has to be made by hand in Word.

For verification, if `pandoc` is installed: `pandoc --track-changes=accept -t plain FILE` must show the revised text and `--track-changes=reject` the original.
