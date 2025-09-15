import dash
from dash import dcc, html
from config import COLORS, DEFAULTS


class UIComponents:
    """Create and manage UI components for the Dash application."""

    def __init__(self):
        self.colors = COLORS
        self.defaults = DEFAULTS

    def create_main_layout(self):
        """Create the main application layout."""
        return html.Div([
            # Header section
            self._create_header(),

            # Main content area
            html.Div([
                # Chart container
                html.Div([
                    dcc.Graph(
                        id='main-chart',
                        config={
                            'displayModeBar': True,
                            'displaylogo': False,
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
                        }
                    ),
                ], className='chart-container'),

                # Controls container
                html.Div([
                    # Stock symbol input
                    html.Div([
                        html.Label('Stock Symbol:', className='input-label'),
                        dcc.Input(
                            id='stock-symbol',
                            type='text',
                            placeholder='Enter ticker (e.g., AAPL, MSFT)',
                            value=self.defaults['stock_symbol'],
                            className='stock-input',
                            debounce=True
                        ),
                    ], className='input-group'),

                    # Time range dropdown
                    html.Div([
                        html.Label('Time Range:', className='input-label'),
                        dcc.Dropdown(
                            id='time-range',
                            options=[
                                {'label': '1 Month', 'value': 'month'},
                                {'label': '3 Months', 'value': '3 months'},
                                {'label': '6 Months', 'value': '6 months'},
                                {'label': '1 Year', 'value': 'year'},
                                {'label': '2 Years', 'value': '2 years'},
                                {'label': '5 Years', 'value': '5 years'},
                                {'label': '10 Years', 'value': '10 years'},
                                {'label': 'Year to Date', 'value': 'ytd'},
                                {'label': 'Max', 'value': 'max'},
                            ],
                            value=self.defaults['time_range'],
                            className='time-dropdown',
                            clearable=False
                        ),
                    ], className='input-group'),

                    # Indicator toggles
                    html.Div([
                        html.Label('Technical Indicators:',
                                   className='input-label'),
                        dcc.Checklist(
                            id='indicators',
                            options=[
                                {'label': ' Moving Averages', 'value': 'ma'},
                                {'label': ' Bollinger Bands', 'value': 'bb'},
                                {'label': ' RSI', 'value': 'rsi'},
                                {'label': ' MACD', 'value': 'macd'},
                            ],
                            value=['ma', 'rsi', 'macd'],
                            className='indicator-checklist',
                            inline=True
                        ),
                    ], className='input-group'),

                ], className='controls-container'),

            ], className='main-content'),

            # Footer
            self._create_footer(),

            # Loading component
            dcc.Loading(
                id='loading',
                type='cube',
                color=self.colors['accent'],
                children=[html.Div(id='loading-output')]
            ),

            # Error display
            html.Div(id='error-display', className='error-message'),

        ], className='app-container')

    def _create_header(self):
        """Create the header section."""
        return html.Div([
            html.H1('StockCharts Pro', className='app-title'),
            html.P('Professional Stock Analysis & Technical Indicators',
                   className='app-subtitle'),
        ], className='header')

    def _create_footer(self):
        """Create the footer section."""
        return html.Div([
            html.P([
                'Data provided by ',
                html.A('Yahoo Finance',
                       href='https://finance.yahoo.com', target='_blank'),
                ' • Built with ',
                html.A('Plotly Dash', href='https://plotly.com/dash/',
                       target='_blank')
            ], className='footer-text'),
        ], className='footer')

    def get_external_stylesheets(self):
        """Get external stylesheets for the app."""
        return [
            'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
        ]
