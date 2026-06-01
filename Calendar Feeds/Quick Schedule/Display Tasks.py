#!/usr/bin/env python3
import subprocess
import sys
from notion_client import Client
from datetime import datetime, timedelta

NOTION_TOKEN = "ntn_z87966143341wFDpXUisYGSE1LQMxiVuwv2WWZgnJ3q3LR"
notion = Client(auth=NOTION_TOKEN)

databases = {
    "Editing": "2ac20c51aebe805abfa6d73adebfec72",
    "Systems": "29820c51aebe80d89c99d812bbe6f894",
    "Personal": "29820c51aebe80b4abc4c5147ddc288d"
}

def ask_list(prompt, options, multiple=False):
    items = ", ".join(f'"{o}"' for o in options)
    multi = "with multiple selections allowed" if multiple else "without multiple selections allowed"
    script = f'choose from list {{{items}}} with title "Quick Schedule" with prompt "{prompt}" {multi} and empty selection allowed'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    output = result.stdout.strip()
    if output == "false" or not output:
        return None
    if multiple:
        return [x.strip() for x in output.split(",")]
    return output

def ask_input(prompt):
    script = f'display dialog "{prompt}" default answer "" with title "Quick Schedule"'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    output = result.stdout.strip()
    if not output:
        return None
    # output is like: button returned:OK, text returned:8:00AM
    for part in output.split(","):
        if "text returned" in part:
            return part.split("text returned:")[1].strip()
    return None

def fetch_tasks():
    all_tasks = []
    for db_name, db_id in databases.items():
        response = notion.databases.query(database_id=db_id, page_size=100)
        for page in response.get("results", []):
            props = page.get("properties", {})
            name_prop = props.get("Name", {}).get("title", [])
            name = name_prop[0]["plain_text"] if name_prop else None
            hours_prop = props.get("Hours", {}).get("number", None)
            if name and hours_prop is not None:
                all_tasks.append(f"{db_name}: {name} | {hours_prop} hours")
    return all_tasks

def main():
    if len(sys.argv) > 1:
        group_name = sys.argv[1].strip()
    elif not sys.stdin.isatty():
        group_name = sys.stdin.read().strip()
    else:
        print("No group input provided", flush=True)
        sys.exit(1)

    task_list = fetch_tasks()
    if not task_list:
        print("No tasks found in Notion", flush=True)
        sys.exit(1)

    selected = ask_list(f"Select tasks for {group_name}:", task_list, multiple=True)
    if not selected:
        sys.exit(0)

    task_hours = []
    total_hours = 0.0

    for task in selected:
        short = task.split("|")[0].strip()
        hours_str = ask_input(f"Hours for: {short}")
        try:
            hours = float(hours_str)
        except:
            hours = 0.0
        total_hours += hours
        base = task.rsplit("|", 1)[0].strip()
        task_hours.append(f"{base} | {hours} hours")

    start_time_str = ask_input(f"Start time for {group_name}? (e.g. 8:00AM)")
    if not start_time_str:
        sys.exit(1)

    more = ask_list("Add more groups?", ["Yes", "No"])
    if not more:
        more = "No"

    try:
        time_str = start_time_str.strip().upper().replace(" ", "")
        for fmt in ["%I:%M%p", "%I%p", "%H:%M"]:
            try:
                start_dt = datetime.strptime(time_str, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError("bad time")
    except:
        print("Invalid time format", flush=True)
        sys.exit(1)

    end_dt = start_dt + timedelta(hours=total_hours)
    today = datetime.now()

    def fmt(dt):
        dt = dt.replace(year=today.year, month=today.month, day=today.day)
        return dt.strftime("%b %d, %Y at %I:%M %p").replace(" 0", " ")

    print(group_name, flush=True)
    print(f"{fmt(start_dt)} - {fmt(end_dt)}", flush=True)
    for t in task_hours:
        print(t, flush=True)
    print(more, flush=True)

if __name__ == "__main__":
    main()
