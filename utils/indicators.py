import pandas as pd
import numpy as np


def calculate_rsi(data, period=14):
    """
    Calculate the Relative Strength Index (RSI) for given price data.

    Args:
        data (pd.DataFrame): Stock data with 'Close' column
        period (int): Period for RSI calculation (default: 14)

    Returns:
        pd.Series: RSI values
    """
    if 'Close' not in data.columns or len(data) < period:
        return pd.Series(dtype=float)

    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # Avoid division by zero
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))

    return rsi.fillna(50)  # Fill NaN with neutral RSI value


def calculate_moving_average(data, period=20, column='Close'):
    """
    Calculate simple moving average.

    Args:
        data (pd.DataFrame): Stock data
        period (int): Period for moving average
        column (str): Column to calculate MA for

    Returns:
        pd.Series: Moving average values
    """
    if column not in data.columns:
        return pd.Series(dtype=float)

    return data[column].rolling(window=period, min_periods=1).mean()


def calculate_bollinger_bands(data, period=20, std_dev=2, column='Close'):
    """
    Calculate Bollinger Bands.

    Args:
        data (pd.DataFrame): Stock data
        period (int): Period for calculation
        std_dev (float): Standard deviation multiplier
        column (str): Column to calculate bands for

    Returns:
        tuple: (upper_band, middle_band, lower_band)
    """
    if column not in data.columns:
        empty_series = pd.Series(dtype=float)
        return empty_series, empty_series, empty_series

    middle_band = calculate_moving_average(data, period, column)
    std = data[column].rolling(window=period, min_periods=1).std()

    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)

    return upper_band, middle_band, lower_band


def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9, column='Close'):
    """
    Calculate MACD (Moving Average Convergence Divergence).

    Args:
        data (pd.DataFrame): Stock data
        fast_period (int): Fast EMA period
        slow_period (int): Slow EMA period
        signal_period (int): Signal line EMA period
        column (str): Column to calculate MACD for

    Returns:
        tuple: (macd_line, signal_line, histogram)
    """
    if column not in data.columns:
        empty_series = pd.Series(dtype=float)
        return empty_series, empty_series, empty_series

    exp1 = data[column].ewm(span=fast_period, adjust=False).mean()
    exp2 = data[column].ewm(span=slow_period, adjust=False).mean()

    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram
