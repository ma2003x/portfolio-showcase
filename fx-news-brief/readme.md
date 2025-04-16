FX News Brief

This project automates a daily digest of forex market insights by combining social media monitoring with live market data and automated notifications.

Project Structure

fx-news-brief/
├── notify/                    # Notification scripts (SMS, voice)
├── prices/                    # Forex price scraping & analysis
│   ├── price_scraper.py       # Fetch live forex prices & day ranges
│   ├── analyze_prices.py      # Compute % changes, top movers
│   └── README.md              # Docs for the prices module
├── scanner/                   # Twitter-sourced market sentiment
│   ├── scanner.py             # Fetch recent tweets via Apify
│   └── README.md              # Docs for the scanner module
├── summary/                   # NLP summarization of tweets & prices
│   └── README.md              # Docs for the summary module
└── README.md                  # (this file)

Module Overviews

- Scanner
  Gathers tweets from the last 12 hours using Apify’s Twitter Search Scraper.
  -> scanner/README.md

- Prices
  1. price_scraper.py uses yfinance to pull current price, day high & low.
  2. analyze_prices.py computes percent-changes vs. yesterday’s close and identifies top gainers/losers.
  -> prices/README.md

- Summary
  Uses an NLP pipeline (OpenAI GPT API) to generate a concise morning briefing combining social sentiment and market data.
  -> summary/README.md

- Notify
  Sends the generated briefing as an SMS or voice note each morning between 7–8 AM.
  -> notify/README.md

Setup

1. Clone the repository:
   git clone https://github.com/yourusername/portfolio-showcase.git
   cd portfolio-showcase/fx-news-brief

2. Environment variables:
   export APIFY_TOKEN="your_apify_token"
   export OPENAI_API_KEY="your_openai_key"
   (On Windows PowerShell use setx.)

3. Install dependencies:
   pip install requests yfinance beautifulsoup4 openai twilio

Usage Workflow

1. Run Scanner:
   python scanner/scanner.py
   - Produces scanner/forex_tweets_apify.json

2. Fetch & Analyze Prices:
   python prices/price_scraper.py
   python prices/analyze_prices.py
   - Produces prices/forex_prices.json and prices/forex_price_analysis.json

3. Generate Summary:
   python summary/generate_briefing.py

4. Send Notification:
   python notify/send_notification.py

Scheduled Execution

Use cron (Linux/macOS) or Task Scheduler (Windows) to automate:

0 7 * * * cd /path/to/portfolio-showcase/fx-news-brief && \
  python scanner/scanner.py && \
  python prices/price_scraper.py && \
  python prices/analyze_prices.py && \
  python summary/generate_briefing.py && \
  python notify/send_notification.py

For full details, see each module’s own README.
