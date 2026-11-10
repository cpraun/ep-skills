#!/usr/bin/env python3
"""
Locate a quoted passage in a source document and check it against the location
the draft cites for it.

Sources are read with the library's own readers, so locations are exact:
- PDF  -> read-pdf (page:line, paragraph tags; OCR for scanned pages)
- DOCX -> handle-docx (text with tracked changes applied; one line per paragraph)
- TXT / MD -> one line per line

Result `status`:
    verbatim           the quote is in the source, at the cited location
    minor-divergence   only punctuation / case / spacing differ, at the cited location
    ellipsis           all fragments around an ellipsis ("...", "…", "[...]") appear
                       in order at the cited location — whether the omission changes
                       the meaning is for the reader to judge
    wrong-location     the text is in the source, but not at the cited location
    not-found          the text is not in the source; `closest` gives the most
                       similar passage and its similarity (0–1)

Usage:
    locate_citation.py SOURCE --quote "..." [--para "[0034]" | --claim 3 | --page 7 [--lines 12-14]]
                       [--lang deu]
Prints JSON.
"""

import argparse
import difflib
import json
import pathlib
import re
import sys

SKILLS_DIR = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SKILLS_DIR / "util" / "read-pdf" / "scripts"))
sys.path.insert(0, str(SKILLS_DIR / "util" / "handle-docx" / "scripts"))

PARA_RE = re.compile(r"^\s*(\[\d{1,5}\]|\(\d{1,4}\)|\d{1,4}\.)\s+")
ELLIPSIS_RE = re.compile(r"\s*(?:\[\s*(?:\.\.\.|…)\s*\]|\.\.\.|…)\s*")
CHAR_MAP = {
    "‘": "'", "’": "'", "‚": "'", "′": "'",
    "“": '"', "”": '"', "„": '"', "«": '"', "»": '"',
    "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-", "−": "-",
    " ": " ", " ": " ", " ": " ", "\t": " ",
    "ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl",
    "­": "",
}
# Ellipsis fragments must lie within this many characters of each other.
MAX_ELLIPSIS_SPAN = 3000


# --- Reading sources into located lines ---------------------------------------

def _tag_kind(tag):
    """('para', 34) for [0034] / (34); ('claim', 3) for '3.'; None otherwise."""
    if not tag:
        return None
    n = int(re.sub(r"\D", "", tag))
    return ("claim", n) if tag.endswith(".") else ("para", n)


def read_segments(path, lang="eng"):
    """Lines of a source as dicts: text, page (PDF only), line, para (tag the line
    belongs to, as ('para'|'claim', n))."""
    path = pathlib.Path(path)
    suffix = path.suffix.lower()
    segs = []
    if suffix == ".pdf":
        import pdf_extract
        pdf_extract.require("pdfinfo", "poppler")
        pages = pdf_extract.extract(path, range(1, pdf_extract.page_count(path) + 1),
                                    False, lang, 300)
        ctx = None
        for pg in pages:
            for i, ln in enumerate(pg["lines"], 1):
                ctx = ln["para"] or ln["para_ctx"] or ctx   # carry paragraphs across pages
                segs.append({"text": ln["text"], "page": pg["page"], "line": i,
                             "para": _tag_kind(ctx)})
    elif suffix == ".docx":
        import docx
        import docx_helper
        text = docx_helper.read_text_with_changes_applied(docx.Document(path))
        segs = _lines_to_segments(text.split("\n"))
    else:
        segs = _lines_to_segments(path.read_text(encoding="utf-8").split("\n"))
    return segs


def _lines_to_segments(lines):
    segs, ctx = [], None
    for i, text in enumerate(lines, 1):
        m = PARA_RE.match(text)
        if m:
            ctx = m.group(1)
        segs.append({"text": text, "page": None, "line": i, "para": _tag_kind(ctx)})
    return segs


# --- Normalisation with a map back to the source lines ------------------------

def _normalise(segs, loose=False):
    """(normalised text, list mapping each character to its segment index).
    Strict: unify quotes, dashes, spaces and ligatures; join words hyphenated at
    a line end; collapse whitespace. Loose additionally: lower case, punctuation
    removed."""
    chars = []
    for i, s in enumerate(segs):
        for ch in s["text"]:
            for c in CHAR_MAP.get(ch, ch):
                chars.append((c, i))
        chars.append(("\n", i))
    # join "compri-\nsing" -> "comprising"
    out = []
    k = 0
    while k < len(chars):
        c, i = chars[k]
        if (c == "-" and k + 1 < len(chars) and chars[k + 1][0] == "\n" and out
                and out[-1][0].isalpha() and k + 2 < len(chars) and chars[k + 2][0].islower()):
            k += 2
            continue
        out.append((c, i))
        k += 1
    if loose:
        out = [(c.lower(), i) if c.isalnum() else (" ", i) for c, i in out]
    text, index = [], []
    for c, i in out:
        if c.isspace():
            if text and text[-1] == " ":
                continue
            c = " "
        text.append(c)
        index.append(i)
    return "".join(text), index


def _norm_quote(quote, loose=False):
    text, _ = _normalise([{"text": quote}], loose)
    return text.strip()


def _find_all(hay, needle):
    found, start = [], hay.find(needle)
    while needle and start >= 0:
        found.append((start, start + len(needle)))
        start = hay.find(needle, start + 1)
    return found


# --- Locations -----------------------------------------------------------------

def _location(segs, index, start, end):
    first, last = segs[index[start]], segs[index[max(start, end - 1)]]
    loc = {"line_start": first["line"], "line_end": last["line"]}
    if first["page"] is not None:
        loc["page"] = first["page"]
        if last["page"] != first["page"]:
            loc["page_end"] = last["page"]
    if first["para"]:
        kind, n = first["para"]
        loc["claim" if kind == "claim" else "para"] = n
    loc["text"] = " ".join(s["text"].strip() for s in segs[index[start]:index[max(start, end - 1)] + 1])
    return loc


def _at_cited(segs, index, start, end, cited):
    """True if the span [start, end) overlaps the cited location."""
    if not cited:
        return True
    span = segs[index[start]:index[max(start, end - 1)] + 1]
    if "para" in cited:
        want = ("para", int(re.sub(r"\D", "", str(cited["para"]))))
        return any(s["para"] == want for s in span)
    if "claim" in cited:
        want = ("claim", int(cited["claim"]))
        return any(s["para"] == want for s in span)
    if "page" in cited:
        if span[0]["page"] is None:
            return None   # no pages in this source type
        lines = cited.get("lines")
        if lines:
            lo, _, hi = str(lines).partition("-")
            lo, hi = int(lo), int(hi or lo)
        for s in span:
            if s["page"] == int(cited["page"]) and (not lines or lo <= s["line"] <= hi):
                return True
        return False
    return True


# --- Main entry ------------------------------------------------------------------

def locate(source, quote, cited=None, lang="eng", segs=None):
    """Locate `quote` in `source` and check it against `cited` (dict with one of
    para / claim / page [+ lines]). Returns a dict with status, match, found, closest."""
    segs = segs if segs is not None else read_segments(source, lang)
    result = {"source": str(source), "quote": quote, "cited": cited or None}

    for kind, loose in (("verbatim", False), ("minor-divergence", True)):
        hay, index = _normalise(segs, loose)
        hits = _find_all(hay, _norm_quote(quote, loose))
        if hits:
            return _verdict(result, kind, segs, index, hits, cited)

    fragments = [f for f in ELLIPSIS_RE.split(quote) if f.strip()]
    if len(fragments) > 1:
        hay, index = _normalise(segs)
        hits = _ellipsis_hits(hay, [_norm_quote(f) for f in fragments])
        if hits:
            return _verdict(result, "ellipsis", segs, index, hits, cited)

    result.update(status="not-found", match=None, found=[], closest=_closest(segs, quote))
    return result


def _ellipsis_hits(hay, fragments):
    hits = []
    for start, end in _find_all(hay, fragments[0]):
        pos, ok = end, True
        for f in fragments[1:]:
            nxt = hay.find(f, pos)
            if nxt < 0 or nxt - pos > MAX_ELLIPSIS_SPAN:
                ok = False
                break
            pos = nxt + len(f)
        if ok:
            hits.append((start, pos))
    return hits


def _verdict(result, kind, segs, index, hits, cited):
    found = [dict(_location(segs, index, s, e), at_cited=_at_cited(segs, index, s, e, cited))
             for s, e in hits]
    checks = [f["at_cited"] for f in found]
    if any(c is True for c in checks):
        status = kind
    elif all(c is None for c in checks):
        status = kind
        result["note"] = "cited location type not available in this source (e.g. a page in a Word file)"
    else:
        status = "wrong-location"
    result.update(status=status, match=kind, found=found, closest=None)
    return result


def _closest(segs, quote):
    hay, index = _normalise(segs, loose=True)
    q = _norm_quote(quote, loose=True)
    if not q or not hay:
        return None
    n, step = len(q), max(1, len(q) // 8)
    best = (0.0, 0)
    sm = difflib.SequenceMatcher(autojunk=False)
    sm.set_seq2(q)
    for start in range(0, max(1, len(hay) - n + 1), step):
        sm.set_seq1(hay[start:start + n])
        if sm.real_quick_ratio() > best[0] and sm.quick_ratio() > best[0]:
            r = sm.ratio()
            if r > best[0]:
                best = (r, start)
    ratio, start = best
    loc = _location(segs, index, start, min(len(hay), start + n))
    return dict(loc, similarity=round(ratio, 3))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=pathlib.Path)
    ap.add_argument("--quote", required=True)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--para", help='cited paragraph, e.g. "[0034]"')
    g.add_argument("--claim", type=int, help="cited claim number")
    g.add_argument("--page", type=int, help="cited page (PDF)")
    ap.add_argument("--lines", help="cited lines on that page, e.g. 12-14")
    ap.add_argument("--lang", default="eng", help="OCR language(s) for scanned PDFs, e.g. deu+eng")
    a = ap.parse_args()
    cited = ({"para": a.para} if a.para else {"claim": a.claim} if a.claim
             else dict({"page": a.page}, **({"lines": a.lines} if a.lines else {})) if a.page else None)
    print(json.dumps(locate(a.source, a.quote, cited, a.lang), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
