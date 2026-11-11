---
name: learn
description: >-
  Record lessons, user corrections and heuristics from the session as learned rules of a trainable skill (in ~/.ep-skills/learned/), after the user selects which. Invoked as /learn <skill-name>.
disable-model-invocation: true
---

# Learn (Skill Self-Improvement & Multi-Aspect Heuristic Extraction)

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

This skill turns the user's corrections and preferences from the current session into learned rules of a trainable skill, after the user has selected which ones to record. The rules of a skill of this plugin are kept in `~/.ep-skills/learned/<skill_name>.md`, outside the plugin folder, so a plugin update does not remove them. It never edits the target skill's `SKILL.md`.

## Step 1 — Identify and validate the target skill

1. Take the skill name from the argument (`/learn draft-oa-summary`). If none is given, infer it from the skill used in the session, or ask.
2. Locate the skill directory, using the first match: `../<skill_name>/` or `../*/<skill_name>/` (a skill in a group folder such as `check/`) next to this skill's directory (this plugin); `.claude/skills/<skill_name>/` in the working directory; `~/.claude/skills/<skill_name>/`. If several match, list them and ask; if none, say where you looked and stop.
3. The skill must be trainable: `trainable: true` in its frontmatter. Otherwise stop: *"Skill `<skill_name>` is not marked as trainable. To enable learning for this skill, add `trainable: true` to its `SKILL.md` frontmatter."*

## Step 2 — Extract candidate rules

Review the session for corrections of the skill's output and for stated preferences on style, wording, terminology, citations, layout, priorities and recurring omissions. Record **preferences only**: a correction of an EPC rule, legal standard or safeguard is not a learned rule — the target skills never let learned rules override their legal rules. If the session showed the skill's legal content is wrong, say so and suggest correcting its `SKILL.md`.

Split the feedback into atomic, independent rules (formatting separate from legal-reasoning preferences), each in this form:

```markdown
### [YYYY-MM-DD] <Aspect Title>
- **Trigger / Context**: <when the rule applies>
- **Learned Rule**: <what to do or avoid>
- **Rationale**: <the session feedback behind it>
- **Example**:
  - ❌ *Avoid*: <previous pattern>
  - ✅ *Prefer*: <preferred pattern>
```

## Step 3 — Let the user select

Show every candidate in full, numbered. Then ask with AskUserQuestion (`multiSelect: true`): *"Which of these candidate lessons should be recorded for `<skill_name>`?"*, one option per aspect (`Aspect 1: <Short Title>`, "(Recommended)" where you recommend it). The tool allows 4 options per question and 4 questions per call; split larger sets. Selecting nothing or answering "none" cancels. Without the tool, accept a plain-text answer ("1 and 3", "all", "none").

## Step 4 — Update the rules file

The rules file is `~/.ep-skills/learned/<skill_name>.md` for a skill of this plugin, and `LEARNED.md` in the skill's own folder for a project or user skill.

- **Cancel:** confirm that nothing was changed.
- **Old location:** if a skill of this plugin still has a `LEARNED.md` in its folder and the rules file does not exist, move that file's content to the rules file first and tell the user.
- **Selection:** if the rules file does not exist, create it (and the folder) with:

  ```markdown
  # Learned Rules & User Preferences: <skill_name>

  > [!NOTE]
  > This file contains heuristics, formatting preferences, and lessons learned from past interactive sessions.
  > When executing `<skill_name>`, treat these rules as high-priority constraints overriding default style.

  ---
  ```

  Check each selected rule for conflicts with existing entries, append the rules separated by `---`, and confirm what was saved.
