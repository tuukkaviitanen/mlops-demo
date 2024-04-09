from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
import pandas as pd
import pickle
from prophet import Prophet

client = CryptoHistoricalDataClient()

current = datetime.now()
current_date = current.strftime("%Y-%m-%d")

# Creating request object
request_params = CryptoBarsRequest(
  symbol_or_symbols=["BTC/USD"],
  timeframe=TimeFrame.Hour,
  start="2021-01-01",
  end=current_date
)

print("Fetching training data...")

data = client.get_crypto_bars(request_params)

print("Fetched train data")

df = data.df

# Reset the index of the DataFrame
df.reset_index(inplace=True)

# Select only the "timestamp" and "close" columns
df = df[["timestamp", "close"]]

# Remove timezone information from the timestamps in the "ds" column
df['timestamp'] = df['timestamp'].dt.tz_localize(None)

#Change headers for prophet
df.columns = ['ds','y']

#convert timestamp to correct form
df['ds'] = pd.to_datetime(df['ds'])

print("Training model...")

model = Prophet(interval_width=0.8) #default 80& confidence
model.fit(df)

print("Model trained")

#save model
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)
