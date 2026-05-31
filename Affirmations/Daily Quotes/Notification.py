import time
import random
from notion_client import Client
import subprocess

# --- CONFIG ---
NOTION_API_KEY = "ntn_z87966143341wFDpXUisYGSE1LQMxiVuwv2WWZgnJ3q3LR"  # ← paste your Notion API key here
PAGE_ID = "27820c51aebe8019a2fbf064159e06a7"  # Your page ID
# ----------------

notion = Client(auth=NOTION_API_KEY)

def get_quotes_from_notion(page_id):
    """Fetches all 'quote' blocks from a Notion page."""
    response = notion.blocks.children.list(block_id=page_id)
    quotes = []

    for block in response.get("results", []):
        if block["type"] == "quote":
            text_elements = block["quote"]["rich_text"]
            if text_elements:
                quote = "".join([t["plain_text"] for t in text_elements]).strip()
                if quote:
                    quotes.append(quote)

    return quotes

def show_quote_notification(quotes):
    """Displays a random quote as a Mac notification."""
    quote = random.choice(quotes)
    subprocess.run(["osascript", "-e", f'display notification "{quote}" with title "Daily Quote" sound name "default"'])

def main():
    quotes = get_quotes_from_notion(PAGE_ID)
    if not quotes:
        print("⚠️ No quote blocks found on the Notion page.")
        return

    print(f"✅ Loaded {len(quotes)} quote blocks from Notion.")
    while True:
        show_quote_notification(quotes)
        # Wait 1–3 hours randomly between notifications
        time.sleep(random.randint(3600, 10800))

if __name__ == "__main__":
    main()
