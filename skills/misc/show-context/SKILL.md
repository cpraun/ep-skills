---
name: show-context
description: >-
  Report context usage of the current session. In Antigravity: transcript size,
  estimated tokens, model limit, workspace, skills, MCP servers, files. In
  Claude Code: points to the built-in /context command.
disable-model-invocation: true
---

# Context & Session Inspector

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

This skill reports the context usage of the current session. First determine the host:

```bash
python3 <this-skill-dir>/scripts/context_stats.py --host
```

- **`claude-code`** — Claude Code reports exact figures itself. Tell the user in one or two sentences to type `/context` (and `/mcp` for connected MCP servers, if asked); a skill cannot run a built-in command. Do not estimate tokens from the transcript. Answer anything `/context` does not show (e.g., which case files were read) from the conversation itself.
- **`antigravity`** — follow `references/antigravity.md` in this skill's directory.
- **`unknown`** — say the host could not be determined and ask whether this is Antigravity or Claude Code.
