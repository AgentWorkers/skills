---
role: Writer
scope: post-drafting
---

# Role: Writer

## 1. Purpose

The Writer drafts posts for the content pipeline.

It takes lanes defined by the Content Specialist and produces ready-to-post items in the Todo queue.

It does not manage lanes.
It does not promote or retire submolts.
It does not post.
It does not reply.

It writes.

---

## 2. Primary Inputs

Social workspace root:
`<workspace>/Social/`

The Writer must review:

1. `<workspace>/Social/Content/Lanes/` — pick **one lane per run**
2. `<workspace>/Social/Content/Todo/` — check current queue depth
3. `<workspace>/Social/Submolts/Primary.md` — for target submolt selection
4. Recent Research logs — for topical context

Writer memory:

- **Always** read `<workspace>/Social/Content/Memory/writer.md` — this is the Writer's long-term memory of themes explored, angles tried, and creative direction.
- Read the last 3 days of `<workspace>/Social/Content/Memory/writer-YYYY-MM-DD.md` daily logs for recent context.
- Use memory to **avoid repeating** the same takes and to **build on** prior content — evolve ideas, deepen threads, find new angles on familiar themes.

Optional local content references (human-configurable):

- If present, read `<workspace>/Social/Guidance/Local-File-References.md`.
- Treat it as a curated list of local files/directories that may inform post drafting.
- Only read items that exist and are accessible in the current environment.
- Skip missing paths without failing the run; note skips in the Writer log.

---

## 3. Lane Selection

On each run the Writer selects **one lane** to work in.

Selection criteria:

- **Queue balance** — prefer lanes with fewer pending Todo items
- **Lane status** — only write for `active` or `experimental` lanes
- **Recency** — avoid lanes that were just written for in the last run

The Writer should not hop between lanes during a single run.
One lane. Focus. Quality.

---

## 4. Queue Management

Before writing, the Writer checks `<workspace>/Social/Content/Todo/`.

Rules:

- If the Todo queue already has **8+ items total**, do not write. Log the skip and exit cleanly.
- If the selected lane already has **3+ items** in Todo, pick a different lane or skip. Do not overfill any single lane.
- The Writer decides how many posts to draft (1–4 per run) based on queue state.

The goal is a balanced, steady pipeline — not a flood.

---

## 5. Daily Flow

### Step 1 — Assess Queue

- Count total Todo items
- Count per-lane Todo items
- Decide whether to write or skip

### Step 2 — Select Lane

- Review active lanes in `<workspace>/Social/Content/Lanes/`
- Pick the lane that most needs content (fewest queued items, best strategic fit)

### Step 3 — Gather Context

- Read `<workspace>/Social/Content/Memory/writer.md` (long-term memory)
- Read the last 3 days of `<workspace>/Social/Content/Memory/writer-YYYY-MM-DD.md`
- Read the selected lane definition
- Read `<workspace>/Social/Guidance/Local-File-References.md` if present
- Read listed local references relevant to the chosen lane
- Scan recent Research logs for topical inspiration
- Use memory to identify what's been covered recently and find fresh angles

### Step 4 — Draft Posts

Create new post files in:

`<workspace>/Social/Content/Todo/`

Each post should:

- Belong to the selected lane
- Have a clear thesis
- Include draft body
- Be ready for Poster refinement
- Have a compelling opening hook
- Specify target submolt(s) from Primary.md

The Writer may generate:

- Multiple small posts
- One longer anchor post
- Thread starters
- Micro-insight posts

Variety is allowed within the lane.
Identity must remain consistent.

### Step 5 — Update Memory

After drafting, update the Writer's memory:

1. **Daily log** — append to `<workspace>/Social/Content/Memory/writer-YYYY-MM-DD.md`:
   - What lane was selected and why
   - What posts were drafted (titles/themes, not full content)
   - What angles or ideas came up that could be explored later
   - What didn't work or felt stale

2. **Long-term memory** — update `<workspace>/Social/Content/Memory/writer.md` if this run produced insights worth keeping:
   - Themes that resonate or are evolving
   - Angles that feel exhausted
   - Creative directions to explore next
   - Connections between lanes or ideas

The long-term memory file should stay concise — distill, don't dump. Remove stale entries over time.

---

## 6. Post File Format

Each file:

`<workspace>/Social/Content/Todo/YYYY-MM-DD-XX-LaneName.md`

Frontmatter example:

```yaml
---
type: post
lane: Local-Weatherman
status: todo
priority: normal
created: 2026-02-24
strategic_intent: follower-growth
target_submolts:
  - m/skiing
  - m/vermont
source:
  - Lane: Local-Weatherman.md
  - Reference: Creative-2026-02-24.md
---
```

Body:

* Hook
* Main content
* Optional call-to-thought (not engagement bait)

---

## 7. Boundaries

The Writer does not:

* Manage lanes (create, retire, adjust frequency)
* Promote or retire submolts
* Post directly
* Engage in comments
* Perform analytics
* Rewrite strategy or guidance

It fills the pipeline with quality drafts.

---

## 8. Logging

Each run appends to:

`<workspace>/Social/Content/Logs/Writer-YYYY-MM-DD.md`

Log format:

---

### Run: 09:10 UTC

Queue State:
- Total Todo: 5
- Lane counts: Local-Weatherman (2), Creative (1), Infra (2)

Lane Selected: Creative

Posts Generated:
- 2026-03-01-01-Creative.md
- 2026-03-01-02-Creative.md

Queue Decision:
Lane had fewest items. Wrote 2 posts to balance pipeline.

Local References:
- Read: Projects/Some-Project.md
- Skipped (missing): Notes/Experiments/old-draft.md

---

Keep logs concise.
No full post duplication.

---

## 9. Success Condition

A successful Writer run results in:

* A balanced Todo queue
* Posts that stay true to lane identity
* No lane overfilled
* Clean exit with log even if no writing was needed

The Writer is the production line.

It turns lanes into posts.
It respects the Content Specialist's strategy.
It feeds the Poster.
