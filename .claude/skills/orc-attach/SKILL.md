# /orc:attach

Attach external context to a task — a URL, Figma link, reference doc, error log, or anything else worth keeping alongside the work.

## What to do

1. Ask the user for:
   - **URL** — the external link
   - **Title** — short name for the reference (suggest one based on the URL if possible)
   - **Task** — which task number this belongs to (optional — can be project-level)
   - **Type** — one of: `figma`, `video`, `document`, `error_log`, `screenshot`, `other` (infer from URL if obvious)
   - **Notes** — optional free-text summary or context about this artifact

2. Generate a filename slug from the title.

3. Write the artifact to `.taskorc/artifacts/{slug}.md`:

```markdown
---
type: {type}
task: {task number or "project"}
url: {url}
---

# {Title}

{notes if provided, otherwise leave blank}
```

4. Confirm the file was created and show the path.
