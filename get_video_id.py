from googleapiclient.discovery import build
from dotenv import load_dotenv
import pandas as pd
import os
import sys

def collect_video_ids(query="Rainbow 6 Siege Rocket League", max_videos=3000):
    # Load API key from .env or environment variable
    load_dotenv()
    youtube_api_key = os.getenv("API_KEY")

    # Check for missing API key
    if not youtube_api_key:
        print("ERROR: No API key found.")
        print("→ Please set your key using:")
        print('   export API_KEY="YOUR_API_KEY_HERE"')
        print("or add it to a .env file like:")
        print("   API_KEY=YOUR_API_KEY_HERE")
        sys.exit(1)

    # Initialize YouTube API client
    api = build("youtube", "v3", developerKey=youtube_api_key)
    print(f"✅ Connected to YouTube API using key: {youtube_api_key[:6]}...")

    videos = []
    next_page = None

    print(f"Searching for videos related to '{query}'...")

    # Loop until we reach the limit or run out of pages
    while True:
        res = api.search().list(
            part="id",
            q=query,
            type="video",
            maxResults=50,
            pageToken=next_page
        ).execute()

        for item in res["items"]:
            videos.append(item["id"]["videoId"])

        next_page = res.get("nextPageToken")
        if not next_page or len(videos) >= max_videos:
            break

    print(f"✅ Found {len(videos)} video IDs for query: '{query}'")

    # Convert to DataFrame and save
    df = pd.DataFrame(videos, columns=["video_id"])
    csv_path = "Video_Ids.csv"
    df.to_csv(csv_path, index=False)
    print(f"✅ Saved video IDs → {csv_path}")

    return df

if __name__ == "__main__":
    collect_video_ids()
