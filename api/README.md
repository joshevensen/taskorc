# TaskOrc API

The headless FastAPI backend. Source of truth for all TaskOrc data — Users, Projects, Tasks, Notes, Logs, and Artifacts.

## Overview

- **Auth** — magic link → JWT. Tokens are validated on every request with no database lookup. No sessions.
- **Storage** — PostgreSQL
- **Runtime** — Python 3.13+, managed with [uv](https://docs.astral.sh/uv/)

## Development

```bash
uv run fastapi dev
```

Runs at http://localhost:8000. Interactive docs at http://localhost:8000/docs.

Requires a running PostgreSQL instance with migrations applied before starting.

## Deployment

```bash
uv run fastapi deploy
```

> FastAPI Cloud is currently in private beta. Join the waitlist at https://fastapicloud.com

## Project Structure

```
api/
  main.py          # FastAPI app entry point
  pyproject.toml   # Dependencies
```

## Dependencies

Add dependencies with uv:

```bash
uv add <package>
```
