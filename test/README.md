# Skill test harness

The skills in this plugin are **prompts, not code**, so a test cannot be a unit
test — there is no function to call. Each test instead **invokes a model with the
skill loaded, captures the output, and checks it against deterministic rules**.
This is an *eval*.

Everything needed to run the evals lives under this one `test/` directory: the
shared harness scripts, the per-skill scenarios, and the pytest configuration.

## What runs against what

The harness sends each scenario to an LLM and grades the reply. It can run
against either provider, chosen by the `MODEL_PROVIDER` env var (see *Running*):

- **Gemini** (default) — the model behind Google Antigravity, a first-class host
  for this plugin.
- **Claude** — the model behind Claude Cowork, the other host.

Either way it tests a skill's *prompt against the model* — the substance of
whether the instructions produce correct behaviour. It does **not** drive the
host IDE itself (skill discovery, the `/`-invocation UI); that has no scriptable
headless mode and stays a manual smoke check. The provider coupling lives
entirely in `runner.py`; gates and scenarios are provider-agnostic.

## Layout

```text
test/
  README.md                 this file
  pytest.ini                makes test/ the pytest rootdir; pythonpath = .
  env_sample.sh             sample to specify environment variables should be completed by he user and renamed to env.sh
  conftest.py               registers the --show-model-output flag
  requirements.txt          pytest, pyyaml, google-genai, anthropic
  runner.py                 the model seam: generate(...) dispatches to Gemini or Claude
  gates.py                  the deterministic gates (the only grading step)
  skilltest.py              discovery + SKILL.md loading helpers
  <skill-name>/             one folder per skill under test
    test_<skill>.py         a GATE_PROFILE + parametrized run over cases/
    cases/
      NN-<label>/           one scenario
        input.md            what a user would supply
        expected.yaml       the gate assertions
```

The scenarios test skills that live elsewhere (`../skills/<name>/`). Each test
file finds its skill via `skilltest.skill_dir_for()`, which maps the suite folder
`test/<name>/` to `skills/<name>/` — no hard-coded paths.

Because `test/` sits **outside** `skills/`, `agents/`, and every other directory
the plugin loader reads, it is inert in production by construction: the loader
never scans it. (Guard rule kept anyway: no file here is named `SKILL.md`.)

## What the gates check

Grading is a single deterministic step — `gates.run_gates(output, expected,
profile)` in `gates.py`. Pure string/regex over the model's output, stable,
hard-fail; each check maps to an explicit `SKILL.md` rule and each failure names
the rule it violated:

- **Structure** — the output contains the skill's mandated shape (for
  `check-art-54-epc`, the feature table + conclusion; for `check-art-123-2-epc`,
  a COMPLIANT / NON-COMPLIANT / UNCERTAIN finding).
- **Scope discipline** — the out-of-scope refusal sentence when required.
- **Forbidden phrases** — no "drift" language (e.g. Art. 56 reasoning leaking
  into an Art. 54 novelty test).
- **Input discipline** — ask for missing input rather than inventing it.

`gates.py` is **skill-agnostic**. The skill-specific bits — the invocation name
used in the refusal sentence, the structure markers, and the drift phrases — live
in a `GATE_PROFILE` dict at the top of each suite's `test_<skill>.py`. Which
checks fire per scenario is driven by that scenario's `expected.yaml`.

The gates verify that output is well-shaped and in-scope; they do **not** judge
whether the legal conclusion is correct — that is left to the attorney reviewing
the skill's real output.

## Running

Run every command in this section from **inside this `test/` directory** (`cd`
into it first). `pytest.ini` lives here, so `test/` is pytest's rootdir and the
paths below are relative to it. (From the repo root instead, the equivalent is
`pytest test/…` — see the note at the end.)

### First, check whether you already have the dependencies

A virtual environment is **not** required — if `google-genai`, `pytest`, and
`pyyaml` are already importable on your machine, run the suite directly. Check
with:

```sh
python3 -c "import pytest, yaml, google.genai, anthropic; print('deps OK')"
```

- Prints **`deps OK`** → skip straight to *Run* below, no venv needed.
- Raises `ModuleNotFoundError` → install the missing packages (see *Install*).

### Install (only if the check failed)

```sh
pip install -r requirements.txt
```

If that is refused with `error: externally-managed-environment` (PEP 668 — common
on macOS/Homebrew and Debian system Python), don't force it. Use a virtual
environment, which keeps these packages out of the system Python:

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Choose a provider and set your API key

Configuration lives in `test/env.sh`, which is **gitignored** so your key never
reaches the repo. Set `MODEL_PROVIDER` and fill in the key and model for that
provider, then source it (it is meant to be sourced, not executed):

```sh
# test/env.sh
export MODEL_PROVIDER="gemini"                 # gemini (default) | claude

# --- Gemini (Google) ---
export GEMINI_API_KEY="paste-your-key-here"    # or GOOGLE_API_KEY
export GEMINI_MODEL="gemini-2.5-pro"           # verify the current model id

# --- Claude (Anthropic) ---
export ANTHROPIC_API_KEY="paste-your-key-here"
export ANTHROPIC_MODEL="claude-opus-5"         # verify the current model id
```

```sh
source ./env.sh
```

You only need the key+model for the provider you select; the other block can stay
on placeholders. Values apply regardless of whether you use a venv. The model id
is required — see the model-id note below. (`ANTHROPIC_MAX_TOKENS`, default
16000, is an optional Claude override.)

### Run

```sh
pytest                                  # every suite
pytest check-art-54-epc                 # one skill
pytest -k mosaicking                    # one scenario (substring of its id)
```

To run from the repo root instead of `cd`-ing in, prefix the target:
`pytest test/`, `pytest test/check-art-54-epc`.

Each scenario costs **one** model call to the selected provider (to generate the
output the gates then check). There is no second grading call.

To print the model's raw output to the console while debugging, add
`--show-model-output`. It prints live for every scenario (pass or fail) — no `-s`
needed, because the flag suspends pytest's output capture around the print:

```sh
pytest -k mosaicking --show-model-output
```

> **Model id.** `runner.py` defaults each provider's model to a placeholder that
> **must be checked** against the current list — model ids change between
> releases. Override via env var; no code edit needed:
>
> - Gemini: `GEMINI_MODEL`, list at <https://ai.google.dev/gemini-api/docs/models>
> - Claude: `ANTHROPIC_MODEL`, list at <https://platform.claude.com/docs/en/about-claude/models/overview>

### Deterministic suites (no model call, no API key)

The suites for `check-citations`, `util-pdf` and part of `util-docx` test scripts, not prompts:

- `check-citations/` — its locator script, on the citations listed per case in
  `check-citations/cases/*/citations.yaml`; add your own documents there, see
  [the cases README](check-citations/cases/README.md).
- `util-pdf/` — its extractor on text, scanned and mixed PDFs.
- `util-docx/` — besides the eval (`test_util_docx.py`), tests of the skill's helper script
  on real Word files: templates and formatting (`test_docx_helper.py`); tracked changes
  written and read (`test_docx_redline.py`, cross-checked against `pandoc` if installed);
  the same on a fictitious application saved by Microsoft Word with Word's own tracked
  changes (`test_docx_word_fixture.py`, fixture in `util-docx/fixtures/`; set
  `UTIL_DOCX_OUTPUT_DIR` to also write an amended copy for a manual check in Word).

Run all of them from the repo root:

```sh
pytest test/util-docx test/util-pdf test/check-citations -k 'not test_gates'
```

## Writing a new scenario

Add a directory under a skill's `cases/` with two files.

**`input.md`** — exactly what a user would type or attach (claim text, D1
passages, …). Self-contained; never rely on the skill inventing prior-art
content. Use synthetic examples only — no real application numbers, docket
references, or client matter.

**`expected.yaml`** — which gate checks apply to this scenario:

| field | meaning |
| :--- | :--- |
| `expect_output` | if `true` (default), the skill's normal assessment is expected — the profile's structure markers must be present; if `false`, they must be **absent** and the skill must ask for input instead of fabricating an answer |
| `must_ask` | if `true`, the output must ask for missing input (implied whenever `expect_output` is `false`; set it explicitly for a *provisional* answer that still asks) |
| `must_refuse` | if `true`, the output must carry the out-of-scope refusal sentence for this skill |
| `forbidden` | extra phrases that must not appear in the output |
| `rule` | traceability: which `SKILL.md` rule the scenario exercises |

All fields are optional and default to the permissive value; a scenario sets only
what it wants enforced. Record the `SKILL.md` rule each scenario exercises in
`rule:`.

**Prove a scenario bites.** After writing it, temporarily weaken the relevant
`SKILL.md` rule and confirm the scenario goes red, then revert. A test that
passes against a broken skill tests nothing.

## Adding a suite for another skill

From inside this `test/` directory:

1. `mkdir <skill-name>` and add a `cases/` folder inside it.
2. Copy `check-art-54-epc/test_check_54.py` to `<skill-name>/test_<skill>.py`.
   It needs no path edits — `skill_dir_for(__file__)` derives the skill from the
   folder name.
3. Rewrite its `GATE_PROFILE` for the new skill: set `skill` to the invocation
   name, `structure` to the regex markers that skill's output must contain (read
   its `SKILL.md` Output Format), and `drift` to any phrases it must never emit.
4. Write the scenarios under `cases/`.

The `<skill-name>` folder must match the skill's directory name under
`../skills/`, since that is how `skill_dir_for()` locates the skill.

The `runner.py` / `gates.py` / `skilltest.py` code is shared and reused unchanged;
only the `GATE_PROFILE` and the scenarios are per-skill. See `check-art-123-2-epc/`
for a worked second example (a different output shape and refusal target).
