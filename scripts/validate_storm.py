import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

df = pd.read_csv("data/model_ready_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# March-April 2023 storm window
storm_window = df[(df["timestamp"] >= "2023-03-20") & (df["timestamp"] <= "2023-04-30")]
print(f"Storm window rows: {len(storm_window)}")

lag_vars = ["xray_flux", "solar_wind_speed", "imf_bz", "kp_index", "dst_index"]
lag_windows = ["1h", "3h", "6h", "12h", "24h"]
feature_cols = [f"{v}_lag_{w}" for v in lag_vars for w in lag_windows]
feature_cols += ["hour_of_day", "day_of_year"]

stations = ["hyderabad", "bangalore", "lucknow", "colombo"]

for station in stations:
    target_col = f"tec_{station}_target_1h"
    sub = storm_window.dropna(subset=feature_cols + [target_col])
    if len(sub) == 0:
        print(f"{station}: no data in this window")
        continue

    model = XGBRegressor()
    model.load_model(f"data/xgb_{station}_1h.json")
    preds = model.predict(sub[feature_cols])

    mae = mean_absolute_error(sub[target_col], preds)
    rmse = np.sqrt(mean_squared_error(sub[target_col], preds))
    print(f"{station:12s} | Storm-window MAE: {mae:.3f} | RMSE: {rmse:.3f} | n={len(sub)}")