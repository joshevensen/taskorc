---
name: orc-next
description: Find the highest-priority planned task and offer to start building it immediately.
disable-model-invocation: true
allowed-tools: Read Glob
model: claude-haiku-4-5-20251001
---

Find the next task to work on and kick off the build.

## Steps

1. Read all files in `.taskorc/tasks/`. Find all tasks with `status: planned`, sorted by `priority` ascending. The lowest priority number is next.

2. If no planned tasks exist, check for drafts and say: "No planned tasks. You have {n} draft(s) — run `/orc-plan {ID}` to plan one."

3. Display the top task:
   ```
   Next up: [002] 002 — ORM Models

   {full description}

   Ready to build? (yes/no)
   ```

4. If yes — run `/orc-build {ID}` immediately.

5. If no — show the next task in the queue and ask again, or suggest `/orc-prioritize` to reorder.
