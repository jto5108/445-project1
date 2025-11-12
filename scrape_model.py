# scrape_model.py
import pandas as pd, numpy as np, joblib, os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report

def train_scrape_model(csv_path="data/youtube_videos_scraped.csv", model_path="models/scrape_model.joblib"):
    os.makedirs("models", exist_ok=True)
    df = pd.read_csv(csv_path)
    df.fillna("", inplace=True)
    
    df["text"] = df["title"] + " " + df["channel"]
    y = df["category"]

    tfidf = TfidfVectorizer(max_features=300)
    X_text = tfidf.fit_transform(df["text"]).toarray()
    num_features = df[["views"]].apply(pd.to_numeric, errors="coerce").fillna(0)
    X = np.hstack([X_text, num_features.values])

    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    print("Scrape Model Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds, zero_division=0))
    
    joblib.dump({"model": model, "tfidf": tfidf, "encoder": le}, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_scrape_model()
