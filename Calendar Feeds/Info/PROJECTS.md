# PROJECTS — How to Use the Projects Database

## Overview
MJ's projects now live in the **Projects database** in the Projects & Tasks page in Notion (ID: 36520c51-aebe-80be-aecd-c13b87fd9551). Claude queries this database at the start of every session. This file explains how to read and act on that data.

## How to Read the Projects Database
Each row is a project with these key properties:

- Project (title) 
The project name

- Type
Personal or Work project

- Status
Active or Inactive. Only Active projects matter for scheduling. Inactive = ignore completely.

- Weekly Allocation 
Target hours per week for this project

- Deadline
If set, use it to guide urgency as the date approaches. Claude should honor deadlines as much as realistically possible but must never panic over them or inflate schedule pressure artificially. If the remaining hours needed cannot reasonably fit before the deadline — for example, 40 hours of work left with only a weekend remaining — Claude must not treat it as a crisis. Instead, calmly flag the situation to MJ, show the math clearly (hours remaining vs hours realistically available), and suggest a specific extended deadline based on MJ's typical daily capacity. Ask MJ to confirm, then update the Deadline property in the Projects database. Once extended, treat the new date as the active deadline and stop referencing the old one. The goal is realistic progress, not guilt.

- Details
Description of what the project is about


## How Projects Work Internally
Each project page contains its own structure inside:

- A Callout block 
Project overview and notes

- A Timeline database 
High-level milestones with dates and statuses

- A Stages Progress database 
Tracks which stages are complete, with links to tasks per stage

- A Tasks database 
The actual schedulable tasks for this project, with full properties (Status, Type, Focus, Constraints, Hours, Urgency, Location, Details, Stage, Groups, Date)

When looking for tasks to schedule, Claude must open each Active project page and query its internal Tasks database — not a top-level tasks list.

## How Claude Should Use This Data
- Cross-reference project names against task names to understand what work belongs to which project
- Compare hours logged in HISTORY.md this week against Weekly Allocation to gauge whether MJ is on track
- Use the Stage property on tasks to understand where in a project's lifecycle a task sits
- Use Deadline to gently guide urgency as a project's end date approaches — but never catastrophize. If completion is clearly impossible by the deadline, flag it calmly, show MJ the math, suggest a realistic extension, and update the property once confirmed.
- Dropped and Inactive projects must be ignored during scheduling unless MJ explicitly brings them up

## The Other Database
Personal tasks not tied to any Personal or Work Project live in the Other database 
(ID: 29820c51-aebe-80b4-abc4-c5147ddc288d) in the Projects & Tasks page. 

These are things like chores, exercise, wellbeing, and miscellaneous personal tasks. Query this alongside project Tasks databases when building a schedule.
