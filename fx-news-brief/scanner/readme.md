# Scanner Module

This directory contains the **scanner** script that fetches recent forex‑related tweets using Apify’s Twitter Search Scraper. The output is a JSON file of tweets from the last 12 hours, which feeds into downstream processing (summary, notifications, etc.).

## Requirements

- Python 3.7+
- `requests` library (install via `pip install requests`)
- Valid Apify API token with access to the Twitter Search Scraper actor

## Installation

1. Clone or open your `fx-news-brief` project.
2. Ensure the `scanner` directory contains:
   - `scanner.py` (the main script)
3. Install dependencies:
   ```bash
   pip install requests
   ```

## Configuration

- **APIFY_TOKEN**: Set your Apify token as an environment variable:
  ```bash
  export APIFY_TOKEN="your_token_here"
  ```
  On Windows PowerShell:
  ```powershell
  setx APIFY_TOKEN "your_token_here"
  ```

- **Configuration variables** live at the top of `scanner.py`:
  - `RAW_TERMS`: List of search terms (keywords or phrases).
  - `MAX_ITEMS`: How many tweets to request (fetch extra to allow in‑script filtering).

## Usage

Run the scanner script from your project root:

```bash
python fx-news-brief/scanner/scanner.py
```

This will:
1. Create or verify the subdirectories (`notify`, `prices`, `scanner`, `summary`).
2. Call the Apify actor to fetch up to `MAX_ITEMS` tweets matching `RAW_TERMS`.
3. Filter for tweets created in the last 12 hours.
4. Save the filtered results as `forex_tweets_apify.json` in this folder.

## Output

- **`forex_tweets_apify.json`**: Array of tweet objects with fields like `created_at`, `text`, `username`, `url`, etc.

Once generated, use this JSON in your summary or notification modules.
