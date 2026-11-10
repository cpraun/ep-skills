---
name: check-art-123-2-epc
description: >-
  Assess whether patent claim text, an amendment, or a feature adds
  subject-matter under Art. 123(2) EPC (Gold Standard: directly and
  unambiguously disclosed). Use for any added-matter, basis, or
  Zwischenverallgemeinerung check. Not Art. 84/54/56/76.
version: "1.0"
---

# Art. 123(2) EPC — Added-Matter Assessment Skill

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

This skill assesses added matter under Art. 123(2) EPC, and nothing else. Out of scope: clarity (Art. 84, use `/check-art-84-epc`), sufficiency (Art. 83, use `/check-art-83-epc`), novelty (Art. 54, use `/check-art-54-epc`), inventive step (Art. 56), divisional basis (Art. 76(1), use `/check-art-76-1-epc`), a full Art. 123(3) analysis, amendments beyond straightforward fall-back reformulations, and national-court or UPC standards.

If the user asks for any of these, deliver the Art. 123(2) assessment first, then answer the out-of-scope part with a single sentence: *"That is outside the scope of /check-art-123-2-epc. To do [X], please use [the appropriate other command/skill] or run a separate request."* Do not silently perform the out-of-scope task. Follow-up questions about the assessment itself are in scope.

## Inputs to gather

> **Insufficient input → `/grill-me`.** A single missing file is simply asked for, as described below. If the input is otherwise not sufficient to execute this skill reliably — goals, strategy or key facts unclear, several documents or answers missing, or the next step would rest on a guess — do not guess and do not proceed on assumptions. Say what is missing and suggest that the user run `/grill-me check-art-123-2-epc` first to settle it, then re-run this skill.

- **The claim, amendment or feature under examination** — required. If the input starts with an `@filename` reference, the claim or feature is the text that follows it. If no amendment is given, ask for it.
- **The application as originally filed** (description, claims, drawings) — required for a definitive finding. Sources, in this order: a document referenced via `@filename`; the application most recently shared in the conversation; a file in the project directory matching `description`, `claims` or `application`. If it is missing, give at most a provisional analysis, state that the finding is UNCERTAIN, and name the passages needed to complete it.
- **The surrounding claim** — optional, for an isolated feature. Ask only if it materially affects the finding.

If no input is given at all, ask for both. If an `@filename` does not resolve, report it and ask for the file another way; do not search the web. If it is unclear which part is the amendment and which the original, ask one focused question. If several amendments are given, ask whether to assess them jointly or separately.

## The legal standard

Gold Standard (G 2/10, point 4.3, following G 3/89 and G 11/91): would the skilled person, using common general knowledge, **directly and unambiguously** derive the amended subject-matter from the application as filed?

- A standard of derivability, not of novelty: the feature must be positively disclosed, not merely not excluded.
- Basis is description + claims + drawings as filed; not the abstract, not the priority document.
- Implicit disclosure counts only if it follows necessarily and directly (T 823/96).
- Common general knowledge fills only what is technically self-evident; it cannot supply a feature that is not disclosed.
- The amendment must not present the skilled person with technical information not directly and unambiguously derivable from the application as filed (G 2/10, point 4.5.1).

## Workflow

Show your reasoning for each step.

1. **Identify the amendment.** Quote the text assessed and its claim context; for an isolated feature, note that the analysis assumes a claim context the user should confirm. Classify the amendment type(s):

   | Type | Amendment |
   |---|---|
   | A | Deletion of a feature |
   | B | Generalisation of a feature |
   | C | Intermediate generalisation (Zwischenverallgemeinerung) |
   | D | Selection from one or more lists |
   | E | Numerical range |
   | F | Added feature |
   | G | Disclaimer (disclosed: G 2/10; undisclosed: G 1/03, G 2/03, G 1/16) |
   | H | Change of claim category |

2. **Identify the basis.** Cite the passages of the application as filed (paragraph, claim, figure) that could support the amendment.
3. **Apply the Gold Standard.** Is the feature explicit or only implicit? If features come from different passages, was the combination presented as a coherent unit, or does it result from independent selections? Is a feature disclosed only within a specific embodiment?
4. **Apply the type-specific tests.** Read the section for each type identified in Step 1 in `references/amendment-types.md` in this skill's directory and apply its tests.
5. **State the finding:** COMPLIANT (cite the basis), NON-COMPLIANT (name the objection, e.g., intermediate generalisation, and suggest a compliant reformulation or fall-back where possible), or UNCERTAIN (state exactly what information is needed). Flag an Art. 123(2)/(3) "inescapable trap" where relevant, without a full Art. 123(3) analysis.

## Output format

```
**Art. 123(2) EPC Assessment**

**Claim / Feature under examination:** [exact text]
**Amendment type:** [e.g., "Intermediate generalisation (Type C)"]
**Identified disclosure basis:** [passages of the application as filed]
**Gold Standard analysis:** [Steps 2–4]
**Finding:** [COMPLIANT / NON-COMPLIANT / UNCERTAIN]
**Basis for finding:** [concise reasoning]
**Recommended action (if non-compliant or uncertain):** [reformulation, fall-back, or information needed]
**Relevant EPO case law:** [decisions relied on]
```
