---
name: check-art-84-epc
description: >-
  Assess clarity and conciseness of one or more patent claims under Art. 84
  EPC from the claim wording alone — indefinite, ambiguous, Klarheit,
  concise. Pre-filing or examination claim review. Not for support,
  sufficiency (Art. 83), or added matter.
---

# Clarity and Conciseness Assessment under Article 84 EPC

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

This skill assesses clarity and conciseness (Art. 84, second requirement) from the claim wording, and nothing else. Out of scope:

- **Support by the description** (Art. 84, third requirement) — it needs a comparison with the description.
- **Sufficiency** (Art. 83) — use `/check-art-83-epc`. Clarity concerns whether the skilled person can determine the scope; sufficiency whether they can carry out the invention; an ambiguity is a sufficiency issue only where it prevents carrying out the invention (T 593/09).
- **Added matter** (Art. 123(2)) — use `/check-art-123-2-epc`. Flag only an Art. 123(2) risk in a suggested fix.
- **Novelty** (Art. 54) — use `/check-art-54-epc`. **Inventive step** (Art. 56). **Divisional basis** (Art. 76(1)) — use `/check-art-76-1-epc`.
- **Amendments** beyond straightforward rewording fixes, and **scope of protection / infringement** under Art. 69 (Art. 69 does not cure a clarity defect).

If the user asks for any of these, deliver the clarity assessment first, then answer the out-of-scope part with a single sentence: *"That is outside the scope of /check-art-84-epc. To do [X], please use [the appropriate other command/skill] or run a separate request."* Do not silently perform the out-of-scope task. Follow-up questions about the assessment itself (e.g., "why is 'substantially' High rather than Medium?") are in scope.

## Inputs to gather

> **Insufficient input.** Ask for a single missing file, as described below. If more is missing or the goal is unclear, do not guess: say what is missing and suggest `/grill-me check-art-84-epc` first.

1. **The claim(s) to be assessed** — required, and sufficient on their own. If no claim text is given, ask for it; if only a publication number is given, ask for the claim text and do not search the web unless the user explicitly authorises it. If several claim sets are supplied, ask which one to use.
2. **The description and figures** — optional; do not ask for them. If supplied, consult them when interpreting the claims: read each term as the skilled person would in light of the description and drawings (G 1/24; Guidelines F-IV, 4.2). They cannot cure wording that is unclear in itself: a term with no clear meaning in the claim remains a clarity defect even if the description explains it, and the fix is to amend the claim. Do not read limitations from the description into the claim.
3. **The user's specific concerns** (e.g., "the term 'substantially' worries me") — address them explicitly, without limiting the analysis to them.
4. **Procedural context** — optional. In opposition, clarity of granted, unamended claims cannot be examined unless an amendment introduces the defect (G 3/14). Note this in the "Procedural context" line, but still perform the analysis if requested.

## Issue types and the legal standard

A claim is unclear if the skilled person, with common general knowledge, cannot determine the scope of protection from the claim wording (Guidelines F-IV, 4). **Broad is not unclear**: do not raise an issue, or mark it High, merely because a claim is broad.

Check every claim for each type below. The bold name is the value for the **Type** column.

- **Relative term** ("thin", "high", "substantially", "about") — unclear unless the term has a well-recognised meaning in the art (e.g., "high-frequency amplifier") or the claim gives a precise reference point; recourse to the description is generally not enough (F-IV, 4.6; for "about", "approximately", "substantially": F-IV, 4.7).
- **Optional feature** ("preferably", "for example", "such as", "in particular", "if desired") — creates doubt about the scope; generally to be avoided in independent claims (F-IV, 4.9).
- **Result-to-be-achieved** — unclear unless the result can be verified by tests specified in the claim or known to the skilled person, and the claim does not reserve every solution achieving it (F-IV, 4.10).
- **Parameter** — must be measurable by a method known to the skilled person; if no method is specified and several methods give different results, the parameter is unclear (F-IV, 4.11).
- **Functional feature** ("means for", "configured to") — permissible if the function is sufficiently defined and the skilled person can identify means to perform it (F-IV, 4.10 and 6.5).
- **Disclaimer** — permissible if what is excluded is itself clear (F-IV, 4.19; G 1/03, G 2/03, G 1/16).
- **Trade mark** — unclear; a trade mark identifies origin, not technical content, and its meaning may change (F-IV, 4.8).
- **Open range** ("at least", "up to") — not unclear as such. Where it covers values the invention cannot achieve, the objection lies mainly under Art. 83 (sufficiency); flag it briefly.
- **Mixed category** — a claim must be of a single category (F-IV, 3.1). Watch computer-implemented claims that conflate apparatus and method, and use claims: "use of X for Y" is clear, "use of X" alone is not.
- **Missing essential feature** — a feature obviously essential to the invention's operation is absent (Art. 84, first sentence; F-IV, 4.5).
- **Back-reference** — a reference to a claim that does not exist or does not fit.
- **Inconsistent terminology** — e.g., "the device" and "said apparatus" for the same element, within a claim or between claims; a "wherein" clause that leaves open whether it limits the claim.
- **Comprising/consisting** — flag only inconsistent or unusual use.
- **Prolix** — a claim made unnecessarily long by redundant phrases or repeated definitions.
- **Conciseness — claim set** — an unreasonable number of claims; dependent claims that do not narrow; claims that repeat each other's scope; more than one independent claim per category outside Rule 43(2)(a)–(c) EPC (F-IV, 5 and 3.2).
- **Other** — e.g., a Rule 43 form point (two-part form under Rule 43(1), reference signs under Rule 43(7)). Flag briefly if relevant; the full formal check is `/check-claim-formalities-epc`.

## Workflow

1. **Read each claim.** Identify its category, structure (preamble, characterising portion) and back-references.
2. **Spot issues** using the types above, claim by claim.
3. **Check the claim set as a whole** for Conciseness — claim set issues and terminology inconsistent between claims. With a single claim, write "Not applicable — single claim".
4. **Grade each issue.**
   - **High** — the examiner will almost certainly raise it; the scope cannot be determined.
   - **Medium** — the examiner is likely to raise it; reasonable people could disagree.
   - **Low** — minor or borderline. Mark a borderline issue Low rather than hedging in the text.
5. **Suggest a fix** where it is a straightforward rewording (delete "preferably", give a dimension, name a measurement method). If the fix needs a feature from the description, write "Requires substantive amendment from description" and do not invent the feature. Flag any fix that risks Art. 123(2) as a caveat in the fix column.
6. **Cross-check before delivering.** If an issue rests on the description's content (support), on whether the invention can be carried out (Art. 83), on the prior art (Art. 54/56) or on the original disclosure (Art. 123(2)), it is not a clarity issue: remove it. For every High issue, confirm the claim is ambiguous, not merely broad.

## Output format

One table per claim, then the cross-claim section; English; no executive summary, no general remarks at the end. Issue numbers are 1.1, 1.2 for claim 1, 2.1 for claim 2, X.1 for cross-claim issues. A claim without issues gets the single line "No clarity or conciseness issues identified."; a claim set without cross-claim issues gets "No cross-claim issues identified."

```
# Clarity and Conciseness Assessment under Art. 84 EPC

**Claim(s) analyzed:** [list]
**Procedural context:** [examination / opposition / pre-filing review / other — e.g., G 3/14 caveat for opposition]

## Claim 1 [label, e.g., "(independent, apparatus)"]

| Issue # | Claim wording | Type | Severity | Suggested fix |
|---|---|---|---|---|
| 1.1 | "…" | … | High / Med / Low | … |
| 1.2 | "…" | … | … | … |

## Claim 2 …

[as above for each claim]

## Cross-claim observations

| Issue # | Claim wording | Type | Severity | Suggested fix |
|---|---|---|---|---|
| X.1 | … | … | … | … |
```
