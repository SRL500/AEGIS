from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from xgboost import XGBRegressor

app = Flask(__name__)
CORS(app)

model = XGBRegressor()
model.load_model("data/xgb_model_1h.json")

feature_cols = [
    "TEC_lag1", "TEC_lag2", "TEC_lag3",
    "Bz_lag1", "Bz_lag2", "Bz_lag3",
    "Kp_lag1", "Kp_lag2", "Kp_lag3",
    "speed_lag1", "speed_lag2", "speed_lag3",
]

@app.route("/predict/<station>")
def predict(station):
    df = pd.read_csv("data/features_v1.csv")
    station_data = df[df["station"] == station].sort_values("datetime")
    if station_data.empty:
        return jsonify({"error": "station not found"}), 404

    latest = station_data.iloc[-1]
    X = latest[feature_cols].values.reshape(1, -1)
    pred = model.predict(X)[0]

    risk = "Green"
    if abs(pred) > 5:
        risk = "Red"
    elif abs(pred) > 2:
        risk = "Yellow"

    return jsonify({
        "station": station,
        "predicted_disturbance_1h": float(pred),
        "risk": risk
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)