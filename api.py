import pickle
import dateutil.parser as datetimeParser
import pandas as pd
from flask import Flask, jsonify, request, Response
from waitress import serve
import os

# Open the file in binary mode
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

def predictBitcoinPrice(date):
  pred_data = {
    'timestamp': [date]
  }
  predDf = pd.DataFrame(pred_data)
  predArray = model.predict(predDf)
  predPrice = predArray[0]
  return predPrice

app = Flask("Crypto predict API")

@app.route('/bitcoin', methods=['GET'])
def bitcoin():
  if(request.method == 'GET'):
    dateInput = request.args.get('date')
    parsedDate = datetimeParser.parse(dateInput)

    data = {
      "price": predictBitcoinPrice(parsedDate),
      "date": parsedDate,
    }
    return jsonify(data)

@app.route('/healthz', methods=['GET'])
def healthcheck():
    if(request.method == 'GET'):
      return Response(status=200)


port = int(os.environ.get("PORT", 8080))

print(f"Server starts listening on port {port}...")

serve(app, host="0.0.0.0", port=port)

print(f"Server is no longer listening on port {port}")
