import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import json

df = pd.read_csv("data/model_ready_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

stations = ["hyderabad", "bangalore", "lucknow", "colombo"]
horizons = ["1h", "3h", "6h"]

# Shared feature set: all lag features + temporal features
lag_vars = ["xray_flux", "solar_wind_speed", "imf_bz", "kp_index", "dst_index"]
lag_windows = ["1h", "3h", "6h", "12h", "24h"]
feature_cols = [f"{v}_lag_{w}" for v in lag_vars for w in lag_windows]
feature_cols += ["hour_of_day", "day_of_year"]

print(f"Using {len(feature_cols)} features")

results = {}

for station in stations:
    for horizon in horizons:
        target_col = f"tec_{station}_target_{horizon}"
        model_key = f"{station}_{horizon}"

        sub = df.dropna(subset=feature_cols + [target_col])
        X = sub[feature_cols]
        y = sub[target_col]

        split_idx = int(len(sub) * 0.85)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

        model = XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.05, random_state=42)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))

        print(f"{model_key:25s} | Train: {len(X_train):5d} | Test: {len(X_test):5d} | MAE: {mae:6.3f} | RMSE: {rmse:6.3f}")

        model.save_model(f"data/xgb_{model_key}.json")
        results[model_key] = {"mae": mae, "rmse": rmse, "train_rows": len(X_train), "test_rows": len(X_test)}

with open("data/xgb_results_summary.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nAll 12 models trained and saved.")