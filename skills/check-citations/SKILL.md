---
name: check-citations
description: >-
  Verify every quote, paragraph/page reference and claim wording in a draft (DOCX, PDF, text) against the sources in the project: description, claims, D-documents, OAs. Flags misattributions and paraphrases passed off as quotes.
---

# Validate Citations in Patent Documents

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

## Inputs

> **Insufficient input → `/eps-grill-me`.** A single missing file is simply asked for, as described below. If the input is otherwise not sufficient to execute this skill reliably — goals, strategy or key facts unclear, several documents or answers missing, or the next step would rest on a guess — do not guess and do not proceed on assumptions. Say what is missing and suggest that the user run `/eps-grill-me check-citations` first to settle it, then re-run this skill.

- **Target document** — the draft to verify (e.g., `DRAFT - Response to Summons.docx`, `Submission.pdf`).
- **Sources** — the documents in the project directory that the draft cites: description and claims, D-documents, OAs and Summons. If a cited source is not in the project, ask for it; never verify against memory.

Read a `.docx` with the `util-docx` skill's `read_text_with_changes_applied` (the text as amended by tracked changes) and a `.pdf` with the `util-pdf` skill (`pdf_extract.py`, page:line keys).

## Workflow

1. **Extract every citation** from the target: quotations attributed to a document; paragraph, page/line, figure and reference-numeral references (`[0034]`, `page 7, line 12`, `block 215`); quoted statements of the Examining Division or Board (`point 1.1.4 of the Summons`); EPC, case-law and Guidelines references; claim features presented as having literal basis under Art. 123(2) / 76(1).
2. **Locate each quotation** with the bundled script, which reads the source, normalises quotes, dashes, ligatures, hyphenation and whitespace, and reports where the quote really is:

   ```bash
   python3 <this-skill-dir>/scripts/locate_citation.py SOURCE --quote "..." [--para "[0034]" | --claim 3 | --page 7 [--lines 12-14]] [--lang deu]
   ```

   Base the verdict on its `status`, not on your own reading:

   | `status` | Verdict |
   |---|---|
   | `verbatim` | 🟢 Verbatim |
   | `minor-divergence` | 🟡 Minor divergence |
   | `ellipsis` | 🟡, or 🟢 once you have checked that the omission does not change the meaning |
   | `wrong-location` | 🔴 — cite the actual location from `found` |
   | `not-found` | 🔴 — quote the `closest` passage and its similarity |

3. **Check what the script does not:** paraphrases presented as quotes (🔴); reference numerals against the description and drawings (`block 215` vs `block 220`); whether legal references exist and say what is claimed.
4. **Sanity-check the document as a whole:** request hierarchy in a reply to a Summons (main request, auxiliary requests, conditional request for oral proceedings, videoconference); new claim terms that conflict with existing terms; consistency of application numbers, dates and D-document identifiers.

## Output format

```markdown
# Literal Citation & Reference Verification Report

**Target Document**: `<filename>`
**Date of Verification**: `<date>`
**Verification Status**: `[PASSED | PASSED WITH WARNINGS | FAILED (DISCREPANCIES FOUND)]`

## 1. Executive Summary
- Total citations checked: `N`
- Verbatim matches: `N`
- Minor divergences / warnings: `N`
- Critical discrepancies (wrong references / altered quotes): `N`

## 2. Citation Verification Matrix

| # | Location in Target | Cited Source & Reference | Quoted / Cited Text | Verification Status | Notes / Discrepancies |
|---|-------------------|--------------------------|---------------------|---------------------|-----------------------|
| 1 | Sec. I, para. X   | Description, para. [0034]| "..."               | 🟢 Verbatim          | Exact match           |
| 2 | Sec. I, para. Y   | Description, para. [0034]| "..."               | 🔴 Inaccurate        | Quoted "block 220" instead of "block 215" |

## 3. Detailed Discrepancies & Recommended Fixes

### Issue 1: [Short Title]
- **Location in Draft**: `<Section, Paragraph>`
- **Text in Draft**: `<Quoted snippet>`
- **Actual Text in Source**: `<Verbatim snippet from source file>`
- **Problem**: `<why this is defective (wrong numeral, altered quote, Art. 123(2) risk)>`
- **Recommended Revision**:
  `<Exact replacement text ready to copy-paste>`

## 4. Formal, Procedural & Claim Consistency Review
- **Procedural Requests**: `<main/auxiliary requests and oral proceedings>`
- **Antecedent & Clarity Checks**: `<claim terms and dependencies>`
- **Document Identifiers & Deadlines**: `<application numbers, references, Rule 116(1) dates>`
```
