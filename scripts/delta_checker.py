import pandas as pd
import numpy as np
import json
from xgboost import XGBRegressor
from tensorflow import keras
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/model_ready_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

stations = ["hyderabad", "bangalore", "lucknow", "colombo"]
horizons = ["1h", "3h", "6h"]

lag_vars = ["xray_flux", "solar_wind_speed", "imf_bz", "kp_index", "dst_index"]
lag_windows = ["1h", "3h", "6h", "12h", "24h"]
feature_cols = [f"{v}_lag_{w}" for v in lag_vars for w in lag_windows]
feature_cols += ["hour_of_day", "day_of_year"]

results = []

for station in stations:
    for horizon in horizons:
        model_key = f"{station}_{horizon}"
        target_col = f"tec_{station}_target_{horizon}"

        sub = df.dropna(subset=feature_cols + [target_col]).tail(50)  # most recent 50 rows for demo
        X = sub[feature_cols]
        y_actual = sub[target_col].values

        # Load XGBoost
        xgb_model = XGBRegressor()
        xgb_model.load_model(f"data/xgb_{model_key}.json")
        xgb_preds = xgb_model.predict(X)

        # Load LSTM (needs scaling + reshaping, same as training)
        lstm_model = keras.models.load_model(f"data/lstm_{model_key}.keras")
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)  # NOTE: ideally reuse the training scaler, see caveat below
        X_lstm = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))
        lstm_preds = lstm_model.predict(X_lstm, verbose=0).flatten()

        # Delta between the two models = disagreement
        delta = np.abs(xgb_preds - lstm_preds)
        avg_delta = delta.mean()

        # Confidence: high agreement (low delta) = high confidence
        max_reasonable_delta = 5.0  # TECU, tune based on your data's scale
        confidence = max(0, 1 - (avg_delta / max_reasonable_delta))

        result = {
            "station": station,
            "horizon": horizon,
            "xgb_pred_latest": float(xgb_preds[-1]),
            "lstm_pred_latest": float(lstm_preds[-1]),
            "avg_model_delta": float(avg_delta),
            "confidence": round(float(confidence), 3)
        }
        results.append(result)
        print(f"{model_key:20s} | XGB: {xgb_preds[-1]:7.3f} | LSTM: {lstm_preds[-1]:7.3f} | Delta: {avg_delta:6.3f} | Confidence: {confidence:.2f}")

with open("data/delta_checker_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved to data/delta_checker_results.json")