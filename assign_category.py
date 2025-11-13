import pandas as pd

def assign_categories(df):
    """
    Assign categories to videos based on keywords in the title or description.

    Parameters:
        df (pd.DataFrame): Must contain a 'title' or 'description' column.

    Returns:
        pd.DataFrame: Original dataframe with an added 'category' column.
    """

    if 'title' not in df.columns:
        raise ValueError("DataFrame must contain a 'title' column to assign categories.")

    def get_category(title):
        title = str(title).lower()

        if any(word in title for word in ["tutorial", "lesson", "course", "education", "how to"]):
            return "Education"
        elif any(word in title for word in ["game", "playthrough", "minecraft", "fortnite"]):
            return "Gaming"
        elif any(word in title for word in ["news", "update", "report", "breaking"]):
            return "News"
        elif any(word in title for word in ["music", "song", "official video", "album"]):
            return "Music"
        elif any(word in title for word in ["review", "unboxing", "tech", "gadget"]):
            return "Technology"
        elif any(word in title for word in ["comedy", "funny", "laugh", "skit"]):
            return "Entertainment"
        else:
            return "Other"

    # Apply the keyword-based category detection
    df["category"] = df["title"].apply(get_category)

    return df


# Example standalone run for testing
if __name__ == "__main__":
    sample = pd.DataFrame({
        "title": [
            "Top 10 funniest comedy moments",
            "Python tutorial for beginners",
            "Latest iPhone 15 review",
            "Official music video - The Weeknd",
            "Breaking news: new tech updates"
        ]
    })

    result = assign_categories(sample)
    print(result)
