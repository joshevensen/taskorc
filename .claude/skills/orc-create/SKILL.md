---
name: orc-create
description: Create a new task. Describe what you want to build and the Orc will write the full task spec — title, description, acceptance criteria, and subtasks.
argument-hint: [brief description of what to build]
disable-model-invocation: true
allowed-tools: Read Write Glob
model: claude-sonnet-4-6
---

Create a new task in `.taskorc/tasks/`.

## Steps

1. If `$ARGUMENTS` is provided, use it as the initial description. Otherwise ask: "What do you want to build?"

2. Ask any clarifying questions needed to understand the scope, constraints, and context.

3. Read `.claude/skills/orc-create/task-template.md` to get the task file format.

4. Determine the next ID by reading `.taskorc/tasks/` with Glob, finding the highest 3-digit numeric prefix, and incrementing by 1 (zero-padded to 3 digits, e.g. `010`).

5. Generate the full task spec:
   - **Title** — short, action-oriented
   - **Description** — what needs to be built and why, with enough context to act on
   - **Acceptance criteria** — 3–8 discrete, verifiable conditions, each independently testable
   - **Subtasks** — ordered breakdown where each subtask has:
     - A human-readable description of what it does
     - A `**Prompt:**` that is a complete, self-contained Claude Code instruction with specific file paths, function signatures, and expected outcomes — no prior context assumed
   - Always end with a "Commit and push" subtask

6. Show the full generated task and ask: "Does this look right, or would you like to adjust anything?"

7. On confirmation, write to `.taskorc/tasks/{ID}-{slug}.md` where slug is lowercase with hyphens.

8. Confirm: "Task {ID} created at `.taskorc/tasks/{ID}-{slug}.md`. Run `/orc-build {ID}` to start."
