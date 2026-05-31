import sys
from notion_client import Client

notion = Client(auth="ntn_z87966143341wFDpXUisYGSE1LQMxiVuwv2WWZgnJ3q3LR")

main_db_ids = {
    "Work": "29520c51aebe80798d10db123c986db0",
    "Personal": "2aa20c51aebe80439c52e60fdf45dd31"
}

source_dbs = {
    "System & Automation": "29820c51aebe80d89c99d812bbe6f894",
    "Editing": "2ac20c51aebe805abfa6d73adebfec72",
    "Personal": "29820c51aebe80b4abc4c5147ddc288d"
}

full_text = sys.argv[1].strip() if len(sys.argv) > 1 else sys.stdin.read().strip()
if not full_text:
    print("NO_INPUT_RECEIVED")
    sys.exit(0)

lines = [line.strip() for line in full_text.splitlines() if line.strip()]
if not lines:
    print("NO_INPUT_RECEIVED")
    sys.exit(0)

group_label = None
summary_lines = []
checklist_lines = []

mode = None
for line in lines:
    if line.upper().startswith("GROUP:"):
        group_label = line.split(":", 1)[1].strip()
    elif line.upper().startswith("SUMMARY:"):
        mode = "summary"
    elif line.upper().startswith("CHECKLIST:"):
        mode = "checklist"
    elif mode == "summary":
        summary_lines.append(line)
    elif mode == "checklist":
        checklist_lines.append(line)

if not group_label:
    group_label = "Unknown Group"

summary_text = " ".join(summary_lines)

page_id = None
for db_name, main_db_id in main_db_ids.items():
    response = notion.databases.query(
        database_id=main_db_id,
        filter={"property": " Calendar", "title": {"equals": f"Group {group_label}"}},
        page_size=1
    )
    if response["results"]:
        page_id = response["results"][0]["id"]
        break

if not page_id:
    print(f"❌ No page found in any main DB for Group {group_label}")
    sys.exit(1)

chunks = [summary_text[i:i + 2000] for i in range(0, len(summary_text), 2000)]
rt_objects = [{"text": {"content": chunk}} for chunk in chunks]

notion.pages.update(
    page_id=page_id,
    properties={"Actionable Steps": {"rich_text": rt_objects}}
)

blocks = []
blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Task Checklist"}}]}
})

current_section = None
for line in checklist_lines:
    stripped = line.strip()
    if not stripped:
        continue
    if stripped.isupper() and len(stripped.split()) <= 6:
        current_section = stripped
        blocks.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": current_section}}]}
        })
        continue
    if current_section and (stripped.startswith("-") or stripped.startswith("*") or stripped.startswith("•") or stripped.startswith("/")):
        task_text = stripped[1:].strip()
        blocks.append({
            "object": "block",
            "type": "to_do",
            "to_do": {
                "checked": False,
                "rich_text": [{"type": "text", "text": {"content": task_text}}]
            }
        })

for i in range(0, len(blocks), 50):
    notion.blocks.children.append(
        block_id=page_id,
        children=blocks[i:i + 50]
    )

for db_name, db_id in source_dbs.items():
    query_res = notion.databases.query(
        database_id=db_id,
        filter={"property": "Groups", "select": {"equals": f"Group {group_label}"}}
    )
    for p in query_res.get("results", []):
        notion.pages.update(page_id=p["id"], archived=True)

print(f"✅ Updated Group {group_label} in main DB and archived matching pages in source DBs.")
