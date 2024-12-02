import pickle
import pandas as pd
from flask import Flask, jsonify, request, Response, current_app
from waitress import serve
import os
from flask_cors import CORS

# Open the file in binary mode
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

def predictBitcoinPrice(date):
  predDf = pd.DataFrame({'ds': [date]})
  forecast = model.predict(predDf)
  prediction = forecast['yhat'].iloc[0]
  predictionHigh = forecast['yhat_upper'].iloc[0]
  predictionLow = forecast['yhat_lower'].iloc[0]

  result = {
    "prediction": prediction,
    "prediction_high": predictionHigh,
    "prediction_low": predictionLow,
    "date": date.isoformat()
  }

  return result

def remove_timezone(date):
  if date.tzinfo is not None:
        # Convert to UTC and then remove the timezone
        date = date.tz_convert('UTC')

  return date.tz_localize(None)

app = Flask("Crypto predict API", static_url_path='/')

CORS(app) # Enables Cross-Origin Resource Sharing

@app.route('/', methods=['GET'])
def index():
  return current_app.send_static_file("index.html")

@app.route('/bitcoin', methods=['GET'])
def bitcoin():
  if(request.method == 'GET'):
    dateInput = request.args.get('date')
    parsedDate = remove_timezone(pd.to_datetime(dateInput))

    result = predictBitcoinPrice(parsedDate)

    return jsonify(result)

port = int(os.environ.get("PORT", 8080))

print(f"Server starts listening on port {port}...")

serve(app, host="0.0.0.0", port=port)

print(f"Server is no longer listening on port {port}")
