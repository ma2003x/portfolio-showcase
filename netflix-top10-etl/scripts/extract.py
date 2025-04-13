import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

URL = "https://www.netflix.com/tudum/top10"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extract_netflix_tudum_html():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    titles = []

    for cell in soup.select("td.title"):
        try:
            row = cell.find_parent("tr")

            rank = cell.select_one("span.rank").text.strip()
            title = cell.select_one("button").text.strip()
            weeks = row.select_one("td[data-uia='top10-table-row-weeks']").text.strip()
            views = row.select_one("td[data-uia='top10-table-row-views']").text.strip()
            runtime = row.select_one("td[data-uia='top10-table-row-runtime']").text.strip()
            hours = row.select_one("td[data-uia='top10-table-row-hours']").text.strip()

            titles.append({
                "Rank": rank,
                "Title": title,
                "Weeks in Top 10": weeks,
                "Views": views,
                "Runtime": runtime,
                "Watch Hours": hours
            })

        except Exception as e:
            print(f"⚠️ Skipping row due to error: {e}")
            continue

    df = pd.DataFrame(titles)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/netflix_tudum_top10.csv", index=False)
    print(f"✅ Extracted {len(df)} rows from Netflix Tudum")

if __name__ == "__main__":
    extract_netflix_tudum_html()