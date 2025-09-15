#!/usr/bin/env python3
"""
StockCharts Pro - Professional Stock Analysis & Technical Indicators

A modern, modular stock charting application built with Dash and Plotly.
Features comprehensive technical analysis tools and real-time data.
"""

import sys
import os
import webbrowser
import logging
from pathlib import Path

# Dash and Plotly imports
import dash
from dash import dcc, html, Input, Output, State
import pandas as pd

# Local imports
from config import COLORS, DEFAULTS, APP_CONFIG
from utils.data_fetcher import StockDataFetcher
from utils.time_utils import get_date_range_from_data
from components.chart_builder import ChartBuilder
from components.ui_components import UIComponents

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class StockChartsApp:
    """Main application class for StockCharts Pro."""

    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.chart_builder = ChartBuilder()
        self.ui_components = UIComponents()
        self.app = self._create_app()
        self._setup_callbacks()

    def _create_app(self):
        """Create and configure the Dash application."""
        # External stylesheets
        external_stylesheets = self.ui_components.get_external_stylesheets()

        app = dash.Dash(
            __name__,
            external_stylesheets=external_stylesheets,
            suppress_callback_exceptions=True,
            title="StockCharts Pro",
            update_title="Loading...",
            meta_tags=[
                {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                {"name": "description",
                    "content": "Professional stock analysis and technical indicators"},
            ]
        )

        # Set the layout
        app.layout = self.ui_components.create_main_layout()

        return app

    def _setup_callbacks(self):
        """Setup all Dash callbacks."""

        @self.app.callback(
            [Output('main-chart', 'figure'),
             Output('error-display', 'children'),
             Output('error-display', 'className'),
             Output('loading-output', 'children')],
            [Input('stock-symbol', 'value'),
             Input('time-range', 'value'),
             Input('indicators', 'value')]
        )
        def update_chart(stock_symbol, time_range, selected_indicators):
            """Update the main chart based on user inputs."""
            try:
                # Validate inputs
                if not stock_symbol or not stock_symbol.strip():
                    return self._create_empty_chart(), "", "error-message", ""

                stock_symbol = stock_symbol.strip().upper()
                time_range = time_range or DEFAULTS['time_range']
                selected_indicators = selected_indicators or []

                logger.info(
                    f"Updating chart for {stock_symbol} with time range {time_range}")

                # Fetch stock data
                hist_data, stock_info = self.data_fetcher.get_stock_data(
                    stock_symbol)

                if hist_data is None or hist_data.empty:
                    error_msg = f"No data found for symbol '{stock_symbol}'. Please check the ticker symbol."
                    return self._create_empty_chart(), error_msg, "error-message show", ""

                # Get date range for filtering
                start_date, end_date = get_date_range_from_data(
                    hist_data, time_range)

                if start_date is None or end_date is None:
                    error_msg = "Unable to determine date range for the selected period."
                    return self._create_empty_chart(), error_msg, "error-message show", ""

                # Filter data for the selected time range
                filtered_data = hist_data[
                    (hist_data.index >= start_date) & (
                        hist_data.index <= end_date)
                ].copy()

                if filtered_data.empty:
                    error_msg = f"No data available for the selected time period."
                    return self._create_empty_chart(), error_msg, "error-message show", ""

                # Create the chart with selected indicators
                figure = self._create_chart_with_indicators(
                    hist_data, stock_info, filtered_data, selected_indicators
                )

                return figure, "", "error-message", ""

            except Exception as e:
                logger.error(f"Error updating chart: {str(e)}", exc_info=True)
                error_msg = f"An error occurred while loading the chart: {str(e)}"
                return self._create_empty_chart(), error_msg, "error-message show", ""

    def _create_chart_with_indicators(self, hist_data, stock_info, filtered_data, selected_indicators):
        """Create chart with selected technical indicators."""
        # Create a modified chart builder that respects indicator selections
        chart_builder = ChartBuilder()

        # Temporarily modify the chart builder methods based on selections
        original_methods = {}

        if 'ma' not in selected_indicators:
            original_methods['_add_moving_averages'] = chart_builder._add_moving_averages
            chart_builder._add_moving_averages = lambda fig, data: None

        if 'bb' not in selected_indicators:
            original_methods['_add_bollinger_bands'] = chart_builder._add_bollinger_bands
            chart_builder._add_bollinger_bands = lambda fig, data: None

        if 'rsi' not in selected_indicators:
            original_methods['_add_rsi_chart'] = chart_builder._add_rsi_chart
            chart_builder._add_rsi_chart = lambda fig, data: None

        if 'macd' not in selected_indicators:
            original_methods['_add_macd_chart'] = chart_builder._add_macd_chart
            chart_builder._add_macd_chart = lambda fig, data: None

        # Create the chart
        figure = chart_builder.create_main_chart(
            hist_data, stock_info, filtered_data)

        # Restore original methods
        for method_name, method in original_methods.items():
            setattr(chart_builder, method_name, method)

        return figure

    def _create_empty_chart(self):
        """Create an empty chart for error states."""
        import plotly.graph_objects as go

        fig = go.Figure()
        fig.update_layout(
            title="No Data Available",
            plot_bgcolor=COLORS['background'],
            paper_bgcolor=COLORS['paper'],
            height=600,
            showlegend=False,
            annotations=[
                dict(
                    text="Enter a valid stock symbol to view chart",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=16, color=COLORS['tertiary'])
                )
            ]
        )
        fig.update_xaxes(showgrid=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, showticklabels=False)

        return fig

    def run(self, debug=None, host=None, port=None):
        """Run the application."""
        debug = debug if debug is not None else APP_CONFIG['debug']
        host = host or APP_CONFIG['host']
        port = port or APP_CONFIG['port']

        logger.info(f"Starting StockCharts Pro on http://{host}:{port}")

        # Open browser automatically if not in debug mode
        if not debug:
            try:
                # Try to open the HTML wrapper first
                html_file = resource_path('index2.html')
                if os.path.exists(html_file):
                    webbrowser.open('file://' + html_file)
                else:
                    # Fallback to direct URL
                    webbrowser.open(f'http://{host}:{port}')
            except Exception as e:
                logger.warning(f"Could not open browser: {e}")

        # Run the server
        self.app.run_server(debug=debug, host=host, port=port)


def main():
    """Main entry point for the application."""
    try:
        app = StockChartsApp()
        app.run()
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
