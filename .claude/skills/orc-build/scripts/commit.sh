#!/bin/bash
# Stop hook — runs after orc-build finishes.
# Commits, pushes, and opens a PR if the task file shows status: complete.

set -euo pipefail

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

COMMIT_MSG="feat: ${TASK_ID} — ${TITLE}"
git commit -m "$COMMIT_MSG"

# Derive expected branch name
BRANCH="task/$(basename "$TASK_FILE" .md)"

# Push — set upstream if this is the first push for this branch
git push -u origin "$BRANCH"

# Build PR body from acceptance criteria in the task file
# Extract lines between the acceptance criteria header and the next ## section
AC_LINES=$(awk '/^## Acceptance Criteria/,/^## /' "$TASK_PATH" \
  | grep -v '^## ' \
  | grep -v '^[[:space:]]*$' \
  | sed 's/- \[x\]/- [ ]/g')  # uncheck boxes so reviewers verify themselves

PR_BODY="$(cat <<EOF
## What was done

Task **${TASK_ID} — ${TITLE}** was completed via \`/orc:build\`.

## How to test

${AC_LINES}
EOF
)"

gh pr create \
  --title "$COMMIT_MSG" \
  --body "$PR_BODY" \
  --base main \
  --head "$BRANCH"
