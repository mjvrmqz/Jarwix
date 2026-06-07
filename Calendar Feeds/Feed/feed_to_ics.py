#!/usr/bin/env python3
import os
import requests
from datetime import datetime, timezone
from ics import Calendar, Event

# === CONFIG ===
NOTION_KEY = os.environ.get("NOTION_KEY", "")
FEED_DB_ID  = os.environ.get("FEED_DB_ID", "")

if not NOTION_TOKEN:
    raise RuntimeError("NOTION_KEY environment variable not set.")

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def query_database(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    results = []
    payload = {}
    while True:
        resp = requests.post(url, headers=HEADERS, json=payload)
        if resp.status_code != 200:
            raise RuntimeError(f"Notion API error {resp.status_code}: {resp.text}")
        data = resp.json()
        results.extend(data["results"])
        if not data.get("has_more"):
            break
        payload["start_cursor"] = data["next_cursor"]
    return results

def create_ics(events):
    cal = Calendar()
    for event in events:
        try:
            title = event["properties"][" Calendar"]["title"][0]["plain_text"]
            start = event["properties"]["Time"]["date"]["start"]
            end = event["properties"]["Time"]["date"].get("end", start)
            steps_list = event["properties"].get("Actionable Steps", {}).get("rich_text", [])
            description = steps_list[0]["plain_text"] if steps_list else ""
        except (KeyError, IndexError, TypeError):
            continue
        e = Event()
        e.name = title; e.begin = start; e.end = end; e.description = description
        cal.events.add(e)
    with open("Feeds/Work Feed/Work Feed.ics", "w") as f:
        f.writelines(cal)
    print(f"  Wrote Calendar Feeds/Feed/Feed.ics ({len(cal.events)} events)")

def main():
    print("Querying Work database...")
    events = query_database(FEED_DB_ID)
    print(f"  {len(events)} entries found")
    create_ics(events)
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print(f"Feed updated at {now}")

if __name__ == "__main__":
    main()
