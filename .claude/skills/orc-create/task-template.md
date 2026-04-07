## Draft template — created by orc-create

---
status: draft
priority: {ID}
---

# {ID} — {Title}

## Description

{What you want to build and why. Can be rough — this is just to get the idea captured.}


## Planned template — filled in by orc-plan

---
status: planned
priority: {ID}
---

# {ID} — {Title}

## Description

{Refined description of what needs to be built and why.}

## Acceptance Criteria

- [ ] {Discrete, verifiable condition for done}
- [ ] {Another condition}

## Subtasks

### 1 — {Subtask title}

{Human-readable description of what this subtask does and why.}

**Prompt:** {Complete, self-contained instruction Claude Code can execute directly. Include file paths, function signatures, and specific requirements. Assume no prior context.}

---

### 2 — {Subtask title}

{Human-readable description.}

**Prompt:** {Complete instruction.}

---

### N — Commit and push

**Prompt:** From the repo root, stage and commit all changes from this task, then push:
```bash
git add {relevant paths}
git commit -m "{conventional commit message}"
git push
```
