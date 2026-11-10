---
name: rewrite
description: >-
  Edit machine-sounding patent-practice prose (response letters, arguments,
  Office Action summaries, client letters, reports) so it reads like a careful
  attorney wrote it, without touching claims, quotations, citations, numbers or
  defined terms. Invoked as /rewrite with a file path or the text.
disable-model-invocation: true
---

# Editing machine-sounding patent prose

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

This skill edits prose that a language model wrote, or that sounds as if it did, so that it reads like the work of a careful patent attorney. It changes style only. Meaning, legal position and every protected item stay as they are. The input is the argument ($ARGUMENTS), which is a file path or the text itself, or text in the user's message. Read `.docx` files with `handle-docx` and `.pdf` files with `read-pdf`.

## Out-of-scope handling

Out of scope: translation (use `/translate-en-de`), verifying quotations or citations (use `/verify-citations`), legal or technical review, amending or shortening claims, and changing a position or adding arguments.

If the user asks for any of these, edit the style first, then state: *"That is outside the scope of /rewrite. To do [X], please use [the right skill]."*

## What may be edited

| Zone | Text | Treatment |
| :--- | :--- | :--- |
| Open | Letters to the EPO or a client, arguments, Office Action summaries, strategy reports, e-mails, cover notes | Edit for style |
| Careful | Description passages of an application | Style only. No change to a term, feature, number or relation; each sentence keeps its scope (Art. 123(2) EPC) |
| Locked | Claims, quotations, quoted passages, reference signs, feature tables, template headings and fixed paragraphs, references to provisions, case law and documents (Art. 56 EPC, T 0641/00, D1, [0023]), numbers, dates, deadlines, names | Copy unchanged. If a locked item has a style fault, report it in the note and leave it |

Treat claims and tables as locked unless the user names them.

## Two rules that differ from general editing

**A term never varies.** Advice for lively prose is to rotate synonyms. In patent text it is the reverse: one term for one concept from first mention to last, so "closure member" never becomes "valve element". If the text already varies a term, do not pick one; report it in the note.

**The actor stays visible.** In arguments say who submits, objects or holds ("The Applicant submits", "The Examiner holds"). Where "it is considered" hides the actor and the text shows who it is, name the actor. Where it does not, leave the sentence and report it.

## Method

1. Read the whole text. Settle the reader (Examiner, client, colleague), the language (English or German; keep it) and the register. EPO submissions are formal, without contractions or rhetoric.
2. List the locked items and the terms in use, each with its places.
3. Find the faults below. Cut a pattern only where it carries no information.
4. Edit one paragraph at a time, then read the full result once for flow.
5. Reconcile with the original: every number, date, reference sign, citation, quotation and term must appear as before, in the same count. No new fact, argument or qualifier may appear, and no hedge that reflects real uncertainty may disappear. Correct any difference before you answer.

## Faults to remove

- **Ceremony:** greetings and good wishes; announcing what the text will do before doing it; a closing paragraph that restates the conclusion.
- **Stacked hedges:** "may possibly", "could potentially", where the position is in fact firm.
- **Reflex structure:** a list of three because three sounds complete; "not only … but also"; every paragraph opening with a label sentence; bullets for reasoning that is an argument.
- **Connective chains:** Moreover, Furthermore, Additionally (German: Zudem, Darüber hinaus, Des Weiteren) where the link is obvious.
- **Empty emphasis:** "crucial", "it should be pointed out that", "truly", "in any meaningful way". Give the concrete reason or cut.
- **Noun-heavy sentences:** "the implementation of the determination of the load" becomes "determining the load". German: "die Durchführung einer Prüfung" becomes "prüfen".
- **Even rhythm:** a series of sentences that are built alike and are equally long. Prefer short sentences, and let the length vary.

## Handing back

- Give the full edited text, in the language and format of the input, with no preface.
- For a `.docx`, produce tracked changes with `handle-docx` only if the user asks. Save to a new file; never overwrite the original.
- After the text, add a note of at most five lines, only for points that need the attorney's decision: locked items with faults, terms that vary, actors that stay unclear, statements that look unsupported or inconsistent with the rest. Do not resolve these yourself.
- The result is a draft for the attorney.

## Example

Original: "It should be pointed out that D1 does not truly disclose a closure member in any meaningful way. Furthermore, it should be emphasised that the valve element of claim 1 offers a significantly improved sealing effect."

Edited: "D1 does not disclose a closure member. The valve element of claim 1 seals significantly better."

Note: "Closure member" and "valve element" may name one component; left as written.

## Never

- Invent facts, arguments, citations or passages, or make a position stronger or weaker.
- Add errors, slang or contractions to look human. The aim is clearer prose.
