"""Backend configuration — time-range constants and defaults."""

TIME_RANGES = {
    'day': 2,
    'week': 5,
    'month': 30,
    'quarter': 90,
    '3 months': 90,
    'half year': 180,
    '6 months': 180,
    '1 year': 365,
    'year': 365,
    '2 years': 730,
    '5 years': 1826,
    '10 years': 3652,
    'year to date': 'ytd',
    'ytd': 'ytd',
    'max': 'max',
}

DEFAULTS = {
    'stock_symbol': '^DJI',
    'time_range': 'ytd',
}

INDICATOR_CONFIG = {
    'rsi_period': 14,
    'ma_short': 20,
    'ma_long': 50,
    'bb_period': 20,
    'bb_std_dev': 2,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
}
