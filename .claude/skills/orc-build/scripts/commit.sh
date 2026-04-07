#!/bin/bash
# Stop hook — runs after orc-build finishes.
# Commits if the task file shows status: complete.

POINTER_FILE="${CLAUDE_PROJECT_DIR}/.taskorc/tmp/current-task"

# No pointer means no build was running
if [ ! -f "$POINTER_FILE" ]; then
  exit 0
fi

TASK_FILE=$(cat "$POINTER_FILE")
TASK_PATH="${CLAUDE_PROJECT_DIR}/.taskorc/tasks/${TASK_FILE}"

# Always clean up the pointer
rm -f "$POINTER_FILE"

if [ ! -f "$TASK_PATH" ]; then
  exit 0
fi

# Read status and title from the task file itself
STATUS=$(grep -m1 '^status:' "$TASK_PATH" | awk '{print $2}')
TASK_ID=$(echo "$TASK_FILE" | grep -oE '^[0-9]+')
TITLE=$(grep -m1 '^# ' "$TASK_PATH" | sed 's/^# [0-9]* — //')

# Only commit if build completed
if [ "$STATUS" != "complete" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR}"

git add -A

# Nothing to commit
if git diff --cached --quiet; then
  exit 0
fi

git commit -m "feat: ${TASK_ID} — ${TITLE}"
