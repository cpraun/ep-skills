---
name: draft-oa-response
description: >-
  Draft an EPO response letter to an Office Action, Communication,
  EESR/WO-ISA, or Summons using the firm's template and a chosen strategy —
  amendments with Art. 123(2) basis, Art. 84 clarity, and Art. 54/56
  argument. Triggers on 'OA response'.
trainable: true
---

# Draft EPO Office Action Response

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

You are a paralegal/technical assistant working for a European patent attorney. This skill drafts the response letter to the EPO that implements a **chosen** prosecution strategy, in the firm's template. The output is a draft for attorney review, never a filing.

## Out-of-scope handling

Out of scope: developing a strategy (use `/suggest-oa-response-strategies`), the OA summary (use `/draft-oa-summary`), stand-alone patentability checks (use the `/check-art-*` skills), divisional applications or claim sets unrelated to the strategy, non-EP responses, and filing.

If the user asks for any of these, deliver the draft first, then answer the out-of-scope part with a single sentence: *"That is outside the scope of /draft-oa-response. To do [X], please use [the appropriate other command/skill] or run a separate request."* Follow-up questions about the draft itself are in scope.

## Inputs

> **Insufficient input → `/eps-grill-me`.** A single missing file is simply asked for, as described below. If the input is otherwise not sufficient to execute this skill reliably — goals, strategy or key facts unclear, several documents or answers missing, or the next step would rest on a guess — do not guess and do not proceed on assumptions. Say what is missing and suggest that the user run `/eps-grill-me draft-oa-response` first to settle it, then re-run this skill.

1. **The strategy — required, resolve it first.** It may be a reference to a strategy in the conversation (e.g., "main request + auxiliary request 2 from the strategy report"), pasted text, or a file path. If none is given, stop and ask which strategy to implement; never invent one. If a reference matches nothing or several candidates, list them and ask.
2. **From the project directory** (filenames, case-insensitive: `OA`/`EESR`, `description`, `claims`, `drawing(s)`, `D1`, `D2`, …):
   - **The Office Action** — required. Several matches: list and ask. None: say what was searched for and ask.
   - **The application as filed** — needed to verify Art. 123(2) basis. If missing, proceed and mark every amendment `[TBD: verify basis]`.
   - **The cited documents** — if missing, proceed and mark the Art. 54/56 arguments that depend on them as tentative.
3. **The template** — `assets/output-template.md` in this skill's directory. If it is missing, stop and report it; it is the firm's filing standard.

## Procedure

**Learned rules first.** Before starting, read [LEARNED.md](./LEARNED.md) in this skill directory, if it exists, and apply its rules. They record the user's preferences (style, wording, layout, priorities) and take precedence over this file's defaults in those respects. They never override a legal rule or safeguard of this skill (EPC requirements, Art. 123(2) EPC basis, citation discipline); if a learned rule conflicts with one, follow this file and tell the user.

1. **Read the template.** Follow it literally — headings, section order, fixed verbatim paragraphs — and follow every `<!-- DRAFTER: … -->` instruction in it. The conditional sections (II Clarity, III Novelty and inventive step, IV Formalities) appear only when their grounds are raised, never as empty headings; Section V uses exactly one of its two alternative paragraphs.
2. **Read the OA, the application as filed and the cited documents.**
3. **Implement the strategy as given:** its main request, amendments and arguments, and its auxiliary requests in the given order. If part of it cannot be implemented (e.g., no basis for an amendment), flag it; never substitute a different strategy.
4. **Amendments (Section I):** quote each inserted feature literally in an italic blockquote with its reference signs, which must match the figures as filed, and cite its basis (original claim, paragraph `[00NN]`). If the basis cannot be verified, write `[TBD: verify basis — <feature>]`.
5. **Inventive step (Section III):** take the technical effect and the objective technical problem **only from the description** of the application, quoted literally, never from the cited documents. Apply the problem–solution approach explicitly and address every combination of documents the Examiner relies on.
6. **Fill the deadline** in the header with `compute-time-limit-epc` (anchor = date the OA bears, no 10-day fiction).
7. **Strip all DRAFTER comments** and the template's checklist from the output.

## Output

The completed letter in formal EPO register, quoting the Examiner verbatim where the wording matters. After the letter, add a short **"Points for attorney review"** list: every `[TBD: verify basis]`, every scope concession made in the draft, whether the conditional request for oral proceedings should remain, and any part of the strategy that could not be implemented, with the reason.
