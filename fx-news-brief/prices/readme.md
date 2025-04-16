# Prices Module

This directory contains scripts to scrape and analyze live forex pair data.

## Contents

- `price_scraper.py`: Fetches today's price, high, and low for configured forex pairs using Yahoo Finance (`yfinance`).
- `analyze_prices.py`: Reads the raw price data and computes:
  - Percent change versus yesterday's close
  - Top gainer and top loser among the tracked pairs

## Requirements

- Python 3.7+
- `yfinance` library (`pip install yfinance`)

## Installation

1. Navigate to the `prices` directory:
   ```bash
   cd fx-news-brief/prices
   ```
2. Install dependencies:
   ```bash
   pip install yfinance
   ```

## Configuration

- In `price_scraper.py`, configure the `PAIRS` list with your desired forex tickers (Yahoo format, e.g. `EURUSD=X`).
- Adjust `MAX_ITEMS` in both scripts if you need more or fewer data points.

## Usage

### 1. Scrape Raw Prices

Run the scraper to generate `forex_prices.json`:

```bash
python price_scraper.py
```

The output file will contain:
```json
{
  "retrievedAt": "2025-04-16T20:34:38.205427Z",
  "data": [
    {
      "symbol": "EURUSD",
      "timestamp": "2025-04-16T00:00:00+01:00",
      "currentPrice": 1.13947,
      "dayHigh": 1.14155,
      "dayLow": 1.12854
    },
    ...
  ]
}
```

### 2. Analyze Price Movements

Run the analyzer to compute percent changes and identify movers:

```bash
python analyze_prices.py
```

This produces `forex_price_analysis.json` with structure:
```json
{
  "generatedAt": "2025-04-17T07:00:00Z",
  "analysis": [
    {"symbol":"EURUSD","currentPrice":1.13947,"yesterdayClose":1.13000,"pctChange":0.84},
    ...
  ],
  "topGainer": {...},
  "topLoser": {...}
}
```

## Next Steps

- **Summary Integration**: Have your summary module (`summary/generate_briefing.py`) ingest `forex_price_analysis.json` alongside the tweet JSON to craft a comprehensive morning digest.
- **Scheduling**: Use cron or Task Scheduler to run both scripts daily before the summary step.

For detailed usage of the summary and notify modules, refer to the root `README.md`.

