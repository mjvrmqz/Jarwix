# JARWIX SYSTEM OVERVIEW
### Written for me, not for Claude

---

## The Big Picture

Jarwix is a scheduling system that runs through Claude + Notion. The idea is simple: instead of manually figuring out what to do every day, I talk to Claude and it handles the thinking — reading my projects, my energy, my constraints, and building my day for me.

There are 5 agents. Each one is just a set of instructions telling Claude how to behave in a specific situation. Claude reads the right one based on what I say. The agents don't talk to each other — they all just read and write to the same Notion databases.

**The agents have no memory of each other. They only know what's in Notion.**

---

## The Two Types of Things in This System

**Agents** — instructions for Claude. They live in GitHub. Claude reads them and follows them.

**Databases** — where my actual data lives. They live in Notion. Agents read from and write to them.

That's it. Agents are logic. Databases are data.

---

## The Databases (What Lives Where)

### Dashboard (personal context)
- **About Me** — who I am, how I work, my life priorities, my schedule personality
- **State (Entries)** — my daily check-in: energy, mood, wake time, sleep time, day type
- **Contacts** — people in my life with relationship context
- **Preferences** — my scheduling preferences (when I like to work, meeting preferences, etc.)
- **Time Block** — reserved time slots that can never be scheduled over
- **Constraints** — hard limits that can never be broken (e.g. no work after 10pm)
- **Recurring** — standing weekly/monthly commitments

### Projects & Tasks
- **Projects** — each project has its own page containing:
  - Internal Tasks database (tasks for that project)
  - Stages Progress database (what phase the project is in)
  - Brain Dump database (mid-week ideas and captures for that project)
  - Timeline
- **Other** — personal or work tasks not tied to any project
- **Task Dump** — freeform personal task ideas, not tied to any project

### Calendar Feeds
- **Feed** — the single calendar. Every scheduled event ends up here.
- **Changes** — log of every time an event was delayed, cancelled, pushed, or skipped

---

## The 5 Agents

### 1. Planning Agent
**When:** Sunday (or start of week). Run once per week.

**What it does:** Sets up the whole week. I tell it my goals in plain messy language and it handles everything — maps goals to existing projects, creates new projects if needed, allocates hours by priority, generates tasks, logs fixed events, sets day types. It writes all of this directly to Notion so the rest of the system has something to work with.

**What I give it:** A messy brain dump of what I want to accomplish this week, my hour cap, any fixed events, and how I want each day to feel (light/medium/heavy). I don't need to be structured — it figures it out.

**What it writes to:** Projects (status + allocation), each project's internal Tasks database, Other database, Time Block, Constraints, State.

**Think of it as:** Me manually filling out all my Notion databases on Sunday, but Claude does it for me based on what I tell it.

---

### 2. Auto Scheduler
**When:** Every morning (or whenever I want to build my day).

**What it does:** Reads everything in Notion and builds my actual daily schedule. It checks my energy from State, looks at what tasks exist across all projects, respects my constraints and time blocks, groups compatible tasks together, and outputs a full schedule with justification for every decision.

**What I give it:** Nothing upfront — it reads Notion itself. I just say "build my schedule" and it goes. It'll ask me about my day type if needed.

**What it reads from:** Everything — Projects, Tasks, Other, Brain Dump, Task Dump, State, Constraints, Time Block, Recurring, Preferences, About Me, Feed (history), Changes (patterns).

**What it writes to:** Feed (the calendar). Also writes Day Type to State.

**Important:** The Auto Scheduler has no idea who the Planning Agent is. It doesn't care. It just reads the databases and builds the day. If I filled those databases manually or the Planning Agent did it — same thing to the Auto Scheduler.

---

### 3. Task Selector
**When:** Anytime I want to add tasks without doing a full planning session.

**What it does:** Helps me add individual tasks to the right place in Notion. If I say "add a task" it asks me the relevant properties (type, focus, urgency, hours, location, etc.) and writes it directly to the correct database. It can also suggest tasks if I'm stuck — it reads Brain Dump, Task Dump, and Stages Progress to come up with ideas.

**What I give it:** The task I want to add (or ask it to suggest some).

**What it writes to:** The correct project's internal Tasks database (if project-related) or the Other database (if standalone).

**Think of it as:** A smarter, more structured way to manually add tasks to Notion mid-week.

---

### 4. Cancellations Agent
**When:** Anytime something gets cancelled, delayed, pushed, or skipped.

**What it does:** Logs the change to the Changes database and updates the Feed entry accordingly. If a task gets skipped, it sets it back to Available so it can be rescheduled.

**What I give it:** What happened and why.

**What it writes to:** Changes database, Feed (updated times or Done? status), project Tasks database (resets status if skipped).

**Why it matters:** The Auto Scheduler reads Changes to find patterns — if certain tasks keep getting skipped at certain times, it uses that to make smarter decisions in future scheduling.

---

### 5. Task Summarizer
**When:** End of day or whenever I want to review what I actually did.

**What it does:** Finds incomplete Feed entries and walks me through them one by one. For each one it asks how it went, why, and what to consider next time. Then it checks off completed steps and marks the entry as Done in Notion.

**What I give it:** My honest answers about how each task went.

**What it writes to:** Feed (marks Done?, checks off Actionable Steps, fills in reflection notes).

---

## The Weekly Flow

```
SUNDAY
  └─ Run Planning Agent
       └─ Tell it my goals (messy is fine)
       └─ It sets up projects, tasks, hours, day types in Notion

EVERY MORNING (Mon–Sun)
  └─ Run Auto Scheduler
       └─ It reads everything and builds my day
       └─ I approve, it writes to Feed

DURING THE DAY (anytime)
  └─ Brain Dump → throw ideas into a project's Brain Dump (Auto Scheduler will see it)
  └─ Task Selector → add a specific task mid-week
  └─ Cancellations Agent → something changed, log it

END OF DAY (optional)
  └─ Run Task Summarizer
       └─ Review what got done, mark things complete
```

---

## The Brain Dump vs Planning Agent (they're not the same thing)

**Planning Agent** = runs once on Sunday. I tell it my goals and it generates tasks for the week. It writes to the Tasks database.

**Brain Dump** = runs anytime during the week. I have a random idea or task mid-Tuesday, I throw it in the project's Brain Dump so I don't forget it. The Auto Scheduler reads it the next morning and works it in.

They serve completely different moments. Planning Agent = intentional weekly setup. Brain Dump = frictionless mid-week capture.

---

## The Key Mental Model

The agents are just me, but automated. If I removed all 5 agents, the system would still work — I'd just be filling Notion manually every Sunday and every morning. The agents do that filling for me based on what I tell them.

**None of the agents know about each other. They only know what's in Notion.**

That's the whole thing.

---

## FAQ — Questions I Actually Had

**Do I need to fill out the State database before running the Auto Scheduler?**
Yes. The Auto Scheduler's first step is reading today's State entry — your wake time, energy, mental clarity, mood, and physical state. If today's entry doesn't exist or doesn't match today's date, it will ask you to fill it in before doing anything. So always do your State check-in before running it.

**Does the Auto Scheduler know about my easy/medium/hard day rotation system?**
Partially. It knows about Light/Medium/Heavy days and checks if your actual energy matches what the Planning Agent planned for the day (e.g. if Sunday said Heavy but you're low energy, it flags the mismatch and asks what to do). But the specific rotation logic — like "always do easy after hard" — is not baked into the agent file. That should live in your Preferences database in Notion so the Auto Scheduler reads and respects it as a standing rule.

**What if I only have 2 projects to work on in a week?**
Nothing breaks. The Planning Agent just allocates your hours across those two projects and the Auto Scheduler builds your days from that smaller pool. If you run out of tasks mid-week, that's when Brain Dump or Task Selector come in. Or you just have a lighter week. That's fine.

**What's the difference between the Stages Progress database and the Internal Tasks database?**
They answer different questions:
- **Stages Progress** = where is this project overall? (Phase 1 done, Phase 2 in progress, etc.)
- **Internal Tasks** = what do I actually do next? (individual actionable tasks with hours, focus, urgency)

Stages Progress is the map. Internal Tasks is the to-do list. The Task Selector reads Stages Progress to suggest relevant tasks — if you're in Phase 2 it won't suggest Phase 3 work.

**How does the system know which tasks are already done?**
The Internal Tasks database has a **Status** property. Tasks start as Available. When scheduled they get written to Feed. When completed, the Task Summarizer marks the Feed entry as Done. The Auto Scheduler and Task Selector filter by `Status ≠ Done` so completed tasks never get re-surfaced. The Stages Progress database has its own Done checkbox per stage — that's separate and marks an entire phase as complete, not individual tasks.

**Does the Brain Dump filter out entries I've already acted on?**
The Task Selector only reads Brain Dump entries where `Done? = unchecked`. The Auto Scheduler follows the same logic in practice. Once you've acted on a Brain Dump entry, check it off so it stops showing up. Claude does not delete Brain Dump entries automatically — that's always manual.

**If Stage 1 is marked done and there are unchecked Brain Dump entries, do they get assigned to Stage 2?**
Not automatically. Brain Dump entries don't have a stage attached to them. When the agent reads them, it interprets them in the context of whatever stage is currently active. So if Stage 2 is now active, those entries get treated as Stage 2 work. The agent uses context to figure it out — it doesn't reassign or retag entries in Notion.

**What's the point of the hourly allocation (e.g. 40% = 24 hours to Goal 1) if I can't always predict 24 hours of tasks?**
The allocation is a priority signal, not a hard contract. It tells the system "if there's a choice, Goal 1 comes first." If you only have 10 hours of visible tasks for that goal, the system schedules 10 hours — it doesn't force you to fill the remaining 14. New tasks reveal themselves as you work, and mid-week you can add more via Brain Dump or Task Selector. The Planning Agent also generates tasks from your goal description to help fill that pool — so you're not manually inventing every task yourself.

**Can I give the Planning Agent a messy unstructured paragraph instead of a clean list of goals?**
Yes, that's exactly what it's designed for. Dump whatever's in your head — project names, rough hours, things you want to get done, how you want the week to feel. The Planning Agent maps it to your existing projects, asks follow-up questions if something is too vague, and handles the structure itself.

---

## Updating This File

This file is meant to stay simple and human-readable. Whenever the system changes (new agent, new database, new flow), just ask Claude to patch this file. It should never need a full rewrite — just small updates as the system evolves.
