# JARWIX AGENT SYSTEM — OVERVIEW

This document is a plain-language map of how the entire agent system works. Read this first if you're lost.

---

## The Two Agents

The system runs on two agents that hand off to each other. They never overlap.

```
SUNDAY NIGHT          →        EVERY MORNING
─────────────────────────────────────────────
Planning Agent        →        Auto Scheduler Agent
"What are we doing    →        "Here's today's
 this week?"                    schedule."
```

---

## Planning Agent — Sunday Night

**One sentence:** You tell it your goals for the week, it sets everything up in Notion so Auto Scheduler can run on autopilot all week.

**What it does, in order:**

1. **Reads last week silently** — checks what projects exist, what got done in Feed, your current energy from State. You don't see this.

2. **Asks you five things in one message:**
   - What are your 3-4 goals this week?
   - What's your max hours (work + personal separately)?
   - Any fixed events not already in Notion? (dentist, trips, calls)
   - What's the workload vibe per day? (Light / Medium / Heavy)
   - Any loose personal things you want to happen but haven't planned?

3. **Activates / deactivates projects** — your goals map to projects. If a goal doesn't have a project yet, it creates one. Projects not mentioned get set to Inactive.

4. **Distributes hours** — splits your hour cap across goals by priority (first goal gets ~40%, last gets ~10%). Subtracts fixed events from the cap first so the math is realistic. Shows you the split and waits for your OK.

5. **Generates tasks** — for each project, creates enough concrete tasks to fill that project's hour allocation. Shows you the list before writing anything.

6. **Captures personal intentions** — loose things you mentioned ("go skiing Tuesday") get written to the Other tasks database so Auto Scheduler can find and schedule them.

7. **Locks the week** — writes everything to Notion: project statuses, hour allocations, tasks, fixed events (Time Block + Constraints), day types (Light/Medium/Heavy per day), personal intentions. Nothing is written until you confirm.

**Output:** Notion is fully set up. Auto Scheduler has everything it needs.

---

## Auto Scheduler Agent — Every Morning

**One sentence:** It reads what Planning Agent set up plus your current state today, then builds a specific hour-by-hour schedule.

**What it does, in order:**

1. **Reads everything silently** — State (your energy, mood, sleep), Time Block (fixed events), Constraints (hard limits), Recurring (standing commitments), Projects (active only), Other tasks, Feed (recent history). Fixed events are reserved immediately — they cannot be moved.

2. **Checks if today matches the plan** — compares the day type Planning Agent set (e.g., "Heavy") against your actual energy and clarity today. If there's a mismatch (heavy day planned, but you're low energy), it flags it and asks what you want to do. You decide — it doesn't override silently.

3. **Talks through active projects** — for each active project, it reads where you are in the stage progression and suggests one concrete task. You can redirect or approve. One project at a time.

4. **Checks iMessages** — scans for anything time-sensitive from your contacts before locking the schedule.

5. **Builds the schedule** — slots tasks into your three windows based on your Night Owl pattern:
   - Morning: admin, calls, review only
   - Midday: maintenance, organization
   - Afternoon/Evening: deep work, creative, flow
   
   Applies the day type cap (Light = ~50% work, Medium = ~65%, Heavy = ~80%). Groups compatible tasks. Adds prep/decompression buffers for Away tasks.

6. **Presents the schedule with justification** — every task has a "why this task, why this window, why this duration" explanation. Shows planned vs actual day type if they differ.

7. **Writes to Notion on approval** — project tasks go to the project's internal Tasks DB first, then Feed. Other tasks go straight to Feed. Actionable steps written directly to each Feed entry.

**Output:** A complete day schedule in Notion Feed, ready to execute.

---

## How They Hand Off

```
Planning Agent writes:          Auto Scheduler reads:
──────────────────────────────────────────────────────
Project Status (Active)    →    Only Active projects
Weekly Allocation          →    How many hrs per project
Internal Tasks (per proj)  →    Task pool to draw from
Other database             →    Personal tasks to schedule
Time Block                 →    Fixed events to reserve
Constraints                →    Hard limits to never break
State.Planned Day Type     →    Compare vs actual energy
```

Auto Scheduler writes back:
- `Feed` — the scheduled events (source of truth for what happened)
- `State.Day Type` — what the day actually turned out to be
- `State.Today's Wake Up Time` — if you confirm you're starting your day

---

## Key Databases at a Glance

| Database | What it is | Who writes it |
|---|---|---|
| Projects | Active/Inactive projects + hour allocations | Planning Agent |
| Internal Tasks (per project) | Task pool for each project | Planning Agent + Auto Scheduler |
| Other | Personal tasks not tied to any project | Planning Agent (intentions) + you |
| Time Block | Fixed, immovable events | Planning Agent (new events you name) + you |
| Constraints | Hard limits on availability | Planning Agent (hard blocks you name) + you |
| State | Daily energy, mood, day type, sleep | You (fill in morning) + Auto Scheduler (Day Type) |
| Feed | Every scheduled event + completion status | Auto Scheduler |
| Task Dump | Raw personal task ideas | You |
| Brain Dump (per project) | Raw project thoughts | You |

---

## The Most Important Rules

1. **Nothing is written to Notion without your confirmation.** Every agent has confirmation gates before any write.
2. **Time Block entries are always respected.** Auto Scheduler reserves them first, before any other logic runs.
3. **Constraints are never overridden.** If something conflicts, it gets flagged — never silently scheduled over.
4. **Planning Agent sets priorities. Auto Scheduler executes them.** Auto Scheduler never re-ranks your goals — it just works with what Planning Agent set up.
5. **Day Type is a plan, not a mandate.** If your actual state doesn't match, Auto Scheduler flags the mismatch and lets you decide.
