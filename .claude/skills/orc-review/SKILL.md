---
name: orc-review
description: Review unresolved PR comments one at a time — fix, skip, or reply. Resolves all threads and commits any fixes.
argument-hint: "[PR number or URL]"
allowed-tools: Read Write Edit Bash Glob Grep
model: claude-sonnet-4-6
---

Work through every unresolved review thread on a PR, one at a time. For each thread decide to fix, skip, or comment. Claude drafts all replies. Resolve every thread and commit any fixes at the end.

## Steps

### 1 — Find the PR and check out its branch

Get the repo owner and name:
```bash
gh repo view --json owner,name --jq '"owner=\(.owner.login) name=\(.name)"'
```

**If `$ARGUMENTS` is provided:**
- Strip to a bare number (handle full GitHub URLs like `https://github.com/owner/repo/pull/123` or bare `123`)
- Fetch the PR's branch: `gh api repos/{owner}/{name}/pulls/{number} --jq '.head.ref'`
- Ensure the branch is fetched and check it out: `git fetch origin {branch} && git checkout {branch}`

**If no argument:**
- Use the current branch's open PR: `gh pr view --json number,headRefName`
- If no open PR exists, stop and say so

Store the PR number as `PR_NUMBER` for use in all subsequent API calls.

### 2 — Fetch all unresolved review threads

Run this GraphQL query via `gh api graphql`:

```graphql
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          startLine
          comments(first: 20) {
            nodes {
              id
              body
              author { login }
              diffHunk
            }
          }
        }
      }
    }
  }
}
```

Filter to threads where `isResolved: false` and `isOutdated: false`. If none remain, say "No unresolved review threads — nothing to do." and stop.

Group threads by file (`path`). Process all threads in the same file consecutively before moving to the next file.

### 3 — For each thread, show context and prompt for a decision

Display:
```
─────────────────────────────────────────
[N/TOTAL] {path}
─────────────────────────────────────────

{diffHunk}

💬 {author}: {comment body}
─────────────────────────────────────────
Options: (f)ix  (s)kip  (c)omment
```

Wait for the user to choose. Accept `f`, `s`, `c`, or the full words.

### 4 — Execute the choice

#### (f) Fix

1. Read the file. Propose a specific code change that addresses the comment.
2. Show the proposed diff and ask: "Apply this fix? (yes/no/edit)"
   - **yes** — apply the edit
   - **no** — fall back to skip flow
   - **edit** — open discussion, let the user describe what they want instead, then re-propose
3. Draft a reply for the thread. Base it on what was actually changed — be specific, e.g. *"Fixed — moved the ownership check before the query so we never hit the DB on an unauthorized request."* Show the draft and ask: "Post this reply? (yes/edit)"
4. Post the reply via GraphQL `addPullRequestReviewThreadReply`
5. Resolve the thread via GraphQL `resolveReviewThread`

#### (s) Skip

1. Draft a reply explaining why no change was made. Use context from the diff hunk and comment to write a clear, non-dismissive justification — e.g. *"Intentional — the linear scan is fine for single-user context; noted in a comment in the code. Will revisit if we move to multi-user."* Show the draft and ask: "Post this reply? (yes/edit)"
2. Post the reply
3. Resolve the thread

#### (c) Comment

1. Draft a reply that opens or continues discussion — ask a clarifying question, push back with reasoning, or note a tradeoff. Show the draft and ask: "Post this reply? (yes/edit)"
2. Post the reply
3. Resolve the thread (resolving means the thread is closed on GitHub — the posted comment still stands as a record of the discussion)

### 5 — GraphQL mutations

**Post a reply:**
```graphql
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: $threadId
    body: $body
  }) {
    comment { id }
  }
}
```

**Resolve a thread:**
```graphql
mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread { isResolved }
  }
}
```

Both are run via:
```bash
gh api graphql -f query='{mutation}' -f threadId='{id}' -f body='{text}'
```

### 6 — Commit and push any fixes

After all threads are processed, check if any files were modified:
```bash
git diff --name-only
```

If there are changes:
1. Run a quick sanity import check: `cd api && uv run python -c "import app" 2>&1` (skip if no Python files changed)
2. Stage all modified files: `git add -A`
3. Commit with: `git commit -m "fix: address PR #{PR_NUMBER} review comments"`
4. Push: `git push`

If no changes were made, skip the commit step.

### 7 — Summary

Print a summary:
```
Review complete.
  Fixed:    N threads
  Skipped:  N threads
  Comments: N threads

{commit SHA if committed, otherwise "No code changes."}
```

## Rules

- Never resolve a thread without posting a reply first — every resolved thread needs a paper trail
- Never auto-post a reply without showing the draft to the user first
- Never commit without running the sanity check first (when Python files changed)
- If a GraphQL mutation fails, report the error and continue to the next thread — don't abort the whole review
- Skip threads marked `isOutdated: true` — they refer to stale code and can't be meaningfully resolved
