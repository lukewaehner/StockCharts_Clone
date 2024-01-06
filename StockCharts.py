import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# for applet
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
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


def calculate_rsi(data, period=14):
    # Calculate price changes
    delta = data['Close'].diff(1)

    # Gain and loss for each period
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate the average gain and average loss over the specified period
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # Calculate relative strength (RS)
    rs = avg_gain / avg_loss

    # Calculate the RSI
    rsi = 100 - (100 / (1 + rs))
    return rsi


color_1 = '#CFD6EA'
color_2 = '#B0B2B8'
color_3 = '#7D7E75'
color_4 = '#4F5D2f'
color_5 = '#423629'

app.layout = html.Div([
    # Main chart and controls container
    html.Div([
        # Main chart container
        html.Div([
            dcc.Graph(id='mainChart'),
        ], style={'borderRadius': '10px', 'border': f'2px solid {color_4}', 'padding': '10px', 'backgroundColor': color_1, 'width': '65vw'}),

        # Dropdown and input container
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

                style={'width': '250px', 'borderRadius': '10px',
                       'border': f'1px solid {color_2}'}
            ),
            dcc.Input(
                id='stock-symbol',
                type='text',
                placeholder='Enter a Stock Ticker Symbol',
                # Input properties...
                style={'width': '250px', 'display': 'block', 'padding': '10px',
                       'textAlign': 'center', "border": f'1px solid {color_2}', 'borderRadius': '10px'}
            ),
        ], style={'padding': '10px', 'backgroundColor': color_3, 'textAlign': 'center', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'gap': '50px', 'border': f'2px solid {color_5}', 'borderRadius': '10px', 'flexWrap': 'wrap'}),
    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center', 'gap': '20px', 'margin': 'auto', 'width': '90%'}),  # Style for centering
], style={'display': 'flex', 'flexDirection': 'column', 'width': '80vw', 'height': '100vh', 'backgroundColor': color_2, 'justifyContent': 'center',
          'position': 'fixed', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)',
          'borderRadius': '10px', 'boxShadow': '0px 0px 10px 5px rgba(255,255,255,0.75)'})


@app.callback(
    Output('mainChart', 'figure'),
    Input('time-range', 'value'),
    Input('stock-symbol', 'value'),  # Add this line for the stock symbol input
)
def update_chart(selected_time_range, selected_stock_symbol):
    if not selected_time_range:
        selected_time_range = 'ytd'
    if not selected_stock_symbol:
        selected_stock_symbol = '^DJA'
    symbol = yf.Ticker(selected_stock_symbol)
    hist = symbol.history(period='max')
    # plotly -> create
    mainChart = make_subplots(rows=2, cols=1, shared_xaxes=True,
                              row_heights=[0.3, 0.7], vertical_spacing=0.1, specs=[[{"secondary_y": False}], [{"secondary_y": True}]])
    # <------------------------ Bottom Chart ------------------------>
    # Candlestick main trace
    # print(hist.index)
    mainChart.add_trace(go.Candlestick(x=hist.index,
                                       open=hist['Open'],
                                       high=hist['High'],
                                       low=hist['Low'],
                                       close=hist['Close'],
                                       name='Price'), row=2, col=1)

    # volume trace
    hist['diff'] = hist['Close'] - hist['Open']
    hist['color'] = 'red'  # Initialize 'color' column with 'red'
    hist.loc[hist['diff'] >= 0, 'color'] = 'green'
    mainChart.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker={
                        'color': hist['color']}), secondary_y=True, row=2, col=1)
    # MA20 trace
    mainChart.add_trace(go.Scatter(x=hist.index, y=hist['Close'].rolling(
        window=30).mean(), marker_color='blue', name='30 Day MA'), row=2, col=1)
    # update x-axis range
    if len(hist.index) < abs(timeFunc(selected_time_range)):
        start_date = hist.index[timeFunc('max')]
    else:
        start_date = hist.index[timeFunc(selected_time_range)]
    end_date = hist.index[-1]

    # filter the data
    filtered_data = hist[(hist.index >= start_date) & (hist.index <= end_date)]

    start_date = filtered_data.index[0]
    end_date = filtered_data.index[-1]
    # Set x-axis initial range
    mainChart.update_xaxes(range=[start_date, end_date], type='date', ticktext=filtered_data.index.strftime(
        '%b-%y'), tickvals=filtered_data.index, tickmode='auto',  # Set to 'auto' or 'linear' based on your preference
        nticks=10, row=2, col=1)
    # Set y-axis range
    # Calculate the minimum and maximum values for the Y-axis
    offsetPercentage = max(hist['Close']) * 0.00  # 1
    min_y = min(filtered_data['Low']) - offsetPercentage
    max_y = max(filtered_data['High']) + offsetPercentage
    mainChart.update_yaxes(range=[min_y, max_y],
                           secondary_y=False, row=2, col=1)
    # descale volume to percentage of y axis (8%)
    avgVol = sum(filtered_data['Volume']) / len(filtered_data['Volume'])
    VolumePercentageMaximizer = avgVol / 0.08
    mainChart.update_yaxes(
        range=[0, VolumePercentageMaximizer], secondary_y=True, row=2, col=1)

    # <------------------------ Top Chart ------------------------>
    # RSI trace
    rsi = calculate_rsi(filtered_data)
    mainChart.add_trace(go.Scatter(
        x=rsi.index, y=rsi, marker_color='purple', name='RSI'), row=1, col=1)

    # update title
    mainChart.update_layout(
        title={'text': symbol.info["symbol"], 'x': 0.5},
        xaxis_rangeslider_visible=False,
        xaxis2_rangeslider_visible=False,
        plot_bgcolor='#ACCBE1',
        paper_bgcolor='#FFF',
        margin=dict(l=100, r=100, t=100, b=100, pad=10),
        showlegend=False,
    )
    mainChart.update_yaxes(
        showgrid=False,
        gridcolor='white',
        gridwidth=1,
        secondary_y=False,
        row=2,
        col=1
    )

    # show chart
    return mainChart


if __name__ == '__main__':
    app.run_server(debug=False)
