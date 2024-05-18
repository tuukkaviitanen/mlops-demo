import pickle
import pandas as pd
from flask import Flask, jsonify, request, Response
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
    "prediction low": predictionLow,
    "date": date
  }

  return result

app = Flask("Crypto predict API")

CORS(app) # Enables Cross-Origin Resource Sharing

@app.route('/bitcoin', methods=['GET'])
def bitcoin():
  if(request.method == 'GET'):
    dateInput = request.args.get('date')
    parsedDate = pd.to_datetime(dateInput)

    result = predictBitcoinPrice(parsedDate)

    return jsonify(result)

@app.route('/healthz', methods=['GET'])
def healthcheck():
    if(request.method == 'GET'):
      return Response(status=200)


port = int(os.environ.get("PORT", 8080))

print(f"Server starts listening on port {port}...")

serve(app, host="0.0.0.0", port=port)

print(f"Server is no longer listening on port {port}")
