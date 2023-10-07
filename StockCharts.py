import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import pickle

#define symbol and vars

#get vars
with open('ytdCall.pkl', 'rb') as file:
        ytdCall = pickle.load(file)
with open('lastDate.pkl', 'rb') as file:
        lastDate = pickle.load(file)

today = datetime.date.today()
year1, week_number1, weekday1 = today.isocalendar()
year2, week_number2, weekday2 = lastDate.isocalendar()

if weekday1 < 5:
       if week_number1 > week_number2:
                inputChange = ytdCall - (today-lastDate).days + ((week_number1 - week_number2)*2)
       else:
                inputChange = ytdCall - (today-lastDate).days #calculates the number of days to change
else:
        if week_number1 > week_number2:
         inputChange = ytdCall - (today-lastDate).days + ((week_number1 - week_number2-1)*2) - (weekday1-4)
        else:   
         inputChange = ytdCall - (today-lastDate).days - (weekday1-4) #calculates the number of days to change
if not lastDate == today:
                lastDate += today - lastDate
                ytdCall = inputChange
#dump vars
with open('lastDate.pkl', 'wb') as file:
        pickle.dump(lastDate, file)
with open('ytdCall.pkl', 'wb') as file:
    pickle.dump(ytdCall, file)

ranges = {'day': 2,
        'week': 5,
        'month': 30,
        'quarter': 90,
        '3 months': 90,
        'half year': 120,
        '6 months': 120,
        '1 year': 365,
        'year': 365,
        '2 years': 730,
        '5 years': 1826,
        '10 years': 3652,
        'year to date': ytdCall,
        'ytd': ytdCall,
        'max': 'max'
                   }
dictDate = ranges[input("What start date do you want to  view from: \n")]

#symbol = yf.Ticker(input("Enter a Ticker"))
symbol = yf.Ticker('TSLA')
hist = symbol.history(period='max')
print(hist.index[-192])
#plotly -> create
mainChart = make_subplots(specs=[[{"secondary_y": True}]])
#Candlestick main trace
mainChart.add_trace(go.Candlestick(x=hist.index,
                                open=hist['Open'],
                                high=hist['High'],
                                low=hist['Low'],
                                close=hist['Close']))

#volume trace
hist['diff'] = hist['Close'] - hist['Open']
hist.loc[hist['diff']>=0, 'color'] = 'green'
hist.loc[hist['diff']<0, 'color'] = 'red'
mainChart.add_trace(go.Bar(x=hist.index,y=hist['Volume'],name='Volume', marker={'color': hist['color']}), secondary_y=True)
#descales volume
mainChart.update_yaxes(range=[0,5000000000],secondary_y=True)
mainChart.update_yaxes(visible=False, secondary_y=True)

#MA20 trace
mainChart.add_trace(go.Scatter(x=hist.index,y=hist['Close'].rolling(window=20).mean(),marker_color='blue',name='20 Day MA'))

#set x-axis initial to show scoped portions
if not dictDate == "max":
        #start_date = hist.index[-1 * dictDate]
        start_date = hist.index[dictDate]
        end_date = hist.index[-1]
        mainChart.update_xaxes(range=[start_date, end_date])

#rangeslider tekkkkk
mainChart.update_layout(xaxis_rangeslider_visible=True)

#update title
mainChart.update_layout(title={'text': symbol.info["symbol"], 'x':0.5})

#show chart
mainChart.show()
