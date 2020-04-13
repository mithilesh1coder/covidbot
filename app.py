# flask_ngrok_example.py
from flask import Flask, request, make_response, jsonify
from flask_ngrok import run_with_ngrok
import requests

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run


@app.route("/", methods=["GET"])
def home():
    return "Welcome to covid Bot"


@app.route("/webhook", methods=["POST"])
def webhook():
    if request.get_json().get("queryResult").get("action") != "covidIntent":
        return {}

    val = request.json
    query_city = val["queryResult"]["parameters"]["location"]["admin-area"]
    data = requests.get(
        "https://api.covid19india.org/v2/state_district_wise.json"
    ).json()

    sum = 0

    for i in range(len(data)):
        if data[i]["state"].lower() == query_city.lower():
            for j in range(len(data[i]["districtData"])):

                sum = sum + int(data[i]["districtData"][j]["confirmed"])

    print(sum)
    final_res = {"fulfillmentText": "Total cases in " + query_city + " is " + str(sum)}
    return make_response(jsonify(final_res))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
