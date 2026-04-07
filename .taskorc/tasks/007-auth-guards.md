---
status: planned
priority: 7
---

# 7 — Authorization Guards

## Description

Every resource must be scoped to the authenticated user. Task 6 wired up auth via `get_current_user` but did not enforce ownership — a user could request any project by ID and get a response. This task adds ownership checks in services so that cross-user access returns 403, not leaked data.

The guards live in services, not routers. Routers pass the current user in; services verify ownership before executing the query.

## Acceptance Criteria

- [ ] A user cannot read, update, or delete another user's Projects — returns 403
- [ ] A user cannot read, create, update, or delete Tasks belonging to a Project they do not own — returns 403
- [ ] A user cannot read, create, update, or delete Notes belonging to a Project they do not own — returns 403
- [ ] A user cannot read Logs belonging to a Project they do not own — returns 403
- [ ] A user cannot read, update Artifacts attached to a Project or Task they do not own — returns 403
- [ ] All checks raise `HTTPException(status_code=403, detail="Forbidden")` — never 404 (do not leak whether the resource exists)
- [ ] Ownership checks are in service functions, not in routers
- [ ] A reusable `assert_project_owner(db, project_id, user_id)` helper avoids duplicating the ownership query across services

## Subtasks

### 1 — Ownership helper

**Prompt:** Create `api/app/services/ownership.py`. Implement `assert_project_owner(db: AsyncSession, project_id: UUID, user_id: UUID) -> Project`. Query the DB for the project. If not found or `project.user_id != user_id`, raise `HTTPException(status_code=403, detail="Forbidden")`. Return the `Project` object if ownership passes. This helper will be called at the top of any service function that operates on a project or its children.

---

### 2 — Guard project service

**Prompt:** Update `api/app/services/project.py`. Add `user_id: UUID` parameter to `get_project`, `update_project`. At the start of each function call `assert_project_owner(db, project_id, user_id)`. For `list_projects` the query already filters by `user_id` — no additional check needed. Pass `current_user.id` from the router into these service calls.

---

### 3 — Guard task service

**Prompt:** Update `api/app/services/task.py`. Every function that takes a `project_id` must call `assert_project_owner(db, project_id, user_id)` first. For functions that take a `task_id` directly (get, update, set_subtasks, complete_subtask), load the task first, then call `assert_project_owner` using `task.project_id`. Add `user_id: UUID` parameter to all affected functions and pass `current_user.id` from the router.

---

### 4 — Guard note service

**Prompt:** Update `api/app/services/note.py`. Apply the same pattern as tasks: project-scoped functions call `assert_project_owner` up front; note-scoped functions load the note first then check `note.project_id`. Add `user_id: UUID` to all affected functions.

---

### 5 — Guard log service

**Prompt:** Update `api/app/services/log.py`. Add `assert_project_owner` call at the start of both `create_log` and `list_logs`. Add `user_id: UUID` parameter to both functions and pass `current_user.id` from the router.

---

### 6 — Guard artifact service

**Prompt:** Update `api/app/services/artifact.py`. For `create_artifact`, resolve the parent (project or task) and verify the user owns it before creating. For `get_artifact`, `update_artifact`, and `list_artifacts`, resolve ownership through the artifact's `parent_type` and `parent_id`. If the parent is a task, traverse to its project to check ownership. Raise 403 on any ownership failure.

---

### 7 — Update routers to pass user_id

**Prompt:** Review all routers in `api/app/routers/`. Wherever a service function now requires `user_id`, pass `current_user.id` (where `current_user` comes from `Depends(get_current_user)`). No router should be doing ownership logic itself — just forwarding the user ID into the service.

---

### 8 — Commit and push

**Prompt:** From the repo root, stage and commit all changes from this phase, then push:
```bash
git add api/app/services/ api/app/routers/
git commit -m "feat(api): phase 7 — authorization guards"
git push
```
