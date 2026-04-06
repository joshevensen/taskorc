# TaskOrc

> Your personal AI project manager. It knows your business, remembers your decisions, and gets things built.

TaskOrc is an open source AI project manager for solo founders and indie developers. It connects Claude Code to a persistent memory layer — so every planning session, every build, every bug fix accumulates institutional knowledge about your project instead of evaporating when the conversation ends.

## The Problem

Building a software product solo means wearing every hat. The mental overhead of switching between roles — holding context, making decisions, remembering why things were built a certain way — is relentless.

Existing PM tools don't help. They're boards for tracking work, not systems for thinking through it. They don't know your codebase, don't remember your past decisions, and have no opinion about what to work on next. Every AI coding session starts from scratch.

TaskOrc is built around a different premise: **you shouldn't have to carry context in your head**. The Orc carries it for you.

## How It Works

TaskOrc has three jobs:

1. **Remember** — accumulate knowledge about you, your business, and your codebase over time
2. **Plan** — shape vague ideas into specs and executable tasks, informed by that memory
3. **Execute** — hand tasks to Claude Code, either with you supervising or fully autonomously

The memory layer is what separates TaskOrc from a task list plus Claude. It is the compounding asset. The longer you use it, the smarter the Orc becomes about what you're building and why.

## Memory

Memory is the core of TaskOrc. It is built across three dimensions:

- **Founder** — how you think, your working patterns, the tradeoffs you consistently make. Maintained by the Orc as it learns.
- **Business** — product direction, strategic context, past decisions and their reasoning, user insights. Stored as structured Notes on each Project.
- **Code** — codebase architecture, patterns, technical decisions, and what exists where. Written directly into the codebase as comments, docblocks, and module READMEs — versioned alongside the code and natively readable by Claude Code.

Memory builds passively through activity and actively when you tell the Orc something via `/orc:remember`. The flywheel: more activity → richer logs → smarter notes → better planning → more valuable Orc.

## Skills

You interact with TaskOrc through skills — slash commands installed via the [Orc Claude plugin](#installation). Skills are namespaced `/orc:skill-name` for instant autocomplete discoverability.

### Workflow Skills

| Skill | Purpose |
|---|---|
| `/orc:create` | Plan a feature or change — opens a memory-informed planning conversation |
| `/orc:build` | Execute a task — guided (you supervise) or autonomous (Orc builds, you review the PR) |
| `/orc:tweak` | Small change with no planning needed — straight to execution |
| `/orc:bug` | Fix a defect — takes a Sentry URL or plain description |
| `/orc:complete` | Close out a completed task — cleans branch, updates memory |

### Utility Skills

| Skill | Purpose |
|---|---|
| `/orc:remember` | Tell the Orc something worth knowing |
| `/orc:inbox` | Everything requiring your attention across all projects |
| `/orc:next` | Get the highest-priority task and start building |
| `/orc:status` | Plain language summary of where a task stands |
| `/orc:prioritize` | Reorder the task queue |
| `/orc:hold` | Deliberately pause a task |
| `/orc:cancel` | Kill a task |
| `/orc:attach` | Add external context — Figma links, error logs, screenshots, docs |

### Base Skills

| Skill | Purpose |
|---|---|
| `/orc:setup` | Onboarding — connect to the API, create your first project, seed memory |
| `/orc:about` | Conversational help — ask anything about how TaskOrc works |
| `/orc:sync` | Refresh the local config cache |

## Execution Modes

**Guided** — you invoke `/orc:build` in your terminal. The Orc loads the task with full context and you supervise the work directly. A branch and PR are created when complete.

**Autonomous** — the Orc fires `claude --remote` with the task ID and context. Claude Code on the web executes the subtasks in a secure VM. You review the diff in the browser and merge the PR. You never open your editor.

You choose the mode per task. Complex or risky work — guided. Routine, well-defined tasks — autonomous.

## Architecture

CLI-first. No web app. Three components:

```
taskorc/
  api/        # FastAPI — Users, Projects, Tasks, Notes, Logs, Artifacts
  cli/        # Node.js (oclif) — orc auth, orc project, orc task, etc.
  plugin/     # Claude plugin — skills, hooks, agents
```

**API** — headless FastAPI backend. The source of truth for all data. Auth via magic link, validated by JWT on every request with no database lookup.

**CLI** — GitHub CLI-style commands used by skills as subprocesses to read and write TaskOrc data. The binary is `orc`. Not for direct use — skills call it behind the scenes.

**Plugin** — skills installed as a Claude plugin from the marketplace. Global hooks ensure every skill invocation is logged and evaluated for memory, regardless of whether the skill completed cleanly.

## Installation

### 1. Run the API

```bash
cd api
uv run fastapi dev
```

### 2. Install the CLI

```bash
cd cli
npm install
npm run build
npm link        # makes orc available globally
```

### 3. Install the Plugin

In Claude Code:

```
/plugin install orc@claude-plugins-official
```

Or load locally for development:

```bash
claude --plugin-dir ./plugin
```

### 4. Set Up Your First Project

```
/orc:setup
```

The Orc will walk you through authentication and creating your first project.

## Requirements

- [Claude Code](https://claude.ai/code) with an active subscription
- Python 3.13+ and [uv](https://docs.astral.sh/uv/)
- Node.js 22+
- PostgreSQL

## Contributing

TaskOrc is open source and welcomes contributions. The build sequence that makes the most sense:

1. Memory model — the three dimensions, how Notes and Logs feed it
2. Skills — forces precise definition of what the Orc does at each step
3. API — just enough to support the skills and memory model
4. CLI — auth and API interaction
5. Autonomous execution — wire `claude --remote` into the build skill

See the `.docs/` directory for full concept, entity, and skill documentation.

## License

MIT
