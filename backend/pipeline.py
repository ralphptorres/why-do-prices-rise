#!/usr/bin/env python3
"""
Data pipeline for fetching and storing gas price data.
Currently supports GasWatch PH and DOE sources.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).parent.parent / "data"
PRICES_FILE = DATA_DIR / "prices-history.json"
ANNOTATIONS_FILE = DATA_DIR / "annotations.json"


def load_prices() -> dict:
    if PRICES_FILE.exists():
        with open(PRICES_FILE) as f:
            return json.load(f)
    return {
        "metadata": {
            "version": "1.0",
            "description": "Manila gas price history with regional data",
            "last_updated": datetime.now().isoformat() + "Z",
            "source": "GasWatch PH",
        },
        "prices": [],
    }


def load_annotations() -> dict:
    if ANNOTATIONS_FILE.exists():
        with open(ANNOTATIONS_FILE) as f:
            return json.load(f)
    return {
        "metadata": {
            "version": "1.0",
            "description": "LLM-generated annotations for price movements",
            "last_updated": datetime.now().isoformat() + "Z",
        },
        "annotations": [],
    }


def save_prices(data: dict) -> None:
    data["metadata"]["last_updated"] = datetime.now().isoformat() + "Z"
    with open(PRICES_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved prices to {PRICES_FILE}")


def save_annotations(data: dict) -> None:
    data["metadata"]["last_updated"] = datetime.now().isoformat() + "Z"
    with open(ANNOTATIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved annotations to {ANNOTATIONS_FILE}")


def add_price_entry(
    date: str,
    region: str,
    region_name: str,
    prices: dict,
    source: str = "doe-oimb",
) -> None:
    data = load_prices()

    # Check if entry already exists
    existing = next(
        (p for p in data["prices"] if p["date"] == date and p["region"] == region),
        None,
    )

    entry = {
        "date": date,
        "region": region,
        "region_name": region_name,
        "prices": prices,
        "source": source,
    }

    if existing:
        # Update existing
        idx = data["prices"].index(existing)
        data["prices"][idx] = entry
        print(f"Updated price entry for {date} ({region})")
    else:
        # Add new
        data["prices"].append(entry)
        print(f"Added price entry for {date} ({region})")

    save_prices(data)


def add_annotation(
    date: str,
    region: str,
    event_title: str,
    summary: str,
    tags: list,
    price_impact: str,
    sources: list,
) -> None:
    data = load_annotations()

    # Check if entry already exists
    existing = next(
        (a for a in data["annotations"] if a["date"] == date and a["region"] == region),
        None,
    )

    entry = {
        "date": date,
        "region": region,
        "event_title": event_title,
        "summary": summary,
        "tags": tags,
        "price_impact": price_impact,
        "sources": sources,
    }

    if existing:
        idx = data["annotations"].index(existing)
        data["annotations"][idx] = entry
        print(f"Updated annotation for {date} ({region})")
    else:
        data["annotations"].append(entry)
        print(f"Added annotation for {date} ({region})")

    save_annotations(data)


def fetch_gaswatch_ph() -> None:
    print("Fetching from GasWatch PH... (not yet implemented)")


def list_prices() -> None:
    data = load_prices()
    print(f"\nPrice History ({len(data['prices'])} entries):")
    for p in data["prices"]:
        print(f"  {p['date']} - {p['region_name']}: P{p['prices']['unleaded']:.2f}")


def list_annotations() -> None:
    data = load_annotations()
    print(f"\nAnnotations ({len(data['annotations'])} entries):")
    for a in data["annotations"]:
        print(f"  {a['date']} - {a['event_title']} ({a['price_impact']})")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "fetch":
            fetch_gaswatch_ph()
        elif cmd == "list-prices":
            list_prices()
        elif cmd == "list-annotations":
            list_annotations()
        else:
            print(f"Unknown command: {cmd}")
    else:
        print("Data Pipeline CLI")
        print("Usage: python pipeline.py [fetch|list-prices|list-annotations]")
