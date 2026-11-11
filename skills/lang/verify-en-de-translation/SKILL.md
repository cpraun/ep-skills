---
name: verify-en-de-translation
description: >-
  Verify an English→German translation by comparing source and target,
  reporting only defects: (1) terminology — an English term with two+ German
  equivalents; (2) completeness — English paragraphs with no German
  counterpart. EN→DE checking only.
---

# English → German Translation Check

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

This skill compares an English source with its German translation and reports **defects only**, of two kinds: an English term rendered by two or more German terms (terminology), and an English paragraph without a German counterpart (completeness). Be conservative: flag every candidate inconsistency; whether it is acceptable is the reviewer's decision.

## Out-of-scope handling

Out of scope: producing a translation (use `/translate-en-de`), stylistic editing, grammar correction (unless it is also a consistency or completeness defect), other language pairs or directions, back-translation, and whether a translation is *correct* — a wrong but consistent rendering is not flagged.

If the user asks for any of these, deliver the defect report first, then answer the out-of-scope part with a single sentence: *"That is outside the scope of /verify-en-de-translation. To do [X], please use [the appropriate other tool] or run a separate request."* Do not silently perform the out-of-scope task. Follow-up questions about the findings are in scope.

## Inputs to gather

> **Insufficient input.** Ask for a single missing file, as described below. If more is missing or the goal is unclear, do not guess: say what is missing and suggest `/grill-me verify-en-de-translation` first.

- **English source** and **German target** — given as paths, pasted text or attachments, or found in the project directory (filenames containing `english`, `EN`, `_en`, `-en`, `source` / `german`, `deutsch`, `DE`, `_de`, `-de`, `target`; otherwise tell them apart by content). If one is missing, ask for it and stop.
- If the target is not German, say the skill is EN→DE only and stop.
- If the two texts have a different logical structure (chapters reordered, headings renumbered), say so and ask whether to compare anyway.

Read `.docx` with the `handle-docx` skill and `.pdf` with the `read-pdf` skill. If PDF extraction scrambles paragraph boundaries, proceed on the reflowed text and say so under Notes.

## Method

1. **Align paragraphs** by headings, section numbers, claim numbers, captions and content. Flag every English paragraph without a German counterpart, including omitted boilerplate. A heading merged into the next paragraph or sentences reordered within a paragraph are not findings.
2. **Build the term map.** Terms are content-bearing words and fixed expressions that occur more than once: names of parts and concepts, domain verbs, defined terms. In patent claims, treat every noun phrase as a defined term. For each term, collect every German rendering at the corresponding positions.
3. **Filter.** Reduce to the base form first: inflection, articles and declension ("Schraube" / "der Schrauben") are the same term. Two different German root words for one English term are a finding even if both are correct ("Steuereinheit" / "Steuergerät" for *control unit*). Defined terms — capitalised, quoted or explicitly defined — tolerate no variation. Identical acronyms and names on both sides are consistent; German quotations left in German are not findings.

## Output format

Findings only — no preamble, summary or closing remarks. Omit a section that has no findings. If both are empty, output exactly `No errors found.`

```
### Inconsistent Translations

* **English Term:** `[term]` → **German Translations:** `[rendering A]`, `[rendering B]`

### Incomplete Translation: Missing Paragraphs

* **Missing Paragraph 1:** `[full text of the missing English paragraph]`
```

Optionally append a terse `### Notes` section for German content without an English counterpart, an obvious number or unit mismatch, or PDF extraction artefacts.
