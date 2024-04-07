from flask import Flask, jsonify, request, Response

app = Flask("Crypto predict API")

@app.route('/bitcoin', methods=['GET'])
def bitcoin():
  if(request.method == 'GET'):
    data = {
      "price": 100,
      "date": "2024-06-01",
    }
    return jsonify(data)

@app.route('/healthz', methods=['GET'])
def healthcheck():
    if(request.method == 'GET'):
      return Response(status=200)


app.run()
