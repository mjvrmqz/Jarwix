# STATE — How to Use the State Database

## Overview
MJ's daily state now lives in the State database on the Dashboard page in Notion 
(ID: 36420c51-aebe-80b5-ba08-f6a5c28b1987)

Claude queries the most recent entry at the start of every session. This file explains how to read and act on that data.

## How to Read the State Database
Each row is a daily check-in submitted by MJ. Key properties:

- Today's Date 
The date of this entry.

- Today's Wake Up Time
When MJ woke up. Auto Scheduler uses this to calculate the active day.

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
