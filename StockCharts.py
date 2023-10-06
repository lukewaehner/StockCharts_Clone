import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Define Symbol and Get Ranges
ranges = {'day': '1d',
        'week': '5d',
        'month': '1mo',
        'quarter': '3mo',
        '3 months': '3mo',
        'half year': '6mo',
        '6 months': '6mo',
        '1 year': '1y',
        'year': '1y',
        '2 years': '2y',
        '5 years': '5y',
        '10 years': '10y',
        'year to date': 'ytd',
        'ytd': 'ytd',
        'max': 'max'
                   }

#symbol = yf.Ticker(input("Enter a Ticker"))
symbol = yf.Ticker('TSLA')
hist = symbol.history(period='1y')

#plotly -> create [Input fig = go.Figure(data=go.candlestick)]
mainChart = go.Figure(data=go.Scatter(x=hist.index, y=hist['Close'], mode='lines+markers'))

#Volume subchart
volumeChart = make_subplots(specs=[[{"secondary_y": True}]])
volumeChart.add_trace(go.Scatter(x=hist.index,y=hist['Close'],name='Price'),secondary_y=False)
volumeChart.add_trace(go.Bar(x=hist.index,y=hist['Volume'],name='Volume'),secondary_y=True)
volumeChart.update_yaxes(range=[0,7000000000],secondary_y=True)
volumeChart.update_yaxes(visible=False, secondary_y=True)

mainChart.show()
volumeChart.show()