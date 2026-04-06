# TaskOrc  — Product Concept

> _Your personal AI project manager. It knows your business, remembers your decisions, and gets things built._

---

## The Problem

Building a software product solo means wearing every hat. You are the founder, the PM, the engineer, and the support desk. The mental overhead of switching between those roles — holding context, making decisions, remembering why things were built a certain way — is relentless.

Existing PM tools don't help. They're boards for tracking work, not systems for thinking through it. They don't know your codebase, don't remember your past decisions, and have no opinion about what you should work on next. Every session with an AI coding tool starts from scratch because nothing carries context forward.

TaskOrc is built around a different premise: **you shouldn't have to carry context in your head**. The Orc carries it for you — across your business, your product decisions, and your codebase. It plans your work, breaks it into tasks an AI can execute, and gets things built while you review and direct.

---

## What TaskOrc Is

TaskOrc is a personal AI project manager with three jobs:

1. **Remember** — accumulate knowledge about you, your business, and your codebase over time. This memory informs every planning and execution decision.
2. **Plan** — shape vague ideas into specs and LLM-executable tasks, using that memory to make planning genuinely useful rather than generic.
3. **Execute** — hand tasks to Claude Code as the execution engine. Either you supervise directly, or the Orc runs autonomously and delivers a PR you review.

The memory layer is what separates TaskOrc from a task list plus Claude. It is the compounding asset. The longer you use it, the smarter the Orc becomes about what you're building and why.

---

## Projects

A Project is a software product the founder is building. It is the top-level container for all work, memory, and activity within that codebase. TaskOrc supports multiple Projects — each with its own Tasks, Notes, Logs, and repository configuration.

Project holds everything needed to work with a codebase: the repo URL, tech stack, branch conventions, and tool commands. There is no per-repo config file committed to the repository — all configuration lives in the database.

---

## Tasks

A Task is the primary unit of work. It is both the plan and the spec — capturing what needs to be built, why, what the problem is, and what done looks like. Tasks always belong to a Project.

The Orc generates subtasks from the Task description at planning time. Subtasks are the Orc's internal execution breakdown — each one a precise, LLM-optimized prompt for Claude Code. Every subtask also has a human-readable description so you can inspect what the Orc is about to do before execution begins. Claude Code checks subtasks off as it completes them, giving the Orc a recoverable execution state if something fails mid-run.

Not all work creates a Task. Tweaks and bug fixes bypass the Task entity entirely — the Orc executes and records the activity directly as a Log entry, with a Note created if anything worth remembering surfaces.

---

## Memory

Memory is the core of TaskOrc. It is what makes the Orc a genuine collaborator rather than a stateless tool.

Memory is built across three dimensions:

### Founder

Insight about you as a founder — how you think, your working patterns, the tradeoffs you consistently make, and preferences the Orc has learned over time. Stored as a text field on your User record. The Orc maintains this; you don't write it directly.

### Business

Knowledge about a specific Project — product direction, domain knowledge, strategic context, past decisions and their reasoning, user insights, and constraints. Stored as discrete Notes on the Project — each focused, categorized, and queryable. The Orc creates and updates these as knowledge accumulates.

### Code

Codebase architecture, patterns, technical decisions, and what exists where. Stored directly in the codebase — inline comments, docblocks, and module-level README files written and maintained by the Orc via Claude Code. Code knowledge lives where the code lives, versioned alongside it, and natively readable by Claude Code at execution time.

### How Memory Is Built

Memory accumulates through two mechanisms:

**Active** — you tell the Orc things explicitly through `/orc-remember`. Founding decisions, strategic pivots, technical constraints, personal preferences. The Orc structures what you share and creates Notes on the appropriate memory dimension. You don't write Notes directly — the Orc does.

**Passive** — the Orc infers from activity. Every skill invocation creates a Log entry. Log entries are the Orc's activity trail — an append-only record of what was done, on what entity, and what the outcome was. The Orc mines Log entries over time to surface patterns, update Notes, and deepen its understanding without requiring manual input.

Notes and Logs serve distinct purposes. A Note is knowledge — something the Orc knows about Fibermade. A Log is activity — something the Orc did. Log entries can trigger Note creation when the Orc recognises something worth remembering from its own activity.

The flywheel: more activity → richer Logs → smarter Notes → better planning → more valuable Orc → more reason to use it.

---

## Execution Modes

Execution is triggered at the Task level. Both modes use Claude Code as the engine and run all subtasks — in parallel where independent, sequentially where dependencies require it. If any subtask fails, execution stops immediately and the Orc reports what succeeded and what needs attention before proceeding.

### Guided Mode

You invoke `/orc-build` in Claude Code in your terminal. The Orc loads the Task and all its context — description, problem, acceptance criteria, subtasks, business memory, and code memory — and you supervise the work directly. The branch and PR are created at the end.

### Autonomous Mode

The Orc fires `claude --remote` with the Task ID and full context. Claude Code on the web clones your repo into a secure Anthropic-managed VM and executes the subtasks. If anything fails, execution stops and you are notified before proceeding. You review the diff in the browser and merge the PR. You never open VS Code.

You choose the mode per Task. Complex or risky work — guided. Routine, well-defined Tasks — autonomous. Over time, as the Orc's memory deepens and Task quality improves, more work moves to autonomous.

The long-term direction is a fully autonomous Orc that builds while you sleep and delivers PRs you review in the morning.

---

## The Orc

The Orc is the orchestration layer. It is not a chatbot. It is not a board. It is the thread that runs through everything.

**In planning:** the Orc knows your business goals, your codebase patterns, and your past decisions. It generates specs that reflect reality, not templates.

**In execution:** the Orc briefs Claude Code with everything it needs to build correctly. It tracks outcomes, logs what was built, and feeds that back into memory.

**Over time:** the Orc accumulates institutional knowledge about your projects that would otherwise live only in your head. Every decision recorded. Every pattern learned. Every tradeoff remembered.

The north star: _Does this make the Orc smarter, or does it ask you to carry context you shouldn't have to carry?_

---

## Skills

Skills are the interface between you and TaskOrc. They are instruction files installed as a Claude plugin, prefixed with `/orc-` for instant discoverability in Claude Code.

**Workflow skills** advance a Task through the planning and execution flow. Running a skill _is_ the status update — workflow state emerges from activity, not manual dragging.

**Utility skills** interact with the workflow without advancing it — checking your queue, attaching context, reviewing status.

**Base skills** handle setup, onboarding, and help.

For a full skills reference see `Skills.md`.

---

## Git Integration

TaskOrc treats git as a primary data source, not an afterthought.

- Branch name → tied to a Task
- Commits → activity feeding passive memory
- PR opened / merged → workflow state changes and memory updates

The Orc creates branches, manages naming conventions, and connects git activity back to TaskOrc automatically. In autonomous mode, you never touch git directly — the Orc handles everything from branch creation to PR.

Third-party integrations are handled through existing CLIs and MCP servers — `gh` for GitHub, Laravel Forge and Digital Ocean via their CLIs for deployments, Sentry via MCP for bug context. TaskOrc orchestrates these tools rather than replacing them.

---

## Technical Architecture

CLI-first. No web app.

### 1. API (FastAPI)

The core backend. Manages Users, Projects, Tasks, Notes, Logs, and Artifacts. Headless.

### 2. CLI (Node.js)

One responsibility: API interaction — GitHub CLI-style commands used by skills as subprocesses to read and write TaskOrc data. No skill management — the Claude plugin handles its own updates via the marketplace.

### 3. Auth

Magic link via email. `orc auth login` prompts for your email, sends a magic link, and stores a signed JWT in `~/.config/taskorc/config.json` on click. Every CLI request sends the JWT as a Bearer token — validated by FastAPI on each request with no database lookup. No external auth service required.

### 4. Skills

Installed as a Claude plugin from the Claude marketplace. Updates are handled by the marketplace — no CLI involvement required.

### 5. Execution

Claude Code is the execution engine — locally via terminal for guided mode, via Claude Code on the web for autonomous mode. TaskOrc provides context; Claude Code provides the coding intelligence.

---

## Build Sequence

1. **Design the memory model** — the three dimensions, how Notes and Logs feed it, how memory informs planning
2. **Write the skills** — forces precise definition of what the Orc does at each step, reveals exactly what the API needs
3. **API** — headless, just enough to support the skills and memory model
4. **CLI** — auth, skill management, API interaction
5. **Autonomous execution** — wire `claude --remote` into the execution skill

The memory model step is the most important and most tempting to skip. Don't skip it.

---

## What TaskOrc Is Not

- **Not a team tool** — designed for a solo founder. No roles, no collaboration, no skill matrices.
- **Not a code host** — TaskOrc never touches code directly. Claude Code does.
- **Not a chatbot** — the Orc has opinions and direction. It tells you what to do next. That's the point.
- **Not another board** — there is no board. There is a priority queue, a planning flow, and an execution engine. The Orc manages the queue so you don't have to.
- **Not stateless** — every interaction teaches the Orc something. Memory is the product.