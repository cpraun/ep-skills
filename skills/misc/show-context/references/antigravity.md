# Context report in Antigravity

Part of the `show-context` skill.

1. Run the bundled script with the active conversation ID and model name:

   ```bash
   python3 <this-skill-dir>/scripts/context_stats.py <conversation-id> "<model name>"
   ```

   It reads the session transcript (`~/.gemini/antigravity/brain/<id>/.system_generated/logs/transcript.jsonl`) and prints JSON: transcript size, steps, tool calls, estimated tokens (characters ÷ 4), the model's context limit and the usage percentage. If it reports that the transcript was not found, say so; do not estimate.
2. Present the result as a dashboard:

```markdown
# Session & Context Usage Dashboard

## 1. Context & Token Metrics
- **Active Model:** [Model Name]
- **Model Context Window Limit:** [X,XXX,XXX tokens]
- **Session Transcript Size:** [X.XX KB / X.XX MB]
- **Estimated Current Context Used:** ~[X,XXX] tokens (~[X.XX]% of limit)
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
