# EP Skills — European Patent Prosecution Plugin

## Description

Assistant tools for European patent attorneys: Office Action analysis, response-strategy drafting, document drafting from templates, claim-set reduction and dependencies, deadline computation, English→German translation, PDF/Word handling, and EPO examiner simulation. Covers prosecution before the European Patent Office under Art. 54, 56, 83, 84, 123(2), and 76(1) EPC, plus formalities and procedural steps under R. 71(3), R. 137, R. 161/162, and Art. 116. This domain-specific skill bundle is usable with Google Antigravity, as well as with the Claude app (Claude Code / Claude Cowork) as plugin `ep-skills`. What the plugin covers, what it leaves out and what it can reach on your machine is stated in [SCOPE.md](SCOPE.md).

## Disclaimer — read before use

- **No legal advice.** Every output of these skills is a working draft for review by a qualified European patent attorney. It is not legal advice and must not be filed or sent to a client without that review.
- **No warranty.** The skills are provided "as is" (see [LICENSE](LICENSE)). Language models make mistakes — in particular, verify every **time limit** (e.g. from `compute-time-limit-epc`) against the EPO communication and your docketing system, and every **citation** of the EPC, the Guidelines, case law or a document against its source.
- **Confidentiality.** Using a skill sends the case documents you give it to the provider of the model that runs it. Check this against your professional secrecy obligations before using the skills on client matters; details in [SCOPE.md](SCOPE.md#confidentiality).

## Skills

The bundle groups into three kinds. **Checks** (`check-*` and `verify-citations`) are single-purpose; those marked ✓ have a test suite under [`test/`](test/) (see *Testing the skills*). **`draft-*`** skills produce text from a firm template. Every other skill supports the attorney in analyzing and understanding a case, or is a library tool (`show-help`, `learn`, `grill-me`, `show-context`, `read-pdf`, `handle-docx`). One project folder holds one case; skills find documents by filename (`OA`, `EESR`, `claims`, `description`, `D1`, …) before asking.

**`show-help`, `learn`, `grill-me`, `show-context` and `rewrite` are command only** (`disable-model-invocation: true`): call them explicitly, e.g. `/show-help`; the model never invokes them on its own. The file tools `read-pdf` and `handle-docx` are the opposite: the model loads them only when you refer to a PDF or Word file (see *Document handling*).

### Checks

| Skill | Purpose | Tests |
| :--- | :--- | :---: |
| [`check-art-54-epc`](skills/check/check-art-54-epc/) | Novelty against a single prior-art document (Art. 54 EPC) | ✓ |
| [`check-art-76-1-epc`](skills/check/check-art-76-1-epc/) | Divisional basis in the parent as filed (Art. 76(1) EPC) | ✓ |
| [`check-art-83-epc`](skills/check/check-art-83-epc/) | Sufficiency of disclosure (Art. 83 EPC) | ✓ |
| [`check-art-84-epc`](skills/check/check-art-84-epc/) | Clarity and conciseness of the claims (Art. 84 EPC) | ✓ |
| [`check-art-123-2-epc`](skills/check/check-art-123-2-epc/) | Added subject-matter (Art. 123(2) EPC) | ✓ |
| [`check-claim-formalities-epc`](skills/claims/check-claim-formalities-epc/) | Claim formalities — antecedent basis, numbering, dependencies, independent-claim count (Rule 43 EPC) | ✓ |
| [`check-prefiling`](skills/application/check-prefiling/) | Pre-filing review of a draft application (US, DE or in-house) to be filed at the EPO: formalities, claims, Art. 83/84/123(2), COMVIK, search-stage risks, fees, technical effects | |
| [`verify-citations`](skills/misc/verify-citations/) | Verifies every quote, paragraph/page reference and claim wording in a draft against its sources | ✓ |

### `draft-*` — template-based drafting

| Skill | Purpose |
| :--- | :--- |
| [`draft-oa-summary`](skills/oa/draft-oa-summary/) | Client-facing preliminary review of an Office Action, from the summary template |
| [`draft-oa-response`](skills/oa/draft-oa-response/) | EPO response letter to an Office Action, from the response template |

### Analysis and case-understanding support

| Skill | Purpose |
| :--- | :--- |
| [`analyze-oa`](skills/oa/analyze-oa/) | Initial item-by-item analysis of an Office Action with per-claim novelty tables |
| [`suggest-oa-response-strategies`](skills/oa/suggest-oa-response-strategies/) | Strategic Analysis Report of response options via a panel-of-experts simulation |
| [`suggest-claim-reduction`](skills/claims/suggest-claim-reduction/) | Table of suggested dependent-claim combinations ("or" / "and optionally") to reach ~15 claims and save Rule 162 EPC claims fees |
| [`suggest-claim-dependencies`](skills/claims/suggest-claim-dependencies/) | Suggested augmented back-references of dependent claims, each supported by cited passages of the application as filed |
| [`examine-draft-response`](skills/oa/examine-draft-response/) | Examiner-side stress-test of a proposed response strategy; simulates the next OA |
| [`compute-time-limit-epc`](skills/oa/compute-time-limit-epc/) | Computation of EPC deadlines from an event date |

### Translation and writing

| Skill | Purpose |
| :--- | :--- |
| [`translate-en-de`](skills/lang/translate-en-de/) | English→German translation of claims or a description, with a one-to-one term map; takes a file path or the text as argument |
| [`verify-en-de-translation`](skills/lang/verify-en-de-translation/) | English→German translation consistency and completeness check |
| [`rewrite`](skills/lang/rewrite/) | Edits machine-sounding patent prose (letters, arguments, summaries) so it reads as written by an attorney; leaves claims, quotations, citations, numbers and defined terms untouched; takes a file path or the text as argument; command only |

### Case preparation and library tools

| Skill | Purpose |
| :--- | :--- |
| [`show-help`](skills/misc/show-help/) | Brief help on any skill or agent of the library, or answers to questions about it (e.g. which skills are trainable); command only |
| [`learn`](skills/learn/) | Records your corrections and preferences from a session as learned rules of a trainable skill (see *Learned rules*); command only |
| [`show-context`](skills/misc/show-context/) | Session context usage — computed in Antigravity; in Claude Code it points to the built-in `/context`; command only |
| [`grill-me`](skills/misc/grill-me/) | Interviews the attorney, one question at a time, until the documents, goals and facts needed for a task are clear; ends with a confirmed case brief. Other skills suggest it when their input is insufficient; command only |

### Document handling

| Skill | Purpose |
| :--- | :--- |
| [`read-pdf`](skills/util/read-pdf/) | Read-only PDF text extraction (text layer or OCR via local poppler/tesseract) with page:line and paragraph locations for exact citations |
| [`handle-docx`](skills/util/handle-docx/) | Create and edit Word (.docx) files while preserving the original formatting; new files from your own template `~/.ep-skills/template.docx` or the shipped `template-sample.docx` |

Both are loaded only when a PDF or Word file is involved: when you refer to one, or when `translate-en-de`, `verify-en-de-translation`, `verify-citations`, `grill-me`, `rewrite` and `examine-draft-response` load them to read Word and PDF files.

### Learned rules

Skills marked `trainable: true` (`analyze-oa`, `draft-oa-summary`, `draft-oa-response`, `suggest-oa-response-strategies`, `check-prefiling`, `translate-en-de`, `grill-me`) read `~/.ep-skills/learned/<skill>.md`, if present, and apply your recorded preferences — style, wording, layout, priorities — but never in place of a legal rule or safeguard. `/learn <skill>` writes these rules after you select them. The files are personal and may contain case details. They lie in your home directory, outside the plugin folder, so a plugin update does not remove them; each user builds their own. `/show-help which skills can learn?` lists the trainable skills and their rule counts.

## Requirements

- **Claude Code / Claude Cowork** or **Google Antigravity**.
- **Python 3** for the bundled helper scripts.
- For `read-pdf` (macOS/Linux via Homebrew): `brew install poppler tesseract`, plus `brew install tesseract-lang` for OCR of German, French and other non-English documents.
- For `handle-docx`: `pip install python-docx`. Optionally save your own Word template as `~/.ep-skills/template.docx` (outside the plugin folder, so a plugin update keeps it).
- Antigravity, to run the `read-pdf` / `handle-docx` tools and use `.antigravity_tmp/` and your personal folder `~/.ep-skills/` without approval prompts: add these entries to the allow list (App: Settings > Global Permissions; CLI: `permissions.allow` in `~/.gemini/antigravity-cli/settings.json`):

  ```text
  command(regex:python3 \S*/read-pdf/scripts/pdf_extract\.py( .*)?)
  command(pdfinfo)
  command(pdftotext)
  command(pdftoppm)
  command(tesseract)
  write_file(.antigravity_tmp/)
  write_file(/Users/<you>/.ep-skills/)
  ```

  Give the last entry as the absolute path of the folder `.ep-skills` in your home directory.

  Running `handle-docx` code means running Python the agent writes itself, which an allow-list entry can only permit broadly (`command(python3)`); decide whether you want that.

## Installation

The plugin is on GitHub as `cpraun/ep-skills`.

**Claude app (desktop, Cowork).** Open **Customize → Plugins** (in Cowork, open the Cowork tab first), click **Add → Add marketplace → Add from a repository**, enter `cpraun/ep-skills`, and install **ep-skills**.

**Claude Code (terminal or VS Code).**

```sh
claude plugin marketplace add cpraun/ep-skills
claude plugin install ep-skills@ep-skills
```

**Antigravity (App and CLI).** In a terminal run

```sh
agy plugin install https://github.com/cpraun/ep-skills
```

It installs into `~/.gemini/config/plugins/`, the folder the Antigravity App loads custom plugins from; check **Customizations → Installed** in the App.

Skills are then called as `/ep-skills:<skill>` and agents as `@ep-skills:patent-examiner`. To update, run `claude plugin update ep-skills@ep-skills` (Claude) or the `agy plugin install` command again (Antigravity). Complete the setup under *Requirements* above. Working from a local clone instead? Pass its folder in place of the repository, for example `agy plugin install /path/to/ep-skills`.

## Agents and personas

Two personas run through the library. Each skill that uses one states it briefly; the full persona lives in `agents/` as a subagent:

- **Patent assistant** — drafts and reviews claims, amendments and arguments, and analyzes EPO communications. Used by `analyze-oa`, `draft-oa-summary` and `draft-oa-response`; subagent `@ep-skills:patent-assistant`. `suggest-oa-response-strategies` states its own role (lead strategist leading a panel of experts).
- **EPO examiner** — applies the EPC and the Guidelines strictly, raising objections under Art. 54, 56, 83, 84 and 123(2) without proposing amendments. Used by `examine-draft-response`; subagent `@ep-skills:patent-examiner`.

Claude also selects a subagent automatically when a request matches its `description`.

**Subagent or skill?** `examine-draft-response` stress-tests a strategy you have formed, in your conversation. The `patent-examiner` subagent examines the claims as they stand, in its own context, so it cannot be anchored by the arguments you hope will succeed. Use it for an adversarial pre-filing read of a claim set.

**Constraints of `patent-examiner`.** It runs on the session's model with `tools: [Read, Grep, Glob, WebFetch, Bash]` and the skills `read-pdf` and `handle-docx` preloaded, and it does not see your conversation: give it explicit paths to the claims, the application as filed and each D-document. What it may do with `Bash` and `WebFetch` is stated in [SCOPE.md](SCOPE.md#what-the-plugin-can-reach).

## Development

### Manifests and pre-commit hook

| Path | Read by |
| :--- | :--- |
| `plugin.json` | Google Antigravity |
| `.claude-plugin/plugin.json` | Claude Code / Claude Cowork |
| `.claude-plugin/marketplace.json` | Claude Code / Claude Cowork — lists this repo as marketplace `ep-skills` |

Skills sit in `skills/<name>/`, or in a group folder that both `plugin.json` files list under `skills` (today `skills/application/` for `check-prefiling`, `skills/check/` for the `check-art-*` skills, `skills/claims/` for `check-claim-formalities-epc`, `suggest-claim-reduction` and `suggest-claim-dependencies`, `skills/lang/` for `translate-en-de`, `verify-en-de-translation` and `rewrite`, `skills/misc/` for `show-help`, `grill-me`, `show-context` and `verify-citations`, `skills/oa/` for `analyze-oa`, `draft-oa-summary`, `suggest-oa-response-strategies`, `draft-oa-response`, `examine-draft-response` and `compute-time-limit-epc`, and `skills/util/` for `read-pdf` and `handle-docx`); a group goes exactly one level deep.

The two `plugin.json` files must stay byte-identical; neither host reads the other's copy, so a version bump in only one diverges silently. A `pre-commit` hook in `.githooks/` (distinct from `hooks/`, which Claude reserves for `hooks/hooks.json`) blocks a commit if the staged manifests differ or only one is tracked, and if a skill's working protocol differs from its master. Activate it once per clone:

```sh
git config core.hooksPath .githooks
```

### Working protocol and rules

Every skill starts with the same short working protocol: state the assumptions that change the result, ask instead of guessing, do not agree by default, stay in scope, write short sentences with one term per concept. The master is [`rules/ep-skills.md`](rules/ep-skills.md), which Antigravity loads as a rule. Claude does not load `rules/`, so each `SKILL.md` carries a copy between `<!-- protocol:begin -->` and `<!-- protocol:end -->`; edit the master, then copy the block into every skill. [`rules/antigravity-tools.md`](rules/antigravity-tools.md) applies only in Antigravity: run the `read-pdf` / `handle-docx` tools without asking and keep temporary files in `.antigravity_tmp/` (Antigravity's own prompts follow its permission settings, see *Requirements*).

When a persona changes in substance, check that the short statements in the skills that use it still agree with the agent file; no include mechanism keeps them in sync.

### Testing the skills

The skills are prompts, so each test is an *eval*: it runs a model with the skill loaded and checks the output against deterministic string/regex gates — mandated structure, the out-of-scope refusal, no Art. 56 drift, asking for missing input instead of inventing it. Each failure names the `SKILL.md` rule it violated. The gates check shape and scope, not whether the legal conclusion is right. The harness runs against **Gemini** (default) or **Claude**, set by `MODEL_PROVIDER` in `test/env.sh` (gitignored, holds your key); each scenario costs one model call.

```sh
source test/env.sh
pytest test/                            # every suite
pytest test/check-art-54-epc            # one skill
pytest test/ -k mosaicking              # one scenario

# no model call, no API key:
pytest test/handle-docx test/read-pdf test/verify-citations -k 'not test_gates'
```

Automated tests exist for the skills marked ✓ in the checks table and for `handle-docx` and `read-pdf`; the other skills have been checked manually. Setup, the `expected.yaml` fields, the deterministic suites and how to write a scenario are in **[test/README.md](test/README.md)**.

## Acknowledgments

This package was developed by Christoph von Praun (<praun@alumni.ethz.ch>), with contributions from Mauritius Klein and Christian Hofstetter, and with the help of [Claude](https://claude.com/claude-code) (Anthropic).

The name and idea of `grill-me` come from the skill of the same name in [github.com/mattpocock/skills](https://github.com/mattpocock/skills).
