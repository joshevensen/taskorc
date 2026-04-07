# /orc:complete

Mark a task as complete.

## Arguments

Accepts a task identifier — priority number or filename. If no argument is given, ask which task.

## What to do

1. Find and read the matching file in `.taskorc/tasks/`.

2. If status is already `complete`, say so and stop.

3. Show the acceptance criteria and ask the user to confirm all criteria are actually met before marking complete. If any are unchecked, surface them clearly — do not auto-complete without confirmation.

4. Update the file:
   - Set `status: complete` in frontmatter
   - Check all acceptance criteria boxes (`- [ ]` → `- [x]`)

5. Write the updated file.

6. Display a summary: task title, number of subtasks completed, and a prompt to push if the commit subtask was skipped.
