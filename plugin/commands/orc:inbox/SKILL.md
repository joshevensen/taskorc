# /orc:inbox

Show everything that needs attention across all tasks.

## What to do

1. Read all markdown files in `.taskorc/tasks/` (relative to the repo root).
2. Parse the YAML frontmatter of each file to extract `status` and `priority`.
3. Read the first `##` heading after the frontmatter to get the task title.
4. Group and display tasks in this order:
   - **In Progress** — status: `in_progress`
   - **Planned** — status: `planned`, sorted by priority ascending
   - **Draft** — status: `draft`, sorted by priority ascending
   - **On Hold** — status: `on_hold`
   - Omit `complete` and `cancelled` tasks unless there are no other tasks, in which case show a summary count.
5. For each task show: priority number, title, and filename.

## Output format

```
IN PROGRESS
  [4] 4 — Auth  (4-auth.md)

PLANNED
  [2] 2 — ORM Models  (2-orm-models.md)
  [3] 3 — Migrations  (3-migrations.md)
  ...

COMPLETE (1)
```

If `.taskorc/tasks/` is empty or doesn't exist, say so and suggest running `/orc:create` to add a task.
