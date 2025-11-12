# get_thumbnail.py
import os, requests, pandas as pd

def download_thumbnails(csv_path="data/youtube_videos_api.csv", folder="data/thumbnails"):
    os.makedirs(folder, exist_ok=True)
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        url = row.get("thumbnail_high") or row.get("thumbnail_default")
        if not url: continue
        vid = row["video_id"]
        r = requests.get(url)
        with open(f"{folder}/{vid}.jpg", "wb") as f:
            f.write(r.content)
    print(f"Downloaded thumbnails for {len(df)} videos.")

if __name__ == "__main__":
    download_thumbnails()
