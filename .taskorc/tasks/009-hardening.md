---
status: planned
priority: 9
---

# 9 — Hardening

## Description

Make the API production-ready. This task does not add features — it adds robustness. Consistent error responses, locked-down CORS, and a final audit of all env var documentation.

## Acceptance Criteria

- [ ] All error responses return `{"detail": "..."}` JSON — no HTML error pages, no unhandled exceptions leaking stack traces
- [ ] 404 responses are returned for missing resources, 403 for ownership violations, 422 for validation errors (FastAPI default)
- [ ] Unhandled exceptions return 500 with `{"detail": "Internal server error"}` — no stack trace exposed
- [ ] CORS is configured to allow only expected origins driven by `CORS_ORIGINS` env var
- [ ] All tests still pass after hardening changes
- [ ] Every env var the app reads is declared in `Settings`, present in `.env.example`, and documented in `README.md`

## Subtasks

### 1 — Global exception handler

**Prompt:** In `api/main.py`, add a global exception handler using `@app.exception_handler(Exception)`. It should catch any unhandled exception, log it (use Python's `logging` module, not `print`), and return a JSON response with status 500 and body `{"detail": "Internal server error"}`. Do not expose the exception message or stack trace in the response body. FastAPI's built-in `RequestValidationError` handler already returns 422 — do not override it.

---

### 2 — CORS configuration

**Prompt:** Add `CORSMiddleware` to the FastAPI app in `api/main.py`. Read allowed origins from `settings.CORS_ORIGINS` (a comma-separated string — split and strip whitespace). The CLI is the only client — there is no browser frontend in production. Configure `allow_methods=["*"]` and `allow_headers=["Authorization", "Content-Type"]`. Do not use `allow_origins=["*"]` in any config.

---

### 3 — Final env var audit

**Prompt:** Review `api/app/core/config.py` and `api/.env.example`. Verify every env var the application reads is: declared in `Settings`, present in `.env.example` with a description comment, and listed in `api/README.md` under a "Configuration" section. Ensure `.env` is in `api/.gitignore` and that no secrets appear in any committed file.
