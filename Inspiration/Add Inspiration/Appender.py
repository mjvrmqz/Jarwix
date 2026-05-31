import os
import json
import re
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

NOTION_API_KEY = "ntn_z87966143341wFDpXUisYGSE1LQMxiVuwv2WWZgnJ3q3LR"
DATABASE_ID = "2ae20c51aebe8087bf39d4beb6fd5874"
NOTION_VERSION = "2022-06-28"
NAME_PREFIX = "Inspiration"

CLIENT_SECRETS_FILE = "/Users/mjvrmqz/Personal/Scripts/Notion/Jarwix/Inspiration/Add Inspiration/client_secret.json"
TOKEN_FILE = "/Users/mjvrmqz/Personal/Scripts/Notion/Jarwix/Inspiration/Add Inspiration/token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

MAX_LIKED_SCAN = 20

def extract_existing(notion_items):
    existing_urls = set()
    used_numbers = set()
    for page in notion_items:
        props = page["properties"]
        if "Source" in props:
            files = props["Source"].get("files", [])
            if files and "external" in files[0]:
                existing_urls.add(files[0]["external"]["url"])
        title_text = props["Name"]["title"][0]["plain_text"]
        match = re.match(rf"{NAME_PREFIX} (\d+)$", title_text)
        if match:
            used_numbers.add(int(match.group(1)))
    return existing_urls, used_numbers

def get_next_number(used_numbers):
    n = 1
    while n in used_numbers:
        n += 1
    return n

def add_to_notion(title, url):
    video_id = url.split("v=")[1]
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    data = {
        "parent": {"database_id": DATABASE_ID},
        "cover": {"type": "external", "external": {"url": thumbnail_url}},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]},
            "Source": {"files": [{"name": title, "external": {"url": url}}]}
        }
    }
    requests.post(
        "https://api.notion.com/v1/pages",
        headers={"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": NOTION_VERSION, "Content-Type": "application/json"},
        data=json.dumps(data)
    )

# See full script for OAuth + YouTube scanning logic
