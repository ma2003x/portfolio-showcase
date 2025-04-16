import os
import json
import requests
from datetime import datetime, timedelta, timezone

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
APIFY_TOKEN = os.getenv('APIFY_TOKEN',
                        'apify_api_GzpkFUwPhsHAdfv33Cp5SBn5R1SZ8L2j8tk0')
MAX_ITEMS   = 200  # fetch a bit more, so filtering still leaves enough

RAW_TERMS = [
    "#GDP", "#CPI", "#PPI", "#Inflation", "#Unemployment", "#JobsReport",
    "#ConsumerConfidence", "#RetailSales", "#DurableGoods", "#HousingStarts",
    "#IndustrialProduction", "#PMI", "#ISM", "#BalanceOfTrade", "#Fed",
    "#FOMC", "#FedMinutes", "#InterestRates", "#RateHike", "#QuantitativeEasing",
    "#ECB", "#BOJ", "#BankOfEngland", "#YieldCurve", "#Treasuries",
    "10-Year Treasury", "#BondYields", "#S&P500", "#DowJones", "#Nasdaq",
    "#Russell2000", "#VIX", "#SPX", "Small Caps", "Large Caps", "P/E ratio",
    "Price to Book", "Dividend Yield", "#Buybacks", "#InsiderTrading",
    "#ActivistInvestor", "#MarketSentiment", "#WallStreetBets",
    "Bull market", "Bear market", "#Financials", "#ConsumerStaples",
    "#ConsumerDiscretionary", "#Technology", "#Healthcare", "#Industrials",
    "#Energy", "#Materials", "#Utilities", "#RealEstate", "#BerkshireHathaway",
    "#Apple", "#CocaCola", "#AmericanExpress", "#BankofAmerica", "#JPMorgan",
    "#WellsFargo", "#GoldmanSachs", "#Moody’s", "#Visa", "#Mastercard",
    "#Chevron", "#ExxonMobil", "#Oil", "#WTI", "#Brent", "#Gold", "#Silver",
    "#Copper", "#Commodities", "#FX", "US Dollar", "Euro", "#Bitcoin",
    "#Ethereum", "#Earnings", "#EarningsSeason", "#EarningsCall",
    "Quarterly Report", "10-K", "10-Q", "#Mergers", "#Acquisitions",
    "#Spinoff", "#IPO", "#ESG", "#Sustainability", "#ClimateRisk",
    "#CyberSecurity", "#Geopolitics", "#TradeWar", "Regulation", "Antitrust",
    "#Technicals", "Moving Average", "RSI", "MACD", "#HighFrequency",
    "#SentimentAnalysis", "#AltData", "Charlie Munger", "Howard Marks",
    "Ray Dalio", "Stan Druckenmiller", "Peter Lynch", "#ValueInvesting",
    "#BuyAndHold", "#LongTermInvesting", "#China", "#Europe",
    "#EmergingMarkets", "#OPEC", "#MiddleEast", "#Russia", "#Ukraine",
    "#CreditSpreads", "#HighYield", "#InvestmentGrade", "#Municipals",
    "#FearGreedIndex", "#MarketBreadth", "#PutCallRatio", "#ShortInterest"
]

# Correct Apify actor endpoint for sync run → dataset items
APIFY_RUN_ENDPOINT = (
    "https://api.apify.com/v2/acts/"
    "twittapi~twitter-search-scraper/"
    "run-sync-get-dataset-items"
    f"?token={APIFY_TOKEN}"
)
# ─────────────────────────────────────────────────────────────────────────────

def build_search_query(terms):
    """
    1. Strip leading '#' from each term.
    2. Wrap multi-word terms in quotes.
    3. Join with ' OR '.
    """
    cleaned = [t.lstrip('#') for t in terms]
    def quote_if_needed(t):
        return f'"{t}"' if ' ' in t or '-' in t else t
    return ' OR '.join(quote_if_needed(t) for t in cleaned)

def init_directories(root_dir):
    """Ensure subdirs exist: notify, prices, scanner, summary."""
    for sub in ("notify", "prices", "scanner", "summary"):
        path = os.path.join(root_dir, sub)
        os.makedirs(path, exist_ok=True)
        print(f"✔️ Ready: {path}")

def fetch_raw_tweets(query, num):
    """
    Call the Apify actor with only 'keyword' and 'num' fields.
    Returns a list of tweet dicts (see Output Example for 'created_at' field).
    """
    payload = {
        "keyword": query,  # required by this actor :contentReference[oaicite:2]{index=2}
        "num": num         # optional, defaults to 50 :contentReference[oaicite:3]{index=3}
    }
    print(f"🔍 Running actor with payload: {payload}")
    resp = requests.post(APIFY_RUN_ENDPOINT, json=payload)
    resp.raise_for_status()
    items = resp.json()
    print(f"✅ Actor returned {len(items)} items")
    return items

def filter_last_12_hours(tweets):
    """
    Keep only tweets whose 'created_at' is within the last 12 hours.
    'created_at' format: 'Sun Feb 09 14:39:51 +0000 2025' :contentReference[oaicite:4]{index=4}
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=12)
    kept = []
    for t in tweets:
        ts = t.get("created_at")
        if not ts:
            continue
        # parse Twitter's created_at
        dt = datetime.strptime(ts, "%a %b %d %H:%M:%S %z %Y")
        if dt >= cutoff:
            kept.append(t)
    print(f"🔎 {len(kept)} tweets from the last 12 hours (cutoff: {cutoff.isoformat()})")
    return kept

if __name__ == "__main__":
    # Determine directories
    this_dir     = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(this_dir, ".."))
    print(f"📂 Project root: {project_root}\n")

    # 1) Init subfolders
    init_directories(project_root)

    # 2) Build the OR‑joined search query
    search_query = build_search_query(RAW_TERMS)

    # 3) Fetch raw tweets from Apify
    try:
        raw = fetch_raw_tweets(search_query, MAX_ITEMS)
    except Exception as e:
        print(f"❌ Failed to fetch tweets: {e}")
        exit(1)

    # 4) Filter to last 12 hours
    recent = filter_last_12_hours(raw)

    # 5) Save filtered results
    out_path = os.path.join(this_dir, "forex_tweets_apify.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(recent, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Saved {len(recent)} recent tweets to: {out_path}")
