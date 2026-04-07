---
name: orc-inbox
description: Show all tasks grouped by status. Use to see what needs attention, what's in progress, and what's planned next.
disable-model-invocation: true
allowed-tools: Read Glob
model: claude-haiku-4-5-20251001
---

Show everything that needs attention across all tasks.

## Steps

1. Read all markdown files in `.taskorc/tasks/` using Glob.
2. Parse the YAML frontmatter of each file to extract `status` and `priority`.
3. Read the `# {ID} — {Title}` heading to get the task title.
4. Group and display tasks in this order:
   - **In Progress** — `in_progress`
   - **Planned** — `planned`, sorted by priority ascending
   - **Draft** — `draft`, sorted by priority ascending
   - **On Hold** — `on_hold`
   - Omit `complete` and `cancelled` unless there are no other tasks — then show a count.
5. For each task show: ID, title, filename.

## Output format

```
IN PROGRESS
  [004] 004 — Auth  (004-auth.md)

PLANNED
  [002] 002 — ORM Models  (002-orm-models.md)
  [003] 003 — Migrations  (003-migrations.md)

COMPLETE (1)
```

If `.taskorc/tasks/` is empty, say so and suggest running `/orc-create`.
