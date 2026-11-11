---
name: suggest-claim-dependencies
description: >-
  Suggest augmented back-references for dependent claims (Rule 43(4) EPC), each backed by cited description passages to avoid intermediate generalisation under Art. 123(2). Triggers on 'multiple dependencies', 'Rückbezüge erweitern'.
---

# Suggested Claim Dependencies (Rule 43(4) EPC)

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

This skill **suggests** augmented back-references for dependent claims ("according to any one of claims 1 to 4"), so that the claim set covers more feature combinations as fall-back positions. Each new combination is admissible only if it is directly and unambiguously disclosed in the application as filed, so every suggestion comes with the cited passage supporting every combination it creates. The deliverable is a list of dependent claims with original back-reference, suggested back-reference and supporting passages, plus points for attorney review — not the wording of the amended claim set.

## The rules (apply strictly)

1. **Back-references only.** Only the back-references of dependent claims change. No feature is added, deleted or reworded, and an independent claim never becomes dependent.
2. **Same category.** A dependent claim refers back only to claims of the same category (product to product, method to method).
3. **Preceding claims.** Suggest back-references to preceding claims only, so the set stays readable and the numbering need not change.
4. **Every resulting combination needs basis.** Adding claim Y to the back-references of claim X creates the combination X + Y **and** X + every combination Y itself covers (Y's own back-references, recursively). It also extends every claim that refers back to X. Each of these combinations must be directly and unambiguously disclosed in the application as filed (Gold Standard, G 2/10 — verify). Check them all; one combination without basis means the back-reference is not suggested.
5. **What counts as basis.**
   - *Strong:* a passage disclosing the features together (e.g. in one embodiment), provided no feature is extracted from features it is functionally or structurally linked with in that passage (intermediate generalisation, Guidelines H-V, 3.2.1 — verify); or a passage presenting the feature as generally applicable to the other embodiments/aspects (e.g. "in any of the embodiments described above", "this applies equally to …").
   - *Weak — flag, do not rely on alone:* a generic statement that "all features may be combined"; disclosure of the features only in separate embodiments; support only from the drawings.
   - *Not basis:* the absence of a contradiction; the claims being "compatible"; what the skilled person "might" combine.
6. **No contradictory or alternative combinations.** Never make a claim refer back to a claim adding an alternative it excludes (e.g. "made of copper" referring back to "made of aluminium"); this would be unclear (Art. 84 EPC).
7. **Basis is the application as filed.** If the current claims differ from the claims as filed, the claims as filed and the description as filed are the reference.

## Out-of-scope handling

Deliver the list first; then, for any of the following, state in one sentence: *"That is outside the scope of /suggest-claim-dependencies. To do [X], please use [the appropriate skill] or run a separate request."* Out of scope: drafting the amended claim set; reducing the claim count (`/suggest-claim-reduction`); Art. 123(2) assessment of other amendments (`/check-art-123-2-epc`); claim formalities (`/check-claim-formalities-epc`); divisional basis (`/check-art-76-1-epc`); patentability-driven restructuring (`/suggest-oa-response-strategies`); non-EP offices.

## Inputs to gather

> **Insufficient input.** Ask for a single missing file, as described below. If more is missing or the goal is unclear, do not guess: say what is missing and suggest `/grill-me suggest-claim-dependencies` first.

1. **The claim set.** Required.
2. **The application as filed** — description, claims and drawings. Required: without it nothing is suggested. Ask for it if missing.

## Citation discipline

Cite the application as filed precisely: paragraph number or page/line, and quote the relevant words verbatim in the original language. Never invent a passage or paragraph number. Never cite an EPC Article/Rule, Guidelines section or Board decision from memory without verifying it on epo.org; otherwise mark it `[unverified]`.

## Workflow

### Step 1 — Parse the claims

For every claim record: number; category; independent or dependent; original back-reference(s); the feature it adds; and alternatives it excludes. Build the dependency graph.

### Step 2 — Map each feature to the description

For each dependent claim's feature, locate the passages of the application as filed that disclose it, and record in which context: which embodiment, together with which other features, and whether it is presented as generally applicable or linked to other features.

### Step 3 — Generate candidates

For each dependent claim X, every preceding claim Y of the same category that X does not yet refer back to is a candidate. Discard Y at once if rule 6 excludes it.

### Step 4 — Check each candidate

For each candidate X → Y, list every new combination it creates (rule 4) and look for basis for each in the map from Step 2 (rule 5). Suggest the back-reference only if every new combination has basis; rate it *strong* if all basis is strong, otherwise list it under "not suggested" with the reason. Where a cascade into claims depending on X lacks basis, the candidate is not suggested.

Process claims in numbering order, and check later candidates against the back-references already suggested, since those change what each claim covers.

### Step 5 — Emit the deliverable

Fill in `assets/output-template.md` exactly (read it first). Give the suggested back-reference in the form the claim would use ("claim 1 or 2", "any one of claims 1 to 4"). Remove all DRAFTER comments. Note that a multiply dependent claim counts as one claim, so the claims fees under Rule 162 EPC do not change (verify).

## Worked example

Claims: 1 (independent, a heating device with a housing), 2 (claim 1, housing made of aluminium), 3 (claim 1, a temperature sensor), 4 (claim 1, a timer), 5 (claim 1, housing made of steel).

| Claim | Feature | Original back-reference | Suggested back-reference | New combinations | Supporting passages (as filed) | Basis |
|---|---|---|---|---|---|---|
| 3 | temperature sensor | 1 | 1 or 2 | 1+2+3 | [0024]: "The aluminium housing … carries a temperature sensor …" | strong |
| 4 | timer | 1 | any one of claims 1 to 3 | 1+2+4, 1+3+4, 1+2+3+4 (the last via claim 3 → 2) | [0026]: "In all embodiments described above, the device may further comprise a timer …"; [0024] | strong |

Not suggested: 5 → 2 (steel vs. aluminium are alternatives, rule 6). 5 → 3: the sensor is disclosed only in the aluminium-housing embodiment [0024]; no passage discloses it with a steel housing (rule 5 — intermediate generalisation).

## Conventions

Write in the language of the user's request; quote passages in the original language, with a short gloss if different. No executive summary, no closing remarks.

## Edge cases

- **Claims already multiply dependent:** check only the additional back-references.
- **Several independent claims of the same category:** a dependent claim may refer back to more than one of them only if the feature is disclosed for each; apply rule 4.
