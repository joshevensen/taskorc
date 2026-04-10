---
name: orc-hold
description: Put a task on hold. Sets status to on_hold so it's out of the active queue but not cancelled.
argument-hint: "[task ID or filename]"
allowed-tools: Read Write Glob
model: claude-haiku-4-5-20251001
---

Put a task on hold.

## Steps

1. Match `$ARGUMENTS` against files in `.taskorc/tasks/`. If missing or ambiguous, list active tasks and ask.

2. If status is already `on_hold`, say so and stop.

3. Set `status: on_hold` in the frontmatter and write the file.

4. Confirm: "Task {ID} is on hold. Run `/orc-build {ID}` to pick it back up."
