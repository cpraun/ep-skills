---
name: check-art-76-1-epc
description: >-
  Assess whether a European divisional's claims are directly and
  unambiguously derivable from the parent application as filed under Art.
  76(1) EPC — basis, filing date, intermediate generalisation. Divisional
  basis. Not Art. 123(2), 84, 54/56.
---

# Art. 76(1) EPC — Divisional-Basis Assessment Skill

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

This skill checks whether each claim of a European divisional application, feature by feature and as a combination, is directly and unambiguously derivable from the earlier (parent) application as filed — Art. 76(1), second sentence, EPC. It does nothing else. Out of scope: Art. 123(2) for amendments within the same application (use `/check-art-123-2-epc`), Art. 123(3), the formalities of Art. 76(1), first sentence (pendency, designations, fees), novelty (use `/check-art-54-epc`) and inventive step, clarity (use `/check-art-84-epc`), sufficiency (use `/check-art-83-epc`), and drafting amendments, fall-back claims or auxiliary requests: the skill identifies the gap, it does not remedy it.

If the user asks for any of these, deliver the basis assessment first, then answer the out-of-scope part with a single sentence: *"That is outside the scope of /check-art-76-1-epc. To do [X], please use [the appropriate other command/skill] or run a separate request."* Do not silently perform the out-of-scope task. Follow-up questions about the assessment itself are in scope.

## Inputs to gather

> **Insufficient input → `/eps-grill-me`.** A single missing file is simply asked for, as described below. If the input is otherwise not sufficient to execute this skill reliably — goals, strategy or key facts unclear, several documents or answers missing, or the next step would rest on a guess — do not guess and do not proceed on assumptions. Say what is missing and suggest that the user run `/eps-grill-me check-art-76-1-epc` first to settle it, then re-run this skill.

1. **The divisional claim(s)** — process exactly the claims named.
2. **The earlier application as filed** (description, claims, drawings). Without it, no assessment is possible: ask for it and do not assess. If the user supplies the **granted patent** or a later amended version of the parent, stop and ask for the application as filed; do not assess on the granted text. A published A-document is acceptable if it corresponds to the parent as filed.
3. **Every earlier application in the chain**, for a divisional of a divisional. Basis must exist in *each* earlier application as filed, back to the root (G 1/05, G 1/06). Ask for any missing link.
4. **The drawings.** If missing, proceed and flag drawing-only support as unverifiable.
5. **The Art. 76(1) objection raised**, if any — optional; use it to prioritise.

Do not search the web for the parent unless the user explicitly authorises it.

## The legal standard

The Gold Standard of G 2/10 applies under Art. 76(1) as under Art. 123(2); both provisions follow the same principles (G 1/05, G 1/06): the skilled person, using common general knowledge, must **directly and unambiguously** derive each feature and the specific combination claimed from the parent as filed.

- The parent must positively disclose the subject-matter; absence of contradiction is not enough. The abstract and the priority document are not part of the basis.
- Implicit disclosure counts only if the implication is necessary and direct (T 823/96).
- The divisional must not present the skilled person with technical information not directly and unambiguously derivable from the parent as filed (G 2/10, point 4.5.1).
- If basis is missing, it is missing: no hedging about what the parent "would suggest".

## Workflow

1. **Decompose** each claim into features M1, M2, … at EPO examiner granularity. For dependent claims, list only the additional features (e.g., "M3.1: … [from claim 3]").
2. **Interpret** a feature only where its wording is ambiguous or differs from the parent's terminology: one sentence, informed by the parent, without importing limitations. Otherwise omit this section.
3. **Map each feature to the parent** with a precise citation (paragraph, page and line, claim, figure and reference sign) and assess it:
   - **Yes** — directly and unambiguously derivable from a specific passage
   - **No** — not disclosed
   - **Implicit** — necessarily and directly read by the skilled person; say why
   - **Drawings only** — basis only in a drawing; admissible if the skilled person derives it directly and unambiguously (T 169/83). Always flag it for the attorney.
   - **Partial / intermediate generalisation** — something close is disclosed, but not the feature at the claimed level of generality; spell out the gap. In most cases this means no basis as claimed.
4. **Check the combination.** Is the specific combination claimed disclosed as a coherent unit in the parent?
   - **Intermediate generalisation** — a feature lifted from an embodiment without the features the parent presented as inseparable from it.
   - **Multiple independent selections** — one item from list A and one from list B, not presented together in the parent (T 727/00, T 686/99). A "particularly preferred" pointer must be in the parent itself.
   - **Chain divisionals** — repeat the check against each earlier application; a combination missing in any link breaks the chain.
   - For ranges, generalisations, disclaimers, a Euro-PCT parent or dropped reference signs, read the matching section of `references/special-cases.md` in this skill's directory.
5. **Cross-check before delivering.** Every Yes / Implicit / Drawings only has a citation. The basis is the parent **as filed**, not as granted. No novelty or inventive-step reasoning: if you are about to write "obviously combine", "straightforward to modify" or "would arrive at", stop. No remedial wording.

## Output format

Tabular per claim, English, no executive summary, no remedial section, no general remarks at the end. Use exactly the five columns below, also for chain divisionals: name each earlier application inside the cells (e.g., Citation "D1 [0015]; P: none"), never as additional columns.

```
# Art. 76(1) EPC — Divisional-Basis Assessment

**Claim(s) analysed:** [list]
**Earlier application(s):** [parent; for chain divisionals, each link from immediate parent to root]
**Disclosure basis used:** [description + claims + drawings of the earlier application(s) as filed]

## Claim interpretation (only if relevant features need it)

[brief notes; omit section if all features self-explanatory]

## Claim 1 [label, e.g., "(independent, apparatus)"]

| Feature | Claim wording | Basis in earlier application | Citation | Assessment |
|---|---|---|---|---|
| M1 | … | … | … | Yes / No / Implicit / Drawings only / Partial — [one-sentence justification] |
| M2 | … | … | … | … |

**Combination check:** [2–4 sentences: is the specific combination disclosed as a coherent unit; any intermediate generalisation, multiple selection, range or generalisation issue]

**Conclusion:** Claim 1 [complies / does not comply / status uncertain] with Art. 76(1) EPC. [Brief reasoning citing M-numbers and passages; for chain divisionals, state that each earlier application was checked.]

## Claim N …

[as above for each requested claim]
```
