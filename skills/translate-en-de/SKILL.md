---
name: translate-en-de
description: >-
  Translate English patent claims or a description into German with a one-to-one term map. Takes a file path or text as argument. Asks about doubtful terms first; writes only the translation to a file. Übersetzung, R. 71(3).
trainable: true
---

# Patent Translation

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

This skill translates English patent claims and/or a description into German, as a draft for attorney review. Its argument is the English text, as a file path or as the text itself. Two hard requirements:

1. **Completeness** — every paragraph, claim, heading, table cell and caption is translated; nothing is summarised, merged, skipped or added.
2. **A one-to-one term map** — each source term has **exactly one** German rendering throughout claims and description, and **different** source terms get **different** renderings (if the source distinguishes "fastening element" from "fixing element", so does the translation).

## Out-of-scope handling

Out of scope: checking an existing translation (use `/check-en-de-translation`), other language pairs, improving or correcting the source (the translation mirrors its ambiguities, breadth and apparent errors; errors are reported, never fixed), legal review of the claims (use the `check-art-*` skills), and free or adapted translation. For each such request, answer with a single sentence: *"That is outside the scope of /translate-en-de. To do [X], please use [the appropriate other skill] or run a separate request."*

## Inputs to gather

> **Insufficient input → `/eps-grill-me`.** A single missing file is simply asked for, as described below. If the input is otherwise not sufficient to execute this skill reliably — goals, strategy or key facts unclear, several documents or answers missing, or the next step would rest on a guess — do not guess and do not proceed on assumptions. Say what is missing and suggest that the user run `/eps-grill-me translate-en-de` first to settle it, then re-run this skill.

1. **Source text** — required. If the argument is an existing file, read it (`.docx` with the `util-docx` skill, `.pdf` with the `util-pdf` skill; reflow PDF paragraphs and say if the structure could not be recovered); otherwise it is the text itself. If ambiguous, ask once. If the text is not English, say so and stop.
2. **Glossary or reference translation** — optional (client glossary, parent application, published claim translations). If supplied, its term choices are **binding**.
3. **Output location** — optional.

## Method

**Learned rules first.** Before starting, read [LEARNED.md](./LEARNED.md) in this skill directory, if it exists, and apply its rules. They record the user's preferences (style, wording, layout, priorities) and take precedence over this file's defaults in those respects. They never override a legal rule or safeguard of this skill (EPC requirements, Art. 123(2) EPC basis, citation discipline); if a learned rule conflicts with one, follow this file and tell the user.

If the source contains claims, also read `references/claims.md` in this skill's directory (claim phraseology and an example).

1. **Segment the source** into paragraphs (with numbers such as `[0012]`), headings, tables, captions, lists and claims (with numbers and dependencies), and note reference signs, formulae, sequence identifiers, numbers with units, document citations and trade marks. This is the completeness baseline.
2. **Build the term map** before translating. Terms are content-bearing words and fixed expressions naming parts, materials, properties, steps, functions or relations; every noun phrase and functional verb in the claims is a term, and explicitly defined terms are fixed. Choose the established technical term of the field, or the binding glossary term; keep parallel terms parallel (*first/second element* → *erstes/zweites Element*). Then make the map one-to-one:
   - inflection, case and articles are grammar, not different renderings;
   - two source terms that would naturally share a rendering get distinct renderings (*attach / fasten / fix* → *anbringen / befestigen / fixieren*);
   - one source word with two meanings (*bearing* as part vs. orientation) is two terms;
   - compounds contain the mapped rendering (*Sensor*, *Sensorgehäuse* — not *Fühlergehäuse*).
3. **Resolve doubts in one round, before translating:** renderings that differ in scope (*comprise* → *umfassen* / *aufweisen*; *layer* → *Schicht* / *Lage*), terms without a one-to-one rendering, coined terms, and ambiguities German forces you to resolve (the gender of "it" or "which"). For each, give the term, its location, your proposal and the alternatives with a one-line reason; use AskUserQuestion where available, with the recommended option first. If there is no genuine doubt, do not ask.
4. **Translate** segment by segment, applying the term map mechanically:
   - faithful, not free — when in doubt, the literal rendering; restructure only where German grammar requires it;
   - same paragraph and claim numbers, order, headings and list numbering, one target paragraph per source paragraph;
   - reference signs, formulae, sequence identifiers and document citations unchanged; numbers and units unchanged, decimal separators German (`1.5 mm` → `1,5 mm`);
   - articles carry antecedent basis exactly as in the source (*a lever … the lever* → *ein Hebel … der Hebel*);
   - hedges kept (*substantially* → *im Wesentlichen*, *about* → *etwa*); trade marks unchanged; German quotation marks „…“.

   For a long description, translate in sections and append each to the output file. A new term found mid-way is added to the map; if it is doubtful, stop and ask before continuing.
5. **Verify against the baseline and the map:** the same number of paragraphs, claims, headings, cells and captions; every reference sign as often as in the source; every term rendered as mapped; no German term used for two source terms; claims unchanged in dependencies, one sentence each, antecedents matching. Fix every defect before delivering.
6. **Report in the reply**, briefly: the output path; the term map as a table (`Source term | Target term | Note`), at least for all claim terms and all terms resolved in Step 3; source issues noticed but not corrected (typos, wrong reference signs, missing antecedents, inconsistent source terms — translated as two terms); extraction problems.

If the user later changes a rendering, update **every** occurrence in the output file and the map.

## Output

- The file contains **the translation only** — no preamble, notes, term map or source text.
- Filename: the source basename with `.de` inserted (`claims.txt` → `claims.de.txt`); inline text → `translation.de.txt` in the working directory.
- Format: `.txt` / `.md` → same; `.docx` → `.docx` via the `util-docx` skill (otherwise `.txt`, and say so); `.pdf` → `.txt`.
- If the output file exists, ask before overwriting.
