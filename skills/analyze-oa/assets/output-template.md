<!--
DRAFTER GUIDANCE — strip every "<!-- DRAFTER: ... -->" comment from the output
before returning. The deliverable below is a working analysis for the
responsible European patent attorney, not a client letter, strategy report, or
filing draft. Keep the section structure fixed; choose the right shape within
each section based on the OA at hand. Preserve the Examiner's own item numbers
throughout — every objection ties back to "OA item 1.", "OA item 2.1", etc.
-->

# Initial OA Analysis — [application number / short title]

*Working analysis for the responsible European patent attorney. Not a final response, client letter, strategy report, or filing draft.*

---

## 1. Procedural snapshot

- **Type of communication:** [OA under Art. 94(3) EPC / EESR / Communication / Summons under Art. 116 EPC]
- **Date of the OA:** [date in EN-US, e.g., May 5, 2026]
- **Examining Division location:** [Munich / The Hague / Berlin]
- **Language of the proceedings:** [EN / DE / FR]
- **Response deadline:** [date computed via the `compute-time-limit-epc` skill] — [extendable to <date> under R. 132 EPC / not extendable] — *footnote: anchor under R. 126(2) / R. 127(2) EPC (in force from 1 November 2023) = date the document bears (no 10-day fiction); period = <four months / two months / six months / …> under R. 132(2) EPC; R. 131 EPC same-number rule applied; R. 134(1) EPC closed-day check at the end. Legal-basis trail and computation reproduced verbatim from `compute-time-limit-epc`.*
- **Status of the application:** [first OA / second OA / response to summons / EESR with WO-ISA / divisional of EP …]

<!-- DRAFTER: If a procedural element is not on the face of the OA, write "[not stated in OA]" rather than guessing.

EXCEPTION — Response deadline. The Response deadline line is MANDATORY in every deliverable and must always contain a computed date. The OA may state the period numerically; if it does not, infer the period from the legal basis (typically 4 months under R. 132(2) EPC for a Communication under Art. 94(3); 6 months under R. 161(1) / R. 162 EPC for Euro-PCT; the date set by the summons for R. 116(1) EPC; 2 months under Art. 108 EPC for a notice of appeal; etc.). In all cases, delegate the computation to the `compute-time-limit-epc` skill — anchor under R. 126(2) / R. 127(2) EPC (in force from 1 November 2023) = date the document bears (no 10-day fiction); R. 131 EPC same-number rule; R. 134(1) EPC closed-day check. If the period had to be inferred rather than read off the OA, flag the inference in §9 "Points for attorney review". Do NOT leave the deadline blank and do NOT write "not stated in OA". -->

---

## 2. Overview of the objections

<!-- DRAFTER: One row per OA item, in the OA's own numbering. Preserve the Examiner's hierarchy (1., 2., 2.1, 3., …). "Initial read" is a one-sentence triage, not an argument. -->

| OA item | Legal basis | Affected claims | Cited art | Examiner's point (one line, quoted where the wording matters) | Initial read |
|---|---|---|---|---|---|
| 1. | Art. 54 EPC | [claims] | D[n] | *"[short verbatim quote]"* | [Tentative — D[n] not provided, see §3.1] |
| 2.1 | Art. 56 EPC | [claims] | D[n] + D[m] | *"[short verbatim quote]"* | [Chain well-formed but OTP appears retrospective — see §4] |
| 3. | Art. 84 EPC | [claims] | — | [type of clarity defect, e.g., relative term "substantially"] | [Well-founded under F-IV, 4.6 unless redefined in the description — see §5] |
| … | … | … | … | … | … |

---

## 3. Novelty (Art. 54 EPC) — feature-by-feature analysis

<!-- DRAFTER: One subsection per (claim, D-document) pair the Examiner relied on. If the Examiner raised Art. 54 against claim 1 over D1 and over D2 in the alternative, produce 3.1 (claim 1 vs D1) and 3.2 (claim 1 vs D2). If novelty was also challenged against claim 7 over D1, produce 3.3 (claim 7 vs D1). Mandatory table format follows check-art-54-epc literally. If the OA raises no Art. 54 objection, write a single sentence below the heading and omit the per-claim subsections. -->

[If no Art. 54 objection is raised: "No Art. 54 objection raised in the OA." and omit the rest of this section.]

### 3.1 Claim [X] against D[n]

**Claim wording analysed:**

> *"[verbatim claim text, broken at the feature level where useful]"*

**Examiner's allegation:**

> [OA item number] — *"[verbatim quote of the Examiner's statement, with item number]"*

**D[n] passages cited by the Examiner:** [precise citations, e.g., "Fig. 2; par. [0023]–[0025]; claim 3"]

<!-- DRAFTER: If D[n] is not in context, add a literal note before the table:
"D[n] has not been provided in this conversation. The analysis below is built solely on the passages the Examiner quoted in the OA and is therefore tentative." -->

<!-- DRAFTER: Add a one-to-two-sentence claim-interpretation note ONLY where a feature's reading is not self-evident (G 1/24 — the description and drawings are always consulted). Omit if all features are self-explanatory. -->

*Claim interpretation (only if needed):* [one to two sentences]

| Feature | Claim wording | D[n] disclosure | Citation | Assessment |
|---|---|---|---|---|
| M1 | *"[verbatim feature wording]"* | [what D[n] discloses — paraphrase or short quote] | [par. / fig. / claim of D[n]] | Yes / No / Implicit / Partial — [one-sentence justification] |
| M2 | *"…"* | … | … | … |
| … | … | … | … | … |

**Conclusion:** Claim [X] is [novel / not novel] over D[n]. [Brief reasoning citing the M-numbers — 2 to 4 sentences. If not novel, name the M-numbers and the D[n] passages that anticipate. If novel, name the M-numbers that distinguish.]

<!-- DRAFTER: For dependent claims, list only the additional features (M2.1, M2.2, …, labelled with the claim number) and inherit the parent's features. If the parent is novel, say so briefly rather than rebuilding the inherited rows. -->

### 3.2 Claim [Y] against D[n]

[as above]

### 3.3 Claim [X] against D[m]

[as above — only if the Examiner relied on a second document in the alternative]

<!-- DRAFTER: Repeat one subsection per (claim, D-document) pair the Examiner challenged. -->

---

## 4. Inventive step (Art. 56 EPC)

<!-- DRAFTER: One block per OA item. Characterise only; do not develop the rebuttal — that is for the strategy phase. -->

[If no Art. 56 objection is raised: "No Art. 56 objection raised in the OA." and omit the rest of this section.]

### 4.1 [OA item number] — claim(s) [list]

**Examiner's problem–solution chain (Guidelines G-VII, 5):**

- **Closest prior art:** D[n] — *"[Examiner's justification, verbatim]"*
- **Distinguishing features:** [as the Examiner identifies them, verbatim from the OA]
- **Objective technical problem:** *"[as the Examiner formulated it, verbatim]"*
- **Combination relied on:** [D[n] + D[m] / D[n] + common general knowledge / single-document approach]

**Initial read on the chain:** [one short paragraph — is the CPA appropriate (same purpose, similar effect, minimum structural modifications)? Is the distinguishing feature correctly identified against the claim wording? Is the OTP free of hindsight (formulated without reference to the claimed solution)? Is the combination motivated by a pointer in D[n]? Note defects on the face of the OA, but do not develop the rebuttal.]

<!-- DRAFTER: Repeat per Art. 56 OA item. -->

---

## 5. Clarity (Art. 84 EPC)

<!-- DRAFTER: If one or two terms are challenged, use short prose. If the OA raises many clarity points across the claim set, use a small table (issue / wording / type / severity). For each objection cite the OA item number and identify the type per check-art-84-epc. -->

[If no Art. 84 objection: "No Art. 84 objection raised in the OA." and omit the rest of this section.]

[Body — prose or small table, as appropriate. For each objection, cite Guidelines F-IV section and apply the type taxonomy of check-art-84-epc.]

---

## 6. Sufficiency (Art. 83 EPC)

<!-- DRAFTER: Short prose, one paragraph per objection per check-art-83-epc. Identify the alleged defect type (whole-scope sufficiency, undue burden, plausibility under G 2/21, parameter unobtainable, etc.). -->

[If no Art. 83 objection: "No Art. 83 objection raised in the OA." and omit the rest of this section.]

[Body.]

---

## 7. Added matter (Art. 123(2) EPC)

<!-- DRAFTER: One paragraph per amendment objected to, citing the basis as alleged by the Examiner and what the application as filed actually says where you can see it. Apply the Gold Standard of check-art-123-2-epc. Note intermediate-generalisation risk if the amendment is description-sourced. -->

[If no Art. 123(2) objection: "No Art. 123(2) objection raised in the OA." and omit the rest of this section.]

[Body.]

---

## 8. Other grounds

<!-- DRAFTER: Art. 76(1) for divisionals (apply check-art-76-1-epc), formalities (R. 137, R. 161/162, R. 43, Art. 82 unity, two-part form under R. 43(1)), etc. One line per item. If nothing applies, omit the whole section. -->

[Body — one line per item, or omit the section entirely.]

---

## 9. Points for attorney review

<!-- DRAFTER: Bullet list, kept short. Items that need the attorney's decision or that you flagged as inference / tentative / unverifiable. Examples below — adapt to the case. -->

- D[n] not in context — novelty analysis in §3.1 is tentative; please provide D[n] for a definitive read.
- Application as filed not in context — claim interpretation in §3.1 done on the face of the claim wording alone.
- Examiner's OTP in §4.1 appears formulated retrospectively from the claimed solution; worth flagging in the strategy phase.
- Response deadline in §1 computed via `compute-time-limit-epc` under the post-1-November-2023 R. 126(2) / R. 127(2) EPC regime; verify the final date against the EPO closing-days notice for the relevant year (R. 134(1) EPC) and against the docketing system. Confirm whether a R. 132 EPC extension or, if missed, further processing under Art. 121 + R. 135 EPC is to be docketed.
- [Add further items only where attorney input is genuinely needed; do not pad.]
