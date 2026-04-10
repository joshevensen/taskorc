---
name: orc-status
description: Show the full status of a specific task — description, acceptance criteria, subtasks, and linked artifacts.
argument-hint: "[task ID or filename]"
allowed-tools: Read Glob
model: claude-haiku-4-5-20251001
---

Show the full status of a task.

## Steps

1. Match `$ARGUMENTS` against files in `.taskorc/tasks/`. If missing or ambiguous, list options and ask.

2. Read and display:
   - **Status** and **priority**
   - **Description** in full
   - **Acceptance criteria** — checked and unchecked items clearly distinguished
   - **Subtasks** — titles only (not full prompts)
   - **Artifacts** — list any `.taskorc/artifacts/` files where `task:` frontmatter matches this ID

3. End with a one-line next step:
   - `planned` → "Run `/orc-build {ID}` to start."
   - `in_progress` → "Run `/orc-build {ID}` to continue."
   - `complete` → "This task is complete."
   - `on_hold` → "This task is on hold."
