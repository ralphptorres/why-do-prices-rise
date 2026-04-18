#!/usr/bin/env python3

import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

GASWATCH_URL = "https://gaswatchph.com/js/data.js"
DATA_DIR = Path(__file__).parent.parent / "data"
PRICES_FILE = DATA_DIR / "prices-history.json"


def fetch_gaswatch_data() -> str:
    """Fetch raw data.js from GasWatch PH."""
    try:
        with urllib.request.urlopen(GASWATCH_URL) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def parse_gaswatch_data(js_content: str) -> dict:
    """Parse JavaScript data.js into Python dict."""
    try:
        # Extract PRICE_HISTORY array
        match = re.search(r'const PRICE_HISTORY = \[(.*?)\];', js_content, re.DOTALL)
        if not match:
            print("Could not find PRICE_HISTORY in data")
            return None

        history_str = "[" + match.group(1) + "]"

        # Quote unquoted keys
        history_str = re.sub(r'(\w+):\s*', r'"\1": ', history_str)

        # Remove trailing commas before closing braces/brackets
        history_str = re.sub(r',\s*([}\]])', r'\1', history_str)

        price_history = json.loads(history_str)
        return price_history
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None


def transform_to_our_format(price_history: list) -> dict:
    """Transform GasWatch format to our format."""
    prices = []

    for entry in price_history:
        week_date = entry.get("week")
        if not week_date:
            continue

        prices.append({
            "date": week_date,
            "region": "ncr",
            "region_name": "Metro Manila",
            "prices": {
                "unleaded": entry.get("unleadedAvg"),
                "diesel": entry.get("dieselAvg"),
            },
            "source": "gaswatch-ph",
        })

    return {
        "metadata": {
            "version": "1.0",
            "description": "Manila gas price history from GasWatch PH",
            "last_updated": datetime.now().isoformat() + "Z",
            "source": "GasWatch PH",
        },
        "prices": prices,
    }


def save_prices(data: dict) -> None:
    """Save prices to JSON."""
    with open(PRICES_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data['prices'])} price entries to {PRICES_FILE}")


if __name__ == "__main__":
    print("Fetching data from GasWatch PH...")
    js_content = fetch_gaswatch_data()

    if js_content:
        print("Parsing data...")
        price_history = parse_gaswatch_data(js_content)

        if price_history:
            print(f"Found {len(price_history)} weeks of data")
            data = transform_to_our_format(price_history)
            save_prices(data)
            print("Success!")
        else:
            print("Failed to parse data")
    else:
        print("Failed to fetch data")
