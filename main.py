# main.py
from 1_API_Collection.get_video_id import collect_video_ids
from 1_API_Collection.get_video_metadata import fetch_metadata
from 3_Scraped.get_specific_data import scrape_youtube_data
from 2_Model_Development.api_model import train_api_model
from 2_Model_Development.scrape_model import train_scrape_model

def main():
    print("=== DATA COLLECTION ===")
    collect_video_ids("technology", 20)
    fetch_metadata()
    scrape_youtube_data()

    print("\n=== MODEL TRAINING ===")
    train_api_model()
    train_scrape_model()

if __name__ == "__main__":
    main()
