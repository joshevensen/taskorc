---
name: orc-plan
description: Take a draft task and flesh it out into a full spec with acceptance criteria and subtasks, then mark it planned and ready to build.
argument-hint: "[task ID or filename]"
disable-model-invocation: true
allowed-tools: Read Write Glob
model: claude-sonnet-4-6
---

Turn a draft task into a fully planned spec.

## Steps

1. Match `$ARGUMENTS` against files in `.taskorc/tasks/`. If missing or ambiguous, list drafts and ask. If the task is not a `draft`, say so and stop.

2. Read the draft task. Display the title and description, then ask any clarifying questions needed to understand:
   - Scope and constraints
   - What "done" actually looks like
   - Any technical approach preferences or things to avoid

3. Read `.claude/skills/orc-create/task-template.md` for the planned format.

4. Generate the full spec:
   - **Description** — refine if needed, or keep as-is if it's already clear
   - **Acceptance criteria** — 3–8 discrete, verifiable conditions, each independently testable
   - **Subtasks** — ordered breakdown where each subtask has:
     - A human-readable description of what it does
     - A `**Prompt:**` that is a complete, self-contained Claude Code instruction with specific file paths, function signatures, and expected outcomes — no prior context assumed
   - Always end with a "Commit and push" subtask

5. Show the full spec and ask: "Does this look right, or would you like to adjust anything?"

6. On confirmation, rewrite the task file with:
   - `status: planned`
   - The refined description (if changed)
   - The acceptance criteria section
   - The subtasks section

7. Confirm: "Task {ID} is now planned. Run `/orc-build {ID}` when you're ready to start."
