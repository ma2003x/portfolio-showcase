import os
import json
from datetime import datetime
import yfinance as yf

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Input/output filenames
INPUT_FILE  = "forex_prices.json"
OUTPUT_FILE = "forex_price_analysis.json"

# ─────────────────────────────────────────────────────────────────────────────

def load_prices(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["data"]

def fetch_yesterday_close(symbol):
    """
    Get the previous trading day's close price for the given symbol.
    We'll request 2 days of history and take the older Close.
    """
    ticker = yf.Ticker(symbol + "=X")
    df = ticker.history(period="2d")
    if len(df) < 2:
        raise ValueError(f"Not enough history for {symbol}")
    # The first row is yesterday's data
    return float(df["Close"].iloc[0])

def analyze(prices):
    """
    For each price entry, compute pct change vs. yesterday's close.
    Return a list of dicts with symbol, current, yesterday_close, pct_change.
    """
    results = []
    for row in prices:
        sym = row["symbol"]
        current = row["currentPrice"]
        try:
            yesterday = fetch_yesterday_close(sym)
        except Exception as e:
            print(f"⚠️  Skipping {sym}: {e}")
            continue

        pct = (current - yesterday) / yesterday * 100
        results.append({
            "symbol": sym,
            "currentPrice": current,
            "yesterdayClose": yesterday,
            "pctChange": round(pct, 4)
        })
    return results

def find_extremes(analysis):
    """
    Identify the biggest gainer and the biggest loser by pctChange.
    """
    if not analysis:
        return None, None
    sorted_by_change = sorted(analysis, key=lambda x: x["pctChange"])
    loser = sorted_by_change[0]
    gainer = sorted_by_change[-1]
    return gainer, loser

if __name__ == "__main__":
    # 1) Paths
    this_dir = os.path.dirname(os.path.abspath(__file__))
    prices_dir = this_dir  # fx-news-brief/prices
    infile  = os.path.join(prices_dir, INPUT_FILE)
    outfile = os.path.join(prices_dir, OUTPUT_FILE)

    print(f"📂 Loading prices from {infile}")
    raw_prices = load_prices(infile)

    # 2) Analyze
    print("⚙️  Computing percent changes vs. yesterday's close...")
    analysis = analyze(raw_prices)

    # 3) Find top movers
    top_gainer, top_loser = find_extremes(analysis)
    print(f"📊 Top gainer: {top_gainer['symbol']} {top_gainer['pctChange']}%")
    print(f"📊 Top loser:  {top_loser['symbol']} {top_loser['pctChange']}%")

    # 4) Write analysis JSON
    output = {
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "analysis": analysis,
        "topGainer": top_gainer,
        "topLoser": top_loser
    }
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"💾 Saved analysis to {outfile}")
