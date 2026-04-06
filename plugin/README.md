# TaskOrc Plugin

The Claude plugin. Skills and hooks that turn Claude Code into the Orc — your personal AI project manager.

## Overview

Skills are namespaced `/orc:skill-name` for instant autocomplete discoverability in Claude Code. Hooks run automatically on every skill invocation to log activity and evaluate it for memory, regardless of whether the skill completed cleanly.

## Installation

**From the Claude marketplace:**

```
/plugin install orc@claude-plugins-official
```

**Locally for development:**

```bash
claude --plugin-dir ./plugin
```

## Skills

### Workflow

| Skill | Purpose |
|---|---|
| `/orc:create` | Plan a feature or change — opens a memory-informed planning conversation |
| `/orc:build` | Execute a task — guided (you supervise) or autonomous (Orc builds, you review the PR) |
| `/orc:tweak` | Small change with no planning needed — straight to execution |
| `/orc:bug` | Fix a defect — takes a Sentry URL or plain description |
| `/orc:complete` | Close out a completed task — cleans branch, updates memory |

### Utility

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

### Base

| Skill | Purpose |
|---|---|
| `/orc:setup` | Onboarding — connect to the API, create your first project, seed memory |
| `/orc:about` | Conversational help — ask anything about how TaskOrc works |
| `/orc:sync` | Refresh the local config cache |

## Project Structure

```
plugin/
  .claude-plugin/
    plugin.json    # plugin metadata
  commands/        # one SKILL.md per /orc:skill-name
  hooks/
    hooks.json     # event hooks configuration
```

## Adding a Skill

Create a new directory under `commands/` and add a `SKILL.md`:

```
commands/
  orc:skill-name/
    SKILL.md
```

Skills have access to the `orc` CLI binary (must be built and linked from `../cli`) for reading and writing TaskOrc data.
