# /orc:status

Show the full status of a specific task.

## Arguments

Accepts a task identifier — priority number or filename. If no argument is given, ask which task.

## What to do

1. Find and read the matching file in `.taskorc/tasks/`.

2. Display a plain-language summary:
   - **Status** and **priority**
   - **Description** in full
   - **Acceptance criteria** — show checked and unchecked items clearly
   - **Subtasks** — list all with their titles (no need to show full prompts)
   - **Artifacts** — list any files in `.taskorc/artifacts/` that reference this task

3. End with a one-line "what's next" recommendation based on the current status:
   - `planned` → "Run `/orc:build {n}` to start this task."
   - `in_progress` → "This task is in progress. Run `/orc:build {n}` to continue."
   - `complete` → "This task is complete."
   - `on_hold` → "This task is on hold."
