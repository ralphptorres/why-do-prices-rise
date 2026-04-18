# why do prices rise

A geopolitical price tracker and forecasting platform for fuel in Manila. Might
cover grocery and commodity prices across the Philippines and beyond in the
future.

## features

- **interactive price graphs** - track gas prices in manila and other provinces
- **contextual annotations** - chips in the ui that explain why prices increased
  or decreased
- **event linking** - hover over chips to see news sources providing context for
  price movements
- **price forecasting** - view predictions for upcoming gas prices
- **AI-powered backend** - analyzes price data and geopolitical events

## getting started

### requirements
- Python 3.13+
- uv (Python package manager)

### installation

```bash
git clone <repo-url>
cd why-do-prices-rise
uv sync
```

### running the project

Start the backend API:
```bash
uv run uvicorn backend.main:app --reload
```
API will be available at http://localhost:8000

Serve the frontend:
```bash
cd frontend
python -m http.server 8000
```
Frontend will be available at http://localhost:8000

### data management

View price data:
```bash
uv run python backend/pipeline.py list-prices
```

View annotations:
```bash
uv run python backend/pipeline.py list-annotations
```

## license

todo
