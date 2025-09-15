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
        """Add candlestick chart to the main subplot."""
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price',
                increasing_line_color=self.colors['success'],
                decreasing_line_color=self.colors['danger'],
                increasing_fillcolor=self.colors['success'],
                decreasing_fillcolor=self.colors['danger']
            ),
            row=2, col=1
        )

    def _add_volume_chart(self, fig: go.Figure, data: pd.DataFrame):
        """Add volume chart as secondary y-axis."""
        # Color volume bars based on price movement
        colors = []
        for i in range(len(data)):
            if data['Close'].iloc[i] >= data['Open'].iloc[i]:
                colors.append(self.colors['success'])
            else:
                colors.append(self.colors['danger'])

        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker={'color': colors, 'opacity': 0.6},
                yaxis='y2'
            ),
            secondary_y=True,
            row=2, col=1
        )

    def _add_moving_averages(self, fig: go.Figure, data: pd.DataFrame):
        """Add moving average lines."""
        ma20 = calculate_moving_average(data, 20)
        ma50 = calculate_moving_average(data, 50)

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=ma20,
                name='MA20',
                line=dict(color=self.colors['info'], width=2),
                opacity=0.8
            ),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=ma50,
                name='MA50',
                line=dict(color=self.colors['warning'], width=2),
                opacity=0.8
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
                line=dict(color=self.colors['tertiary'], width=1, dash='dash'),
                opacity=0.6
            ),
            row=2, col=1
        )

        # Add lower band with fill
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=lower,
                name='BB Lower',
                line=dict(color=self.colors['tertiary'], width=1, dash='dash'),
                fill='tonexty',
                fillcolor=f"rgba(125, 126, 117, 0.1)",
                opacity=0.6
            ),
            row=2, col=1
        )

    def _add_rsi_chart(self, fig: go.Figure, data: pd.DataFrame):
        """Add RSI indicator to top subplot."""
        rsi = calculate_rsi(data, self.config['rsi_period'])

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=rsi,
                name='RSI',
                line=dict(color='purple', width=2)
            ),
            row=1, col=1
        )

        # Add RSI reference lines
        fig.add_hline(y=70, line_dash="dash", line_color="red",
                      opacity=0.7, row=1, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green",
                      opacity=0.7, row=1, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="gray",
                      opacity=0.5, row=1, col=1)

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
        """Update chart layout and styling."""
        # Calculate price range for main chart
        price_offset = (filtered_data['High'].max(
        ) - filtered_data['Low'].min()) * self.config['price_offset_percentage']
        min_price = filtered_data['Low'].min() - price_offset
        max_price = filtered_data['High'].max() + price_offset

        # Calculate volume scaling
        avg_volume = filtered_data['Volume'].mean()
        volume_max = avg_volume / self.config['volume_percentage']

        # Update layout
        fig.update_layout(
            title={
                'text': f"{symbol_info.get('shortName', symbol_info['symbol'])} ({symbol_info['symbol']})",
                'x': 0.5,
                'font': {'size': 20, 'color': self.colors['dark']}
            },
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['paper'],
            font={'color': self.colors['dark']},
            height=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=80, r=80, t=100, b=80)
        )

        # Update axes
        fig.update_yaxes(range=[0, 100], title="RSI", row=1, col=1)
        fig.update_yaxes(range=[min_price, max_price],
                         title="Price ($)", row=2, col=1)
        fig.update_yaxes(range=[0, volume_max],
                         title="Volume", secondary_y=True, row=2, col=1)
        fig.update_yaxes(title="MACD", row=3, col=1)

        # Remove range slider and update x-axis
        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.update_xaxes(title="Date", row=3, col=1)

        # Style grid
        for row in [1, 2, 3]:
            fig.update_yaxes(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.3)',
                gridwidth=1,
                row=row,
                col=1
            )
            fig.update_xaxes(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.3)',
                gridwidth=1,
                row=row,
                col=1
            )
