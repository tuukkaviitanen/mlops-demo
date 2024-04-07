from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import pandas as pd
import dateutil.parser as datetimeParser
import pickle

# deps:  
# pip install alpaca-py
# pip install scikit-learn
# pip install python-dateutil

# todo:
# X = päivä
# y = vwap/ muu hinta. Muilla featureilla ei väliä?

# No keys required for crypto data
client = CryptoHistoricalDataClient()

def get_dates():
    current = datetime.now()
    year_ago = current - timedelta(days=365) # using smaller timeframe for development
    current_formatted = current.strftime("%Y-%m-%d")
    year_ago_formatted = year_ago.strftime("%Y-%m-%d")
    return current_formatted, year_ago_formatted

current_date, year_ago_date = get_dates()

# Creating request object
request_params = CryptoBarsRequest(
  symbol_or_symbols=["BTC/USD"],
  timeframe=TimeFrame.Day,
  start=year_ago_date,
  end=current_date
)

# Retrieve daily bars for Bitcoin in a DataFrame and printing it
data = client.get_crypto_bars(request_params)

# example rows of data:
#                                         open        high         low       close    volume  trade_count          vwap
# symbol  timestamp
# BTC/USD 2024-04-05 00:00:00+00:00  68496.5950  68738.1875  68251.3910  68666.0500  0.026063          3.0  68362.656246
#         2024-04-05 01:00:00+00:00  68598.0000  68632.9300  67861.1705  68157.3100  0.000580          2.0  68169.501510
#         2024-04-05 02:00:00+00:00  68150.4835  68150.4835  67510.9525  67636.3900  0.002519          6.0  67670.694690
#         2024-04-05 03:00:00+00:00  67662.6400  68019.8100  67662.6400  67867.6900  0.025481          1.0  67781.970000

# data explanation:
# open = The price of Bitcoin at the beginning of the time period (e.g., a day, hour, or minute) 
#        covered by the data. It represents the first trade that occurred during that period.
# high = The highest price of Bitcoin reached during the time period.
# low = The lowest price of Bitcoin reached during the time period.
# close = The price of Bitcoin at the end of the time period. It represents the last trade that occurred during that period.
# volume = The total amount of Bitcoin traded during the time period. Usually measured in terms of Bitcoin quantity, but sometimes it's denominated in another currency like USD.
# trade_count = The number of trades executed during the time period.
# vmap = Volume Weighted Average Price

# Convert to dataframe
# print(data.df)
df = data.df

from sklearn.model_selection import train_test_split

X = df.index.to_series() # timestamp
X = X.index.get_level_values('timestamp').to_frame()
# print(X)

y = df.iloc[:,-1] # vwap = target variable

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)

model = RandomForestRegressor()

model.fit(X_train,y_train)

y_pred = model.predict(X_test)

print("accuracy: ", r2_score(y_test,y_pred))

# save model 
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

# example

pred_date = "2024-04-15T06:00:00.000Z" # 2024-02-23T06:00:00.000Z
pred_data = {
    'timestamp': [datetimeParser.parse(pred_date)]
}
pred_df = pd.DataFrame(pred_data)

predicted_price = model.predict(pred_df)

print(f"Predicted price for {pred_date}: {predicted_price[0]}")





