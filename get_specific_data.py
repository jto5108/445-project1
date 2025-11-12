# get_specific_data.py
import requests, re, os, pandas as pd
from bs4 import BeautifulSoup

def scrape_youtube_links_from_google(query="technology videos", max_results=10):
    print("Searching Google for YouTube links...")
    query = query.replace(" ", "+")
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(f"https://www.google.com/search?q={query}+site:youtube.com", headers=headers)
    links = re.findall(r"https://www\.youtube\.com/watch\?v=[\w-]+", r.text)
    links = list(dict.fromkeys(links))[:max_results]
    print(f"Found {len(links)} YouTube links from Google.")
    return links

def get_video_info(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.text if soup.title else "Unknown"
    views = re.search(r"(\d[\d,]*) views", r.text)
    views = views.group(1).replace(",", "") if views else "0"
    return {"title": title, "url": url, "views": views, "category": "Unknown"}

def scrape_youtube_data(query="technology videos", output_csv="data/youtube_videos_scraped.csv"):
    os.makedirs("data", exist_ok=True)
    links = scrape_youtube_links_from_google(query)
    data = [get_video_info(u) for u in links]
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Saved scraped data to {output_csv}")
    return df

if __name__ == "__main__":
    scrape_youtube_data()
