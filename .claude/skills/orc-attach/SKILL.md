---
name: orc-attach
description: Attach external context to a task — a URL, Figma link, error log, reference doc, or anything else worth keeping alongside the work.
argument-hint: "[url] [task ID]"
allowed-tools: Read Write Glob
model: claude-haiku-4-5-20251001
---

Attach an artifact to a task or the project.

## Steps

1. Parse `$ARGUMENTS` for a URL (`$0`) and optional task ID (`$1`). Ask for anything missing:
   - **URL** — the external link
   - **Title** — short name (suggest one based on the URL)
   - **Task ID** — which task this belongs to, or "project" for project-level
   - **Type** — infer from URL if obvious, otherwise ask: `figma`, `video`, `document`, `error_log`, `screenshot`, `other`
   - **Notes** — optional context or summary

2. Generate a filename slug from the title (lowercase, hyphens).

3. Write to `.taskorc/artifacts/{slug}.md`:

```markdown
---
type: {type}
task: {task ID or "project"}
url: {url}
---

# {Title}

{notes if provided}
```

4. Confirm: "Artifact saved to `.taskorc/artifacts/{slug}.md`."
