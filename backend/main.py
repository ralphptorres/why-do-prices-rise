import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Why Do Prices Rise API",
    description="Geopolitical price tracker API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).parent.parent / "data"
PRICES_FILE = DATA_DIR / "out" / "prices-history.json"
ANNOTATIONS_FILE = DATA_DIR / "out" / "annotations.json"


def load_prices() -> dict:
    if PRICES_FILE.exists():
        with open(PRICES_FILE) as f:
            return json.load(f)
    return {"metadata": {}, "prices": []}


def load_annotations() -> dict:
    if ANNOTATIONS_FILE.exists():
        with open(ANNOTATIONS_FILE) as f:
            return json.load(f)
    return {"metadata": {}, "annotations": []}


@app.get("/")
def root():
    return {
        "message": "Why Do Prices Rise API",
        "endpoints": {
            "prices": "/api/prices",
            "prices_by_region": "/api/prices?region=ncr",
            "annotations": "/api/annotations",
            "annotations_by_region": "/api/annotations?region=ncr",
            "health": "/health",
        }
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/prices")
def get_prices(region: str = None):
    data = load_prices()
    prices = data.get("prices", [])
    
    if region:
        prices = [p for p in prices if p.get("region") == region]
    
    return {
        "metadata": data.get("metadata", {}),
        "prices": prices,
    }


@app.get("/api/annotations")
def get_annotations(region: str = None):
    data = load_annotations()
    annotations = data.get("annotations", [])
    
    if region:
        annotations = [a for a in annotations if a.get("region") == region]
    
    return {
        "metadata": data.get("metadata", {}),
        "annotations": annotations,
    }


@app.get("/api/prices/{region}")
def get_prices_by_region(region: str):
    return get_prices(region=region)


@app.get("/api/annotations/{region}")
def get_annotations_by_region(region: str):
    return get_annotations(region=region)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
