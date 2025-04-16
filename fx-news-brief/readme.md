# FX News Brief

This project automates a daily digest of forex market insights by combining social media monitoring with live market data and automated notifications.

## Project Structure

```
fx-news-brief/
├── notify/       # Scripts or templates for notification (SMS, voice note)
├── prices/       # Modules to scrape live forex pair prices and day ranges
├── scanner/      # Fetches recent forex-related tweets via Apify
│   └── scanner.py
│   └── README.md # (this file explains the scanner module)
├── summary/      # Processing scripts to summarize tweets and price data
└── README.md     # (this file explains the overall fx-news-brief project)
```

## Overview of Components

1. **Scanner** (`scanner/`): Gathers tweets from the last 12 hours using Apify’s Twitter Search Scraper.
2. **Prices** (`prices/`): Scrapes live forex pair prices (e.g., EUR/USD, GBP/USD) and daily high/low from a financial data source.
3. **Summary** (`summary/`): Uses an NLP pipeline (OpenAI’s GPT API) to generate a concise morning briefing combining social sentiment and market data.
4. **Notify** (`notify/`): Sends the generated briefing as an SMS or voice note each morning between 7–8 AM.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/portfolio-showcase.git
   cd portfolio-showcase/fx-news-brief
   ```

2. **Environment variables**:
   ```bash
   export APIFY_TOKEN="your_apify_token"
   export OPENAI_API_KEY="your_openai_key"
   ```
   (On Windows PowerShell, use `setx` instead of `export`.)

3. **Install dependencies** for each module (example):
   ```bash
   pip install requests beautifulsoup4 openai twilio
   ```

## Usage Workflow

1. **Run Scanner**:
   ```bash
   python scanner/scanner.py
   ```
   - Generates `scanner/forex_tweets_apify.json`.

2. **Fetch Prices**:
   Implement and run `prices/price_scraper.py` to create `prices/forex_prices.json`.

3. **Generate Summary**:
   ```bash
   python summary/generate_briefing.py
   ```
   - Reads JSON files from `scanner/` and `prices/`, writes `summary/daily_briefing.txt`.

4. **Send Notification**:
   ```bash
   python notify/send_notification.py
   ```
   - Sends the `daily_briefing.txt` via SMS or voice call.

## Scheduled Execution

Use cron (Linux/macOS) or Task Scheduler (Windows) to automate:

- **Daily at 7 AM**: Run scanner → prices → summary → notify

Example crontab entry:
```
0 7 * * * cd /path/to/portfolio-showcase/fx-news-brief && \
  python scanner/scanner.py && \
  python prices/price_scraper.py && \
  python summary/generate_briefing.py && \
  python notify/send_notification.py
```

---

For detailed module documentation, see each subfolder’s `README.md`.
