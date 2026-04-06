# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

Three-component monorepo — each component lives in its own subdirectory and has its own toolchain:

```
taskorc/
  api/      # FastAPI backend (Python 3.13+, uv) — source of truth for all data
  cli/      # oclif CLI (TypeScript, Node.js 22+) — binary is `orc`
  plugin/   # Claude plugin — skills namespaced /orc:skill-name, hooks, agents
```

The CLI is not for direct user use — plugin skills invoke it as a subprocess. The plugin is distributed via the Claude marketplace (`/plugin install orc@claude-plugins-official`) or loaded locally for development with `claude --plugin-dir ./plugin`.

Auth is magic link → JWT. The JWT is validated on every API request with no database lookup; tokens are stored at `~/.config/taskorc/config.json`.

See `.docs/` for full concept, entity, and skill documentation.

## Build & Test Commands

All commands must be run from the relevant subdirectory.

**CLI** (`cd cli`):
```bash
npm install
npm run build    # tsc → dist/
npm run lint     # eslint
npm test         # mocha
npm link         # installs orc globally after build
```

**API** (`cd api`):
```bash
uv run fastapi dev    # development server
```
The API requires a running PostgreSQL instance and migrations applied before running.

## Commit Conventions

Use conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
