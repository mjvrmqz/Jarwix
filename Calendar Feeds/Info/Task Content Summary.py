#!/usr/bin/env python3
"""
Task Content Summary
====================
Populates or updates the body of a Calendar Feeds database page (Personal or Work)
with actionable-step checkboxes and a Reflection | Reason | Considerations table.

TWO MODES
---------
create  — Called right after a new task page is added to Calendar Feeds.
          Writes to_do checkbox blocks + an empty reflection table to the page.

update  — Called during the "Task Summary" workflow.
          Checks off completed items and fills in the reflection table cells.

INPUT (JSON via stdin  OR  --input <file.json>)
-----------------------------------------------
CREATE mode:
  {
    "mode": "create",
    "page_id": "2aa20c51-aebe-8043-9c52-e60fdf45dd31",
    "checklist": [
      "Warm up for 5 minutes",
      "Complete 3 sets of squats",
      "Cool down and stretch"
    ]
  }

UPDATE mode:
  {
    "mode": "update",
    "page_id": "2aa20c51-aebe-8043-9c52-e60fdf45dd31",
    "completed": [
      "Warm up for 5 minutes",
      "Cool down and stretch"
    ],
    "reflection": "Felt strong throughout the session.",
    "reason": "Good sleep the night before.",
    "considerations": "Increase squat weight next time."
  }

USAGE
-----
  # via stdin
  echo '{"mode":"create","page_id":"...","checklist":["Step 1","Step 2"]}' | python3 "Task Content Summary.py"

  # via file flag
  python3 "Task Content Summary.py" --input payload.json

ENV
---
  Reads NOTION_TOKEN from:
    /Users/mjvrmqz/Personal/Scripts/Notion/Jarwix/Calendar Feeds/Past Feed/.env
  or from the NOTION_TOKEN environment variable directly.
"""

import argparse
import json
import os
import sys
import requests

# ── Config ────────────────────────────────────────────────────────────────────

ENV_PATH = os.path.expanduser(
    "/Users/mjvrmqz/Personal/Scripts/Notion/Jarwix/Calendar Feeds/Past Feed/.env"
)
NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"

# ── Token loading ──────────────────────────────────────────────────────────────

def load_token() -> str:
    token = os.environ.get("NOTION_TOKEN", "")
    if not token and os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line.startswith("NOTION_TOKEN="):
                    token = line.split("=", 1)[1].strip()
                    break
    if not token:
        raise RuntimeError(
            "NOTION_TOKEN not found. Set it as an env var or in:\n  " + ENV_PATH
        )
    return token


def make_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

# ── Notion API helpers ─────────────────────────────────────────────────────────

def get_block_children(block_id: str, headers: dict) -> list:
    """Retrieve all child blocks of a page/block (handles pagination)."""
    results = []
    url = f"{BASE_URL}/blocks/{block_id}/children"
    params = {}
    while True:
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            raise RuntimeError(f"GET children failed {resp.status_code}: {resp.text}")
        data = resp.json()
        results.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        params["start_cursor"] = data["next_cursor"]
    return results


def append_blocks(page_id: str, children: list, headers: dict) -> None:
    """Append a list of block objects to a page."""
    url = f"{BASE_URL}/blocks/{page_id}/children"
    resp = requests.patch(url, headers=headers, json={"children": children})
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"PATCH blocks failed {resp.status_code}: {resp.text}")


def delete_block(block_id: str, headers: dict) -> None:
    """Delete (archive) a block."""
    url = f"{BASE_URL}/blocks/{block_id}"
    resp = requests.delete(url, headers=headers)
    if resp.status_code not in (200, 204):
        raise RuntimeError(f"DELETE block failed {resp.status_code}: {resp.text}")


def update_block(block_id: str, payload: dict, headers: dict) -> None:
    """Patch (update) a block's content."""
    url = f"{BASE_URL}/blocks/{block_id}"
    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(f"PATCH block failed {resp.status_code}: {resp.text}")

# ── Block builders ─────────────────────────────────────────────────────────────

def make_todo(text: str, checked: bool = False) -> dict:
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "checked": checked,
            "color": "default",
        },
    }


def make_reflection_table(
    reflection: str = "",
    reason: str = "",
    considerations: str = "",
) -> dict:
    """Returns a table block with a header row and one data row."""

    def cell(text: str) -> list:
        if text:
            return [{"type": "text", "text": {"content": text}}]
        return []

    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": 3,
            "has_column_header": True,
            "has_row_header": False,
            "children": [
                # Header row
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            [{"type": "text", "text": {"content": "Reflection"}}],
                            [{"type": "text", "text": {"content": "Reason"}}],
                            [{"type": "text", "text": {"content": "Considerations"}}],
                        ]
                    },
                },
                # Data row
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            cell(reflection),
                            cell(reason),
                            cell(considerations),
                        ]
                    },
                },
            ],
        },
    }

# ── Mode: CREATE ───────────────────────────────────────────────────────────────

def mode_create(payload: dict, headers: dict) -> None:
    """
    Clear the page, write checkbox blocks for each checklist item,
    then append an empty reflection table.
    """
    page_id = payload["page_id"]
    checklist: list[str] = payload.get("checklist", [])

    if not checklist:
        print("⚠  No checklist items provided — aborting create.", file=sys.stderr)
        sys.exit(1)

    # 1. Clear any existing content
    print(f"Clearing existing blocks on page {page_id}…")
    existing = get_block_children(page_id, headers)
    for block in existing:
        delete_block(block["id"], headers)
    print(f"  Deleted {len(existing)} existing block(s).")

    # 2. Build the new block list
    blocks: list[dict] = []

    for item in checklist:
        blocks.append(make_todo(item, checked=False))

    # Spacer paragraph between checkboxes and table
    blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": []},
    })

    blocks.append(make_reflection_table())

    # 3. Append to page
    append_blocks(page_id, blocks, headers)
    print(f"✅ Created {len(checklist)} checklist item(s) + reflection table on page {page_id}.")

# ── Mode: UPDATE ───────────────────────────────────────────────────────────────

def mode_update(payload: dict, headers: dict) -> None:
    """
    Check off completed to_do blocks by name,
    and fill in the reflection table's data row.
    """
    page_id = payload["page_id"]
    completed: set[str] = set(payload.get("completed", []))
    reflection: str = payload.get("reflection", "")
    reason: str = payload.get("reason", "")
    considerations: str = payload.get("considerations", "")

    blocks = get_block_children(page_id, headers)

    todo_updated = 0
    table_updated = False

    for block in blocks:
        btype = block.get("type")

        # ── Check off completed to_do items ──
        if btype == "to_do":
            rt = block["to_do"].get("rich_text", [])
            text = "".join(r.get("plain_text", "") for r in rt).strip()
            if text in completed:
                update_block(block["id"], {"to_do": {"checked": True}}, headers)
                todo_updated += 1

        # ── Fill the reflection table ──
        elif btype == "table" and not table_updated:
            # The data row is the second child of the table block
            table_children = get_block_children(block["id"], headers)
            if len(table_children) >= 2:
                data_row_id = table_children[1]["id"]

                def cell(text: str) -> list:
                    return [{"type": "text", "text": {"content": text}}] if text else []

                update_block(
                    data_row_id,
                    {
                        "table_row": {
                            "cells": [
                                cell(reflection),
                                cell(reason),
                                cell(considerations),
                            ]
                        }
                    },
                    headers,
                )
                table_updated = True

    print(f"✅ Checked off {todo_updated} item(s). Table updated: {table_updated}.")

# ── Entry point ────────────────────────────────────────────────────────────────

def parse_input() -> dict:
    parser = argparse.ArgumentParser(
        description="Populate or update a Calendar Feeds task page in Notion."
    )
    parser.add_argument(
        "--input", "-i",
        metavar="FILE",
        help="Path to JSON payload file. If omitted, reads from stdin.",
    )
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r") as f:
            return json.load(f)
    else:
        raw = sys.stdin.read().strip()
        if not raw:
            print("Error: no input provided via stdin or --input.", file=sys.stderr)
            sys.exit(1)
        return json.loads(raw)


def main() -> None:
    payload = parse_input()

    mode = payload.get("mode", "create").lower()
    if mode not in ("create", "update"):
        print(f"Error: unknown mode '{mode}'. Use 'create' or 'update'.", file=sys.stderr)
        sys.exit(1)

    token = load_token()
    headers = make_headers(token)

    if mode == "create":
        mode_create(payload, headers)
    else:
        mode_update(payload, headers)


if __name__ == "__main__":
    main()
