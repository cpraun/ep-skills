# Context report in Antigravity

Part of the `show-context` skill.

1. Run the bundled script with the active conversation ID and, if you know it for certain, the active model's context limit in tokens:

   ```bash
   python3 <this-skill-dir>/scripts/context_stats.py <conversation-id> [context-limit-tokens]
   ```

   It reads the session transcript (`~/.gemini/antigravity/brain/<id>/.system_generated/logs/transcript.jsonl`) and prints JSON: transcript size, steps, tool calls and estimated tokens (characters ÷ 4). The usage percentage is given only if you passed the limit. Never guess a limit: without one, report the tokens and say that the model's limit is not known. If the script reports that the transcript was not found, say so; do not estimate.
2. Present the result as a dashboard:

```markdown
# Session & Context Usage Dashboard

## 1. Context & Token Metrics
- **Active Model:** [Model Name]
- **Model Context Window Limit:** [X,XXX,XXX tokens / not known]
- **Session Transcript Size:** [X.XX KB / X.XX MB]
- **Estimated Current Context Used:** ~[X,XXX] tokens (~[X.XX]% of limit, only if the limit is known)
- **Total Conversation Steps/Turns:** [N] steps
- **Tool Invocations Logged:** [N] calls

## 2. Environment & Session Details
- **Conversation ID:** `[UUID]`
- **Active Workspace:** `[Path]`
- **Current Local Time:** [Timestamp]

## 3. Active Customizations & Skills
- **Skills Available/Loaded:** [List of skills]
- **MCP Servers Connected:** [List of servers]
- **Background Tasks:** [None / List active tasks]

## 4. Referenced Files & Artifacts
- **Files Read / Analyzed:** [List of files]
- **Artifacts Generated:** [List of artifacts in brain directory]
```
