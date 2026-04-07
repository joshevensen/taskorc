---
name: orc-prioritize
description: Review and reorder the task queue. Presents all active tasks with context and facilitates a prioritization conversation. Can recommend an order and explain why.
disable-model-invocation: true
allowed-tools: Read Write Glob
model: claude-sonnet-4-6
---

Review and reorder the task queue.

## Steps

1. Read all files in `.taskorc/tasks/`. Collect tasks with status `planned` or `draft`, sorted by current priority ascending.

2. Display the current queue with context for each task:
   - Priority number, ID, title, status
   - First sentence of the description

   Example:
   ```
   Current queue:

   [1] 002 — ORM Models (planned)
       Define all six SQLAlchemy models in Python.

   [2] 003 — Migrations (planned)
       Initialize Alembic and generate the first migration.
   ...
   ```

3. Ask: "Would you like to reorder these, or should I recommend a priority order?"

   **If the user wants a recommendation:** Analyse the tasks for dependencies, risk, and logical sequencing. Propose a new order with a short reason for each placement. Ask for confirmation before applying.

   **If the user wants to reorder manually:** Facilitate the conversation — accept instructions like "move 005 above 003" or "swap 006 and 007" and show the updated order after each change. Confirm the final order before writing.

4. On confirmation, update the `priority` frontmatter field in each affected task file to reflect the new order (1, 2, 3... or whatever numbering the user prefers).

5. Confirm: "Queue updated. Run `/orc-next` to start on the top priority task."
