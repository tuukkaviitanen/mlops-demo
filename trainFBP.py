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
from prophet.plot import plot_plotly, plot_components_plotly
from prophet import Prophet 
from statsmodels.tools.eval_measures import rmse

#Set dataset and training parameters 
datasetSize=365 #Set dataset size in days
testSplitSize=50 #Set size of the test split for train and test sets
forecastPeriod=8760 #Set the length of the forecast (in hours) year is 8760, 30 days is 720, 180 days is 4320
selectedColumn="vwap" #Set which price data column to forecast by: open, high, low, close, vwap

client = CryptoHistoricalDataClient()

current = datetime.now()
current_date = current.strftime("%Y-%m-%d")
startDate = (current - timedelta(days=datasetSize)).strftime("%Y-%m-%d")
print(current_date)
print(startDate)

# Creating request object
request_params = CryptoBarsRequest(
  symbol_or_symbols=["BTC/USD"],
  timeframe=TimeFrame.Hour,
  start="2021-01-01",
  end=current_date
)

data = client.get_crypto_bars(request_params)

df = data.df

# Reset the index of the DataFrame
df.reset_index(inplace=True)

# Select the "timestamp" and "high" columns
df = df[["timestamp", selectedColumn]]

# Remove timezone information from the timestamps in the "ds" column
df['timestamp'] = df['timestamp'].dt.tz_localize(None)

#Change headers for prophet
df.columns = ['ds','y']

#convert timestamp to correct form
df['ds'] = pd.to_datetime(df['ds'])

# Split the dataframe into training and testing sets
train = df.iloc[:len(df)-testSplitSize]
test = df.iloc[len(df)-testSplitSize:]

m = Prophet(interval_width=0.8) #default 80& confidence
m.fit(train)
future = m.make_future_dataframe( periods=forecastPeriod, freq='H') #MS for monthly, H for hourly
forecast = m.predict(future)

predictions = forecast.iloc[-testSplitSize:]['yhat']

#save model
with open('modelFBPa.pkl', 'wb') as file:
    pickle.dump(m, file)

