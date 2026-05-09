# StockCharts

A calm, restrained stock-charting interface. FastAPI backend serving Yahoo Finance data and technical indicators; React + TypeScript frontend rendering with [lightweight-charts](https://github.com/tradingview/lightweight-charts).

![Python](https://img.shields.io/badge/Python-3.10+-green?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-19-61dafb?style=flat-square&logo=react)
![Vite](https://img.shields.io/badge/Vite-8-646cff?style=flat-square&logo=vite)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## Architecture

```
┌─────────────────────────┐         ┌───────────────────────────┐
│  frontend/  (Vite)      │  /api/* │  backend/  (FastAPI)      │
│  React + TS             │ ──────▶ │  yfinance + pandas/numpy  │
│  lightweight-charts     │  proxy  │  indicators (RSI, MACD…)  │
│  http://localhost:5173  │         │  http://127.0.0.1:8000    │
└─────────────────────────┘         └───────────────────────────┘
```

The frontend is the only surface a user opens. Vite proxies `/api/*` to the backend, so there is no CORS dance in normal dev use.

## Quick start

Prerequisites: Python 3.10+, Node 18+, npm.

```bash
git clone https://github.com/lukewaehner/StockCharts_Clone.git
cd StockCharts_Clone
./dev.sh
```

First run creates `backend/.venv` and installs `frontend/node_modules` automatically. Subsequent runs skip both. Open http://localhost:5173.

### Run sides individually

```bash
./backend/run.sh    # FastAPI on :8000
./frontend/run.sh   # Vite on :5173
```

Each script is self-contained — it bootstraps its own deps and runs in dev mode with hot reload.

## API

Backend exposes a small JSON API. With the backend running:

| Endpoint | Description |
| --- | --- |
| `GET /api/health` | Liveness check. |
| `GET /api/stock/{symbol}?range=ytd&indicators=ma,bb,rsi,macd` | Candles, volume, summary, key stats, and selected indicators. |

`range` accepts: `day`, `week`, `month`, `quarter`, `6 months`, `1 year`, `2 years`, `5 years`, `10 years`, `ytd`, `max`. `indicators` is a comma-separated subset of `ma`, `bb`, `rsi`, `macd`.

Interactive docs: http://127.0.0.1:8000/docs.

## Indicators

- **Moving averages** — 20 / 50 SMA
- **Bollinger Bands** — 20-period, 2 σ
- **RSI** — 14-period
- **MACD** — 12 / 26 / 9 with histogram

Periods live in `backend/app/config.py` (`INDICATOR_CONFIG`).

## Project structure

```
StockCharts_Clone/
├── dev.sh                  # Boot both servers
├── backend/
│   ├── run.sh              # Backend-only runner
│   ├── requirements.txt
│   └── app/
│       ├── main.py         # FastAPI routes
│       ├── config.py       # Time ranges + indicator periods
│       └── utils/
│           ├── data_fetcher.py
│           ├── indicators.py
│           └── time_utils.py
└── frontend/
    ├── run.sh              # Frontend-only runner
    ├── package.json
    ├── vite.config.ts
    ├── index.html
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── api/
        ├── components/     # Chart, Header, Controls, KeyStats, …
        ├── hooks/
        └── index.css
```

## Design intent

See `frontend/PRODUCT.md` for the full brief. In short: calm, typographic, restrained. The chart is the subject; chrome defers. Anti-references are Robinhood, default TradingView, and generic SaaS dashboards.

## License

MIT — see [LICENSE](LICENSE).
