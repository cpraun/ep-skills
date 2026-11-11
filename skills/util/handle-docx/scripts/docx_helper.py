"""
Helper utilities for creating and modifying Microsoft Word (.docx) files
while preserving run-level formatting, styles, and OpenXML (w:) markup.
"""

import copy
import os
from datetime import datetime, timezone
import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
# The user's own template lives outside the plugin folder, so a plugin update keeps it.
USER_TEMPLATE = os.path.join(os.path.expanduser("~"), ".ep-skills", "template.docx")


def load_document(input_path=None, user_template=USER_TEMPLATE, template_dir=ASSETS_DIR):
    """
    Loads an existing Word document, falls back to the user's own template
    (~/.ep-skills/template.docx), else to the shipped template-sample.docx, or
    initializes a blank document.
    """
    if input_path and os.path.exists(input_path):
        return docx.Document(input_path)

    for template in (user_template, os.path.join(template_dir, "template-sample.docx")):
        if os.path.exists(template):
            return docx.Document(template)

    return docx.Document()


def copy_run_formatting(source_run, target_run):
    """
    Copies the exact OpenXML <w:rPr> formatting block (font name, size, color,
    bold, italic, underline, highlight, etc.) from source_run to target_run.
    """
    if source_run._r.rPr is not None:
        target_rPr = target_run._r.get_or_add_rPr()
        target_run._r.remove(target_rPr)
        target_run._r.insert(0, copy.deepcopy(source_run._r.rPr))


def replace_text_in_paragraph(paragraph, old_text, new_text):
    """
    Replaces `old_text` with `new_text` inside a paragraph while preserving
    run-level font and formatting properties—even when `old_text` is split
    across multiple XML <w:r> runs by Word's spellchecker or revision history.
    """
    if old_text not in paragraph.text:
        return False

    # Fast path: check if old_text exists completely inside single runs
    replaced_in_single = False
    for run in paragraph.runs:
        if old_text in run.text:
            run.text = run.text.replace(old_text, new_text)
            replaced_in_single = True

    if replaced_in_single and old_text not in paragraph.text:
        return True

    # Cross-run replacement: map character indices to (run_index, char_index_in_run)
    while old_text in paragraph.text:
        runs = paragraph.runs
        char_map = []
        for r_idx, run in enumerate(runs):
            for c_idx in range(len(run.text)):
                char_map.append((r_idx, c_idx))

        full_text = paragraph.text
        start_pos = full_text.find(old_text)
        if start_pos == -1:
            break
        end_pos = start_pos + len(old_text) - 1

        start_run_idx, start_char_idx = char_map[start_pos]
        end_run_idx, end_char_idx = char_map[end_pos]

        if start_run_idx == end_run_idx:
            run = runs[start_run_idx]
            run.text = run.text[:start_char_idx] + new_text + run.text[end_char_idx + 1:]
        else:
            # Place prefix + replacement into the starting run (preserving its formatting)
            first_run = runs[start_run_idx]
            last_run = runs[end_run_idx]

            prefix = first_run.text[:start_char_idx]
            suffix = last_run.text[end_char_idx + 1:]

            first_run.text = prefix + new_text
            for r_idx in range(start_run_idx + 1, end_run_idx):
                runs[r_idx].text = ""
            last_run.text = suffix

    return True


def iter_all_paragraphs(doc):
    """
    Yields every paragraph in the document: body, nested tables, headers, and footers.
    """
    for p in doc.paragraphs:
        yield p

    def _iter_tables(tables):
        for table in tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        yield p
                    yield from _iter_tables(cell.tables)

    yield from _iter_tables(doc.tables)

    for section in doc.sections:
        for container in (
            section.header,
            section.first_page_header,
            section.even_page_header,
            section.footer,
            section.first_page_footer,
            section.even_page_footer,
        ):
            if container is not None:
                for p in container.paragraphs:
                    yield p
                yield from _iter_tables(container.tables)


def replace_text_everywhere(doc, replacements: dict):
    """
    Replaces all key->value pairs in `replacements` across body, tables,
    headers, and footers while preserving formatting.
    """
    count = 0
    for paragraph in iter_all_paragraphs(doc):
        for old_text, new_text in replacements.items():
            if replace_text_in_paragraph(paragraph, old_text, new_text):
                count += 1
    return count


def set_cell_shading(cell, fill_hex: str):
    """
    Applies a background fill color (e.g. 'D9E1F2') to a Word table cell using OpenXML <w:shd>.
    """
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex.lstrip("#"))
    tcPr.append(shd)


def _next_rev_id(element):
    """A revision id not yet used in the document part. Word numbers all
    annotations (insertions, deletions, moves, move ranges, formatting changes,
    bookmarks, comments) from one pool, so every w:id in the part is considered."""
    root = element.getroottree().getroot()
    ids = [int(v) for e in root.iter() if (v := e.get(qn("w:id")) or "").isdigit()]
    return max(ids, default=0) + 1


def _revision(tag, author, rev_id, element):
    rev = OxmlElement(tag)
    rev.set(qn("w:id"), str(rev_id if rev_id is not None else _next_rev_id(element)))
    rev.set(qn("w:author"), author)
    rev.set(qn("w:date"), datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    return rev


def add_tracked_insertion(paragraph, text: str, author: str = "AI Editor", rev_id: int = None):
    """
    Appends text to a paragraph wrapped in an OpenXML <w:ins> Track Changes revision tag.
    """
    ins = _revision("w:ins", author, rev_id, paragraph._p)

    run_el = OxmlElement("w:r")
    # Inherit formatting from the last run in the paragraph if present
    if paragraph.runs and paragraph.runs[-1]._r.rPr is not None:
        run_el.append(copy.deepcopy(paragraph.runs[-1]._r.rPr))

    text_el = OxmlElement("w:t")
    if text.startswith(" ") or text.endswith(" "):
        text_el.set(qn("xml:space"), "preserve")
    text_el.text = text

    run_el.append(text_el)
    ins.append(run_el)
    paragraph._p.append(ins)


# Run content that is plain text for splitting: <w:t> (its characters), tabs and
# breaks (one character each, as in accepted_text), and Word's zero-width marker.
_CHAR_TAGS = {qn("w:tab"): "\t", qn("w:br"): "\n", qn("w:cr"): "\n"}
_ZERO_WIDTH = {qn("w:lastRenderedPageBreak"), qn("w:rPr")}


def _run_text(r):
    return "".join((c.text or "") if c.tag == qn("w:t") else _CHAR_TAGS.get(c.tag, "") for c in r)


def _run_splittable(r):
    """True if a <w:r> holds only text, tabs and breaks (no fields, drawings, notes)."""
    return all(c.tag == qn("w:t") or c.tag in _CHAR_TAGS or c.tag in _ZERO_WIDTH for c in r)


def _split_run(r, offset):
    """Split a splittable <w:r> at character `offset`; both halves keep the run
    formatting. Returns the second half (inserted right after `r`)."""
    tail = copy.deepcopy(r)
    head_items, tail_items, pos = [], [], 0
    for c in [c for c in r if c.tag != qn("w:rPr")]:
        text = (c.text or "") if c.tag == qn("w:t") else _CHAR_TAGS.get(c.tag, "")
        if pos + len(text) <= offset:
            head_items.append(c)
        elif pos >= offset:
            tail_items.append(c)
        else:   # a <w:t> straddling the split point
            cut = offset - pos
            first, second = copy.deepcopy(c), copy.deepcopy(c)
            first.text, second.text = text[:cut], text[cut:]
            for t in (first, second):
                t.set(qn("xml:space"), "preserve")
            head_items.append(first)
            tail_items.append(second)
        pos += len(text)
    for el, items in ((r, head_items), (tail, tail_items)):
        for c in [c for c in el if c.tag != qn("w:rPr")]:
            el.remove(c)
        for c in items:
            el.append(copy.deepcopy(c))
    r.addnext(tail)
    return tail


def _isolate_runs(paragraph, old_text):
    """The direct <w:r> elements of `paragraph` that hold exactly the first
    occurrence of `old_text`, splitting runs at its boundaries. None if not found
    or if the range touches a run with fields, drawings or notes, or text inside
    another element (hyperlink, earlier tracked change, content control)."""
    children = list(paragraph._p)
    texts = []
    for c in children:
        if c.tag == qn("w:r"):
            texts.append(_run_text(c))
        else:
            # Hyperlinks, earlier revisions etc. count with their visible text, so
            # a search cannot match across them, but they are never split.
            texts.append("".join(t.text or "" for t in c.iter(qn("w:t"))
                                 if not any(a.tag in _REMOVED for a in t.iterancestors())))
    start = "".join(texts).find(old_text)
    if start < 0 or not old_text:
        return None
    end, pos, selected = start + len(old_text), 0, []
    for r, text in zip(children, texts):
        r_start, r_end = pos, pos + len(text)
        pos = r_end
        if r_end <= start or r_start >= end:
            continue
        if r.tag != qn("w:r") or not _run_splittable(r):
            return None
        if start > r_start:
            r = _split_run(r, start - r_start)
            r_start = start
        if end < r_end:
            _split_run(r, end - r_start)
        selected.append(r)
    return selected


def add_tracked_deletion(paragraph, old_text: str, author: str = "AI Editor", rev_id: int = None):
    """
    Marks the first occurrence of `old_text` in a paragraph as a tracked deletion
    (<w:del> with <w:delText>), keeping the formatting of the deleted runs.
    Returns the <w:del> element, or None if the text was not found.
    """
    runs = _isolate_runs(paragraph, old_text)
    if not runs:
        return None
    dele = _revision("w:del", author, rev_id, paragraph._p)
    runs[0].addprevious(dele)
    for r in runs:
        for t in r.findall(qn("w:t")):
            t.tag = qn("w:delText")
            t.set(qn("xml:space"), "preserve")
        dele.append(r)
    return dele


def add_tracked_replacement(paragraph, old_text: str, new_text: str, author: str = "AI Editor"):
    """
    Redlines `old_text` -> `new_text` as Word does: a tracked deletion of the old
    text immediately followed by a tracked insertion of the new text, which takes
    the formatting of the first deleted run. Returns True if performed.
    """
    dele = add_tracked_deletion(paragraph, old_text, author)
    if dele is None:
        return False
    ins = _revision("w:ins", author, None, paragraph._p)
    run_el = OxmlElement("w:r")
    rpr = dele.find(f"{qn('w:r')}/{qn('w:rPr')}")
    if rpr is not None:
        run_el.append(copy.deepcopy(rpr))
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = new_text
    run_el.append(t)
    ins.append(run_el)
    dele.addnext(ins)
    return True


_REMOVED = (qn("w:del"), qn("w:moveFrom"))


def accepted_text(paragraph):
    """
    The paragraph's text with all tracked changes applied: inserted and moved-to
    text included, deleted and moved-from text left out.

    Use this instead of `paragraph.text`, which in python-docx ignores text inside
    <w:ins> and so shows neither the original nor the revised version.
    """
    out = []
    for el in paragraph._p.iter(qn("w:t"), qn("w:tab"), qn("w:br"), qn("w:cr")):
        if any(a.tag in _REMOVED for a in el.iterancestors()):
            continue
        if el.tag == qn("w:t"):
            out.append(el.text or "")
        elif el.tag == qn("w:tab"):
            out.append("\t")
        else:
            out.append("\n")
    return "".join(out)


def has_tracked_changes(doc):
    """True if the document body contains tracked insertions, deletions or moves."""
    body = doc.element.body
    return any(True for _ in body.iter(qn("w:ins"), qn("w:del"), qn("w:moveFrom"), qn("w:moveTo")))


def _mark_removed(paragraph):
    """True if the paragraph mark itself is a tracked deletion or move-away, so that
    on acceptance the paragraph merges with the following one."""
    rpr = paragraph._p.find(f"{qn('w:pPr')}/{qn('w:rPr')}")
    return rpr is not None and any(c.tag in _REMOVED for c in rpr)


def read_text_with_changes_applied(doc):
    """
    The body text of a document, in reading order (paragraphs and tables), with
    all tracked changes applied — what the reader of the revised document sees.
    One line per paragraph; table cells separated by ' | '. A paragraph whose
    paragraph mark is deleted is joined with the next paragraph, as Word does.
    """
    lines, pending = [], ""
    for block in doc.iter_inner_content():
        if hasattr(block, "rows"):
            if pending:
                lines.append(pending)
                pending = ""
            for row in block.rows:
                lines.append(" | ".join(
                    "\n".join(accepted_text(p) for p in cell.paragraphs) for cell in row.cells))
        elif _mark_removed(block):
            pending += accepted_text(block)
        else:
            lines.append(pending + accepted_text(block))
            pending = ""
    if pending:
        lines.append(pending)
    return "\n".join(lines)
