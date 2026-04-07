# /orc:build

Execute a task by working through its subtasks in order.

## Arguments

Accepts a task identifier as an argument — either the priority number (e.g. `/orc:build 2`) or the filename without extension (e.g. `/orc:build 2-orm-models`). If no argument is given, ask the user which task to build or suggest running `/orc:inbox` to see what's available.

## What to do

1. Find the matching file in `.taskorc/tasks/`. If the argument is a number, match on files starting with that number. If ambiguous, list matches and ask.

2. Read the task file. Display the title, description, and acceptance criteria so the user can confirm before execution begins.

3. Load any artifacts in `.taskorc/artifacts/` that reference this task number. Summarize their content as additional context.

4. Update the task file's frontmatter: set `status: in_progress`. Write the file.

5. Work through each subtask in order, one at a time:
   - Display the subtask title and description before starting
   - Execute the subtask's **Prompt** as a Claude Code operation
   - Confirm completion before moving to the next subtask
   - If a subtask fails, stop and report what happened — do not continue to the next subtask

6. After all subtasks are complete, remind the user to run `/orc:complete {task}` to close it out.

## Notes

- Do not skip subtasks. The order matters — later subtasks depend on earlier ones.
- If the task status is already `complete`, say so and ask if the user wants to re-run it.
- The commit and push subtask (always the last one) should be run as written — do not skip it.
