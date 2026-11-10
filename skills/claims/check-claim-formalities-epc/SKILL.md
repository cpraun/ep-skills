---
name: check-claim-formalities-epc
description: >-
  Check the formal drafting of patent claims under the EPC — antecedent
  basis, terminology, numbering, dependency/references and independent-claim
  count (Rule 43 EPC), two-part form. Formal counterpart to
  /check-art-84-epc. Not substantive grounds.
---

# Claim Formalities Assessment under the EPC (Rule 43 EPC and antecedent basis)

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

This skill checks the **formal drafting** of claims: antecedent basis, terminology, numbering and dependencies, independent claims per category, and Rule 43 form. It does not judge what the wording means technically. Out of scope: substantive clarity (relative terms, result-to-be-achieved, parameters, adequacy of functional features, prolixity — use `/check-art-84-epc`), support by the description, sufficiency (use `/check-art-83-epc`), added matter (use `/check-art-123-2-epc`), novelty and inventive step, unity (Art. 82 / Rule 44), and claims-fee reduction (use `/suggest-claim-reduction`).

If the user asks for any of these, deliver the formalities assessment first, then answer the out-of-scope part with a single sentence: *"That is outside the scope of /check-claim-formalities-epc. To do [X], please use [the appropriate other command/skill] or run a separate request."* Do not silently perform the out-of-scope task. Follow-up questions about the assessment itself are in scope.

## Inputs to gather

> **Insufficient input → `/grill-me`.** A single missing file is simply asked for, as described below. If the input is otherwise not sufficient to execute this skill reliably — goals, strategy or key facts unclear, several documents or answers missing, or the next step would rest on a guess — do not guess and do not proceed on assumptions. Say what is missing and suggest that the user run `/grill-me check-claim-formalities-epc` first to settle it, then re-run this skill.

1. **The claim set** — required; assessed as a set. If no claims are given, ask for them and stop; never fabricate a claim set. If only a publication number is given, ask for the claim text and do not search the web unless the user explicitly authorises it. If several claim sets are given, ask which one to use.
2. **Whether the application has drawings** — needed only for the reference-sign check. If unknown, do not ask; perform that check conditionally and flag "verify against the drawings".
3. **Procedural context** — optional.

The description is not needed.

## The formalities standard

### A. Antecedent basis and terminology (Art. 84 EPC)

- **Antecedent basis.** Every "the X" / "said X" needs a prior "a X" / "an X" in the same claim or in a claim it depends on. Exception, applied narrowly: elements that are inherent or universally present ("the atmosphere", "the user").
- **Double introduction.** "a housing … a housing" when one housing is meant.
- **Broken chain.** An element introduced in a dependent claim is relied on by a sibling claim that does not depend on it.
- **Terminology consistency.** The same element must have the same name throughout the set ("the container" in claim 1, "said vessel" in claim 3). Apply the article system of the claim language (German "ein/der", French "un/le").

### B. Numbering and dependencies (Rule 43(3)–(6) EPC)

- **Numbering** — consecutive Arabic numerals (Rule 43(5)); flag gaps and duplicates.
- **Dependency references** — only to a *preceding*, existing claim; flag forward, self, non-existent and circular references (Rule 43(4)).
- **Multiple dependency** — admissible at the EPO, including a multiply dependent claim referring to another multiply dependent claim. Never flag the multiplicity itself; flag only cumulative or ambiguous wording ("according to claims 1 and 2" instead of "according to any one of claims 1 to 2") and poor grouping of claims that refer to the same claim(s) (Rule 43(4)).
- **References to the description or drawings** ("as shown in Figure 3") — not allowed unless absolutely necessary (Rule 43(6)).

### C. Independent claims per category (Rule 43(2) EPC)

More than one independent claim in the same category is allowed only for (a) interrelated products, (b) different uses of a product or apparatus, or (c) alternative solutions that cannot appropriately be covered by one claim. Flag any category with more than one independent claim that does not evidently fall within an exception. Borderline cases are the attorney's call: flag and explain, do not decide.

### D. Claim form

- **Single category per claim** (Guidelines F-IV, 3.1) — e.g., "a method of using apparatus X comprising parts A, B and C" is mixed.
- **Single sentence** — an EPO drafting convention, not an absolute rule.
- **Transitional phrase** — missing or unusual; "comprising" and "consisting of" mixed inconsistently for the same element.
- **Two-part form** (Rule 43(1)) — required only "wherever appropriate"; flag an independent claim not in two-part form as a Medium or Low observation unless the form is clearly inapposite. US-style claims: judge against EPO expectations.
- **Reference signs** (Rule 43(7)) — expected in parentheses when the application has drawings; they do not limit the claim.
- **Means-plus-function** — check only the form (category, antecedent basis of "the means"); the definition of the function is substantive clarity.

## Workflow

1. **Parse the claim set:** number, independent or dependent, referenced claims, category, transitional phrase. Build the dependency graph.
2. **Run checks A–D**, reading claims in dependency order. Antecedent basis, numbering and dependency references are mechanical checks: do them exhaustively and quote the exact wording.
3. **Grade each issue.**
   - Type: one of {Antecedent basis, Terminology inconsistency, Numbering, Dependency reference, Multiple dependency (Rule 43(4)), Independent claims per category (Rule 43(2)), Mixed category, Single-sentence form, Transitional phrase, Two-part form (Rule 43(1)), Reference to description/drawings (Rule 43(6)), Reference signs (Rule 43(7)), Other}.
   - Severity: **High** — will almost certainly be raised (missing antecedent basis, forward or non-existent reference, Rule 43(2) outside the exceptions, mixed category). **Medium** — likely (terminology inconsistency, cumulative multiple-dependency wording, two-part form where clearly appropriate). **Low** — minor or conventional (grouping, single sentence, borderline reference signs).
   - Suggested fix: a concrete rewording (e.g., "insert 'a housing' at first mention in claim 1", "renumber claim 5 → 4", "recast as 'according to any one of claims 1 to 3'"). Do not invent claim text, reference signs or disclosure; if a fix would add or remove subject-matter, note the Art. 123(2) caveat.
4. **Cross-check before delivering.** Remove substantive clarity issues and antecedent-basis flags for genuinely inherent elements. For each High issue, confirm it is a formal defect, not a style preference.

## Output format

English, no executive summary, no closing remarks. A claim without issues gets the single line "No formal issues identified."; a set without cross-claim issues gets "No cross-claim issues identified."; a single claim gets "Not applicable — single claim" for the cross-claim section.

```
# Claim Formalities Assessment under the EPC

**Claim(s) analyzed:** [list]
**Drawings present:** [yes / no / unknown — affects the Rule 43(7) reference-sign check]
**Procedural context:** [pre-filing / examination / amendment review / other — if relevant]

## Claim 1 [label, e.g., "(independent, apparatus)"]

| Issue # | Claim wording / element | Type | Severity | Suggested fix |
|---|---|---|---|---|
| 1.1 | "…" | Antecedent basis | High | … |
| 1.2 | "…" | … | … | … |

## Claim 2 …

[as above for each claim]

## Cross-claim observations

| Issue # | Element / claims | Type | Severity | Suggested fix |
|---|---|---|---|---|
| X.1 | … | Independent claims per category (Rule 43(2)) | High | … |
```
