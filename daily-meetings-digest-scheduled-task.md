# Daily Meetings Digest

## Purpose

At the end of each working day, fetch all Google Meet transcripts from that day's meetings and produce a consolidated digest with action items. Output the digest **directly in chat** — do not create a file unless explicitly asked. Then add the user's own action items to the Work Kanban board.

---

**Scope:** All meetings on the current calendar day that have already ended.

---

## Step-by-Step Instructions

### Step 0 — Establish the current time correctly

Before filtering anything, get the real current time in the user's timezone (Asia/Kolkata):

```
TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M %Z'
```

You will compare every event's end time against this. Do all comparisons in a single consistent timezone (convert everything to UTC, or everything to IST) — never mix.

### Step 1 — Fetch today's calendar events

Use the **Google Calendar MCP** to list all events for today on the primary calendar, timezone Asia/Kolkata.

Keep only events that:
- Have **already ended** (see the timezone rule in Step 1a)
- Have at least one attendee beyond the organiser (real meetings, not solo blocks)
- Are not all-day events, out-of-office markers, or focus-time blocks

### Step 1a — Determine "ended" using the UTC offset, NOT the timeZone label

**Critical, this is a known failure point.** A Google Calendar event timestamp looks like:

```
"end": { "dateTime": "2026-06-25T16:30:00+05:30", "timeZone": "Europe/London" }
```

The `timeZone` field is only a **display label** and can disagree with the actual offset on the timestamp. The authoritative value is the **UTC offset baked into the dateTime string** (`+05:30` above). That timestamp is an unambiguous moment in time regardless of the label.

Rule: parse the offset-aware `dateTime` directly and compare it to "now". Do **not** re-interpret the time using the `timeZone` label. In the example above, `16:30:00+05:30` is 16:30 IST — even though the label says Europe/London.

If a meeting is still in progress or upcoming, skip it (it won't have a complete transcript) and list it under "Not yet ended".

### Step 2 — Find the Gemini Notes attachment

For each ended event, check the `attachments` field for a file titled **"Notes by Gemini"**. The `fileUrl` looks like:

```
https://docs.google.com/document/d/{FILE_ID}/edit?...
```

Extract `FILE_ID` from that URL. If no attachment exists, note the meeting name under "Skipped" and continue — never fail the whole run.

### Step 3 — Read each transcript

For each `FILE_ID`, use the **Google Drive MCP** to read the file content.

The document has two sections:
- **Notes** — Gemini's structured summary (Summary, Decisions, Next Steps, Details)
- **Transcript** — full verbatim transcript

Summarise from the **Notes** section. Use the **Transcript** only to resolve ambiguity or recover a missed action item.

If Gemini explicitly states no summary was produced (e.g. "not enough conversation in a supported language"), record the meeting with no action items and a one-line note explaining why — do not invent content from the sparse transcript.

If a Drive read fails, note the error against that meeting and continue.

**Very large documents:** long sessions can exceed the tool's token limit. The read tool will persist the full response to a file, but that file is a single very long JSON line that `Read` cannot open and `Grep` reports as "omitted long matching line". When this happens, delegate to a subagent (Agent tool, general-purpose) with the file ID and ask it to return only the Notes section — it can tile the long line using Grep with `output_mode: "content"`, `-o: true`, `multiline: true`, a narrow pattern like `.{1,200}`, and pagination via `head_limit`/`offset`. Never abandon a meeting without trying this.

### Step 4 — Extract action items

From each meeting's **Next Steps** section, capture for every item: **Who** (assignee), **What** (task), and **Meeting** (source).

Any item assigned to **Kishan Baradeswaran** must also appear in the **Your Action Items** section at the top.

Decisions marked **"Needs Further Discussion"** in the Gemini Notes are **open items**, not closed decisions — surface them as such.

### Step 5 — Output the digest IN CHAT

Post the digest as a chat message using this structure (use light formatting; this is not a file):

The **Meeting summaries** section MUST be a bulleted list, never a prose paragraph. Keep every bullet short and scannable.

**Do not write a `.md` (or any) file** unless the user explicitly asks for a file. The digest lives in chat.

### Step 6 — Add your action items to the Work Kanban

After posting the digest, write the items from **Your action items** (Kishan's own items only — not other people's, not "the group" items) into the Work Kanban board.

**File:** `/Users/kb/Library/Mobile Documents/iCloud~md~obsidian/Documents/all-notes/Work/Work Kanban.md`

If that folder is not connected to the session, request it with `request_cowork_directory` using the path `/Users/kb/Library/Mobile Documents/iCloud~md~obsidian/Documents/all-notes/Work`. If access cannot be obtained, say so at the end of the digest and list the items that would have been added — never fail the run over this.

Rules:

- **Column:** append to the `## Now` section, after the existing cards. Never touch `Next`, `Later`, `Blocked`, or `Done`.
- **Format:** match the board's existing style exactly — `- [ ] Task description #powerverse @{06-Aug-2026}` using today's date in `DD-Mmm-YYYY` form.
- **Tag:** `#powerverse` for Powerverse work, `#Ryewalk` for Ryewalk work, `#telstra` for Telstra work. When a task spans Powerverse and Ryewalk (e.g. Nambikk.ai work with Ramakrishnan), use `#powerverse` and mention the judgement call in your closing note.
- **Phrasing:** one short imperative line per card, consistent with the terse style already on the board. Include the key name or system so it stands alone without the digest.
- **Deduplicate:** read the file first. Skip any item already present anywhere on the board (`Now`, `Next`, `Later`, `Blocked`, or `Done`) — match on meaning, not exact wording, since the same task recurs across days with different phrasing.
- **Add automatically.** Do not wait for confirmation; this task runs unattended.
- Use `Edit` for a targeted insertion. Do not rewrite the file, reorder cards, or alter the `kanban:settings` block at the bottom.

Close the digest with a one-line note of what was added and what was skipped as a duplicate.

---

## Edge Cases

| Situation | Behaviour |
|---|---|
| No meetings today | Output: "No meetings found for today." and skip Step 6 |
| Meeting has no Gemini attachment | List under Skipped, continue |
| Gemini produced no summary | Record with no action items + one-line reason |
| Drive read fails | Note error against that meeting, continue |
| Transcript too large for the read tool | Delegate Notes extraction to a subagent (see Step 3) |
| Transcript very long | Rely on Notes; scan transcript only for missing action items |
| Meeting still in progress / upcoming | List under "Not yet ended", skip |
| No action items for Kishan today | Skip Step 6, note "nothing to add to the board" |
| Kanban folder not accessible | List the items in chat that would have been added, continue |

---

## Connected MCPs Required

| MCP | Purpose |
|---|---|
| **Google Calendar** | List today's events and read attachment metadata |
| **Google Drive** | Read the Gemini Notes document content |

---

## Notes

- The Gemini Notes doc is the single source of truth. Do not fetch raw Meet recordings.
- The file ID is in the `fileUrl` of the calendar attachment — parse it from there, don't search Drive.
- **Time handling is the #1 thing to get right:** trust the UTC offset on the timestamp, never the `timeZone` display label.
- Default output is **inline chat**, not a file. The only file this task writes to is the Work Kanban board.
