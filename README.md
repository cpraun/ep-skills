# EP Skills — EPO Patent Prosecution Plugin

## Description

Assistant tools for European patent attorneys: Office Action analysis, response-strategy drafting, document drafting from templates, claim-set reduction and dependencies, deadline computation, English→German translation, PDF/Word handling, and EPO examiner simulation. Covers prosecution before the European Patent Office under Art. 54, 56, 83, 84, 123(2), and 76(1) EPC, plus formalities and procedural steps under R. 71(3), R. 137, R. 161/162, and Art. 116. This domain-specific skill bundle is usable with Google Antigravity, as well as with the Claude app (Claude Code / Claude Cowork) as plugin `ep-skills`.

## Disclaimer — read before use

- **No legal advice.** Every output of these skills is a working draft for review by a qualified European patent attorney. It is not legal advice and must not be filed or sent to a client without that review.
- **No warranty.** The skills are provided "as is" (see [LICENSE.txt](LICENSE.txt)). Language models make mistakes — in particular, verify every **time limit** (e.g. from `compute-time-limit-epc`) against the EPO communication and your docketing system, and every **citation** of the EPC, the Guidelines, case law or a document against its source.
- **Confidentiality.** Using a skill sends the case documents you give it to the provider of the model that runs it. Before using the skills on client matters, make sure this is compatible with your professional secrecy obligations, your client's instructions and your firm's policies, and that the provider's terms are adequate (e.g. data retention, no training on your data).

## Skills

The bundle groups into three kinds. **`check-*`** skills are single-purpose checks; those marked ✓ have a test suite under [`test/`](test/) (see *Testing the skills*). **`draft-*`** skills produce text from a firm template. Every other skill supports the attorney in analyzing and understanding a case, or is a library tool (`eps-*`, `util-*`). One project folder holds one case; skills find documents by filename (`OA`, `EESR`, `claims`, `description`, `D1`, …) before asking.

**`eps-*` skills are command only** (`disable-model-invocation: true`): call them explicitly, e.g. `/eps-help`; the model never invokes them on its own. The **`util-*`** skills are the opposite: the model loads them only when you refer to a PDF or Word file (see *Document handling*).

### `check-*` — checks

| Skill | Purpose | Tests |
| :--- | :--- | :---: |
| [`check-art-54-epc`](skills/check-art-54-epc/) | Novelty against a single prior-art document (Art. 54 EPC) | ✓ |
| [`check-art-76-1-epc`](skills/check-art-76-1-epc/) | Divisional basis in the parent as filed (Art. 76(1) EPC) | ✓ |
| [`check-art-83-epc`](skills/check-art-83-epc/) | Sufficiency of disclosure (Art. 83 EPC) | ✓ |
| [`check-art-84-epc`](skills/check-art-84-epc/) | Clarity and conciseness of the claims (Art. 84 EPC) | ✓ |
| [`check-art-123-2-epc`](skills/check-art-123-2-epc/) | Added subject-matter (Art. 123(2) EPC) | ✓ |
| [`check-claim-formalities-epc`](skills/check-claim-formalities-epc/) | Claim formalities — antecedent basis, numbering, dependencies, independent-claim count (Rule 43 EPC) | ✓ |
| [`check-pre-filing-epc`](skills/check-pre-filing-epc/) | Pre-filing review of a draft application (US, DE or in-house) to be filed at the EPO: formalities, claims, Art. 83/84/123(2), COMVIK, search-stage risks, fees, technical effects | |
| [`check-citations`](skills/check-citations/) | Verifies every quote, paragraph/page reference and claim wording in a draft against its sources | ✓ |

### `draft-*` — template-based drafting

| Skill | Purpose |
| :--- | :--- |
| [`draft-oa-summary`](skills/draft-oa-summary/) | Client-facing preliminary review of an Office Action, from the summary template |
| [`draft-oa-response`](skills/draft-oa-response/) | EPO response letter to an Office Action, from the response template |

### Analysis and case-understanding support

| Skill | Purpose |
| :--- | :--- |
| [`analyze-oa`](skills/analyze-oa/) | Initial item-by-item analysis of an Office Action with per-claim novelty tables |
| [`suggest-oa-response-strategies`](skills/suggest-oa-response-strategies/) | Strategic Analysis Report of response options via a panel-of-experts simulation |
| [`suggest-claim-reduction`](skills/suggest-claim-reduction/) | Table of suggested dependent-claim combinations ("or" / "and optionally") to reach ~15 claims and save Rule 162 EPC claims fees |
| [`suggest-claim-dependencies`](skills/suggest-claim-dependencies/) | Suggested augmented back-references of dependent claims, each supported by cited passages of the application as filed |
| [`examine-draft-response`](skills/examine-draft-response/) | Examiner-side stress-test of a proposed response strategy; simulates the next OA |
| [`compute-time-limit-epc`](skills/compute-time-limit-epc/) | Computation of EPC deadlines from an event date |

### Translation and writing

| Skill | Purpose |
| :--- | :--- |
| [`translate-en-de`](skills/translate-en-de/) | English→German translation of claims or a description, with a one-to-one term map; takes a file path or the text as argument |
| [`check-en-de-translation`](skills/check-en-de-translation/) | English→German translation consistency and completeness check |
| [`humanize`](skills/humanize/) | Rewrites AI-sounding text so it reads like careful human writing, keeping meaning, facts and terminology; takes a file path or the text as argument |

### Case preparation and library tools

| Skill | Purpose |
| :--- | :--- |
| [`eps-help`](skills/eps-help/) | Brief help on any skill or agent of the library, or answers to questions about it (e.g. which skills are trainable); command only |
| [`eps-learn`](skills/eps-learn/) | Records your corrections and preferences from a session as learned rules of a trainable skill (see *Learned rules*); command only |
| [`eps-context`](skills/eps-context/) | Session context usage — computed in Antigravity; in Claude Code it points to the built-in `/context`; command only |
| [`eps-grill-me`](skills/eps-grill-me/) | Interviews the attorney, one question at a time, until the documents, goals and facts needed for a task are clear; ends with a confirmed case brief. Other skills suggest it when their input is insufficient; command only |

### Document handling

| Skill | Purpose |
| :--- | :--- |
| [`util-pdf`](skills/util-pdf/) | Read-only PDF text extraction (text layer or OCR via local poppler/tesseract) with page:line and paragraph locations for exact citations |
| [`util-docx`](skills/util-docx/) | Create and edit Word (.docx) files while preserving the original formatting; new files from your own `assets/template.docx` (git-ignored) or the shipped `template-sample.docx` |

Both use the `util-` prefix so that they do not collide with the host's own `pdf` / `docx` skills. They are loaded only when a PDF or Word file is involved: when you refer to one, or when `translate-en-de`, `check-en-de-translation`, `check-citations`, `eps-grill-me` and `examine-draft-response` load them to read Word and PDF files.

### Learned rules

Skills marked `trainable: true` (`analyze-oa`, `draft-oa-summary`, `draft-oa-response`, `suggest-oa-response-strategies`, `check-pre-filing-epc`, `translate-en-de`, `eps-grill-me`) read a `LEARNED.md` in their folder, if present, and apply your recorded preferences — style, wording, layout, priorities — but never in place of a legal rule or safeguard. `/eps-learn <skill>` writes these rules after you select them. `LEARNED.md` files are personal and may contain case details, so they are excluded from git (`.gitignore`); each user builds their own. `/eps-help which skills can learn?` lists the trainable skills and their rule counts.

## Requirements

- **Claude Code / Claude Cowork** or **Google Antigravity**.
- **Python 3** for the bundled helper scripts.
- For `util-pdf` (macOS/Linux via Homebrew): `brew install poppler tesseract`, plus `brew install tesseract-lang` for OCR of German, French and other non-English documents.
- For `util-docx`: `pip install python-docx`. Optionally place your own Word template at `skills/util-docx/assets/template.docx` (excluded from git; see `assets/CUSTOMIZE.txt`).
- Antigravity, to run the `util-pdf` / `util-docx` tools and use `.antigravity_tmp/` without approval prompts: add these entries to the allow list (App: Settings > Global Permissions; CLI: `permissions.allow` in `~/.gemini/antigravity-cli/settings.json`):

  ```text
  command(regex:python3 \S*/util-pdf/scripts/pdf_extract\.py( .*)?)
  command(pdfinfo)
  command(pdftotext)
  command(pdftoppm)
  command(tesseract)
  write_file(.antigravity_tmp/)
  ```

  Running `util-docx` code means running Python the agent writes itself, which an allow-list entry can only permit broadly (`command(python3)`); decide whether you want that.

## Installation

Clone the repository, then register the folder with your host:

```sh
git clone https://github.com/cpraun/ep-skills.git

# Antigravity
agy plugin install /path/to/ep-skills

# Claude Code (CLI or VS Code)
claude plugin marketplace add /path/to/ep-skills
claude plugin install ep-skills@ep-skills
```

In the Claude desktop app (Cowork), open **Customize → Plugins → Add → Add marketplace → Add from a repository**, enter `cpraun/ep-skills`, and install `ep-skills`. Skills are then called as `/ep-skills:<skill>`, agents as `@ep-skills:patent-examiner`. To update, run `git pull`, then install again in Antigravity or run `/reload-plugins` in Claude Code. Complete the setup under *Requirements* above.

## Agents and personas

Two personas run through the library. Each skill that uses one states it briefly; the full persona lives in `agents/` as a subagent:

- **Patent assistant** — drafts and reviews claims, amendments and arguments, and analyzes EPO communications. Used by `analyze-oa`, `draft-oa-summary`, `suggest-oa-response-strategies` and `draft-oa-response`; subagent `@ep-skills:patent-assistant`.
- **EPO examiner** — applies the EPC and the Guidelines strictly, raising objections under Art. 54, 56, 83, 84 and 123(2) without proposing amendments. Used by `examine-draft-response`; subagent `@ep-skills:patent-examiner`.

Claude also selects a subagent automatically when a request matches its `description`.

**Subagent or skill?** `examine-draft-response` stress-tests a strategy you have formed, in your conversation. The `patent-examiner` subagent examines the claims as they stand, in its own context, so it cannot be anchored by the arguments you hope will succeed. Use it for an adversarial pre-filing read of a claim set.

**Constraints of `patent-examiner`.** It runs on the session's model with `tools: [Read, Grep, Glob, WebFetch, Bash]` and the skills `util-pdf` and `util-docx` preloaded, so it reads PDF and Word files and cites them by page:line and paragraph. It is instructed to use `Bash` only for these skills' scripts and never to create, change or delete files — an instruction, not a technical restriction. It uses `WebFetch` only to verify its EPC, Guidelines and case-law citations on epo.org, never to search for prior art, and marks every citation it could not verify `[unverified]`. It does not see your conversation: give it explicit paths to the claims, the application as filed and each D-document.

## Development

### Manifests and pre-commit hook

| Path | Read by |
| :--- | :--- |
| `plugin.json` | Google Antigravity |
| `.claude-plugin/plugin.json` | Claude Code / Claude Cowork |
| `.claude-plugin/marketplace.json` | Claude Code / Claude Cowork — lists this repo as marketplace `ep-skills` |

The two `plugin.json` files must stay byte-identical; neither host reads the other's copy, so a version bump in only one diverges silently. A `pre-commit` hook in `.githooks/` (distinct from `hooks/`, which Claude reserves for `hooks/hooks.json`) blocks a commit if the staged manifests differ or only one is tracked, and if a skill's working protocol differs from its master. Activate it once per clone:

```sh
git config core.hooksPath .githooks
```

### Working protocol and rules

Every skill starts with the same short working protocol: state the assumptions that change the result, ask instead of guessing, do not agree by default, stay in scope, write short sentences with one term per concept. The master is [`rules/ep-skills.md`](rules/ep-skills.md), which Antigravity loads as a rule. Claude does not load `rules/`, so each `SKILL.md` carries a copy between `<!-- protocol:begin -->` and `<!-- protocol:end -->`; edit the master, then copy the block into every skill. [`rules/antigravity-tools.md`](rules/antigravity-tools.md) applies only in Antigravity: run the `util-pdf` / `util-docx` tools without asking and keep temporary files in `.antigravity_tmp/` (Antigravity's own prompts follow its permission settings, see *Requirements*).

When a persona changes in substance, check that the short statements in the skills that use it still agree with the agent file; no include mechanism keeps them in sync.

### Testing the skills

The skills are prompts, so each test is an *eval*: it runs a model with the skill loaded and checks the output against deterministic string/regex gates — mandated structure, the out-of-scope refusal, no Art. 56 drift, asking for missing input instead of inventing it. Each failure names the `SKILL.md` rule it violated. The gates check shape and scope, not whether the legal conclusion is right. The harness runs against **Gemini** (default) or **Claude**, set by `MODEL_PROVIDER` in `test/env.sh` (gitignored, holds your key); each scenario costs one model call.

```sh
source test/env.sh
pytest test/                            # every suite
pytest test/check-art-54-epc            # one skill
pytest test/ -k mosaicking              # one scenario

# no model call, no API key:
pytest test/util-docx test/util-pdf test/check-citations -k 'not test_gates'
```

Automated tests exist for the skills marked ✓ in the `check-*` table and for `util-docx` and `util-pdf`; the other skills have been checked manually. Setup, the `expected.yaml` fields, the deterministic suites and how to write a scenario are in **[test/README.md](test/README.md)**.

## Acknowledgments

This package was developed by Christoph von Praun (<praun@alumni.ethz.ch>), with contributions from Mauritius Klein and Christian Hofstetter, and with the help of [Claude](https://claude.com/claude-code) (Anthropic).
