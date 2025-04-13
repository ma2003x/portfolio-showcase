import pandas as pd
import os

INPUT_PATH = "data/raw/netflix_tudum_top10.csv"
OUTPUT_PATH = "data/processed/netflix_tudum_top10_cleaned.csv"

def runtime_to_minutes(runtime_str):
    """Convert runtime string like '2:05' to total minutes."""
    try:
        h, m = runtime_str.split(":")
        return int(h) * 60 + int(m)
    except:
        return None

def transform_netflix_data():
    df = pd.read_csv(INPUT_PATH)

    # Remove commas and convert numeric fields
    df["Views"] = df["Views"].str.replace(",", "").astype(int)
    df["Watch Hours"] = df["Watch Hours"].str.replace(",", "").astype(int)

    # Convert runtime to total minutes
    df["Runtime (Minutes)"] = df["Runtime"].apply(runtime_to_minutes)

    # Rename columns for consistency
    df.rename(columns={
        "Rank": "Rank",
        "Title": "Title",
        "Weeks in Top 10": "Weeks",
        "Views": "Total Views",
        "Watch Hours": "Total Watch Hours"
    }, inplace=True)

    # Save to processed
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Transformed data saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    transform_netflix_data()
