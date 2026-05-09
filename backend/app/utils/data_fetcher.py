import logging
import time
from typing import Optional, Tuple

import pandas as pd
import yfinance as yf


class StockDataFetcher:
    """Handle stock data retrieval with caching and error handling."""

    def __init__(self):
        self.cache: dict = {}
        self.logger = logging.getLogger(__name__)

    def get_stock_data(self, symbol: str, max_retries: int = 3
                       ) -> Tuple[Optional[pd.DataFrame], Optional[dict]]:
        if symbol in self.cache:
            return self.cache[symbol]

        for attempt in range(max_retries):
            try:
                self.logger.info(
                    f"Fetching {symbol} (attempt {attempt + 1}/{max_retries})")

                ticker = yf.Ticker(symbol)
                hist = ticker.history(
                    period='max',
                    auto_adjust=True,
                    prepost=False,
                    actions=False,
                )

                if isinstance(hist.columns, pd.MultiIndex):
                    hist.columns = (hist.columns.droplevel(1)
                                    if hist.columns.nlevels > 1
                                    else hist.columns)

                if hist.empty:
                    self.logger.warning(f"No data for {symbol}")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    return None, None

                info = self._get_stock_info_safe(ticker, symbol)
                self.cache[symbol] = (hist, info)
                return hist, info

            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {symbol}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                self.logger.error(f"All attempts failed for {symbol}: {e}")
                return None, None

        return None, None

    def _get_stock_info_safe(self, ticker, symbol: str) -> dict:
        try:
            info = ticker.info
            if not info or 'symbol' not in info:
                info = {'symbol': symbol, 'shortName': symbol, 'longName': symbol}
        except Exception as e:
            self.logger.warning(f"Could not fetch info for {symbol}: {e}")
            info = {'symbol': symbol, 'shortName': symbol, 'longName': symbol}
        return info

    def clear_cache(self):
        self.cache.clear()
