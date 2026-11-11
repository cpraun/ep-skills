---
name: check-prefiling
description: >-
  Pre-filing review of a draft application (US, DE or in-house) for filing at the EPO: formalities, claims, Art. 83/84/123(2), COMVIK, Rules 62a/63/64, fees, technical effects. Use for 'pre-EP filing review' or 'EP filing check'.
trainable: true
---

# Pre-EP Filing Review

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

Act as a European patent attorney reviewing a draft application before it is filed as a European patent application (Art. 75, 78 EPC). Produce a concise, numbered list of suggested revisions that the user can work through step by step. Do not be verbose.

Do not assume where the draft comes from or what technology it concerns. Determine both from the text (Step 3) and apply origin- or field-specific checks only when they fit.

**Learned rules first.** Read `~/.ep-skills/learned/check-prefiling.md`, if it exists, and apply its rules. They record the user's preferences (style, wording, layout, priorities) and take precedence over this file's defaults in those respects. They never override a legal rule or safeguard of this skill; if one conflicts, follow this file and tell the user. If the file cannot be read, continue without it.

## Step 1 – Establish the filing situation (ask before proceeding)

> **Insufficient input → `/grill-me`.** A single missing file is simply asked for, as described below. If the input is otherwise not sufficient to execute this skill reliably — goals, strategy or key facts unclear, several documents or answers missing, or the next step would rest on a guess — do not guess and do not proceed on assumptions. Say what is missing and suggest that the user run `/grill-me check-prefiling` first to settle it, then re-run this skill.

Ask in one structured question round, only what is decision-relevant and not evident from the documents:
- **Priority**: first filing, or EP filing claiming priority (which application, date; is the priority text available)?
- **Scope of changes allowed**: only formalities and pure additions (priority to be kept / text frozen), or substantive revision permitted?
- **Language of filing**: EP official language, or other language with translation (Art. 14(2), Rule 6(1) EPC)?
- Optional: claim strategy (keep the existing claim set or adapt to EP style; budget for claim and page fees).

If the questions are dismissed, assume: no priority claimed, substantive suggestions permitted but marked as such, filing in the language of the draft. State the assumptions at the top of the output.

## Step 2 – Constraints

- **Priority claimed / text frozen**: do not change the substance of existing text. Allowed: (1) formal corrections, (2) deleting contradictory or obviously wrong text (state why), (3) pure additions of technical effects (see F). Flag that additions not contained in the priority application are only entitled to the EP filing date (same invention, Art. 87(1) EPC, G 2/98; later reliance on effects, G 2/21).
- **First filing, revision allowed**: substantive suggestions are permitted (fallback positions, missing embodiments, definitions, effects). Remind the user that the filed text fixes the content for all later amendments (Art. 123(2) EPC) and for later priority claims.
- Every proposed addition or replacement gives: location, position ("append at end of …" / "replace X by Y"), full wording in quotes, and its basis in the draft.
- Write additions in the language, terminology and style of the draft.

## Step 3 – Read everything and profile the draft

- Read the full description, claims, any clauses/aspects, abstract and every drawing sheet; render the drawings as images, do not rely on extracted text alone.
- Cite the draft's own paragraph numbers; if there are none, use page/line and recommend paragraph numbering. `markitdown` may renumber paragraphs as list items, so verify numbers against the source.
- Check page sizes (`pdfinfo` or the document settings).
- **Profile the draft** in one line at the top of the output:
  - *Drafting origin/style*, from indicators such as claim wording, boilerplate, headings, spelling, units, paper size (e.g. US style, DE/European style, translation from JP/CN/KR, inventor or in-house draft).
  - *Technical field and claim types* (e.g. CII/AI, mechanical, electrical, chemical/pharma, biotech; product, method, use).
- If priority is claimed, compute the 12-month deadline (Art. 87(1) EPC). If less than 2 weeks away, put it first and separate must-do-before-filing items from items that can be fixed after filing.

## Step 4 – Checklist (always)

### A. Filing formalities
- Priority claim: number, date, office correct; declaration within 16 months (Rule 52); priority document or DAS code (Rule 53); search results of the priority application (Rule 141) unless the office of first filing is exempt.
- Designation of inventor (Rule 19) and applicant data ready.
- Page fee from page 36 (Rule 38(2), RFees); claim fees from claim 16 and higher fee from claim 51 (Rule 45).
- Translation needed if not filed in an official language (Rule 6(1)).

### B. Drawings (Rule 46; Rule 49 and Decision of the President on presentation of documents)
- A4 sheets; blank margins, no frames; sheet numbering "x/y".
- Reference signs: every sign in the drawings appears in the description and vice versa; identical labels in figure and text; the same sign used for the same element throughout.
- Figure content matches the text (flowchart steps vs. method claim; arrows, boxes, numbers that are shown but not explained).
- Minimal text in drawings; photos/screenshots/graphs legible in black and white.

### C. Description – form and consistency (Rules 42, 48)
- Title, technical field, background (Rule 42(1)(b)), problem and solution recognisable (Rule 42(1)(c)), brief description of drawings consistent with the figures, at least one way of carrying out the invention (Rule 42(1)(e)).
- Incomplete or garbled sentences, typos in terms and reference signs, wrong actor or wrong element named.
- Self-contradictions and statements that conflict with the claims (e.g. a feature called "essential" that is optional in the claims).
- Terminology drift for the same element; align with the claim terms. Key claim terms defined consistently.
- Units (SI, Rule 49 / Decision of the President), formulae, ranges and parameters: consistent and with measuring methods where needed.
- Rule 48 issues: disparaging statements, ordre public, irrelevant matter. Trademarks identified as such.
- Statements without effect or objectionable at the EPO (e.g. incorporation by reference of essential matter, "the claims cover all modifications", "invention according to the invention" wording that limits scope).
- Numbered clauses / aspects: acceptable as basis at filing; must be deleted or marked as not being claims before grant.

### D. Claims (Art. 84, Rule 43)
- Antecedent basis within and between claims; consistent terms with the description.
- Two-part form where appropriate (Rule 43(1)).
- One independent claim per category (Rule 43(2)) unless an exception applies; otherwise risk of a **Rule 62a** invitation.
- Back-references between categories where possible ("apparatus configured to carry out the method of claim 1") to reduce fees and inconsistencies.
- Vague or relative terms, result-to-be-achieved wording, optional features ("e.g.", "preferably", "in particular") in independent claims; propose specifying dependent claims with basis. Very unclear claims risk a **Rule 63** declaration.
- Use multiple dependencies (allowed at the EPO) to secure fallback combinations.
- Reference signs in brackets (Rule 43(7)).

### E. EP substance
- **Search scope (Rule 137(5))** and **unity (Art. 82, Rule 64)**: all intended fallback positions in the claims at filing; independent claims share a single general inventive concept.
- **Art. 83**: for each claim feature, name at least one disclosed way to carry it out across the claimed scope.
- **Art. 84 (support)**: claim scope vs. description; embodiments outside claim 1; claim terms broader than the description.
- **Abstract** (Rule 47): ≤ 150 words, every statement has a basis in the description (the abstract is not part of the disclosure, Art. 85); name the figure to be published.

### F. Technical effects
- For each technically relevant feature without a stated effect, draft one appended sentence stating the effect that follows directly from the disclosed feature, with no new features, parameters, numbers or examples.
- Do not repeat effects already stated (check "advantages" passages first).

## Step 5 – Additional checks (only if the profile fits)

Read `references/profile-checks.md` in this skill's directory and apply the sections that match the drafting origin (US style, DE/European style, translation, inventor or in-house draft) and the technical field (CII/AI, chemistry/pharma/materials, medical, biotech, mechanical/electrical) from Step 3.

## Output format

Group and number continuously; one or two lines per item; always cite paragraph/page, claim or figure:

```
Profile: <origin/style>, <technical field>, <claim types>
Assumptions: <priority, scope of changes, language>

## A. Urgent (only if a deadline applies)
1. ...

## B. Filing formalities and fees
2. ...

## C. Formal points – description and drawings
3. **<Short title>** – [para]/FIG. x: <issue>. Fix: <fix>.

## D. Claims
...

## E. EP substance
...

## F. Technical effects to add
k. End of [para]: *"<proposed sentence>"* (basis: [para])

## G. Can wait (after filing / before grant)
...

## Open questions
- Q1: ...
```

- Give proposed wording only where text is added or replaced.
- No general explanations of the law beyond what the item needs.
- Close by offering to implement the items one by one.

## Common follow-up requests
- "Summarise the subject matter in N words using the description's wording" → build it from the summary/first technical paragraphs, word-count it, cite source paragraphs.
- "Are the claims supported (Art. 83/84)?" → separate Art. 83 (sufficiency) from Art. 84 (support); feature-to-paragraph table.
- "Is the abstract covered by the description?" → table: abstract statement → basis paragraph.
