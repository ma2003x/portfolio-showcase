# 🎬 Netflix Top 10 – ETL Pipeline & Analysis

This project extracts, transforms, and analyzes Netflix's weekly Top 10 rankings from their official [Tudum](https://www.netflix.com/tudum/top10) site. It demonstrates a full **ETL pipeline**, including web scraping, data cleaning, cloud storage, and visual insights using Python.

---

## 🛠️ Tech Stack

- **Python**: Core scripting (ETL, visualizations)
- **Pandas**: Data manipulation & transformation
- **BeautifulSoup**: HTML web scraping
- **Matplotlib**: Visualizations
- **Google Cloud Storage**: Uploading processed data to the cloud
- **GitHub**: Version control & public showcase

---

## 🧱 Project Structure

```
netflix-top10-etl/
│
├── data/               # Raw + processed CSVs
├── notebooks/          # Visual analysis notebooks
├── scripts/            # ETL scripts (extract, transform, load)
├── outputs/            # (Optional) exports, plots
├── configs/            # (Optional) parameter config files
└── README.md
```

---

## 🔄 ETL Pipeline

| Stage       | Description |
|-------------|-------------|
| **Extract** | Scrapes Netflix Tudum Top 10 table from HTML |
| **Transform** | Cleans columns, converts types (e.g., runtime to minutes), formats numbers |
| **Load**    | Uploads cleaned data to **Google Cloud Storage (GCS)** |

---

## 📊 Analysis Highlights

📍 Found in [`notebooks/netflix_top10_analysis.ipynb`](notebooks/netflix_top10_analysis.ipynb):

- **Top 10 by Watch Hours** – Ranked horizontal bar chart
- **Runtime vs Watch Hours** – Do longer titles get more engagement?
- **Views vs Weeks in Top 10** – Flash-in-the-pan hits vs long-term stayers

---

## ☁️ Cloud Integration

This repo simulates a real-world deployment:
- ✅ Automated ETL scripts
- ✅ Authenticated upload to a public [Google Cloud Storage bucket](https://console.cloud.google.com/storage/browser)
- ✅ Publicly sharable CSV output for dashboards or reporting

---

## 🚀 How to Run It

Clone the repo:

```bash
git clone https://github.com/ma2003x/portfolio-showcase.git
cd portfolio-showcase/netflix-top10-etl
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python scripts/extract.py
python scripts/transform.py
python scripts/load.py
```

Launch the analysis notebook:

```bash
jupyter notebook notebooks/netflix_top10_analysis.ipynb
```

---

## ✨ Future Improvements

- Weekly scheduler (e.g., cron or Airflow)
- Push results to BigQuery / Looker Studio
- Add IMDb/RottenTomatoes scores
- Time-series trends across weeks

---

## 🔗 Author

**Mikey (ma2003x)**  
📍 Documenting the journey into data engineering + ML  
📫 [github.com/ma2003x](https://github.com/ma2003x)

---

> 💡 Want the raw CSV? [Grab it from Google Cloud Storage](https://storage.googleapis.com/mikey-netflix-pipeline-etl/cleaned/netflix_tudum_top10_cleaned.csv)
