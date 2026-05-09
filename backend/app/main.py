"""FastAPI application — JSON API for stock data and technical indicators."""

import logging
import math
from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import DEFAULTS, INDICATOR_CONFIG
from app.utils.data_fetcher import StockDataFetcher
from app.utils.indicators import (
    calculate_bollinger_bands,
    calculate_macd,
    calculate_moving_average,
    calculate_rsi,
)
from app.utils.time_utils import get_date_range_from_data

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="StockCharts API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

fetcher = StockDataFetcher()


def _safe_num(value) -> Optional[float]:
    """Convert NaN/inf to None so JSON is valid."""
    if value is None:
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or math.isinf(f):
        return None
    return f


def _to_unix(ts: pd.Timestamp) -> int:
    """Lightweight Charts wants Unix seconds (UTC) for time."""
    if ts.tzinfo is not None:
        ts = ts.tz_convert('UTC').tz_localize(None)
    return int(ts.timestamp())


def _series_to_points(index: pd.DatetimeIndex, values: pd.Series) -> list[dict]:
    out = []
    for ts, v in zip(index, values):
        n = _safe_num(v)
        if n is None:
            continue
        out.append({"time": _to_unix(ts), "value": n})
    return out


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/stock/{symbol}")
def get_stock(
    symbol: str,
    range: str = Query(default=DEFAULTS['time_range']),
    indicators: str = Query(default="ma,bb,rsi,macd"),
):
    symbol = symbol.strip().upper()
    if not symbol:
        raise HTTPException(status_code=400, detail="Symbol is required")

    requested = {s.strip().lower() for s in indicators.split(',') if s.strip()}

    hist, info = fetcher.get_stock_data(symbol)
    if hist is None or hist.empty:
        raise HTTPException(status_code=404,
                            detail=f"No data for symbol '{symbol}'")

    start_date, end_date = get_date_range_from_data(hist, range)
    if start_date is None or end_date is None:
        raise HTTPException(status_code=400,
                            detail="Unable to determine date range")

    filtered = hist[(hist.index >= start_date) & (hist.index <= end_date)].copy()
    if filtered.empty:
        raise HTTPException(status_code=404,
                            detail="No data for selected period")

    candles = []
    volume = []
    for ts, row in filtered.iterrows():
        t = _to_unix(ts)
        candles.append({
            "time": t,
            "open": _safe_num(row.get("Open")),
            "high": _safe_num(row.get("High")),
            "low": _safe_num(row.get("Low")),
            "close": _safe_num(row.get("Close")),
        })
        close = _safe_num(row.get("Close"))
        open_ = _safe_num(row.get("Open"))
        up = (close is not None and open_ is not None and close >= open_)
        volume.append({
            "time": t,
            "value": _safe_num(row.get("Volume")) or 0,
            "color": "rgba(4, 120, 87, 0.45)" if up else "rgba(185, 28, 28, 0.45)",
        })

    indicator_payload: dict = {}

    if 'ma' in requested:
        ma20 = calculate_moving_average(filtered, INDICATOR_CONFIG['ma_short'])
        ma50 = calculate_moving_average(filtered, INDICATOR_CONFIG['ma_long'])
        indicator_payload['ma'] = {
            'short': {'period': INDICATOR_CONFIG['ma_short'],
                      'data': _series_to_points(filtered.index, ma20)},
            'long': {'period': INDICATOR_CONFIG['ma_long'],
                     'data': _series_to_points(filtered.index, ma50)},
        }

    if 'bb' in requested:
        upper, middle, lower = calculate_bollinger_bands(
            filtered,
            period=INDICATOR_CONFIG['bb_period'],
            std_dev=INDICATOR_CONFIG['bb_std_dev'],
        )
        indicator_payload['bb'] = {
            'period': INDICATOR_CONFIG['bb_period'],
            'upper': _series_to_points(filtered.index, upper),
            'middle': _series_to_points(filtered.index, middle),
            'lower': _series_to_points(filtered.index, lower),
        }

    if 'rsi' in requested:
        rsi = calculate_rsi(filtered, INDICATOR_CONFIG['rsi_period'])
        indicator_payload['rsi'] = {
            'period': INDICATOR_CONFIG['rsi_period'],
            'data': _series_to_points(filtered.index, rsi),
        }

    if 'macd' in requested:
        macd_line, signal_line, histogram = calculate_macd(
            filtered,
            fast_period=INDICATOR_CONFIG['macd_fast'],
            slow_period=INDICATOR_CONFIG['macd_slow'],
            signal_period=INDICATOR_CONFIG['macd_signal'],
        )
        hist_points = []
        for ts, v in zip(filtered.index, histogram):
            n = _safe_num(v)
            if n is None:
                continue
            hist_points.append({
                "time": _to_unix(ts),
                "value": n,
                "color": "rgba(4, 120, 87, 0.7)" if n >= 0 else "rgba(185, 28, 28, 0.7)",
            })
        indicator_payload['macd'] = {
            'line': _series_to_points(filtered.index, macd_line),
            'signal': _series_to_points(filtered.index, signal_line),
            'histogram': hist_points,
        }

    last = filtered.iloc[-1]
    prev_close = (float(filtered.iloc[-2]['Close'])
                  if len(filtered) > 1 else float(last['Open']))
    close = float(last['Close'])
    delta = close - prev_close
    pct = (delta / prev_close * 100) if prev_close else 0.0

    return {
        "symbol": symbol,
        "name": info.get('shortName') or info.get('longName') or symbol,
        "info": {
            "exchange": info.get('exchange'),
            "currency": info.get('currency'),
            "quoteType": info.get('quoteType'),
        },
        "summary": {
            "price": _safe_num(close),
            "change": _safe_num(delta),
            "changePct": _safe_num(pct),
            "open": _safe_num(last.get('Open')),
            "prevClose": _safe_num(prev_close),
            "high": _safe_num(last.get('High')),
            "low": _safe_num(last.get('Low')),
            "volume": _safe_num(last.get('Volume')),
        },
        "keyStats": {
            "marketCap": _safe_num(info.get('marketCap')),
            "trailingPE": _safe_num(info.get('trailingPE')),
            "forwardPE": _safe_num(info.get('forwardPE')),
            "trailingEps": _safe_num(info.get('trailingEps')),
            "beta": _safe_num(info.get('beta')),
            "dividendYield": _safe_num(info.get('dividendYield')),
            "fiftyTwoWeekHigh": _safe_num(info.get('fiftyTwoWeekHigh')),
            "fiftyTwoWeekLow": _safe_num(info.get('fiftyTwoWeekLow')),
            "averageVolume": _safe_num(
                info.get('averageVolume')
                or info.get('averageDailyVolume3Month')
            ),
            "targetMeanPrice": _safe_num(info.get('targetMeanPrice')),
        },
        "candles": candles,
        "volume": volume,
        "indicators": indicator_payload,
    }
