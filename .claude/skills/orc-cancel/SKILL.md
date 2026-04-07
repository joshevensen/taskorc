---
name: orc-cancel
description: Cancel a task. Asks for confirmation before setting status to cancelled.
argument-hint: "[task ID or filename]"
disable-model-invocation: true
allowed-tools: Read Write Glob
model: claude-haiku-4-5-20251001
---

Cancel a task.

## Steps

1. Match `$ARGUMENTS` against files in `.taskorc/tasks/`. If missing or ambiguous, list tasks and ask.

2. If status is already `cancelled`, say so and stop.

3. Ask: "Cancel task {ID} — {Title}? This won't delete the file but it will drop out of your inbox. Confirm? (yes/no)"

4. If confirmed, set `status: cancelled` in the frontmatter and write the file.

5. Confirm: "Task {ID} cancelled."

6. If not confirmed, say: "Cancelled cancelled." and stop.
