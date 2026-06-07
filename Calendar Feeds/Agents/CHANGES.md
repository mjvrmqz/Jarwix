# CHANGES — How to Use the Changes Database

## Overview
Event changes (delays, cancellations, pushes) are now logged in the **Changes database** in the Calendar Feeds page in Notion (ID: 36520c51-aebe-805b-a2e0-ff68924d7029). Claude writes to that database directly — not to this file. This file explains how to use that data.

## How to Write to the Changes Database
Each row represents one event that was altered. Properties:
- **Event** (title) — name of the event that was changed
- **Delayed** (checkbox) — check if the event was delayed
- **Cancelled** (checkbox) — check if the event was cancelled
- **Pushed** (checkbox) — check if the event was pushed to a different time or day

The full context of what happened (original time, new time, reason, notes) goes in the **page contents** of that entry — not in properties. Claude creates a new page in the Changes database for each changed event, fills in the Event name, checks the appropriate checkbox(es), and writes the details in the page body.

When MJ delays, cancels, or pushes an event, Claude creates the corresponding entry in the Changes database immediately.

## How Claude Should Use This Data
- Query the Changes database periodically to identify patterns — recurring delays, common cancellation reasons, frequent pushes to certain times of day
- Use these patterns to update BEHAVIOR.md when a clear behavioral trend emerges
- Use delay and cancellation reasons to make smarter scheduling decisions in Auto Scheduler (e.g. if tasks requiring setup are frequently delayed, schedule them earlier with more buffer)
- Reference Changes data when explaining scheduling decisions — "Last time this type of task was scheduled at this time, it got pushed" is valuable reasoning
