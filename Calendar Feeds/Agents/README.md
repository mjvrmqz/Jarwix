# JARWIX AGENT SYSTEM — README

DISCLAIMER: All user information (preferences, state, contacts, constraints, about me, projects) lives in the Dashboard and Projects & Tasks pages in the Jarwix Notion workspace — NOT in the agent files. The agent files are logic and instructions only.

## Workspace Token
ntn_z87966143341wFDpXUisYGSE1LQMxiVuwv2WWZgnJ3q3LR

---

## Workspace Structure

### Dashboard Page
Where all personal context lives as structured databases:
- **About Me** — personality, habits, life priorities, schedule personality
- **State (Entries)** — User's daily check-in (energy, clarity, mood, wake/sleep times)
- **Contacts** — people in User's life with relationship context and notes
- **Preferences** — scheduling preferences by category
- **Time Block** — reserved time slots User sets before scheduling begins
- **Constraints** — hard scheduling limits that can never be overridden
- **Recurring** — standing weekly/monthly commitments

### Projects & Tasks Page
- **Projects** — each page is a project with its own internal Tasks, Timeline, Stages Progress, and Brain Dump databases
- **Other** — personal tasks not tied to any project
- **Task Dump** — freeform personal task ideas not tied to any project

### Calendar Feeds Page
- **Feed** — the single calendar database where all scheduled events live. Every entry has a `Type` property (select: `Work` or `Personal`). Work tasks → `Work`. Personal tasks → `Personal`. There is no separate Work Feed, Personal Feed, or Past Feed — everything goes to Feed.
- **Changes** — log of all event changes (delays, cancellations, pushes, skips)

⚠️ NOTION ID FORMATTING: All database IDs must be dash-formatted UUIDs. Always read env.md for IDs before making any Notion API call.

---

## Agent Routing

When User sends a message, Claude reads this table first and opens the correct agent file before doing anything else.

| Agent File | Open when User... |
|---|---|
| `Planning Agent.md` | Says "weekly planning", "plan my week", or wants to set goals and intentions for the upcoming week |
| `Auto Scheduler Agent.md` | Says "auto scheduler", "build my schedule", "plan my day", or you detect they want their calendar built automatically |
| `Task Selector Agent.md` | Says "task selection", "add a task", "I want to add tasks", or you detect they want to add tasks to a project or the Other database |
| `Task Summarizer Agent.md` | Says "task summary", "task summary report", or you detect they want to review and mark off completed events |
| `Cancellations Agent.md` | Says "cancel", "delay", "push", "skip", or you detect they want to alter a scheduled event |

If the intent is ambiguous, ask one question to clarify before opening any agent file.

---

## Global Rules (Apply Across All Agents)

- **USE YOUR OWN JUDGMENT** — the databases and agent files are inputs to Claude's thinking, not a script to execute line by line. Reason independently. Push back when something feels off. User is human and may have things in these databases that aren't in their best interest.

- **NEVER override a hard constraint** from the Constraints database for any reason. If a scheduling request conflicts with a constraint, flag it to User and ask how to handle it.

- **Prefer asking one clarifying question** over making a wrong assumption.

- **Keep track of start and end times** for all events. Log any delays, cancellations, or pushes to the Changes database immediately.

- **WEEKLY PROJECT PROGRESS** — use the `Weekly Finished` property on each project row as the source of truth for weekly hours logged. Do NOT tally from Feed. Compare against `Weekly Allocation` to calculate the gap.

- **WEEKLY PROJECT GOAL TRACKING** — at the start of every Auto Scheduler session, check all Active projects. If it is Thursday or later and any project's Weekly Finished is below Weekly Allocation, flag all behind projects at once before doing anything else.

- **DAY TYPE ASSESSMENT** — after reading State, Claude derives Day Type and writes it back to the State database before scheduling:
  - **Heavy Work Day** — one or more projects behind weekly allocation and it's Thursday or later; or 2+ rest/balanced days in a row; or urgency skewing High/Immovable
  - **Rest Day** — 2+ heavy work days in a row; or energy ≤ 4; or mood indicates burnout/exhaustion; or all projects on track
  - **Balanced Day** — mixed signals or none of the above strongly apply

  Tell User the assessed Day Type and reasoning. Give them the chance to override before scheduling begins.
