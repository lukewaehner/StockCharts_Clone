var codeSnippet = `
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# for applet
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
# for RSI
import ta
# for timeFunc
import datetime
import pickle

# stylesheet rel
external_stylesheets = ['styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# function to create specific list indexs to call the correct start date


def timeFunc(selected_time_range):
    ranges = {'day': 2,
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
    today = datetime.date.today()
    inputChange = []
    with open('variables/lastDate.pkl', 'rb') as file:
        lastDate = pickle.load(file)
    # ytd call
    if 'ytd' == selected_time_range or 'ytd' == ranges[selected_time_range]:
        with open('variables/ytdCall.pkl', 'rb') as file:
            ytdCall = pickle.load(file)
        while not 0 == ((today-lastDate).days):
            lastDate = lastDate + datetime.timedelta(days=1)
            if lastDate.weekday() < 5:
                inputChange.append(lastDate)
        with open('variables/lastDate.pkl', 'wb') as file:
            pickle.dump(lastDate, file)
        ytdCall = ytdCall - len(inputChange)
        with open('variables/ytdCall.pkl', 'wb') as file:
            pickle.dump(ytdCall, file)
        return ytdCall

    # normal return
    else:
        loggedDays = ranges.get(selected_time_range, 0)
        if loggedDays == 'max':
            return 0
        loggedDays = int(loggedDays)
        while loggedDays > -1:
            inputChange.append(today)
            if today.weekday() > 4:
                inputChange.pop()
            today = today - datetime.timedelta(days=1)
            loggedDays -= 1
        return (-1 * len(inputChange))


app.layout = html.Div([
    html.Div([
        dcc.Graph(id='mainChart'),
    ], style={'borderRadius': '10px', 'border': '2px solid #ccc', 'padding': '20px', 'margin': '20px'}),

    html.Div([
        html.Div([
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
                    {'label': 'YTD', 'value': 'ytd'},
                    {'label': 'max', 'value': 'max'},
                ],
                placeholder="Select a time range",
                style={'width': '100%'},
            )
        ], style={'width': '50%'}),

        html.Div([
            dcc.Input(id='stock-symbol', type='text',
                      placeholder='Enter a Stock Ticker Symbol', style={'width': '50%'},)
        ], style={'width': '50%'})
    ], style={'display': 'flex', 'gap': '20px', 'margin-left': '35px'}),
], style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(
    Output('mainChart', 'figure'),
    Input('time-range', 'value'),
    Input('stock-symbol', 'value'),  # Add this line for the stock symbol input
)
def update_chart(selected_time_range, selected_stock_symbol):
    if not selected_time_range:
        selected_time_range = 'ytd'
    if not selected_stock_symbol:
        selected_stock_symbol = 'DJIA'
    symbol = yf.Ticker(selected_stock_symbol)
    hist = symbol.history(period='max')
    # plotly -> create
    mainChart = make_subplots(specs=[[{"secondary_y": True}]])
    # Candlestick main trace
    mainChart.add_trace(go.Candlestick(x=hist.index,
                                       open=hist['Open'],
                                       high=hist['High'],
                                       low=hist['Low'],
                                       close=hist['Close']))

    # volume trace
    hist['diff'] = hist['Close'] - hist['Open']
    hist['color'] = 'red'  # Initialize 'color' column with 'red'
    hist.loc[hist['diff'] >= 0, 'color'] = 'green'
    mainChart.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker={
                        'color': hist['color']}), secondary_y=True)
    # descales volume
    mainChart.update_yaxes(range=[0, 5000000000], secondary_y=True)
    mainChart.update_yaxes(visible=False, secondary_y=True)

    # MA20 trace
    mainChart.add_trace(go.Scatter(x=hist.index, y=hist['Close'].rolling(
        window=20).mean(), marker_color='blue', name='20 Day MA'))

    # update x-axis range
    if len(hist.index) < abs(timeFunc(selected_time_range)):
        start_date = hist.index[timeFunc('max')]
    else:
        start_date = hist.index[timeFunc(selected_time_range)]
    end_date = hist.index[-1]
    # Set x-axis initial range
    mainChart.update_xaxes(range=[start_date, end_date])

    # rangeslider tekkkkk
    mainChart.update_layout(xaxis_rangeslider_visible=False)

    # update title
    mainChart.update_layout(
        title={'text': symbol.info["symbol"], 'x': 0.5})

    # show chart
    return mainChart


if __name__ == '__main__':
    app.run_server(debug=True)
`;

// Select the <pre> element and add the code
var codeElement = document.getElementById("sourcecode");
codeElement.textContent = codeSnippet;
