# AI Persistent Memory Rules

At the start of every session:

1. Read `.claude/current.md`.
2. Understand the current project status, architecture, active problems, and next steps.
3. Continue existing technical decisions instead of reworking them without reason.
4. After important discussions, update `.claude/current.md` with durable information only.

Requirements:

- Use Markdown.
- Keep it concise.
- Preserve only information with long-term value.
- Do not store casual conversation.
