---
name: check-art-83-epc
description: >-
  Assess sufficiency of disclosure of one or more claims under Art. 83 EPC
  from the application as filed — whether the skilled person can carry out
  the invention (enablement, Ausführbarkeit, whole-scope, G 2/21). Not
  clarity (Art. 84) or novelty.
---

# Sufficiency of Disclosure Assessment under Article 83 EPC

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

## Out-of-scope handling

This skill assesses sufficiency of disclosure under Art. 83 EPC, and nothing else. Out of scope: clarity (Art. 84, use `/check-art-84-epc`), support by the description (Art. 84, third requirement), novelty (Art. 54, use `/check-art-54-epc`), inventive step (Art. 56), added matter (Art. 123(2); the skill only cites the passage supporting a suggested fix), industrial applicability (Art. 57), and amendments beyond straightforward restrictions to enabled subject-matter.

If the user asks for any of these, deliver the sufficiency assessment first, then answer the out-of-scope part with a single sentence: *"That is outside the scope of /check-art-83-epc. To do [X], please use [the appropriate other command/skill] or run a separate request."* Do not silently perform the out-of-scope task. Follow-up questions about the assessment itself are in scope.

## Inputs to gather

> **Insufficient input → `/grill-me`.** A single missing file is simply asked for, as described below. If the input is otherwise not sufficient to execute this skill reliably — goals, strategy or key facts unclear, several documents or answers missing, or the next step would rest on a guess — do not guess and do not proceed on assumptions. Say what is missing and suggest that the user run `/grill-me check-art-83-epc` first to settle it, then re-run this skill.

1. **The claim(s).** If none are named, assess all independent claims; ask before extending to dependent claims.
2. **The description** — mandatory. If only claims are given, ask for the description and do not assess: sufficiency cannot be assessed from the claims alone. Never invent description content.
3. **Figures** — optional.
4. **Procedural context** — optional (examination, opposition, pre-filing review).

If several applications or claim sets are supplied, ask which one to use.

## The legal standard

The skilled person, with the application as filed and the common general knowledge at the filing (or priority) date, must be able to **carry out the invention across the whole scope of the claim without undue burden** (Art. 83 EPC; Guidelines F-III, 1).

- **Total insufficiency** — not even one embodiment can be carried out.
- **Whole-scope insufficiency** — a broad claim (chemical genus, broad parameter range, broad "means for" function) is enabled only for a subset of embodiments (T 409/91).
- **Undue burden** — routine experimentation is acceptable; a research programme is not (T 435/91).
- **Breadth alone is not insufficiency.** A High issue needs a concrete enablement gap: name the embodiments that cannot be carried out.
- Where an unclear feature only blurs the limits of the scope, it is clarity; an ambiguity is insufficiency only where it prevents the skilled person from carrying out the invention (T 593/09; Guidelines F-III, 12).

## Workflow

1. **Field and skilled person.** One or two sentences on the technical field, the skilled person and the relevant common general knowledge.
2. **Scope of each claim.** Category; breadth (single embodiment, defined class, or functional / parameter-defined / generic); the features carrying the inventive contribution. For parameter, functional, range, use, computer-implemented or biological-material claims, read the matching section of `references/claim-types.md` in this skill's directory.
3. **Technical effect.** If the claim or description relies on a technical effect, name it and apply the G 2/21 section of `references/claim-types.md`. If none is relied on, do not invoke G 2/21.
4. **Enablement.** Can at least one embodiment be carried out? Essentially all? Where are the working examples, and are they representative of the scope? Is there guidance for selecting from broad classes?
5. **Grade each issue.** Type: one of {Whole-scope insufficiency, Total insufficiency, Plausibility (G 2/21), Insufficient examples, Parameter unobtainable, Functional / reach-through, Missing guidance for selection, Undue burden / research programme, Biological material — deposit, Inventive contribution not reproducible, Other}. Severity:
   - **High** — the objection will almost certainly succeed; the disclosure plainly does not enable the claim across its scope.
   - **Medium** — likely to be raised; depends on argument and evidence.
   - **Low** — borderline. Mark a borderline issue Low rather than hedging in the text.
6. **Suggest a fix** only as a restriction to subject-matter actually supported by the description, with the citation (e.g., "Restrict to compounds of formula I where R1 = methyl, ethyl or propyl; supported by [0042] and Examples 1–3"). Otherwise write "No straightforward fix — would require either evidence that the claim is enabled across its scope or substantive amendment beyond the original disclosure (Art. 123(2) caveat)."
7. **Cross-check before delivering.** Remove issues that are really clarity (Art. 84), support (claim broader than the disclosure although the disclosed examples are enabled), inventive step or added matter.

## Output format

One table per claim, English, no executive summary, no general remarks at the end. Issue numbers are 1.1, 1.2 for claim 1, 2.1 for claim 2. A claim without issues gets the single line "No sufficiency issues identified."

```
# Sufficiency of Disclosure Assessment under Art. 83 EPC

**Claim(s) analyzed:** [list]
**Application:** [bibliographic reference, if known]
**Procedural context:** [examination / opposition / pre-filing review / other]
**Technical field and skilled person:** [one or two sentences]

## Claim 1 [label, e.g., "(independent, product)"]

[Optional: one short paragraph on the technical effect relied upon, if any]

| Issue # | Aspect of claim | Type | Severity | Suggested fix |
|---|---|---|---|---|
| 1.1 | "…" | … | High / Med / Low | … |
| 1.2 | "…" | … | … | … |

## Claim 2 …

[as above for each claim]
```
