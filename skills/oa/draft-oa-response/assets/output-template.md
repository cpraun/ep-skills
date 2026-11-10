<!--
SCAFFOLD TEMPLATE — `output-template.md`
Mirrors the firm's standard structure for an EPO response letter
(ONLINE FILING header, five Roman-numeral sections, concluding remarks,
enclosures). Bracketed `[...]` items are placeholders to be filled in by
the assistant. HTML comments marked `DRAFTER:` carry guidance on which
blocks to keep, adapt, or omit for the case at hand and must be removed
from the final filing. The `draft-oa-response` skill consumes this
template and produces a draft response letter to the EPO.
-->

**ONLINE FILING**

European Patent Office
80298 Munich
<!-- DRAFTER: For Examining Divisions in The Hague, replace the address with:
2280 HV Rijswijk
NETHERLANDS -->

*DRAFT — to be filed by* [response deadline]

European Patent Application [application number]
"[title of patent application]"
[applicant]
Our File: [internal reference]

---

In response to [title of the OA / Communication / Summons] dated [date of the OA]:

<!-- DRAFTER: Adapt the following paragraph to what is actually submitted in this filing (claims only; claims + description; main + auxiliary requests; clean copy only vs. clean + annotated). Adjust the claim ranges (new claims X–Y vs. originally filed claims 1–M). -->

An amended set of claims [1–N] is herewith submitted which should replace the claims on file. The new claims are enclosed as a clean copy and an annotated version, in which annotations show differences from claims [1–M] as originally filed ("original claims" in the following). [In addition, an amended description is submitted.]

---

<!-- DRAFTER: Include section I whenever amendments are filed (the standard case). If no amendments are filed, omit this section entirely. -->

# I. New claims and their original disclosure

<!-- DRAFTER: Keep the following paragraph verbatim. -->

Amendments discussed in the following should not be construed as acquiescence to the assertions set forth by the Examining Division and are being submitted solely to expedite prosecution of this application.

<!-- DRAFTER: For each amended independent claim, indicate the source(s) in the originally filed application (claims and/or description paragraphs), quote the inserted feature literally in italics, and explain any cancellations. Repeat the block as needed for further amended claims. -->

New claim [X] is based on original claims [...] [and on paragraph [00NN] of the description] and includes the following amendments:

> *"…[literal text of the inserted feature, with reference signs preserved]…"*

[Original claim [Y] has been cancelled to avoid redundancy.]

[New independent claim [Y] (original claim [Z]) has been amended to perform the method of any of claims [1–N].]

No new matter is added by these amendments, so that the new claims meet the requirements of Art. 123(2) EPC.

<!-- DRAFTER: Keep the following paragraph verbatim. -->

Any subject matter deleted as a result of the amendment is not to be construed as an abandonment of such subject matter. Specifically, the applicant reserves the right to pursue such subject matter in a divisional application.

---

<!-- DRAFTER: Include section II only if the OA / Summons raises clarity objections under Art. 84 EPC. Otherwise omit it entirely (do not leave an empty heading). -->

# II. Clarity

Under [item ... of the WO-ISA / point ... of the OA / point ... of the Summons], the Examiner submits that [original claim(s) ...] are not clear pursuant to Article 84 EPC. In particular, it is alleged that [the term *"…"* is vague and unclear / state the alleged ambiguity, quoting the OA literally].

<!-- DRAFTER: Either show how the amendment imports clarifying language from the description / a dependent claim, or argue that the term is clear when read with a mind willing to understand, citing the description literally. -->

New independent claims [X and Y] have been amended [as suggested by the Examiner] and respectively include the definition of [...] from original claims [...]. [Alternatively: the term *"…"* is clear when read in light of paragraph [00NN] of the description, which states: *"…[literal quote]…"*.]

Thus, new claims [X and Y] fulfill the requirements of Article 84 EPC.

---

<!-- DRAFTER: Include section III only if the OA / Summons raises novelty (Art. 54 EPC) and/or inventive-step (Art. 56 EPC) objections. Build the rebuttal on the strategy selected in `suggest-oa-response-strategies`. Quote literally; do not paraphrase technical features. -->

# III. Novelty and inventive step

The Examiner alleges under [item ... of the WO-ISA / point ... of the OA / point ... of the Summons] that claim [X] [is not novel pursuant to Article 54 EPC over the cited reference D1 / does not involve an inventive step pursuant to Article 56 EPC over D1 in combination with D2].

Applicant respectfully disagrees.

## Distinguishing features

D[1] fails to disclose the following features of Claim [X]:

> **F1**: *"…[literal feature text from the claim]…"*

> **F2**: *"…[literal feature text from the claim]…"*

<!-- DRAFTER: For each distinguishing feature, identify the passage of D1 relied on by the Examiner, quote what that passage actually discloses, and explain why it does not disclose F-i. -->

Regarding **F1**, the Examiner cites [Figure ... / paragraph [00NN] / page ... of D1]. However, [identified passage] of D1 does not disclose [F1]. Rather, paragraph [00NN] of D1 discloses: *"…[literal quote]…"*. This disclosure refers to [...], not [the feature required by F1].

Regarding **F2**, [analogous treatment].

Thus, new claim [X] is novel over D[1] according to Art. 54 EPC.

## Technical effect and objective technical problem

<!-- DRAFTER: Source the technical effect and the OTP from the description of the Application under Examination — never from the cited documents. Use literal quotes in italics. -->

Paragraph [00NN] of the description describes the overall challenge in the technical field, namely:

> *"…[literal quote stating the problem]…"*

[Furthermore, Paragraph [00NN] of the description states: *"…[further supporting quote]…"*.]

The distinguishing features provide the advantage and technical effect as described in paragraph [00NN] of the description:

> *"…[literal quote stating the technical effect]…"*

The objective technical problem could thus be phrased as how to [OTP formulation derived from the technical effect].

## Could-would assessment (Art. 56 EPC)

The claimed subject matter solves the objective technical problem by the distinguishing features, namely [F1] and [F2], such that *"…[literal quote from the description showing how the features solve the OTP]…"* (see paragraph [00NN] of the description).

D[1] does not teach or suggest the above-mentioned distinguishing features [F1] and [F2] of new claim [X]. Namely, D[1] does not provide any hint about [F1], nor does it suggest [F2].

Reference D[1] cannot render the claimed solution obvious to the skilled person. D[1] teaches [a different mechanism — describe with literal citation], rather than [the mechanism required by the distinguishing features]. Specifically, paragraph [00NN] of D[1] discloses: *"…"*. [Furthermore, paragraph [00NN] of D[1] discloses: *"…"*.] Therefore, D[1] solves the problem by [different approach], which is technically [unrelated / contrary] to [the claimed approach].

There is no indication in D[1] that would prompt the skilled person to abandon [its mechanism] in favor of [the claimed mechanism]. Doing so would go against the teaching of D[1], which relies on [...]. Consequently, D[1] does not solve the objective technical problem of [OTP].

<!-- DRAFTER: If the Examiner combines D1 with D2 (or further documents), address each combination explicitly with literal citations. -->

When considering D[2] as a combination document, the skilled person learns about [...] (paragraph [00NN]). However, D[2] discloses that this information is used to [...] (paragraph [00NN]):

> *"…[literal quote from D2]…"*

Clearly, D[2] would not be of further help to the skilled person to conceive the claimed subject matter, as D[2] directs the skilled person to [different approach], rather than [the claimed mechanism].

Therefore, when studying the teachings of D[1] alone or in combination with D[2], the skilled person would not get any hint or incentive on how to [arrive at the distinguishing features].

<!-- DRAFTER: Briefly dispose of any "A" references (general state of the art) that the search report cites without particular relevance. -->

Documents D[3], D[4], and D[5] are cited as "*A* document" defining the general state of the art and not being of particular relevance. D[3] relates to [...], D[4] relates to [...], and D[5] relates to [...]. None of these documents disclose or suggest [the distinguishing features F1 and F2].

Therefore, new claim [X] involves an inventive step within the meaning of Article 56 EPC.

[Corresponding arguments apply to independent claim [Y], *mutatis mutandis*.]

---

<!-- DRAFTER: Include section IV if formal objections are raised, or if the description has been amended (e.g., to acknowledge cited references, to remove inconsistencies, or to bring the description into conformity with amended claims). Otherwise omit. -->

# IV. Formalities

The description is brought into conformity with the amended claims.

[The description has been amended to acknowledge references D1 – D[N] in the background section. It is therefore kindly requested not to insist upon the two-part form of the independent claim in accordance with the Guidelines for Examination in the EPO, Part F-IV, 2.3.2.]

[Address any further formal objections raised in the OA, e.g. unity (Art. 82 EPC), Rule 43 EPC issues, etc.]

---

# V. Concluding remarks

<!-- DRAFTER: Section V is mandatory in every response. Choose EXACTLY ONE of the two paragraphs below — the first if responding to a Summons to oral proceedings, the second if responding to any other communication. Delete the unused paragraph and its DRAFTER comment. -->

<!-- DRAFTER: Use this paragraph when responding to a Summons to oral proceedings. -->

The applicant believes that the subject-matter of the claims is now in a state acceptable for grant. An amended description will be filed if the ED agrees on an allowable set of claims. Should the ED, nevertheless, still see deficiencies in the documents on file, it is kindly asked to give the Applicant the opportunity to file further arguments and, if necessary, amendments. Minor issues could be discussed by telephone.

<!-- DRAFTER: Use this paragraph when responding to any other office action (NOT a Summons). -->

All objections raised in the [title of the OA] are addressed. Applicant is of the opinion that the new claims meet the requirements of the EPC. Should the Examiner still see any deficiencies, it is suggested to discuss these matters in a telephone consultation or a personal interview. As a matter of precaution, oral proceedings are requested.

Respectfully,

[Name]
European Patent Attorney
[Reg. No.]

---

**Enclosures**

Amended set of claims [1 to N] (annotated and clean copy)
[Amended description (annotated and clean copy)]

<!--
Drafter checklist before filing:
- Section I is included whenever amendments are filed.
- Section II is included only if clarity objections (Art. 84 EPC) are raised.
- Section III is included only if novelty (Art. 54 EPC) and/or inventive-step (Art. 56 EPC) objections are raised.
- Section IV is included only if formal objections apply or the description has been amended.
- Section V contains EXACTLY ONE of the two alternative paragraphs (Summons vs. other OA).
- Every amendment has verified literal Art. 123(2) EPC basis (page/line or paragraph), confirmed against the application as filed.
- Every cited prior-art passage has been checked verbatim against the source document.
- Reference signs in claim quotations match the latest figures.
- The deadline is correct in the docketing system; further-processing risk has been considered (Art. 121 EPC).
- The conditional oral-proceedings request is present where appropriate (Art. 116 EPC).
- All `<!-- DRAFTER: … -->` comments and unused alternative paragraphs have been removed.
-->
