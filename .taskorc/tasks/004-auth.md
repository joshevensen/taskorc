---
status: planned
priority: 4
---

# 4 — Auth

## Description

Implement Personal Access Token (PAT) authentication. A PAT is generated once via `POST /auth/token`, stored as a bcrypt hash on the User record, and sent as a Bearer token on every subsequent request. No email, no magic links, no JWT. The CLI stores the raw token in `~/.config/taskorc/config.json` after generation — it is never returned by the API again.

Do not move to task 5 until `get_current_user` is working and tested.

## Acceptance Criteria

- [ ] `POST /auth/token` accepts `name` and `email`, upserts the User record, generates a PAT, stores the bcrypt hash on User, and returns the raw token exactly once
- [ ] The raw PAT is never stored — only the bcrypt hash. After generation, it cannot be retrieved via the API
- [ ] `DELETE /auth/token` clears `pat_hash` on the User record (revokes access)
- [ ] `get_current_user` reads the `Authorization: Bearer <pat>` header, finds the User, verifies the PAT against the stored hash, and returns the `User` ORM object
- [ ] `get_current_user` raises HTTP 401 if the header is missing, the token doesn't match, or no User exists
- [ ] PATs are prefixed with `orc_` for easy identification (e.g., `orc_a3f9...`)
- [ ] PAT utilities are covered by unit tests: generate format, hash/verify roundtrip, wrong token rejection

## Subtasks

### 1 — PAT utilities

**Prompt:** Create `api/app/core/auth.py`. Implement three functions using `passlib.hash.bcrypt`:

`generate_pat() -> str` — generates a cryptographically random PAT using `secrets.token_hex(32)`, prefixed with `orc_`. Returns the raw token string (e.g., `orc_a3f9b2c1...`).

`hash_pat(pat: str) -> str` — returns a bcrypt hash of the raw PAT using `passlib.hash.bcrypt.hash(pat)`.

`verify_pat(pat: str, pat_hash: str) -> bool` — returns `True` if the raw PAT matches the stored hash using `passlib.hash.bcrypt.verify(pat, pat_hash)`. Returns `False` on any mismatch — never raises.

---

### 2 — Auth router

**Prompt:** Create `api/app/routers/auth.py` with two endpoints:

`POST /auth/token` — accepts `{"name": "...", "email": "..."}`. Looks up the User by email. If not found, creates a new User with the provided name and email. Generates a PAT via `generate_pat()`. Hashes it via `hash_pat()` and saves the hash to `User.pat_hash`. Returns `{"token": "<raw_pat>", "note": "Store this token — it will not be shown again."}`. This endpoint is intentionally unprotected (it is the bootstrap).

`DELETE /auth/token` — protected by `get_current_user`. Sets `User.pat_hash = None` and saves. Returns `{"message": "Token revoked. Run orc auth login to generate a new one."}`.

Register the router in `main.py` with prefix `/auth` and tag `auth`.

---

### 3 — Auth dependency

**Prompt:** Add `get_current_user` to `api/app/core/auth.py`. Implement it as a FastAPI dependency:

1. Read the `Authorization` header. If missing or not `Bearer <token>`, raise `HTTPException(status_code=401, detail="Missing or invalid Authorization header")`.
2. Extract the raw token from the header.
3. Query the DB: `SELECT * FROM users WHERE pat_hash IS NOT NULL`. Since there is only one user, fetch all and find the one where `verify_pat(token, user.pat_hash)` returns `True`.
4. If no match is found, raise `HTTPException(status_code=401, detail="Invalid token")`.
5. Return the matching `User` ORM object.

Note on step 3: with a single-user system, a linear scan is fine. If this ever becomes multi-user, add a token lookup table instead.

---

### 4 — Update User model

**Prompt:** Update `api/app/models/user.py` to add `pat_hash` (Text, nullable) to the `User` model. This field stores the bcrypt hash of the current active PAT. `NULL` means no active token (logged out). Run `alembic revision --autogenerate -m "add pat_hash to users"` and `alembic upgrade head` to apply.

---

### 5 — Smoke test

**Prompt:** Start the dev server. Manually verify the full flow:
1. `POST /auth/token` with name and email → receive raw `orc_...` token
2. `GET /users/me` with `Authorization: Bearer <token>` → receive user data
3. `GET /users/me` with a wrong token → receive 401
4. `GET /users/me` with no header → receive 401
5. `DELETE /auth/token` with valid token → receive revocation message
6. `GET /users/me` with the now-revoked token → receive 401

---

### 6 — Commit and push

**Prompt:** From the repo root, stage and commit all changes from this phase, then push:
```bash
git add api/app/core/auth.py api/app/routers/auth.py api/app/models/user.py api/alembic/versions/
git commit -m "feat(api): phase 4 — PAT authentication"
git push
```
