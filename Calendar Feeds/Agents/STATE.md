# STATE — How to Use the State Database

## Overview
MJ's daily state now lives in the State database on the Dashboard page in Notion 
(ID: 36420c51-aebe-80b5-ba08-f6a5c28b1987)

Claude queries the most recent entry at the start of every session. This file explains how to read and act on that data.

## How to Read the State Database
Each row is a daily check-in submitted by MJ. Key properties:

- Today's Date 
The date of this entry. Read "Today's Date"(Date property) to determine what data row to use. If the Date property matches today's current date, use that data in that row. Ignore every other data row.

- Today's Wake Up Time
When MJ woke up. Auto Scheduler uses this to calculate the active day. - Read "Today's Date"(Date property) to determine what data row to use. If the Date property matches today's current date, use that data in that row. Ignore every other data row.

- Today's Energy (1–10)
Physical energy level. Low energy = lighter schedule.

- Today's Mental Clarity(1–10) 
Cognitive sharpness. Low clarity = avoid deep work or talk about it with MJ.

- Today's Mood
Free text. Read this carefully — it gives Claude real context about MJ's headspace.

- Today's Physical State 
How MJ feels physically.

- Planned Sleep Time
When MJ plans to sleep. Auto Scheduler never schedules past this.
- Day Type
Claude fills this in, not MJ. Claude writes Heavy Work Day / Rest Day / Balanced Day based on its assessment at the start of the session.

What Claude Does With State Data
- If Today's Date does not match today, ask MJ for a State Entry update before proceeding with Auto Scheduler.
- Use Energy and Mental Clarity together to calibrate schedule intensity
- Use Mood to catch early signs of burnout, overwhelm, or a particularly good day
- Write Day Type back to this entry after assessing it (see Day Type Assessment rule in README)
- Use Today's Wake Up Time and Planned Sleep Time to calculate the active scheduling window
