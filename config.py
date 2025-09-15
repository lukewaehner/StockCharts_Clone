# Configuration settings for StockCharts application

# Color scheme
COLORS = {
    'primary': '#CFD6EA',
    'secondary': '#B0B2B8',
    'tertiary': '#7D7E75',
    'accent': '#4F5D2f',
    'dark': '#423629',
    'background': '#ACCBE1',
    'paper': '#FFF',
    'success': '#28a745',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'info': '#17a2b8'
}

# Chart settings
CHART_CONFIG = {
    'rsi_period': 14,
    'ma_period': 30,
    'volume_percentage': 0.08,
    'price_offset_percentage': 0.01,
    'chart_height': 600,
    'subplot_heights': [0.3, 0.7],
    'vertical_spacing': 0.1
}

# Time range mappings
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
    'max': 'max'
}

# Default values
DEFAULTS = {
    'stock_symbol': '^DJI',  # Changed to Dow Jones Industrial Average
    'time_range': 'ytd'
}

# App settings
APP_CONFIG = {
    'debug': False,
    'host': '127.0.0.1',
    'port': 8050
}
