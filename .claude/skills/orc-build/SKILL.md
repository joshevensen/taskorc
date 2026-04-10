---
name: orc-build
description: Execute a task by working through its subtasks in order, then confirm acceptance criteria before closing it out. Pass the task ID or filename.
argument-hint: "[task ID or filename]"
allowed-tools: Read Write Edit Bash Glob Grep
model: claude-sonnet-4-6
hooks:
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PROJECT_DIR}/.claude/skills/orc-build/scripts/commit.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: agent
          prompt: |
            A file was just edited during an orc-build session. Read the hook input from stdin to find the file path that was changed.

            1. Read the changed file.
            2. If the change is itself a comment, docblock, or README update — stop, do nothing.
            3. If the change contains logic with a non-obvious "why" not explained anywhere in the surrounding code — add a brief inline comment or docblock explaining the reasoning. One line is usually enough.
            4. If the "why" is self-evident from the code — do nothing.

            Be minimal. Do not add comments that restate what the code does. Only capture why a decision was made if a future reader would otherwise wonder.
---

Execute a task by working through its subtasks, then confirm acceptance criteria before closing out.

## Steps

1. **Find the task file.** Match `$ARGUMENTS` against files in `.taskorc/tasks/`:
   - If a 3-digit number, match `{ID}-*.md`
   - If a filename fragment, match by name
   - If ambiguous or missing, list available planned tasks and ask

2. **Read and display** the task title, description, and acceptance criteria so the user can confirm before execution begins.

3. **Load context.** Check `.taskorc/artifacts/` for any files where `task:` frontmatter matches this task ID. Summarize their content as additional context before starting.

4. **Write the pointer file** so the Stop hook knows which task ran:
   ```bash
   mkdir -p .taskorc/tmp
   echo "{filename}" > .taskorc/tmp/current-task
   ```
   Where `{filename}` is the task filename, e.g. `004-auth.md`.

5. **Create the task branch** off the latest remote main:
   ```bash
   bash .claude/skills/orc-build/scripts/branch.sh "{filename}"
   ```
   This fetches `origin/main` and creates `task/{slug}` (e.g. `task/004-auth`). If the branch already exists it checks it out instead.

6. **Update task status** — set `status: in_progress` in the task file frontmatter and write it.

7. **Execute subtasks in order**, one at a time:
   - Display the subtask number and title before starting
   - Execute the subtask's `**Prompt:**` as a Claude Code operation — read code, create files, edit, run commands as needed
   - Confirm it's complete before moving to the next
   - If a subtask fails, leave task status as `in_progress` and stop — report what happened and what completed. Do not continue.

8. **Confirm acceptance criteria.** Display the full acceptance criteria list and ask: "Are all of these met?" Surface any unchecked items clearly. Do not proceed without explicit confirmation.

9. **Close out** — check all acceptance criteria boxes (`- [ ]` → `- [x]`), set `status: complete`, and write the task file.

10. **Write the PR body** to `.taskorc/tmp/pr-body.md`. The commit script reads this file verbatim — write it well. Include:
    - A short **Summary** paragraph (2–4 sentences) explaining what this task accomplished and why it matters in the context of the broader system
    - A **Changes** section listing the key files created or modified, with one-line notes on what each does
    - An **Acceptance criteria** section — copy the full checklist from the task file, but uncheck all boxes (`- [x]` → `- [ ]`) so reviewers can verify each item themselves

11. Say: "Task {ID} complete. The Stop hook will commit, push, and open a pull request."

## Rules

- Do not skip subtasks. Order matters.
- If status is already `complete`, say so and ask whether to re-run.
- The Stop hook handles the git commit — do not commit manually.
