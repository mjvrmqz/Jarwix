from notion_client import Client
import sys
from datetime import datetime
import pytz

NOTION_TOKEN = "ntn_z87966143341wFDpXUisYGSE1LQMxiVuwv2WWZgnJ3q3LR"
notion = Client(auth=NOTION_TOKEN)

# Task databases
TASK_DATABASES = {
    "Editing": "2ac20c51aebe805abfa6d73adebfec72",
    "Systems": "29820c51aebe80d89c99d812bbe6f894",
    "Personal": "29820c51aebe80b4abc4c5147ddc288d",
}

WORK_CALENDAR_DB = "29520c51aebe80798d10db123c986db0"
PERSONAL_CALENDAR_DB = "2aa20c51aebe80439c52e60fdf45dd31"

VALID_GROUPS = {f"Group {i}" for i in range(1, 6)}

GROUP_NAME_MAP = {
    "Group One": "Group 1",
    "Group Two": "Group 2",
    "Group Three": "Group 3",
    "Group Four": "Group 4",
    "Group Five": "Group 5",
}

LOCAL_TZ = pytz.timezone("America/Los_Angeles")

def parse_time_range(time_range_str):
    start_str, end_str = time_range_str.split(" - ")
    start_dt = datetime.strptime(start_str.strip(), "%b %d, %Y at %I:%M %p")
    end_dt = datetime.strptime(end_str.strip(), "%b %d, %Y at %I:%M %p")
    start_dt = LOCAL_TZ.localize(start_dt)
    end_dt = LOCAL_TZ.localize(end_dt)
    return {"start": start_dt.isoformat(), "end": end_dt.isoformat()}

def parse_task_line(line):
    if "|" not in line or ":" not in line:
        return None
    left, hours_part = line.split("|", 1)
    db_name, task_title = left.split(":", 1)
    try:
        hours = float(hours_part.strip().replace(" hours", "").replace(" hour", ""))
    except ValueError:
        return None
    return db_name.strip(), task_title.strip(), hours

def update_hours(database_id, task_title, hours, group_name):
    if group_name not in VALID_GROUPS:
        print(f"Invalid group: {group_name}")
        return False
    response = notion.databases.query(database_id=database_id, page_size=100)
    for page in response["results"]:
        title_prop = page["properties"]["Name"]["title"]
        name = title_prop[0]["plain_text"] if title_prop else ""
        if task_title.lower() in name.lower():
            notion.pages.update(
                page_id=page["id"],
                properties={
                    "Hours": {"number": hours},
                    "Add to Daily Table": {"checkbox": True},
                    "Groups": {"select": {"name": group_name}}
                }
            )
            print(f"Updated: {name} → {hours} → {group_name}")
            return True
    print(f"Task not found: {task_title}")
    return False

def calendar_entry_exists(calendar_db_id, group_name, time_range):
    response = notion.databases.query(database_id=calendar_db_id, page_size=100)
    time_obj = parse_time_range(time_range)
    for page in response["results"]:
        title_list = page["properties"].get(" Calendar", {}).get("title", [])
        title_text = title_list[0]["plain_text"] if title_list else ""
        time_prop = page["properties"].get("Time", {}).get("date", {})
        start_time = time_prop.get("start") if time_prop else None
        if title_text == group_name and start_time == time_obj["start"]:
            return True
    return False

def create_calendar_entry(calendar_db_id, group_name, time_range):
    if calendar_entry_exists(calendar_db_id, group_name, time_range):
        print(f"Skipped duplicate: {group_name} | {time_range}")
        return
    notion.pages.create(
        parent={"database_id": calendar_db_id},
        properties={
            " Calendar": {"title": [{"text": {"content": group_name}}]},
            "Time": {"date": parse_time_range(time_range)},
        },
    )
    print(f"Calendar entry added → {group_name} | {time_range}")

def main():
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        input_text = sys.stdin.read()
    lines = [line.strip() for line in input_text.strip().splitlines() if line.strip()]
    if len(lines) < 3:
        print("Missing group, time range, or tasks.")
        return
    raw_group_name = lines[0]
    group_name = GROUP_NAME_MAP.get(raw_group_name, raw_group_name)
    if group_name not in VALID_GROUPS:
        print(f"Invalid group: {group_name}. Must be one of {sorted(VALID_GROUPS)}")
        return
    time_range = lines[1]
    task_lines = lines[2:]
    work_calendar_needed = False
    personal_calendar_needed = False
    for line in task_lines:
        parsed = parse_task_line(line)
        if not parsed:
            print(f"Skipped invalid line: {line}")
            continue
        db_name, task_title, hours = parsed
        task_db_id = TASK_DATABASES.get(db_name)
        if not task_db_id:
            print(f"Unknown database: {db_name}")
            continue
        updated = update_hours(task_db_id, task_title, hours, group_name)
        if updated:
            if db_name in ("Editing", "Systems"):
                work_calendar_needed = True
            elif db_name == "Personal":
                personal_calendar_needed = True
    if work_calendar_needed:
        create_calendar_entry(WORK_CALENDAR_DB, group_name, time_range)
    if personal_calendar_needed:
        create_calendar_entry(PERSONAL_CALENDAR_DB, group_name, time_range)

if __name__ == "__main__":
    main()
