import os
import json
from datetime import datetime
import yfinance as yf

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
# List your pairs in Yahoo format (i.e. EURUSD=X for EUR/USD).
PAIRS = [
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCHF=X",
    "AUDUSD=X", "USDCAD=X", "NZDUSD=X"
]

# Where to write the JSON
OUTPUT_FILENAME = "forex_prices.json"
# ─────────────────────────────────────────────────────────────────────────────

def init_directory(path):
    """Ensure a directory exists."""
    os.makedirs(path, exist_ok=True)
    print(f"✔️ Ready directory: {path}")

def fetch_pair_data(symbol):
    """
    Use yfinance to get today's high, low, and current price
    for a given forex pair symbol.
    Returns a dict.
    """
    ticker = yf.Ticker(symbol)
    # Get today’s minute-level data (if available), else use 1d history
    df = ticker.history(period="1d")
    if df.empty:
        raise ValueError(f"No data for {symbol}")

    latest = df.iloc[-1]
    return {
        "symbol": symbol.rstrip("=X"),  # e.g. EURUSD
        "timestamp": latest.name.to_pydatetime().isoformat(),
        "currentPrice": float(latest["Close"]),
        "dayHigh": float(latest["High"]),
        "dayLow": float(latest["Low"]),
    }

if __name__ == "__main__":
    # Determine project structure
    this_dir    = os.path.dirname(os.path.abspath(__file__))
    prices_dir  = this_dir  # we're already in fx-news-brief/prices
    print(f"📂 Prices folder: {prices_dir}")

    # 1) Init directory
    init_directory(prices_dir)

    # 2) Fetch data for each pair
    results = []
    for sym in PAIRS:
        try:
            data = fetch_pair_data(sym)
            print(f"  • Fetched {data['symbol']}: {data['currentPrice']} (H:{data['dayHigh']} L:{data['dayLow']})")
            results.append(data)
        except Exception as e:
            print(f"❌ Error fetching {sym}: {e}")

    # 3) Write to JSON
    output_path = os.path.join(prices_dir, OUTPUT_FILENAME)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "retrievedAt": datetime.utcnow().isoformat() + "Z",
            "data": results
        }, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Saved {len(results)} pairs to {output_path}")
