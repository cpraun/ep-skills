---
name: eps-help
description: >-
  Explain briefly how to use the skills and agents of this EP skills library.
  Argument: a skill or agent name for help on it, or a question about the
  library, e.g. which skills are trainable, which fit a task, which run only
  as a command.
disable-model-invocation: true
---

# Help — the EP skills library

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

This skill answers questions about the skills and agents in this library. It does not perform any of them.

## Argument

- **A skill or agent name** (`/eps-help draft-oa-response`, `/eps-help patent-examiner`) → help on that skill or agent. If the name is close but not exact (`/eps-help reduce claims`, `/eps-help 123`), take the obvious match and say which one you took.
- **A question** (`/eps-help which skills can learn?`) → an answer about the library.
- **Nothing** → a short overview of all skills and agents.

## Source of truth

Never answer from memory: skills are renamed, added and changed. Always run

```
python3 <this-skill-dir>/scripts/list_skills.py          # table
python3 <this-skill-dir>/scripts/list_skills.py --json   # for filtering
```

It reports per skill: name, description, whether it is **trainable** (with the number of learned rules in its `LEARNED.md`), whether it is **command only** (`disable-model-invocation: true`), and its path. It reports per agent (`agents/*.md`, `"kind": "agent"` in the JSON): name, description, model, tools, and its path. For help on one skill, also read its `SKILL.md`; for one agent, its agent file.

## Answers

- **One skill** — at most about 10 lines: what it does; how to call it and its required and optional inputs; what you get; trainable / command only, if so; the skills to run before or after it. Do not reproduce its file, legal rules or template.
- **One agent** — at most about 10 lines: what it does; how to call it (`@ep-skills:<name>`, or automatically when a request matches its description); its tools and what it cannot do (e.g. no writing, no web access); that it starts without the conversation, so it needs explicit file paths; the skill that comes closest to it, if one does.
- **A question** — briefly, from the script output, as a list or small table. For "which skill for X?", name one skill or a short sequence with one line of reason each; for a workflow, order the skills by their descriptions rather than assuming an order. If no skill fits, say so; never invent one.
- **Overview** — group by prefix and purpose: `check-*` (checks), `draft-*` (drafting from templates), `suggest-*` / `analyze-*` / `examine-*` (analysis and strategy), translation, tools (`eps-*`, `util-*`), other skills; then the agents; one line per skill or agent; end with how to get help on one of them.

Answer in the user's language; keep skill names, commands and file names unchanged. Mention the plugin prefix (e.g. `/ep-skills:eps-help`) only if a call did not reach the skill or the user asks how to invoke it.
