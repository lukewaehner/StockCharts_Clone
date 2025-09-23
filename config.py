# Configuration settings for StockCharts application

COLORS = {
    # Primary monochromatic palette
    'background': '#f5f5f7',      # Light gray background (Apple-style)
    'surface': '#ffffff',         # Pure white surfaces
    'surface_elevated': '#ffffff',  # Elevated surfaces
    'surface_secondary': '#f9f9f9',  # Secondary surfaces

    # Text colors
    'text_primary': '#1d1d1f',    # Near black for primary text
    'text_secondary': '#86868b',  # Gray for secondary text
    'text_tertiary': '#a1a1a6',   # Light gray for tertiary text
    'text_on_dark': '#ffffff',    # White text on dark backgrounds

    # Accent colors
    'accent': '#007aff',          # Apple blue
    'accent_hover': '#0056d3',    # Darker blue for hover
    'accent_light': '#e3f2fd',    # Light blue for backgrounds

    # Status colors
    'success': '#30d158',         # Apple green
    'warning': '#ff9f0a',         # Apple orange
    'error': '#ff453a',           # Apple red
    'info': '#64d2ff',            # Apple cyan

    # Chart colors
    'chart_primary': '#007aff',   # Main chart color
    'chart_secondary': '#5856d6',  # Purple for secondary data
    'chart_success': '#30d158',   # Green for positive
    'chart_error': '#ff453a',     # Red for negative
    'chart_grid': '#f2f2f7',      # Very light gray for grid lines

    # Borders and dividers
    'border': '#e5e5e7',          # Light border
    'border_strong': '#d2d2d7',   # Stronger border
    'divider': '#f2f2f7',         # Very light divider

    # Legacy compatibility (will be phased out)
    'primary': '#f5f5f7',
    'secondary': '#86868b',
    'tertiary': '#a1a1a6',
    'dark': '#1d1d1f',
    'paper': '#ffffff',
    'danger': '#ff453a',
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
