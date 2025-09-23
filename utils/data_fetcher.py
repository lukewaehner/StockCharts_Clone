import yfinance as yf
import pandas as pd
import logging
import time
from typing import Optional, Tuple


class StockDataFetcher:
    """Handle stock data retrieval with caching and error handling."""

    def __init__(self):
        self.cache = {}
        self.logger = logging.getLogger(__name__)

    def get_stock_data(self, symbol: str, max_retries: int = 3) -> Tuple[Optional[pd.DataFrame], Optional[dict]]:
        """
        Fetch stock data and info for a given symbol with retry logic.

        Args:
            symbol (str): Stock ticker symbol
            max_retries (int): Maximum number of retry attempts

        Returns:
            tuple: (historical_data, stock_info) or (None, None) if error
        """
        # Check cache first
        if symbol in self.cache:
            return self.cache[symbol]

        for attempt in range(max_retries):
            try:
                self.logger.info(
                    f"Fetching data for {symbol} (attempt {attempt + 1}/{max_retries})")

                ticker = yf.Ticker(symbol)

                # Get historical data with explicit parameters to avoid multi-index issues
                hist = ticker.history(
                    period='max',
                    auto_adjust=True,  # Use adjusted prices by default
                    prepost=False,     # Exclude pre/post market data
                    actions=False      # Exclude dividends and splits data
                )

                # Handle multi-index columns in newer yfinance versions
                if isinstance(hist.columns, pd.MultiIndex):
                    # If we have multi-index columns, flatten them
                    hist.columns = hist.columns.droplevel(
                        1) if hist.columns.nlevels > 1 else hist.columns

                if hist.empty:
                    self.logger.warning(
                        f"No historical data found for symbol: {symbol}")
                    if attempt < max_retries - 1:
                        time.sleep(1)  # Wait before retry
                        continue
                    return None, None

                # Get stock info with error handling
                info = self._get_stock_info_safe(ticker, symbol)

                # Cache the result
                self.cache[symbol] = (hist, info)
                self.logger.info(f"Successfully fetched data for {symbol}")
                return hist, info

            except Exception as e:
                self.logger.warning(
                    f"Attempt {attempt + 1} failed for {symbol}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    self.logger.error(f"All attempts failed for {symbol}: {e}")
                    return None, None

        return None, None

    def _get_stock_info_safe(self, ticker, symbol: str) -> dict:
        """
        Safely get stock info with fallback to basic info.

        Args:
            ticker: yfinance Ticker object
            symbol (str): Stock ticker symbol

        Returns:
            dict: Stock information
        """
        try:
            info = ticker.info
            if not info or 'symbol' not in info:
                # Fallback to basic info
                info = {
                    'symbol': symbol,
                    'shortName': symbol,
                    'longName': symbol
                }
        except Exception as e:
            self.logger.warning(f"Could not fetch info for {symbol}: {e}")
            # Create minimal info dict
            info = {
                'symbol': symbol,
                'shortName': symbol,
                'longName': symbol
            }

        return info

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
        self.logger.info("Data cache cleared")

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

    def test_connection(self) -> bool:
        """
        Test connection to Yahoo Finance by fetching a known symbol.

        Returns:
            bool: True if connection is working, False otherwise
        """
        try:
            test_data, _ = self.get_stock_data("AAPL")
            return test_data is not None and not test_data.empty
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
