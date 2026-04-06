# TaskOrc — Skills

---

## Overview

Skills are the primary interface between you and TaskOrc. Every action in the system is a skill invocation. Skills are prefixed with `/orc-` for instant autocomplete discoverability in Claude Code.

Skills fall into three categories:

- **Workflow Skills** — advance a Task through the planning and execution flow
- **Utility Skills** — interact with the workflow without advancing it
- **Base Skills** — setup, memory building, and help

---

## MCP Requirements

The following MCP servers must be configured by the user. They are not bundled with the plugin.

- **Sentry MCP** — required by `/orc-bug` to pull issue details, stack traces, and breadcrumbs. Configure via your Claude MCP settings before using `/orc-bug`.

---

## Global Hooks

These hooks apply across all skill invocations. They are deterministic safety nets — skills are LLM-driven and cannot be relied upon to always log or capture memory. Hooks ensure it always happens.

### Skill Context File

Every skill writes a context file to `.taskorc/tmp/skill-context.json` at three points:

- **Start** — skill name, task ID if applicable, timestamp, status: `in_progress`
- **During** — decisions made, approaches chosen, anything surfaced mid-conversation
- **End** — final outcome, summary, duration, status: `success` | `failure` | `skipped`

The `.taskorc/tmp/` directory is gitignored. The file is deleted by the hook after processing.

If a skill crashes before the final update, the hook reads `in_progress` and logs the entry as `failure`.

### Log Hook (Stop)

Fires after every skill invocation. Reads `.taskorc/tmp/skill-context.json` and calls `orc log create` with the contents. Ensures every skill invocation is recorded regardless of whether the skill completed cleanly.

### Note Evaluation Hook (Stop, prompt-based)

Fires after the Log hook. Sends the skill context and conversation turn to a Claude model (Haiku) with a single question: did anything worth remembering surface? If yes, calls `orc note create` with the Orc's structured output. If no, does nothing.

Notes are business knowledge — decisions, patterns, strategic context. The prompt hook has everything it needs in the conversation turn and does not need file access.

### Code Context Hook (PostToolUse on Edit/Write, agent-based)

Fires after every file edit or write. Spawns a read-only agent that:

1. Reads the changed file and surrounding context
2. Evaluates whether the change has a non-obvious _why_ not captured anywhere
3. If yes — adds or updates an inline comment, docblock, or module README
4. If no — does nothing

The agent detects when an edit is itself a comment or docblock update and skips evaluation to prevent loops.

This is how Code memory is built reliably. The _why_ behind decisions is recorded at the moment of the change, not reconstructed after the fact.

---

## Working Modes

TaskOrc is designed around four distinct working modes. Each has a corresponding skill entry point:

|Mode|Trigger|Entry Skill|
|---|---|---|
|**Feature / Change**|New capability or meaningful improvement|`/orc-create`|
|**Tweak**|Small, obvious change with no planning needed|`/orc-tweak`|
|**Bug**|Sentry issue or reported defect|`/orc-bug`|
|**Remember**|Tell the Orc something worth knowing|`/orc-remember`|

---

## Workflow Skills

Workflow skills advance a Task through the planning and execution flow. Running a skill _is_ the status update — workflow state emerges from activity, not manual input.

---

### `/orc-create`

**Scope:** Task **Use for:** Features and changes — work that benefits from planning and structured breakdown

Opens a conversational planning flow. The Orc draws on Business and Code memory to ask informed questions and understand what you want to build. Determines through conversation whether this is a draft (uncommitted idea) or confirmed work ready for execution.

For confirmed Tasks, the Orc works with you to define the Task fully — description, problem, and acceptance criteria. The Task is the spec. The Orc then generates subtasks: each one a human-readable description paired with an LLM-optimized prompt for Claude Code. You can review subtasks before execution if you want to understand exactly what the Orc is about to do.

**Memory contribution:**

- Log entry via global Log hook
- Business and Code Notes evaluated via global Note hook

**Output:** Task with subtasks ready for execution via `/orc-build`.

---

### `/orc-build`

**Scope:** Task (confirmed, with subtasks) **Use for:** Executing a Task

The primary execution skill. The Orc loads the Task and injects Business and Code memory as context, then begins executing subtasks. Subtasks run in parallel where independent, sequentially where dependencies require it. If any subtask fails, execution stops immediately and the Orc reports what succeeded and what needs attention before proceeding.

You choose the mode:

**Guided** — runs in your terminal via Claude Code. You supervise, steer, and intervene in real time. A PR is opened when all subtasks are complete.

**Autonomous** — fires `claude --remote` with the Task ID and full context. Claude Code on the web clones your repo into a secure Anthropic-managed VM and executes the subtasks. You review the diff in the browser and merge the PR. You never open VS Code.

The Orc recommends a mode based on Task complexity and risk — but you decide.

**Hooks:**

- **Stop (agent-based)** — before the Orc considers the Task done, an agent hook runs the project test suite. If tests fail, the Orc continues working rather than stopping. The hook reads the test command from the Project's configured test command field.
- **PostToolUse on Edit/Write** — global code context hook fires after every file change, evaluating whether the _why_ needs to be captured in the codebase.

**Memory contribution:**

- Log entry via global Log hook
- Code Notes evaluated via global Note hook and code context hook

**Output:** Code written, PR opened, Task status updated.

---

### `/orc-tweak`

**Scope:** None (Log only) **Use for:** Small, obvious changes that don't warrant planning — visual adjustments, content changes, spacing, copy, minor configuration

Lightweight entry point. The Orc asks what needs changing, confirms scope, and proceeds directly to execution. No Task is created. The global hooks handle logging and memory.

**Memory contribution:**

- Log entry via global Log hook
- Code Notes evaluated via global Note and code context hooks

**Output:** Change executed, PR opened, activity logged.

---

### `/orc-bug`

**Scope:** None (Log only) **Arguments:** Sentry issue URL (or plain description if not in Sentry) **Use for:** Fixing defects — surfaced by Sentry, reported by a user, or discovered during other work

**Requires:** Sentry MCP configured

Takes a Sentry issue URL as input. The Orc uses the Sentry MCP to pull down the full issue — stack trace, breadcrumbs, affected users, frequency, and environment context. It presents a plain-language description of what is failing and why, drawing on Code memory to identify the relevant area of the codebase.

The Orc then proposes several fix approaches with tradeoffs. You choose the approach. The Orc creates a branch, implements the fix, runs tests, commits, pushes, and opens a PR. No Task is created — the Log is the record.

For bugs not in Sentry, the skill accepts a plain description instead of a URL and proceeds from there.

**Memory contribution:**

- Log entry via global Log hook
- Code Notes updated with bug pattern, root cause, and fix approach via global Note hook
- Business Notes evaluated if the bug reveals a systemic issue

**Output:** Bug described, fix approach chosen, PR opened, activity logged.

---

### `/orc-complete`

**Scope:** Task (PR merged) **Use for:** Closing out a completed Task

Cleans up the branch, updates Task status to complete, and reflects on the completed work. The Orc reviews what was built and explicitly updates Code memory — annotating relevant files, updating module READMEs, and capturing any architectural decisions that emerged during execution.

**Memory contribution:**

- Log entry via global Log hook
- Explicit Code, Business, and Founder Note updates as part of the close-out reflection
- Completion pattern recorded for future reference

**Output:** Task closed, branch cleaned up, memory updated.

---

## Utility Skills

---

### `/orc-remember`

**Scope:** Memory **Use for:** Telling the Orc something worth knowing — ad hoc, whenever something comes up

Opens a structured conversation for memory building. You tell the Orc about your project, technical decisions, preferences, strategic context, or anything else worth capturing. The Orc asks clarifying questions, then structures what you've shared into Notes on the appropriate memory dimensions.

You don't write Notes directly. The Orc structures and stores them.

**Memory contribution:**

- Notes created or updated across relevant dimensions
- Log entry via global Log hook

---

### `/orc-inbox`

**Scope:** User **Use for:** Seeing everything that needs your attention

Returns a prioritized list across all Projects — open PRs awaiting review, Tasks on hold, failed executions requiring attention, and draft Tasks that may be ready to confirm.

---

### `/orc-status`

**Scope:** Task **Use for:** Plain language summary of where something stands

Returns what's been done, what's in progress, what's next, and any risks. Useful before picking up work after time away.

---

### `/orc-next`

**Scope:** Task queue **Use for:** Finding the highest-priority unstarted Task

Returns the next Task from the priority queue — the most important thing to work on right now — and initiates `/orc-build` immediately.

---

### `/orc-prioritize`

**Scope:** Task queue **Use for:** Reordering what gets worked on next

The Orc presents your current queue with relevant context — Task description, estimated scope, business impact — and facilitates a reprioritization conversation. Can be asked for a recommendation: "what would you prioritize and why?"

---

### `/orc-hold`

**Scope:** Task **Use for:** Deliberately pausing work

A hold is a decision to pause, not an external dependency. The Orc logs the reason and sets a reminder to revisit.

---

### `/orc-cancel`

**Scope:** Task **Use for:** Killing work that's no longer worth doing

Captures why, cleans up any in-flight branches, and closes the Task. Requires confirmation — this is destructive. The cancellation reason is recorded in memory and can inform future prioritization.

---

### `/orc-attach`

**Scope:** Project or Task **Use for:** Adding external context — URLs, Figma links, screenshots, error logs, reference docs

Creates an Artifact attached to the Project or Task. For certain URL types the Orc can pull in a preview or summary. Attached context is available at execution time so Claude Code has everything it needs.

---

## Base Skills

---

### `/orc-setup`

**Use for:** Initial onboarding and reconfiguration

Connects to the TaskOrc API and authenticates via magic link. Creates the first Project — prompting for name, repo URL, tech stack, branch conventions, and tool commands. Runs an initial `/orc-remember` session to seed Business and Founder memory before you start working. Skills are installed and updated separately via the Claude marketplace.

---

### `/orc-about`

**Use for:** Conversational help

Ask the Orc anything about how TaskOrc works, what skills are available, or what to do next.

---

### `/orc-sync`

**Use for:** Forcing a full refresh of the local config cache

Normally handled automatically via TTL-based cache invalidation. Manual override when something feels stale. Skill updates are handled separately by the Claude marketplace.

---

## Skill Summary

|Skill|Category|Scope|Purpose|
|---|---|---|---|
|`/orc-create`|Workflow|Task|Plan a feature or change|
|`/orc-build`|Workflow|Task|Execute subtasks — guided or autonomous|
|`/orc-tweak`|Workflow|Log only|Small change — no Task, straight to execution|
|`/orc-bug`|Workflow|Log only|Fix a defect via Sentry URL or description|
|`/orc-complete`|Workflow|Task|Close out a completed Task|
|`/orc-remember`|Utility|Memory|Tell the Orc something worth knowing|
|`/orc-inbox`|Utility|User|Everything requiring your attention|
|`/orc-status`|Utility|Task|Where something stands|
|`/orc-next`|Utility|Queue|Highest-priority unstarted Task|
|`/orc-prioritize`|Utility|Queue|Reorder the Task queue|
|`/orc-hold`|Utility|Task|Deliberately pause work|
|`/orc-cancel`|Utility|Task|Kill a Task|
|`/orc-attach`|Utility|Project / Task|Add external context|
|`/orc-setup`|Base|User|Onboarding and project creation|
|`/orc-about`|Base|User|Conversational help|
|`/orc-sync`|Base|User|Refresh local config cache|