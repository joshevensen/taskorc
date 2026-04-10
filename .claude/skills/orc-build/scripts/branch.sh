#!/bin/bash
# Step 5 — creates a task branch off the latest remote main before execution begins.
# Usage: branch.sh <task-filename>  e.g. branch.sh 004-auth.md

set -euo pipefail

TASK_FILE="${1:-}"

if [ -z "$TASK_FILE" ]; then
  echo "branch.sh: no task filename provided" >&2
  exit 1
fi

# Derive branch name: strip .md, prefix with task/
BRANCH="task/$(basename "$TASK_FILE" .md)"

cd "${CLAUDE_PROJECT_DIR}"

# Fetch latest remote main without switching branches
git fetch origin main --quiet

# If we're already on this branch (e.g. re-run), just ensure it's up to date
if git rev-parse --verify "$BRANCH" &>/dev/null; then
  echo "branch.sh: branch '$BRANCH' already exists, checking it out"
  git checkout "$BRANCH"
  exit 0
fi

# If the branch exists on origin but not locally, track it
if git ls-remote --exit-code --heads origin "$BRANCH" &>/dev/null; then
  echo "branch.sh: branch '$BRANCH' exists on origin, checking it out as tracking branch"
  git fetch origin "$BRANCH" --quiet
  git checkout --track -b "$BRANCH" "origin/$BRANCH"
  exit 0
fi

git checkout -b "$BRANCH" origin/main
echo "branch.sh: created and checked out '$BRANCH' from origin/main"
