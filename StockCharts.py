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

#plotly -> create
mainChart = make_subplots(specs=[[{"secondary_y": True}]])
#Candlestick main trace
mainChart.add_trace(go.Candlestick(x=hist.index,
                                           open=hist['Open'],
                                           high=hist['High'],
                                           low=hist['Low'],
                                           close=hist['Close']))

#volume trace
mainChart.add_trace(go.Bar(x=hist.index,y=hist['Volume'],name='Volume'),secondary_y=True)
#descales volume
mainChart.update_yaxes(range=[0,5000000000],secondary_y=True)
mainChart.update_yaxes(visible=False, secondary_y=True)

#MA20 trace

mainChart.show()
#volumeChart.show()