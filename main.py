import pandas as pd
from get_video_id import collect_video_ids
from get_video_metadata import fetch_video_metadata
from api_model import train_api_model
from scrape_model import train_scrape_model
from assign_category import assign_categories
from get_specific_data import extract_scrape_data
from get_thumbnail import scrape_thumbnails


def main():
    print("=== YOUTUBE ENGAGEMENT ANALYSIS PROJECT ===")

    # ---------------------------------------------------------------------
    # STEP 1: API DATA COLLECTION
    # ---------------------------------------------------------------------
    print("\n[STEP 1] Collecting YouTube video IDs...")
    df_ids = collect_video_ids(query="technology", max_results=5)
    print(f"✅ Collected {len(df_ids)} video IDs")

    print("\n[STEP 2] Fetching metadata for video IDs...")
    df_meta = fetch_video_metadata(df_ids)
    print(f"✅ Fetched metadata for {len(df_meta)} videos")

    # ---------------------------------------------------------------------
    # STEP 2: SCRAPED DATA COLLECTION
    # ---------------------------------------------------------------------
    print("\n[STEP 3] Extracting scraped data from HTML or thumbnails...")
    df_scraped = extract_scrape_data()
    df_scraped = assign_categories(df_scraped)
    scrape_thumbnails(df_scraped)
    print(f"✅ Extracted and enriched scraped data ({len(df_scraped)} samples)")

    # ---------------------------------------------------------------------
    # STEP 3: MODEL DEVELOPMENT
    # ---------------------------------------------------------------------
    print("\n[STEP 4] Training API-based model...")
    model_api, acc_api = train_api_model(df_meta)
    print(f"✅ API Model trained (Accuracy: {acc_api:.2f})")

    print("\n[STEP 5] Training Web-Scrape-based model...")
    model_scrape, acc_scrape = train_scrape_model(df_scraped)
    print(f"✅ Scrape Model trained (Accuracy: {acc_scrape:.2f})")

    # ---------------------------------------------------------------------
    # STEP 4: COMPARISON SUMMARY
    # ---------------------------------------------------------------------
    print("\n=== COMPARISON SUMMARY ===")
    summary = pd.DataFrame({
        "Source": ["YouTube API", "Web Scrape"],
        "Samples": [len(df_meta), len(df_scraped)],
        "Accuracy": [acc_api, acc_scrape]
    })
    print(summary)
    summary.to_csv("comparison_summary.csv", index=False)
    print("\n✅ Results saved to comparison_summary.csv")


if __name__ == "__main__":
    main()
