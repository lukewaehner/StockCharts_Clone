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
                # Controls container (moved above chart for better UX)
                self._create_controls_panel(),

                # Chart container
                html.Div([
                    dcc.Graph(
                        id='main-chart',
                        config={
                            'displayModeBar': True,
                            'displaylogo': False,
                            'modeBarButtonsToRemove': [
                                'pan2d', 'lasso2d', 'select2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian',
                                'toggleSpikelines'
                            ],
                            'toImageButtonOptions': {
                                'format': 'png',
                                'filename': 'stock_chart',
                                'height': 800,
                                'width': 1200,
                                'scale': 2
                            }
                        },
                        style={'height': '700px'}
                    ),
                ], className='chart-container'),

            ], className='main-content'),

            # Footer
            self._create_footer(),

            # Loading component
            dcc.Loading(
                id='loading',
                type='circle',
                color=self.colors['accent'],
                children=[html.Div(id='loading-output')],
                style={
                    'position': 'fixed',
                    'top': '50%',
                    'left': '50%',
                    'transform': 'translate(-50%, -50%)',
                    'zIndex': 9999
                }
            ),

            # Error display
            html.Div(id='error-display', className='error-message'),

        ], className='app-container')

    def _create_header(self):
        """Create the header section with modern styling."""
        return html.Div([
            html.Div([
                html.H1('StockCharts', className='app-title'),
                html.P('Professional Stock Analysis & Technical Indicators',
                       className='app-subtitle'),
            ], style={'textAlign': 'center'}),
        ], className='header')

    def _create_controls_panel(self):
        """Create the modern controls panel."""
        return html.Div([
            # Stock symbol input
            html.Div([
                html.Label('Stock Symbol', className='input-label'),
                dcc.Input(
                    id='stock-symbol',
                    type='text',
                    placeholder='Enter ticker symbol (e.g., AAPL, TSLA, NVDA)',
                    value=self.defaults['stock_symbol'],
                    className='stock-input',
                    debounce=True,
                    maxLength=10,
                    style={'textTransform': 'uppercase'}
                ),
                html.Div([
                    html.Span(
                        '💡 ', style={'fontSize': '14px', 'marginRight': '4px'}),
                    html.Span('Popular: AAPL, TSLA, NVDA, MSFT, GOOGL',
                              style={
                                  'fontSize': '12px',
                                  'color': 'var(--text-tertiary)',
                                  'marginTop': '4px',
                                  'display': 'block'
                              })
                ])
            ], className='input-group'),

            # Time range dropdown
            html.Div([
                html.Label('Time Period', className='input-label'),
                dcc.Dropdown(
                    id='time-range',
                    options=[
                        {'label': '📅 1 Month', 'value': 'month'},
                        {'label': '📅 3 Months', 'value': '3 months'},
                        {'label': '📅 6 Months', 'value': '6 months'},
                        {'label': '📈 1 Year', 'value': 'year'},
                        {'label': '📈 2 Years', 'value': '2 years'},
                        {'label': '📊 5 Years', 'value': '5 years'},
                        {'label': '📊 10 Years', 'value': '10 years'},
                        {'label': '🗓️ Year to Date', 'value': 'ytd'},
                        {'label': '🔄 All Time', 'value': 'max'},
                    ],
                    value=self.defaults['time_range'],
                    className='time-dropdown',
                    clearable=False,
                    searchable=False
                ),
            ], className='input-group'),

            # Technical indicators
            html.Div([
                html.Label('Technical Indicators', className='input-label'),
                dcc.Checklist(
                    id='indicators',
                    options=[
                        {'label': html.Span(['📈 Moving Averages'], style={
                                            'marginLeft': '8px'}), 'value': 'ma'},
                        {'label': html.Span(['📊 Bollinger Bands'], style={
                                            'marginLeft': '8px'}), 'value': 'bb'},
                        {'label': html.Span(
                            ['⚡ RSI'], style={'marginLeft': '8px'}), 'value': 'rsi'},
                        {'label': html.Span(['🌊 MACD'], style={
                                            'marginLeft': '8px'}), 'value': 'macd'},
                    ],
                    value=['ma', 'rsi', 'macd'],
                    className='indicator-checklist',
                    inline=True
                ),
                html.Div([
                    html.Span('ℹ️ ', style={
                              'fontSize': '14px', 'marginRight': '4px'}),
                    html.Span('Select indicators to overlay on your chart',
                              style={
                                  'fontSize': '12px',
                                  'color': 'var(--text-tertiary)',
                                  'marginTop': '8px',
                                  'display': 'block'
                              })
                ])
            ], className='input-group'),

        ], className='controls-container')

    def _create_footer(self):
        """Create the footer section with modern styling."""
        return html.Div([
            html.Div([
                html.P([
                    'Data provided by ',
                    html.A('Yahoo Finance',
                           href='https://finance.yahoo.com',
                           target='_blank',
                           style={'color': 'var(--accent)', 'textDecoration': 'none'}),
                    ' • Built with ',
                    html.A('Plotly Dash',
                           href='https://plotly.com/dash/',
                           target='_blank',
                           style={'color': 'var(--accent)', 'textDecoration': 'none'}),
                    ' • ',
                    html.Span('Real-time market data',
                              style={'color': 'var(--text-tertiary)', 'fontSize': '0.875rem'})
                ], className='footer-text'),
            ], style={'textAlign': 'center'})
        ], className='footer')

    def get_external_stylesheets(self):
        """Get external stylesheets for the app."""
        return [
            # Modern font stack - prioritizing system fonts
            'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
            # Icons for better visual hierarchy
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
        ]

    def create_error_component(self, message):
        """Create a standardized error component."""
        return html.Div([
            html.Div([
                html.I(className='fas fa-exclamation-triangle',
                       style={'marginRight': '8px', 'fontSize': '16px'}),
                html.Span(message)
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], className='error-message show')

    def create_success_component(self, message):
        """Create a standardized success component."""
        return html.Div([
            html.Div([
                html.I(className='fas fa-check-circle',
                       style={'marginRight': '8px', 'fontSize': '16px', 'color': 'var(--success)'}),
                html.Span(message)
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={
            'background': 'var(--success)',
            'color': 'white',
            'padding': 'var(--space-lg)',
            'borderRadius': 'var(--radius-md)',
            'fontWeight': '500',
            'boxShadow': 'var(--shadow-md)',
            'margin': '10px 0'
        })
