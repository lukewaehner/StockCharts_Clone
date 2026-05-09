import pandas as pd
import numpy as np


def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    if 'Close' not in data.columns or len(data) < period:
        return pd.Series(dtype=float)

    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))

    return rsi.fillna(50)


def calculate_moving_average(data: pd.DataFrame, period: int = 20,
                             column: str = 'Close') -> pd.Series:
    if column not in data.columns:
        return pd.Series(dtype=float)
    return data[column].rolling(window=period, min_periods=1).mean()


def calculate_bollinger_bands(data: pd.DataFrame, period: int = 20,
                              std_dev: float = 2, column: str = 'Close'):
    if column not in data.columns:
        empty = pd.Series(dtype=float)
        return empty, empty, empty

    middle_band = calculate_moving_average(data, period, column)
    std = data[column].rolling(window=period, min_periods=1).std()
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    return upper_band, middle_band, lower_band


def calculate_macd(data: pd.DataFrame, fast_period: int = 12,
                   slow_period: int = 26, signal_period: int = 9,
                   column: str = 'Close'):
    if column not in data.columns:
        empty = pd.Series(dtype=float)
        return empty, empty, empty

    exp1 = data[column].ewm(span=fast_period, adjust=False).mean()
    exp2 = data[column].ewm(span=slow_period, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram
