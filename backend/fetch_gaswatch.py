#!/usr/bin/env python3

import json
import re
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path

GASWATCH_URL = "https://gaswatchph.com/js/data.js"
DATA_DIR = Path(__file__).parent.parent / "data"
PRICES_FILE = DATA_DIR / "out" / "prices-history.json"
SNAPSHOTS_DIR = DATA_DIR / "src"


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


def update_submodule() -> None:
    """Update data submodule to latest."""
    try:
        repo_root = Path(__file__).parent.parent
        subprocess.run(["git", "-C", str(repo_root), "submodule", "update", "--remote"], check=True)
        print("Updated data submodule")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Could not update submodule: {e}")


def save_raw_snapshot(js_content: str) -> None:
    """Save raw GasWatch data.js snapshot."""
    SNAPSHOTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    snapshot_file = SNAPSHOTS_DIR / f"data-{timestamp}.js"
    with open(snapshot_file, "w") as f:
        f.write(js_content)
    print(f"Saved raw data snapshot to {snapshot_file}")


if __name__ == "__main__":
    print("Updating data submodule...")
    update_submodule()

    print("Fetching data from GasWatch PH...")
    js_content = fetch_gaswatch_data()

    if js_content:
        print("Saving raw data snapshot...")
        save_raw_snapshot(js_content)

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
