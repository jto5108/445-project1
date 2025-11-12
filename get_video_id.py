# get_video_id.py
import os, csv
from dotenv import load_dotenv
from googleapiclient.discovery import build

def collect_video_ids(query="technology", max_results=50, output_csv="data/video_ids.csv"):
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YouTube API key missing. Set YOUTUBE_API_KEY in your environment or .env file.")
    
    os.makedirs("data", exist_ok=True)
    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(q=query, part="id", type="video", maxResults=min(max_results, 50))
    response = request.execute()

    ids = [item["id"]["videoId"] for item in response.get("items", []) if "videoId" in item["id"]]
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["video_id"])
        for vid in ids:
            writer.writerow([vid])

    print(f"Saved {len(ids)} video IDs to {output_csv}")
    return ids

if __name__ == "__main__":
    collect_video_ids("technology", 20)
