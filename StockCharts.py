import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import pickle


def timeFunc(str):
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
    with open('lastDate.pkl', 'rb') as file:
        lastDate = pickle.load(file)
    # ytd call
    if 'ytd' == ranges[str]:
        with open('ytdCall.pkl', 'rb') as file:
            ytdCall = pickle.load(file)
        while not 0 == ((today-lastDate).days):
            lastDate = lastDate + datetime.timedelta(days=1)
            if lastDate.weekday() < 5:
                print("appended:", lastDate)
                inputChange.append(lastDate)
        with open('lastDate.pkl', 'wb') as file:
            print("lastDate", lastDate)
            pickle.dump(lastDate, file)
        ytdCall = ytdCall - len(inputChange)
        with open('ytdCall.pkl', 'wb') as file:
            pickle.dump(ytdCall, file)
        return ytdCall

    # normal return
    else:
        loggedDays = ranges[str]
        while loggedDays > -1:
            inputChange.append(today)
            if today.weekday() > 4:
                inputChange.pop()
            today = today - datetime.timedelta(days=1)
            loggedDays -= 1
        return (-1 * len(inputChange))


# symbol = yf.Ticker(input("Enter a Ticker"))
symbol = yf.Ticker('TSLA')
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
hist.loc[hist['diff'] >= 0, 'color'] = 'green'
hist.loc[hist['diff'] < 0, 'color'] = 'red'
mainChart.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker={
                    'color': hist['color']}), secondary_y=True)
# descales volume
mainChart.update_yaxes(range=[0, 5000000000], secondary_y=True)
mainChart.update_yaxes(visible=False, secondary_y=True)

# MA20 trace
mainChart.add_trace(go.Scatter(x=hist.index, y=hist['Close'].rolling(
    window=20).mean(), marker_color='blue', name='20 Day MA'))

startDateVar = input("What start date do you want to  view from: \n")
# set x-axis initial to show scoped portions
if not startDateVar == "max":
    start_date = hist.index[timeFunc(startDateVar)]
    end_date = hist.index[-1]
    mainChart.update_xaxes(range=[start_date, end_date])

# rangeslider tekkkkk
mainChart.update_layout(xaxis_rangeslider_visible=True)

# update title
mainChart.update_layout(title={'text': symbol.info["symbol"], 'x': 0.5})

# show chart
mainChart.show()
