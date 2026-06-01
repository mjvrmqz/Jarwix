#!/usr/bin/env python3
import sys
import tkinter as tk
from notion_client import Client
# ---------------- CONFIG ----------------
NOTION_TOKEN = "ntn_z87966143341wFDpXUisYGSE1LQMxiVuwv2WWZgnJ3q3LR"
EDITING_DB_ID = "2ac20c51aebe805abfa6d73adebfec72"
SYSTEMS_DB_ID = "29820c51aebe80d89c99d812bbe6f894"
PERSONAL_DB_ID = "29820c51aebe80b4abc4c5147ddc288d"
TAG_DATABASE_MAP = {
    "Cognitive Work": EDITING_DB_ID,
    "Admin Work": EDITING_DB_ID,
    "Learning": EDITING_DB_ID,
    "Outreach": EDITING_DB_ID,
    "Other": PERSONAL_DB_ID,
    "Chores": PERSONAL_DB_ID,
    "Exercise": PERSONAL_DB_ID,
    "Wellbeing": PERSONAL_DB_ID,
    "Jarwix": SYSTEMS_DB_ID,
    "MVS Studios": SYSTEMS_DB_ID,
}
notion = Client(auth=NOTION_TOKEN)

def parse_gpt_output(text):
    parsed = {}
    current_key = None
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            parsed[current_key] = value.lstrip()
        else:
            if current_key:
                parsed[current_key] += "\n" + line
    return parsed

def convert_to_notion_properties(parsed):
    props = {
        "Name": {"title": [{"text": {"content": parsed.get("Title", "Untitled")}}]}
    }
    for key, kind in [("Status", "select"), ("Type", "select"), ("Location", "select")]:
        val = parsed.get(key, "").strip()
        if val:
            props[key] = {kind: {"name": val}}
    for key, kind in [("Constraints", "multi_select"), ("Focus", "multi_select")]:
        val = parsed.get(key, "").strip()
        if val:
            items = [x.strip() for x in val.split(",") if x.strip()]
            props[key] = {kind: [{"name": x} for x in items]}
    hours_val = parsed.get("Hours", "").strip()
    if hours_val:
        try:
            props["Hours"] = {"number": float(hours_val)}
        except:
            pass
    tags_val = parsed.get("Tags", "").strip()
    if tags_val:
        tags_list = [x.strip() for x in tags_val.split(",") if x.strip()]
        props["Tags"] = {"multi_select": [{"name": x} for x in tags_list]}
    details_val = parsed.get("Details", "").strip()
    if details_val:
        props["Details"] = {"rich_text": [{"text": {"content": details_val}}]}
    return props

def show_another_task_dialog():
    result = {"choice": None}
    root = tk.Tk()
    root.title("")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()
    tk.Label(frame, text="Would you like to add another task?", font=("Helvetica", 14, "bold")).pack(pady=(0, 15))
    def choose(option):
        result["choice"] = option
        root.destroy()
    tk.Button(frame, text="Yes", width=20, command=lambda: choose("Yes")).pack(pady=5)
    tk.Button(frame, text="No", width=20, command=lambda: choose("No")).pack(pady=5)
    root.mainloop()
    return result["choice"]

def main():
    if len(sys.argv) > 1:
        gpt_text = sys.argv[1].strip()
    elif not sys.stdin.isatty():
        gpt_text = sys.stdin.read().strip()
    else:
        print("❌ No input provided")
        sys.exit(1)
    if not gpt_text:
        print("❌ Empty input")
        sys.exit(1)
    parsed = parse_gpt_output(gpt_text)
    tag_name = parsed.get("Tags", "").split(",")[0].strip()
    database_id = TAG_DATABASE_MAP.get(tag_name)
    if not database_id:
        print(f"❌ Unknown Tag: {tag_name}")
        sys.exit(1)
    notion_props = convert_to_notion_properties(parsed)
    try:
        notion.pages.create(
            parent={"database_id": database_id},
            properties=notion_props
        )
        print(f"✅ Task Added: {parsed.get('Title', 'Untitled')}")
    except Exception as e:
        print(f"❌ Notion Error: {e}")
        sys.exit(1)

    choice = show_another_task_dialog()
    if choice:
        print(choice)

if __name__ == "__main__":
    main()
