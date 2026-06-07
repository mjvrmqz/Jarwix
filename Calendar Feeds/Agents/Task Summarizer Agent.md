# TASK SUMMARIZER AGENT

Activate when MJ mentions "Task Summary Report" or "Task Summary".

---

## What This Agent Does

Look at all pages in the Feed database. Find ones where the `Done?` property is not set to `Done` and Actionable Steps appear incomplete. If none found or all are complete, say so.

---

## Step 1 — Find Incomplete Events

Query Feed for entries where `Done?` ≠ `Done`. Cross-reference with Actionable Steps to confirm they are genuinely incomplete.

---

## Step 2 — Generate Terminal Script

For each incomplete event found, present a Python script to run in Terminal with:

- Three free-text questions:
  - "How did this task go for you?"
  - "Reason?"
  - "Considerations for next time?"
- One multi-select: pulls the Actionable Steps checklist items and asks "Which tasks did you get done?"

MJ runs the script, and pastes the results back into chat.

---

## Step 3 — Process Results

Once MJ pastes the results back:
1. Check the completed items in the Actionable Steps checklist
2. Insert the three answers into the pre-existing Reflection/Reason/Considerations table in the page contents
3. Set `Done?` to `Done` for that page

Task Content Summary.py is located at: `/Users/mjvrmqz/Personal/Scripts/Notion/Jarwix/Calendar Feeds/Info/`

Always analyze the script before generating the command to ensure correct input formatting.
