#!/usr/bin/env python3
"""
Task Content Summary — Populates or updates Calendar Feeds page body.
See file header for full usage docs.
"""

import argparse
import json
import os
import sys
import requests

ENV_PATH = os.path.expanduser(
    "/Users/mjvrmqz/Personal/Scripts/Notion/Jarwix/Calendar Feeds/Past Feed/.env"
)
NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"

def load_token():
    token = os.environ.get("NOTION_TOKEN", "")
    if not token and os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line.startswith("NOTION_TOKEN="):
                    token = line.split("=", 1)[1].strip()
                    break
    if not token:
        raise RuntimeError("NOTION_TOKEN not found.")
    return token

def make_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

def get_block_children(block_id, headers):
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

def append_blocks(page_id, children, headers):
    url = f"{BASE_URL}/blocks/{page_id}/children"
    resp = requests.patch(url, headers=headers, json={"children": children})
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"PATCH blocks failed {resp.status_code}: {resp.text}")

def delete_block(block_id, headers):
    url = f"{BASE_URL}/blocks/{block_id}"
    resp = requests.delete(url, headers=headers)
    if resp.status_code not in (200, 204):
        raise RuntimeError(f"DELETE block failed {resp.status_code}: {resp.text}")

def update_block(block_id, payload, headers):
    url = f"{BASE_URL}/blocks/{block_id}"
    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(f"PATCH block failed {resp.status_code}: {resp.text}")

def make_todo(text, checked=False):
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "checked": checked,
            "color": "default",
        },
    }

def make_reflection_table(reflection="", reason="", considerations=""):
    def cell(text):
        return [{"type": "text", "text": {"content": text}}] if text else []
    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": 3,
            "has_column_header": True,
            "has_row_header": False,
            "children": [
                {"object": "block", "type": "table_row", "table_row": {"cells": [
                    [{"type": "text", "text": {"content": "Reflection"}}],
                    [{"type": "text", "text": {"content": "Reason"}}],
                    [{"type": "text", "text": {"content": "Considerations"}}],
                ]}},
                {"object": "block", "type": "table_row", "table_row": {"cells": [
                    cell(reflection), cell(reason), cell(considerations)
                ]}},
            ],
        },
    }

def mode_create(payload, headers):
    page_id = payload["page_id"]
    checklist = payload.get("checklist", [])
    if not checklist:
        print("⚠  No checklist items provided — aborting.", file=sys.stderr)
        sys.exit(1)
    print(f"Clearing existing blocks on page {page_id}…")
    existing = get_block_children(page_id, headers)
    for block in existing:
        delete_block(block["id"], headers)
    print(f"  Deleted {len(existing)} block(s).")
    blocks = [make_todo(item) for item in checklist]
    blocks.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": []}})
    blocks.append(make_reflection_table())
    append_blocks(page_id, blocks, headers)
    print(f"✅ Created {len(checklist)} item(s) + reflection table on {page_id}.")

def mode_update(payload, headers):
    page_id = payload["page_id"]
    completed = set(payload.get("completed", []))
    reflection = payload.get("reflection", "")
    reason = payload.get("reason", "")
    considerations = payload.get("considerations", "")
    blocks = get_block_children(page_id, headers)
    todo_updated = 0
    table_updated = False
    for block in blocks:
        btype = block.get("type")
        if btype == "to_do":
            rt = block["to_do"].get("rich_text", [])
            text = "".join(r.get("plain_text", "") for r in rt).strip()
            if text in completed:
                update_block(block["id"], {"to_do": {"checked": True}}, headers)
                todo_updated += 1
        elif btype == "table" and not table_updated:
            table_children = get_block_children(block["id"], headers)
            if len(table_children) >= 2:
                data_row_id = table_children[1]["id"]
                def cell(text):
                    return [{"type": "text", "text": {"content": text}}] if text else []
                update_block(data_row_id, {"table_row": {"cells": [
                    cell(reflection), cell(reason), cell(considerations)
                ]}}, headers)
                table_updated = True
    print(f"✅ Checked off {todo_updated} item(s). Table updated: {table_updated}.")

def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", metavar="FILE")
    args = parser.parse_args()
    if args.input:
        with open(args.input) as f:
            return json.load(f)
    raw = sys.stdin.read().strip()
    if not raw:
        print("Error: no input provided.", file=sys.stderr)
        sys.exit(1)
    return json.loads(raw)

def main():
    payload = parse_input()
    mode = payload.get("mode", "create").lower()
    if mode not in ("create", "update"):
        print(f"Error: unknown mode '{mode}'.", file=sys.stderr)
        sys.exit(1)
    token = load_token()
    headers = make_headers(token)
    if mode == "create":
        mode_create(payload, headers)
    else:
        mode_update(payload, headers)

if __name__ == "__main__":
    main()
