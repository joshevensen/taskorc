# TaskOrc — Entities

---

## Overview

TaskOrc is built on a relational database (PostgreSQL). The entity model is intentionally lean — designed for a single founder working across multiple software projects. There are no roles, no multi-user collaboration, and no skill delivery infrastructure. Every entity exists to serve planning, execution, or memory.

Code context is not stored in the database. The Orc directs Claude Code to write context directly into the codebase — inline comments, docblocks, and module-level README files. This keeps code knowledge versioned, co-located with the code, and natively readable by Claude Code without API calls.

---

## Entities

### User

The authenticated founder. There is only ever one User in a TaskOrc instance. The User entity handles auth and stores two distinct types of personal data: configuration settings and founder insight.

**Key attributes:**

- Name and email
- Settings — JSON column for configuration and preferences. Tool choices, execution defaults, notification preferences, and other key/value pairs.
- Founder notes — large text field capturing insight about the founder. How they think, working patterns, tradeoffs they consistently make, and preferences the Orc has learned or been told. Maintained by the Orc — not written directly by the user.
- Timestamps

**Relationships:**

- Has many Projects

---

### Project

A software project the founder is working on. Project is the top-level container for all work, memory, and activity. Since a project maps directly to a business and a codebase, it holds both the repository configuration and the business context that was previously split across a config file and separate memory dimensions.

**Key attributes:**

- Name — the project name
- Description — what this project is and what it does
- Repo URL — the GitHub repository URL
- Tech stack — JSON array of technologies, frameworks, and tools (e.g. `["Laravel", "Vue", "PostgreSQL", "Digital Ocean"]`)
- Branch naming convention — e.g. `feature/`, `fix/`
- Default base branch — e.g. `main`
- Test command — e.g. `php artisan test`
- Lint command — e.g. `./vendor/bin/pint`
- Format command — e.g. `prettier --write`
- Timestamps

**Relationships:**

- Belongs to User
- Has many Tasks
- Has many Notes
- Has many Logs
- Has many Artifacts

---

### Task

The primary unit of work in TaskOrc. A Task is both the plan and the spec — it captures what needs to be built, why, what the acceptance criteria are, and what done looks like. Tasks are always scoped to a Project.

Subtasks are stored as a JSON array on the Task. Each subtask has a human-readable description you can inspect and an LLM-optimized prompt Claude Code executes. The Orc generates subtasks at planning time. You never write them directly, but you can review them before execution. Claude Code checks subtasks off as it completes them — giving the Orc a recoverable execution state if something fails mid-run.

Tweaks and bug fixes do not create Tasks. They are recorded directly as Log entries.

**Key attributes:**

- Title — short description of what needs to be built
- Description — full spec. What needs to be built, why, and relevant context. This is the human-readable plan the Orc and you agree on before execution.
- Problem — optional text field describing the problem being solved or the motivation behind the Task. Useful for grounding planning conversations.
- Acceptance criteria — nullable JSON array defining what done looks like. Each entry is a discrete, verifiable condition.
- Priority — nullable integer. Lower number = higher priority. Managed by the Orc via `/orc-prioritize`.
- Status — current position in the workflow (`draft`, `planned`, `in_progress`, `complete`, `failed`, `on_hold`, `cancelled`)
- Subtasks — JSON array of execution units. Each entry contains:
    - `id` — unique identifier within the Task
    - `description` — human-readable summary of what this subtask does
    - `prompt` — LLM-optimized instruction for Claude Code
    - `completed` — boolean, checked off by Claude Code during execution
- Branch — git branch created for this Task
- PR URL — pull request URL once opened
- Execution mode — `guided` or `autonomous`
- Timestamps

**Relationships:**

- Belongs to Project
- Can have many Artifacts
- Can have many Logs

---

### Note

Business knowledge about a Project. Notes are the Orc's structured memory of the business — product direction, strategic context, domain knowledge, past decisions and their reasoning, user insights, and constraints.

Notes are created and maintained exclusively by the Orc. You never write Notes directly — you tell the Orc things via `/orc-remember` and it structures and stores them. The Orc also creates Notes passively from skill activity when something worth remembering surfaces.

If a Note spans two categories the Orc splits it into two focused Notes rather than compromising on categorization. This keeps each Note tight and retrieval precise.

**Key attributes:**

- Title — short summary of what this Note captures
- Body — the content, written by the Orc in plain prose
- Category — single value from a fixed set: `product`, `strategy`, `users`, `market`, `decisions`, `constraints`, `goals`, `general`
- Timestamps

**Relationships:**

- Belongs to Project

---

### Log

An append-only activity trail. Every skill invocation creates a Log entry. Logs are the Orc's record of what it has done — what skill ran, what it acted on, how long it took, and what the outcome was.

Logs are never updated or deleted. They are the foundation of passive memory — the Orc mines Log history to surface patterns, infer context, and update Notes without requiring manual input.

Logs can be tied to a Task or exist standalone. Tweaks and bug fixes log their activity without creating a Task — the Log is the record.

**Key attributes:**

- Skill — which skill was invoked
- Task — optional reference to the Task the skill ran on
- Duration — how long the skill took in milliseconds
- Outcome — `success`, `failure`, `skipped`
- Summary — brief plain-language description of what the skill did
- Metadata — flexible JSON column for skill-specific data (branch created, PR URL, fix approach chosen, subtasks completed, etc.)
- Timestamps

**Relationships:**

- Belongs to Project
- Optionally belongs to a Task

---

### Artifact

External context attached to a Project or Task. Artifacts capture references that belong to the work but live outside the codebase — Figma links, Loom videos, error logs, screenshots, reference documents, and any other external material attached via `/orc-attach`.

For certain URL types the Orc can pull in a preview or summary at attach time. Artifact content is injected into context at execution time so Claude Code has everything it needs.

**Key attributes:**

- Title — name of the reference
- URL — the external link
- Body — optional summary or preview pulled by the Orc at attach time
- Type — `figma`, `video`, `document`, `error_log`, `screenshot`, `other`
- Parent type — `project` or `task`
- Parent ID — polymorphic reference to the Project or Task
- Timestamps

**Relationships:**

- Belongs to Project or Task (polymorphic)
- Belongs to User

---

## Non-Entity Storage

### Local Config — `~/.config/taskorc/config.json`

Lives on the machine. Never committed. Caches the OAuth token and installed skill versions. Populated by `orc init` and refreshed automatically via TTL-based cache invalidation. All project and repository configuration lives in the database — this file is auth and tooling only.

### Code Context — In the Codebase

Code knowledge lives in the codebase itself, not in the database. The Orc directs Claude Code to write and maintain context directly — inline comments, docblocks, and module-level README files. This keeps code knowledge versioned alongside the code and natively readable by Claude Code at execution time without any API calls.

---

## Entity Summary

|Entity|Purpose|
|---|---|
|User|Auth, settings, and founder insight|
|Project|Top-level container — repo config, tech stack, business context|
|Task|Plan, spec, and execution unit — with subtasks JSON|
|Note|Business knowledge, Orc-created, categorized|
|Log|Append-only activity trail|
|Artifact|External context attached to a Project or Task|