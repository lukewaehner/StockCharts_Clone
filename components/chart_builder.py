import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from config import COLORS, CHART_CONFIG
from utils.indicators import (
    calculate_rsi, calculate_moving_average,
    calculate_bollinger_bands, calculate_macd
)


class ChartBuilder:
    """Build interactive stock charts with technical indicators."""

    def __init__(self):
        self.colors = COLORS
        self.config = CHART_CONFIG

    def create_main_chart(self, data: pd.DataFrame, symbol_info: dict,
                          filtered_data: pd.DataFrame) -> go.Figure:
        """
        Create the main stock chart with subplots.

        Args:
            data (pd.DataFrame): Full historical data
            symbol_info (dict): Stock information
            filtered_data (pd.DataFrame): Filtered data for the selected time range

        Returns:
            go.Figure: Complete chart figure
        """
        # Create subplots: RSI on top, main chart on bottom
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            row_heights=[0.2, 0.6, 0.2],
            vertical_spacing=0.05,
            specs=[
                [{"secondary_y": False}],  # RSI
                [{"secondary_y": True}],   # Main chart with volume
                [{"secondary_y": False}]   # MACD
            ],
            subplot_titles=(
                'RSI', f'{symbol_info.get("shortName", symbol_info["symbol"])}', 'MACD')
        )

        # Add main chart components
        self._add_candlestick_chart(fig, filtered_data)
        self._add_volume_chart(fig, filtered_data)
        self._add_moving_averages(fig, filtered_data)
        self._add_bollinger_bands(fig, filtered_data)

        # Add technical indicators
        self._add_rsi_chart(fig, filtered_data)
        self._add_macd_chart(fig, filtered_data)

        # Update layout and styling
        self._update_chart_layout(fig, symbol_info, filtered_data)

        return fig

    def _add_candlestick_chart(self, fig: go.Figure, data: pd.DataFrame):
        """Add candlestick chart with modern styling."""
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price',
                increasing_line_color=self.colors['chart_success'],
                decreasing_line_color=self.colors['chart_error'],
                increasing_fillcolor=self.colors['chart_success'],
                decreasing_fillcolor=self.colors['chart_error'],
                line={'width': 1}
            ),
            row=2, col=1
        )

    def _add_volume_chart(self, fig: go.Figure, data: pd.DataFrame):
        """Add volume chart with modern styling."""
        # Color volume bars based on price movement
        colors = []
        for i in range(len(data)):
            if data['Close'].iloc[i] >= data['Open'].iloc[i]:
                colors.append(self.colors['chart_success'])
            else:
                colors.append(self.colors['chart_error'])

        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker={'color': colors, 'opacity': 0.4},
                yaxis='y2'
            ),
            secondary_y=True,
            row=2, col=1
        )

    def _add_moving_averages(self, fig: go.Figure, data: pd.DataFrame):
        """Add moving average lines with modern styling."""
        ma20 = calculate_moving_average(data, 20)
        ma50 = calculate_moving_average(data, 50)

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=ma20,
                name='MA20',
                line=dict(color=self.colors['chart_primary'], width=2),
                opacity=0.7
            ),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=ma50,
                name='MA50',
                line=dict(color=self.colors['chart_secondary'], width=2),
                opacity=0.7
            ),
            row=2, col=1
        )

    def _add_bollinger_bands(self, fig: go.Figure, data: pd.DataFrame):
        """Add Bollinger Bands."""
        upper, middle, lower = calculate_bollinger_bands(data)

        # Add upper band
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=upper,
                name='BB Upper',
                line=dict(
                    color=self.colors['text_tertiary'], width=1, dash='dash'),
                opacity=0.5
            ),
            row=2, col=1
        )

        # Add lower band with fill
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=lower,
                name='BB Lower',
                line=dict(
                    color=self.colors['text_tertiary'], width=1, dash='dash'),
                fill='tonexty',
                fillcolor='rgba(0, 122, 255, 0.05)',  # Very subtle blue fill
                opacity=0.5
            ),
            row=2, col=1
        )

    def _add_rsi_chart(self, fig: go.Figure, data: pd.DataFrame):
        """Add RSI indicator."""
        rsi = calculate_rsi(data, self.config['rsi_period'])

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=rsi,
                name='RSI',
                line=dict(color=self.colors['chart_secondary'], width=2)
            ),
            row=1, col=1
        )

        # Add RSI reference lines
        fig.add_hline(y=70, line_dash="dash", line_color=self.colors['chart_error'],
                      opacity=0.6, row=1, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color=self.colors['chart_success'],
                      opacity=0.6, row=1, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color=self.colors['text_tertiary'],
                      opacity=0.4, row=1, col=1)

    def _add_macd_chart(self, fig: go.Figure, data: pd.DataFrame):
        """Add MACD indicator to bottom subplot."""
        macd_line, signal_line, histogram = calculate_macd(data)

        # MACD line
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=macd_line,
                name='MACD',
                line=dict(color='blue', width=2)
            ),
            row=3, col=1
        )

        # Signal line
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=signal_line,
                name='Signal',
                line=dict(color='red', width=2)
            ),
            row=3, col=1
        )

        # Histogram
        colors = ['green' if val >= 0 else 'red' for val in histogram]
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=histogram,
                name='Histogram',
                marker={'color': colors, 'opacity': 0.6}
            ),
            row=3, col=1
        )

    def _update_chart_layout(self, fig: go.Figure, symbol_info: dict,
                             filtered_data: pd.DataFrame):
        """chart layout."""
        # Calculate price range for main chart
        price_offset = (filtered_data['High'].max(
        ) - filtered_data['Low'].min()) * self.config['price_offset_percentage']
        min_price = filtered_data['Low'].min() - price_offset
        max_price = filtered_data['High'].max() + price_offset

        # Calculate volume scaling
        avg_volume = filtered_data['Volume'].mean()
        volume_max = avg_volume / self.config['volume_percentage']

        # chart styling
        fig.update_layout(
            title={
                'text': f"{symbol_info.get('shortName', symbol_info['symbol'])} ({symbol_info['symbol']})",
                'x': 0.02,
                'xanchor': 'left',
                'font': {
                    'size': 24,
                    'color': self.colors['text_primary'],
                    'family': '-apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif'
                },
                'pad': {'b': 20}
            },
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            paper_bgcolor=self.colors['surface'],
            font={
                'color': self.colors['text_primary'],
                'family': '-apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif',
                'size': 12
            },
            height=700,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=0.98,
                xanchor="left",
                x=0.02,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor=self.colors['border'],
                borderwidth=1,
                font={'size': 11}
            ),
            margin=dict(l=60, r=40, t=80, b=60),
            # Modern hover styling
            hoverlabel=dict(
                bgcolor=self.colors['surface'],
                bordercolor=self.colors['border'],
                font_size=12,
                font_family='-apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif'
            )
        )

        # Axes styling
        axis_style = dict(
            showgrid=True,
            gridcolor=self.colors['chart_grid'],
            gridwidth=0.5,
            showline=True,
            linecolor=self.colors['border'],
            linewidth=1,
            tickcolor=self.colors['border'],
            tickfont={'size': 10, 'color': self.colors['text_secondary']},
            titlefont={'size': 12, 'color': self.colors['text_primary']}
        )

        # RSI axis
        fig.update_yaxes(
            range=[0, 100],
            title="RSI",
            row=1, col=1,
            **axis_style
        )

        # Price axis
        fig.update_yaxes(
            range=[min_price, max_price],
            title="Price ($)",
            row=2, col=1,
            **axis_style
        )

        # Volume axis
        fig.update_yaxes(
            range=[0, volume_max],
            title="Volume",
            secondary_y=True,
            row=2, col=1,
            **axis_style
        )

        # MACD axis
        fig.update_yaxes(
            title="MACD",
            row=3, col=1,
            **axis_style
        )

        # Update x-axes
        fig.update_xaxes(
            showgrid=True,
            gridcolor=self.colors['chart_grid'],
            gridwidth=0.5,
            showline=True,
            linecolor=self.colors['border'],
            linewidth=1,
            tickcolor=self.colors['border'],
            tickfont={'size': 10, 'color': self.colors['text_secondary']},
            titlefont={'size': 12, 'color': self.colors['text_primary']},
            row=3, col=1,
            title="Date"
        )

        # Apply same x-axis styling to other rows but without title
        for row in [1, 2]:
            fig.update_xaxes(
                showgrid=True,
                gridcolor=self.colors['chart_grid'],
                gridwidth=0.5,
                showline=True,
                linecolor=self.colors['border'],
                linewidth=1,
                tickcolor=self.colors['border'],
                tickfont={'size': 10, 'color': self.colors['text_secondary']},
                row=row, col=1
            )

        # Remove range slider for cleaner look
        fig.update_layout(xaxis_rangeslider_visible=False)

        # Add subtle separators between subplots
        fig.add_hline(
            y=0, line_color=self.colors['divider'], line_width=1,
            row=1, col=1
        )
