# StockCharts 📈

A professional stock analysis and technical indicators application built with Python, Dash, and Plotly. This modern, modular application provides comprehensive technical analysis tools with real-time data from Yahoo Finance.

![StockCharts](https://img.shields.io/badge/StockCharts-blue?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square&logo=python)
![Dash](https://img.shields.io/badge/Dash-2.14+-blue?style=flat-square&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## Features

### Advanced Charting

- **Interactive Candlestick Charts** - Professional OHLC visualization
- **Volume Analysis** - Color-coded volume bars with price correlation
- **Multiple Time Ranges** - From 1 month to maximum historical data
- **Responsive Design** - Works on desktop, tablet, and mobile devices

### Technical Indicators

- **RSI (Relative Strength Index)** - Momentum oscillator with overbought/oversold levels
- **Moving Averages** - 20-day and 50-day simple moving averages
- **Bollinger Bands** - Volatility bands with statistical analysis
- **MACD** - Moving Average Convergence Divergence with histogram
- **Toggleable Indicators** - Enable/disable indicators as needed

### Modern Architecture

- **Modular Design** - Clean separation of concerns
- **Error Handling** - Robust error management and user feedback
- **Caching System** - Improved performance with data caching
- **Logging** - Comprehensive logging for debugging and monitoring
- **Type Hints** - Full type annotation support

### Features

- **Real-time Data** - Live stock data from Yahoo Finance
- **Symbol Validation** - Automatic validation of stock ticker symbols
- **Styling** - Modern UI with consistent design system
- **Loading States** - Smooth loading animations and feedback
- **Error Messages** - Clear, user-friendly error notifications

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/StockCharts_Clone.git
   cd StockCharts_Clone
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python StockCharts.py
   ```

4. **Open your browser**
   - The application will automatically open in your default browser
   - Or navigate to `http://127.0.0.1:8050`

### Alternative: Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python StockCharts.py
```

## Usage

### Basic Usage

1. **Enter a Stock Symbol**: Type any valid stock ticker (e.g., AAPL, MSFT, GOOGL, TSLA)
2. **Select Time Range**: Choose from 1 month to maximum historical data
3. **Toggle Indicators**: Enable/disable technical indicators as needed
4. **Analyze**: Interactive charts with zoom, pan, and hover capabilities

### Supported Stock Symbols

- **US Stocks**: AAPL, MSFT, GOOGL, AMZN, TSLA, etc.
- **Indices**: ^DJI (Dow Jones), ^GSPC (S&P 500), ^IXIC (NASDAQ)
- **International**: Many international stocks supported
- **ETFs**: SPY, QQQ, VTI, and other ETFs

### Time Ranges

- 1 Month, 3 Months, 6 Months
- 1 Year, 2 Years, 5 Years, 10 Years
- Year to Date (YTD)
- Maximum available data

### Technical Indicators

- **Moving Averages**: 20-day and 50-day SMAs
- **Bollinger Bands**: 20-period with 2 standard deviations
- **RSI**: 14-period with 30/70 levels
- **MACD**: 12/26/9 periods with histogram

## Project Structure

```
StockCharts_Clone/
├── StockCharts.py          # Main application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── index2.html            # HTML wrapper
├── style.css              # Legacy CSS (deprecated)
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── data_fetcher.py    # Stock data fetching and caching
│   ├── indicators.py      # Technical indicators calculations
│   └── time_utils.py      # Time range calculations
├── components/            # UI and chart components
│   ├── __init__.py
│   ├── chart_builder.py   # Chart creation and styling
│   └── ui_components.py   # Dash UI components
├── assets/                # Static assets
│   └── styles.css         # Modern CSS styling
└── StockChartDownload-MacOS/ # Packaged executable
```

## Customization

### Colors and Themes

Edit `config.py` to customize the color scheme:

```python
COLORS = {
    'primary': '#CFD6EA',
    'secondary': '#B0B2B8',
    'accent': '#4F5D2f',
    # ... more colors
}
```

### Technical Indicators

Modify indicator parameters in `config.py`:

```python
CHART_CONFIG = {
    'rsi_period': 14,
    'ma_period': 30,
    'volume_percentage': 0.08,
    # ... more settings
}
```

### Adding New Indicators

1. Add calculation function to `utils/indicators.py`
2. Add chart rendering to `components/chart_builder.py`
3. Update UI controls in `components/ui_components.py`

## Building Executable

The project includes PyInstaller configuration for creating standalone executables:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable (using existing .spec file)
pyinstaller StockCharts.spec
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Yahoo Finance** - For providing free stock data API
- **Plotly/Dash** - For the excellent visualization framework
- **Python Community** - For the amazing ecosystem of libraries

## Version History

### v2.0.0 (Current)

- Complete rewrite with modular architecture
- Added multiple technical indicators
- Modern UI with responsive design
- Improved error handling and caching
- Professional styling and animations

### v1.0.0 (Legacy)

- Basic candlestick charts
- Simple RSI indicator
- Basic time range selection

---
