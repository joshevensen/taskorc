---
name: orc-complete
description: Mark a task as complete after confirming all acceptance criteria are met.
argument-hint: [task ID or filename]
disable-model-invocation: true
allowed-tools: Read Write Glob
model: claude-haiku-4-5-20251001
---

Close out a completed task.

## Steps

1. Match `$ARGUMENTS` against files in `.taskorc/tasks/`. If missing or ambiguous, list options and ask.

2. If status is already `complete`, say so and stop.

3. Display the acceptance criteria and ask: "Are all of these done?" Surface any unchecked items clearly. Do not proceed without explicit confirmation.

4. Update the file:
   - Set `status: complete` in frontmatter
   - Check all acceptance criteria (`- [ ]` → `- [x]`)

5. Write the updated file.

6. Confirm: "Task {ID} marked complete."
