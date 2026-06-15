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

## Updating This File

This file is meant to stay simple and human-readable. Whenever the system changes (new agent, new database, new flow), just ask Claude to patch this file. It should never need a full rewrite — just small updates as the system evolves.
