---
name: orc-create
description: Quickly capture a task idea as a draft. Just needs a title and description — run /orc-plan when ready to flesh it out with acceptance criteria and subtasks.
argument-hint: "[brief description of what to build]"
disable-model-invocation: true
allowed-tools: Read Write Glob
model: claude-haiku-4-5-20251001
---

Capture a new task idea as a draft in `.taskorc/tasks/`.

## Steps

1. If `$ARGUMENTS` is provided, use it as the initial description. Otherwise ask: "What's the idea?"

2. Ask for anything still needed:
   - **Title** — short, action-oriented (suggest one based on the description if possible)
   - **Description** — what you want to build and why. Can be rough.

3. Determine the next ID by reading `.taskorc/tasks/` with Glob, finding the highest 3-digit numeric prefix, and incrementing by 1 (zero-padded to 3 digits).

4. Write to `.taskorc/tasks/{ID}-{slug}.md`:

```markdown
---
status: draft
priority: {ID}
---

# {ID} — {Title}

## Description

{description}
```

5. Confirm: "Draft {ID} captured. Run `/orc-plan {ID}` when you're ready to plan it out."
