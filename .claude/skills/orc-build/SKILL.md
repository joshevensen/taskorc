---
name: orc-build
description: Execute a task by working through its subtasks in order. Pass the task ID or filename.
argument-hint: [task ID or filename]
disable-model-invocation: true
allowed-tools: Read Write Edit Bash Glob Grep
model: claude-sonnet-4-6
---

Execute a task by working through its subtasks in order.

## Steps

1. **Find the task file.** Match `$ARGUMENTS` against files in `.taskorc/tasks/`:
   - If a 3-digit number, match `{ID}-*.md`
   - If a filename fragment, match by name
   - If ambiguous or missing, list available tasks and ask

2. **Read and display** the task title, description, and acceptance criteria so the user can confirm before execution begins.

3. **Load context.** Check `.taskorc/artifacts/` for any files where `task:` frontmatter matches this task ID. Summarize their content as additional context before starting.

4. **Update status.** Set `status: in_progress` in the task file frontmatter and write it.

5. **Execute subtasks in order**, one at a time:
   - Display the subtask number and title before starting
   - Execute the subtask's `**Prompt:**` as a Claude Code operation — read code, create files, edit, run commands as needed
   - Confirm it's complete before moving to the next
   - If a subtask fails, stop immediately and report what happened and what was completed — do not continue

6. After all subtasks complete: "All subtasks done. Run `/orc-complete {ID}` to close this task out."

## Rules

- Do not skip subtasks. Order matters.
- If status is already `complete`, say so and ask whether to re-run.
- The commit and push subtask is always last — run it as written.
