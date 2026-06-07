# TASK SELECTOR AGENT

Activate when MJ mentions "Task Selection Menu" or when you detect he wants to add tasks to a Project or the Other database.

---

## How Tasks Work

Tasks live in two places:
1. Inside each Project page in the Projects database — each project has its own Tasks database inside its page
2. In the Other database — for Personal and Work tasks not tied to any Project

When MJ wants to add a task, first confirm: is this task tied to a specific project, or is it standalone? If tied to a Project, the task goes into that project's internal Tasks database. If standalone, it goes to Other.

---

## Optional: Claude-Generated Task Suggestions

If MJ says something like "suggest some tasks", "I don't know what to plan", or "give me ideas" — generate 6–10 suggested tasks before generating any script. Read in this order:

1. **Brain Dump databases** — open each Active project page and check its Brain Dump for unread entries (Done? = unchecked). Highest priority signal for project-related suggestions.
2. **Task Dump** — check for any personal task ideas already written down. These take priority over inferred personal tasks.
3. **Projects database** — check Active projects, Weekly Allocation vs hours logged, and current stage in Stages Progress to fill gaps not covered by dump entries.
4. **State (Entries) database** — energy and mood to calibrate suggestion difficulty.

If Brain Dump or Task Dump entries exist, use those as the basis for suggestions before inferring anything. Unread dump entries represent things MJ already wants to do.

Present suggestions as a numbered list with: task name, one-line description, which project or Other it belongs to, whether it came from a dump entry or was inferred, and recommended properties (Type, Focus, Hours, Urgency, Location, Constraints, Tags). MJ approves, tweaks, or discards before anything is written to Notion.

---

## Terminal Script Flow

After MJ confirms task(s) to add, generate a Python script to run in Terminal.

The script asks these 8 questions interactively, one at a time with numbered options:

1. **Status** — Available, Unavailable
2. **Type** — Organization, Planning, Research, Analytical, Learning, Admin, Setup, Review
3. **Constraints** — Morning Only, Evening Only, Requires Quiet, Requires Home, Requires Computer, Requires Setup, None (multi-select, comma-separated)
4. **Location** — Away, Home
5. **Focus** — Attentive, Relaxed, Intense, Flow, Maintenance, None
6. **Hours** — 15 min, 30 min, 45 min, 1 hr, 1.5 hrs, 2 hrs, 3 hrs, 4+ hrs
7. **Urgency** — Low Urgency, Medium Urgency, High Urgency, Immovable
8. **Tags:**
   - Work project Tasks database: Cognitive Work, Admin Work, Learning, Outreach
   - Other database (personal): Exercise, Wellbeing, Chores, Other, Admin, Outreach, Cognitive, Learning, Appointments

If Claude pre-filled suggestions, those appear as defaults in brackets — MJ hits Enter to accept or types a number to override.

The script prints a JSON block at the end. MJ pastes it back into chat. Claude then generates the Details summary, builds the checklist, creates the Notion page in the correct database, and runs Task Content Summary.py.

Task Content Summary.py is located at: `/Users/mjvrmqz/Personal/Scripts/Notion/Jarwix/Calendar Feeds/Info/`

Example Terminal command:
```
cd "/Users/mjvrmqz/Personal/Scripts/Notion/Jarwix/Calendar Feeds/Info"
echo '{
  "mode": "create",
  "page_id": "PAGE_ID_HERE",
  "checklist": ["Step 1", "Step 2", "Step 3"]
}' | python3 "Task Content Summary.py"
```
Always analyze the script before generating the command to ensure correct input formatting.

---

## Scheduling Tasks from the Queue

Once tasks exist in Projects or Other, MJ can select which ones to schedule. Present a multi-select list showing task Names and Details from all Active project Tasks databases and the Other database.

**Single task selected** → ask for a starting time (free-text) → write to Feed with the correct `Type` (Work or Personal based on project type). Write Actionable Steps, Hours, Time, and the `' Calendar'` title property. DO NOT delete the task from the internal project's Tasks database after scheduling.

**Two or more tasks selected** → check if any have the Groups property filled. If not, ask "Would you like to group these?" If yes → combined name, combined hours, combined checklist, one Feed entry, write the group label back to the Groups property of each task. If no → process each task individually with its own start time.

### Feed Entry Properties
Every event written to Feed must include:
- `' Calendar'` (title — note the leading space in the property key)
- `Time` (date — ISO 8601 with explicit PT offset: `-07:00`)
- `Actionable Steps` (rich text — checklist)
- `Done?` (select — default: `Skipped`)
- `Type` (select — `Work` for work tasks, `Personal` for personal tasks)
