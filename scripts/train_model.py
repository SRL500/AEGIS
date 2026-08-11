import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

df = pd.read_csv("data/features_v1.csv")
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

feature_cols = [
    "TEC_lag1", "TEC_lag2", "TEC_lag3",
    "Bz_lag1", "Bz_lag2", "Bz_lag3",
    "Kp_lag1", "Kp_lag2", "Kp_lag3",
    "speed_lag1", "speed_lag2", "speed_lag3",
]

horizons = {"1h": "target_1h", "3h": "target_3h", "6h": "target_6h"}
models = {}

for label, target_col in horizons.items():
    print(f"\n{'='*40}\nTraining model for +{label} horizon\n{'='*40}")

    sub = df.dropna(subset=[target_col])
    X = sub[feature_cols]
    y = sub[target_col]

    split_idx = int(len(sub) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    model = XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    print(f"MAE: {mae:.3f} TECU | RMSE: {rmse:.3f} TECU | Train/Test: {len(X_train)}/{len(X_test)}")

    model.save_model(f"data/xgb_model_{label}.json")
    models[label] = model

print("\nAll horizon models trained and saved.")