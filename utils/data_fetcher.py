import yfinance as yf
import pandas as pd
import logging
from typing import Optional, Tuple


class StockDataFetcher:
    """Handle stock data retrieval with caching and error handling."""

    def __init__(self):
        self.cache = {}
        self.logger = logging.getLogger(__name__)

    def get_stock_data(self, symbol: str) -> Tuple[Optional[pd.DataFrame], Optional[dict]]:
        """
        Fetch stock data and info for a given symbol.

        Args:
            symbol (str): Stock ticker symbol

        Returns:
            tuple: (historical_data, stock_info) or (None, None) if error
        """
        try:
            # Check cache first
            if symbol in self.cache:
                return self.cache[symbol]

            ticker = yf.Ticker(symbol)

            # Get historical data
            hist = ticker.history(period='max')
            if hist.empty:
                self.logger.warning(
                    f"No historical data found for symbol: {symbol}")
                return None, None

            # Get stock info
            try:
                info = ticker.info
                if not info or 'symbol' not in info:
                    info = {'symbol': symbol, 'shortName': symbol}
            except Exception as e:
                self.logger.warning(f"Could not fetch info for {symbol}: {e}")
                info = {'symbol': symbol, 'shortName': symbol}

            # Cache the result
            self.cache[symbol] = (hist, info)

            return hist, info

        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {e}")
            return None, None

    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate if a stock symbol exists and has data.

        Args:
            symbol (str): Stock ticker symbol

        Returns:
            bool: True if valid, False otherwise
        """
        hist, info = self.get_stock_data(symbol)
        return hist is not None and not hist.empty

    def clear_cache(self):
        """Clear the data cache."""
        self.cache.clear()

    def get_stock_info(self, symbol: str) -> Optional[dict]:
        """
        Get stock information only.

        Args:
            symbol (str): Stock ticker symbol

        Returns:
            dict: Stock information or None if error
        """
        _, info = self.get_stock_data(symbol)
        return info
