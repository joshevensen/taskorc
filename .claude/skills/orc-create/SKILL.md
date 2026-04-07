# /orc:create

Create a new task file in `.taskorc/tasks/`.

## What to do

1. Ask the user for:
   - **Title** — short description of what needs to be built
   - **Description** — what and why. What problem does this solve?
   - **Acceptance criteria** — list of discrete, verifiable conditions for done
   - **Subtasks** — breakdown of the work. For each subtask: a human-readable description and an LLM-executable prompt Claude Code can act on directly

2. Determine the next priority number by reading existing task files in `.taskorc/tasks/` and incrementing the highest priority found. If no tasks exist, start at 1.

3. Generate a slug from the title (lowercase, hyphens, no special characters).

4. Write the file to `.taskorc/tasks/{priority}-{slug}.md` using this exact format:

```markdown
---
status: planned
priority: {number}
---

# {priority} — {Title}

## Description

{description}

## Acceptance Criteria

- [ ] {criterion 1}
- [ ] {criterion 2}

## Subtasks

### {priority}.1 — {Subtask title}

{human-readable description}

**Prompt:** {LLM-executable instruction}

---

### {priority}.2 — {Subtask title}

...
```

5. Confirm the file was created and show the path.
