import os
import json
import re
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─── CONFIG ─────────────────────────────────────────────
NOTION_API_KEY = "ntn_z87966143341wFDpXUisYGSE1LQMxiVuwv2WWZgnJ3q3LR"
DATABASE_ID = "2ae20c51aebe8087bf39d4beb6fd5874"
NOTION_VERSION = "2022-06-28"
NAME_PREFIX = "Inspiration"

CLIENT_SECRETS_FILE = "/Users/mjvrmqz/Personal/Scripts/Notion/Jarwix/Inspiration/Add Inspiration/client_secret.json"
TOKEN_FILE = "/Users/mjvrmqz/Personal/Scripts/Notion/Jarwix/Inspiration/Add Inspiration/token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

MAX_LIKED_SCAN = 20  

# ─── NOTION HELPERS ───────────────────────────────────
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
        headers={
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json"
        },
        data=json.dumps(data)
    )

# ─── OAUTH & YOUTUBE CLIENT ───────────────────────────
if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
else:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())

youtube = build("youtube", "v3", credentials=creds)

# Get your own channel ID
response = youtube.channels().list(part="id", mine=True).execute()
MY_CHANNEL_ID = response["items"][0]["id"]

# ─── FETCH EXISTING NOTION PAGES ──────────────────────
print("Fetching existing Notion pages...")
notion_items = []
next_cursor = None
while True:
    query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    query_data = {"start_cursor": next_cursor} if next_cursor else {}
    res = requests.post(
        query_url,
        headers={"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": NOTION_VERSION},
        json=query_data
    ).json()
    notion_items.extend(res.get("results", []))
    next_cursor = res.get("next_cursor")
    if not next_cursor:
        break

existing_urls, used_numbers = extract_existing(notion_items)
print(f"Found {len(existing_urls)} existing URLs in Notion.")

# ─── FETCH LAST LIKED VIDEOS ─────────────────────────
print(f"Starting scan of last {MAX_LIKED_SCAN} liked videos...")
new_found = False
next_page_token = None
scanned_videos = 0

while scanned_videos < MAX_LIKED_SCAN:
    liked_request = youtube.videos().list(
        part="snippet",
        myRating="like",
        maxResults=min(50, MAX_LIKED_SCAN - scanned_videos),
        pageToken=next_page_token
    )
    try:
        response = liked_request.execute()
    except HttpError as e:
        print("Error fetching liked videos:", e)
        break

    items = response.get("items", [])
    if not items:
        break

    for item in items:
        scanned_videos += 1
        video_id = item["id"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Scanning video {scanned_videos}/{MAX_LIKED_SCAN}: {video_url}")

        if video_url in existing_urls:
            continue

        # Check comments for 🔥
        user_commented_fire = False
        next_comment_token = None
        while True:
            try:
                comments_request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    textFormat="plainText",
                    maxResults=100,
                    pageToken=next_comment_token
                )
                comments_resp = comments_request.execute()
            except HttpError as e:
                # Skip videos with comments disabled
                if e.resp.status == 403:
                    print("Comments disabled, skipping video.")
                    break
                print("Error fetching comments:", e)
                break

            for c in comments_resp.get("items", []):
                top_comment = c["snippet"]["topLevelComment"]["snippet"]
                author_id = top_comment.get("authorChannelId", {}).get("value")
                if author_id == MY_CHANNEL_ID and "🔥" in top_comment["textDisplay"]:
                    user_commented_fire = True
                    break
            if user_commented_fire:
                break

            next_comment_token = comments_resp.get("nextPageToken")
            if not next_comment_token:
                break

        if not user_commented_fire:
            continue

        # Add to Notion
        num = get_next_number(used_numbers)
        title = f"{NAME_PREFIX} {num}"
        add_to_notion(title, video_url)
        print(f"Added: {title} → {video_url}")

        used_numbers.add(num)
        existing_urls.add(video_url)
        new_found = True

    next_page_token = response.get("nextPageToken")
    if not next_page_token or scanned_videos >= MAX_LIKED_SCAN:
        break

# ─── FINAL OUTPUT ─────────────────────────────────────
if not new_found:
    print("No new videos with 🔥 comments found. Done!")
else:
    print("All matching videos added. Done!")