# CANCELLATIONS AGENT

---

## Changes Database

All event changes are logged in the **Changes database** in the Calendar Feeds page in Notion. Claude writes to that database directly — not to this file.

Each row represents one altered event. Properties:
- **Event** (title) — name of the event that was changed
- **Delayed** (checkbox) — check if the event was delayed
- **Cancelled** (checkbox) — check if the event was cancelled
- **Pushed** (checkbox) — check if the event was pushed to a different time or day
- **Skipped** (checkbox) — check if the event was skipped entirely

The full context (original time, new time, reason, notes) goes in the **page contents** of that entry — not in properties. Create a new page in the Changes database for each changed event, fill in the Event name, check the appropriate checkbox(es), and write full context in the page body.

When User delays, cancels, pushes, or skips an event, create the corresponding entry in Changes immediately.

---

## How to Use Changes Data

- Query the Changes database periodically to identify patterns — recurring delays, common cancellation reasons, frequent pushes to certain times of day
- Use these patterns to make smarter scheduling decisions in Auto Scheduler (e.g. if tasks requiring setup are frequently delayed, schedule them earlier with more buffer)
- Reference Changes data when explaining scheduling decisions — "Last time this type of task was scheduled at this time, it got pushed" is valuable reasoning

---

## Handling Each Change Type

**Cancelled** — mark the Feed entry's `Done?` as `Skipped`. Create a Changes entry with Cancelled checked. Write reason in page body.

**Delayed** — update the Feed entry's `Time` property to the new time. Create a Changes entry with Delayed checked. Write original time, new time, and reason in page body.

**Pushed to another day** — update the Feed entry's `Time` property to the new date/time. Create a Changes entry with Pushed checked. Write original date/time, new date/time, and reason in page body.

**Skipped** — mark the Feed entry's `Done?` as `Skipped`. Create a Changes entry with Skipped checked. Write reason in page body. If the task came from a project's internal Tasks database, update that task's Status back to Available so it can be rescheduled.
