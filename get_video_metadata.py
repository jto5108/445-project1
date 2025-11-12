# get_video_metadata.py
import os, pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build

def fetch_metadata(video_ids_csv="data/video_ids.csv", output_csv="data/youtube_videos_api.csv"):
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("Missing API key. Set YOUTUBE_API_KEY in environment.")

    ids = pd.read_csv(video_ids_csv)["video_id"].dropna().tolist()
    youtube = build("youtube", "v3", developerKey=api_key)

    videos = []
    for i in range(0, len(ids), 50):
        batch = ids[i:i+50]
        req = youtube.videos().list(part="snippet,statistics,contentDetails", id=",".join(batch))
        res = req.execute()
        for v in res.get("items", []):
            s = v["snippet"]; st = v.get("statistics", {})
            videos.append({
                "video_id": v["id"],
                "title": s["title"],
                "channel": s["channelTitle"],
                "publishedAt": s["publishedAt"],
                "categoryId": s.get("categoryId", "Unknown"),
                "views": st.get("viewCount", 0),
                "likes": st.get("likeCount", 0),
                "comments": st.get("commentCount", 0)
            })

    df = pd.DataFrame(videos)
    df.to_csv(output_csv, index=False)
    print(f"Saved {len(df)} videos to {output_csv}")
    return df

if __name__ == "__main__":
    fetch_metadata()
