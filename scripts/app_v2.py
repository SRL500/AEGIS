from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def load_forecasts():
    with open("data/final_forecast_output.json") as f:
        return json.load(f)

@app.route("/forecast/<station>")
def forecast_station(station):
    data = load_forecasts()
    station_forecasts = [d for d in data if d["station"] == station.lower()]
    if not station_forecasts:
        return jsonify({"error": "station not found"}), 404
    return jsonify(station_forecasts)

@app.route("/forecast/all")
def forecast_all():
    data = load_forecasts()
    return jsonify(data)

@app.route("/telemetry/live")
def telemetry_live():
    # Placeholder - in a full production version this would pull live NOAA/GFZ data
    return jsonify({"status": "live telemetry endpoint - integrate live NOAA/GFZ pull here"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)