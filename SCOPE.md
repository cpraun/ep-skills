# Scope of ep-skills

This document states what the plugin is for, what it covers, what it deliberately leaves out, and what it can touch on your machine. For installation and usage see [README.md](README.md).

## Purpose

`ep-skills` supports European patent attorneys in prosecution before the European Patent Office (EPO): understanding Office Actions, planning and drafting responses, checking claims, and handling the documents involved. It works as a paralegal or technical assistant under the supervision of a qualified attorney. Every result is a **working draft for attorney review**, never a final filing.

## Intended users

- European patent attorneys, and paralegal or technical staff working under their supervision.
- Not intended for applicants acting without a professional representative, and not a substitute for legal advice.

## In scope

| Area | What the plugin does | Skills |
| :--- | :--- | :--- |
| Office Actions | Analyzes communications, summarizes them for clients, proposes response strategies, stress-tests a draft response, drafts the response letter, computes EPC time limits | `analyze-oa`, `draft-oa-summary`, `suggest-oa-response-strategies`, `examine-draft-response`, `draft-oa-response`, `compute-time-limit-epc` |
| Checks | Novelty (Art. 54), divisional basis (Art. 76(1)), sufficiency (Art. 83), clarity (Art. 84), added matter (Art. 123(2)), claim formalities (R. 43), pre-filing review, citations against sources | `check-*`, `verify-citations` |
| Claims | Suggests claim combinations to save claims fees (R. 162) and augmented back-references of dependent claims | `suggest-claim-reduction`, `suggest-claim-dependencies` |
| Language | English→German translation with a term map, a consistency and completeness check of a translation, and editing of machine-sounding patent prose | `translate-en-de`, `verify-en-de-translation`, `rewrite` |
| Documents | Reads PDFs with page:line locations (text or OCR); reads and edits Word files with their formatting and tracked changes | `read-pdf`, `handle-docx` |
| Library | Help, learned personal preferences, a case interview before a task, a session context report | `show-help`, `learn`, `grill-me`, `show-context` |
| Agents | An assistant for prosecution work and an examiner simulation for adversarial pre-filing review | `patent-assistant`, `patent-examiner` |

Legal basis: the European Patent Convention (in particular Art. 54, 56, 76(1), 83, 84, 94, 116, 123(2); R. 43, 71(3), 137, 161/162), the Guidelines for Examination and the case law of the Boards of Appeal. Working languages: English and German.

## Out of scope

- **Filing and communication.** The plugin never files with the EPO and never sends anything to the EPO or a client.
- **Other jurisdictions.** USPTO and national prosecution are out of scope. A skill that meets such a request says so and points back to you.
- **Legal advice and decisions.** The attorney decides. Time limits, citations and quotations are for you to verify.
- **Prior-art search.** The plugin works from the documents you supply (OA, claims, application as filed, D-documents). It has no search tool and does not look for prior art.
- **Inventive step as a stand-alone check.** There is no Art. 56 check skill; inventive step is handled inside the Office Action analysis, strategy and examiner-simulation skills.
- **Translation into other languages**, and translation direction German→English.
- **Editing the substance of claims.** `rewrite` changes style only and treats claims, quotations and citations as locked.

Each skill states its own out-of-scope cases and names the skill to use instead.

## Safeguards

- Every skill starts with the same working protocol ([rules/ep-skills.md](rules/ep-skills.md)): state assumptions that change the result, ask instead of guessing, never invent prior art, claim text, passages, dates or citations, do not agree by default, stay in scope.
- `patent-examiner` verifies every EPC, Guidelines and case-law citation on epo.org and marks any it could not verify `[unverified]`.
- `read-pdf` is read-only. Skills write files only when their description says so (for example `translate-en-de` writes the translation, `handle-docx` creates or edits Word files).
- A skill that lacks the input it needs asks for it, or suggests `/grill-me` to settle goals and facts first.

## What the plugin can reach

| | |
| :--- | :--- |
| **Files** | Reads the documents you point it at, in the current project folder (one folder = one case). Writes only as described above. |
| **Network** | None from skills or bundled scripts. The agents `patent-assistant` and `patent-examiner` have `WebFetch`; `patent-examiner` is instructed to use it only to verify citations on epo.org, never to look for prior art. `patent-assistant` is instructed to work from the cited documents and not to introduce further prior art unless asked. |
| **Commands** | `patent-examiner` has `Bash` and is instructed to run only the scripts of `read-pdf` and `handle-docx` and never to create, change or delete files (an instruction, not a technical restriction). The scripts run locally (poppler, tesseract, python-docx). |
| **Hooks, MCP servers** | None. |
| **Personal data on disk** | Learned rules (from `/learn`, in `~/.ep-skills/learned/`) and your own Word template (`~/.ep-skills/template.docx`) lie in your home directory, outside the plugin folder; a plugin update does not remove them. |

`patent-examiner` does not see your conversation; give it explicit paths to the claims, the application as filed and each D-document.

## Confidentiality

Using a skill sends the case documents you give it to the provider of the model that runs it (Anthropic for Claude, Google for Antigravity). Before using the plugin on client matters, make sure this fits your professional secrecy obligations, your client's instructions and your firm's policies, and that the provider's terms are adequate (for example data retention and no training on your data).

## Hosts

Claude Code and the Claude app (Cowork), and Google Antigravity. Some parts are host-specific: `show-context` reports the session in Antigravity and points to the built-in `/context` in Claude Code; `rules/antigravity-tools.md` applies only in Antigravity.

## Status

Pre-1.0. Automated tests cover the checks marked ✓ in the README, `read-pdf` and `handle-docx`; all other skills have been checked by hand. Language models make mistakes: treat every output as a draft. No warranty; see [LICENSE](LICENSE).
