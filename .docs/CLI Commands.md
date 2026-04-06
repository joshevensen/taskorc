# TaskOrc — CLI Commands

---

## Overview

The TaskOrc CLI (`orc`) has two distinct purposes:

- **Core commands** — used by you to manage auth and local config.
- **API commands** — used by skills to interact with TaskOrc data programmatically. Skills invoke these commands as subprocesses to read and write Projects, Tasks, Notes, Logs, and Artifacts.

You interact with TaskOrc through `/orc-` skills in Claude Code. The API commands are the plumbing those skills use behind the scenes — flag-driven, JSON by default, scriptable and precise.

---

## Core Commands

---

### Auth

Manages authentication with the TaskOrc API.

```bash
orc auth login
```

Prompts for your email and sends a magic link. Clicking the link stores a signed JWT in `~/.config/taskorc/config.json`. All subsequent CLI requests send this token as a Bearer header.

```bash
orc auth logout
```

Clears the stored JWT from local config.

```bash
orc auth status
```

Shows whether you are currently authenticated and which account is active.

---

### Config

Manages the local config cache stored at `~/.config/taskorc/config.json`.

```bash
orc config show
```

Displays the current local config — cached user identity, active project context, and cache timestamps.

```bash
orc config sync
```

Refreshes the local config cache from the API. Run when something feels stale.

```bash
orc config reset
```

Wipes the local config completely. Requires `orc auth login` before the CLI is usable again.

---

### System

```bash
orc version
```

Displays the current CLI version.

```bash
orc help
```

Displays available commands and usage. For conversational help about how TaskOrc works, use `/orc-about` in Claude Code.

---

## API Commands

API commands are invoked by skills as subprocesses to read and write TaskOrc data. They are not designed for direct use — you interact with TaskOrc through skills in Claude Code.

All API commands return JSON by default. All commands that write data require a valid JWT in local config.

---

### `orc project`

CRUD operations on Projects.

```bash
orc project create
  --name <string>
  --description <string>
  --repo-url <string>
  --tech-stack <json-array>
  --branch-prefix <string>
  --base-branch <string>
  --test-command <string>
  --lint-command <string>
  --format-command <string>
```

Creates a new Project. Returns the created Project as JSON.

```bash
orc project get <id>
```

Returns a single Project with all related data.

```bash
orc project list
```

Returns all Projects for the authenticated user.

```bash
orc project update <id>
  --name <string>
  --description <string>
  --repo-url <string>
  --tech-stack <json-array>
  --branch-prefix <string>
  --base-branch <string>
  --test-command <string>
  --lint-command <string>
  --format-command <string>
```

Updates a Project.

---

### `orc task`

CRUD operations on Tasks.

```bash
orc task create
  --project <project-id>
  --title <string>
  --description <string>
  --problem <string>
  --acceptance-criteria <json-array>
  --priority <integer>
  --status <draft|planned>
```

Creates a new Task. Returns the created Task as JSON.

```bash
orc task get <id>
```

Returns a single Task with all related data — subtasks, Artifacts, Logs, and current status.

```bash
orc task list
  --project <project-id>
  --status <status>
  --limit <number>
```

Returns a list of Tasks matching the given filters.

```bash
orc task update <id>
  --title <string>
  --description <string>
  --problem <string>
  --acceptance-criteria <json-array>
  --priority <integer>
  --status <status>
  --branch <branch-name>
  --pr-url <string>
  --execution-mode <guided|autonomous>
```

Updates a Task.

```bash
orc task subtasks <id>
  --set <json-array>
```

Replaces the subtasks JSON array on a Task. Each subtask must include `id`, `description`, `prompt`, and `completed`.

```bash
orc task subtask-complete <task-id> <subtask-id>
```

Marks a single subtask as completed. Used by Claude Code to check off subtasks during execution.

```bash
orc task next
  --project <project-id>
```

Returns the highest priority planned Task for the given Project. Used by `/orc-next`.

---

### `orc note`

CRUD operations on Notes.

```bash
orc note create
  --project <project-id>
  --title <string>
  --body <string>
  --category <product|strategy|users|market|decisions|constraints|goals|general>
```

Creates a new Note. Returns the created Note as JSON.

```bash
orc note get <id>
```

Returns a single Note.

```bash
orc note list
  --project <project-id>
  --category <category>
  --limit <number>
```

Returns Notes matching the given filters. Used by skills to retrieve relevant memory before planning or execution.

```bash
orc note update <id>
  --title <string>
  --body <string>
  --category <category>
```

Updates a Note's content or category.

```bash
orc note delete <id>
```

Deletes a Note. Used by the Orc when a Note is superseded or incorrect.

---

### `orc log`

Read and create operations on the activity log. Logs are append-only — no update or delete.

```bash
orc log create
  --project <project-id>
  --skill <skill-name>
  --task <task-id>
  --duration <milliseconds>
  --outcome <success|failure|skipped>
  --summary <string>
  --metadata <json-string>
```

Creates a new Log entry. Called by every skill at the end of its invocation. `--task` is optional — tweaks and bug fixes log without a Task reference.

```bash
orc log list
  --project <project-id>
  --skill <skill-name>
  --task <task-id>
  --limit <number>
```

Returns Log entries matching the given filters.

---

### `orc artifact`

CRUD operations on Artifacts.

```bash
orc artifact create
  --title <string>
  --url <string>
  --body <string>
  --type <figma|video|document|error_log|screenshot|other>
  --parent-type <project|task>
  --parent-id <id>
```

Creates a new Artifact attached to a Project or Task.

```bash
orc artifact get <id>
```

Returns a single Artifact.

```bash
orc artifact list
  --parent-type <project|task>
  --parent-id <id>
```

Returns all Artifacts attached to a given Project or Task.

```bash
orc artifact update <id>
  --title <string>
  --body <string>
```

Updates an Artifact's title or body.

---

### `orc user`

Read and update operations on the authenticated user.

```bash
orc user me
```

Returns the current authenticated user — name, email, settings, and founder notes.

```bash
orc user update
  --founder-notes <string>
  --settings <json-string>
```

Updates the founder notes or settings on the User record. Used by the Orc to maintain Founder memory.

---

## Command Summary

|Group|Purpose|Used By|
|---|---|---|
|`orc auth`|Authentication|You|
|`orc config`|Local config management|You|
|`orc version`|CLI version|You|
|`orc help`|CLI documentation|You|
|`orc project`|Project CRUD|Skills|
|`orc task`|Task CRUD and subtask management|Skills|
|`orc note`|Note CRUD|Skills|
|`orc log`|Activity log|Skills|
|`orc artifact`|Artifact CRUD|Skills|
|`orc user`|User profile and founder memory|Skills|