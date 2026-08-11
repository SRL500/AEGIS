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
target_col = "target_1h"

X = df[feature_cols]
y = df[target_col]

# --- Time-based split: train on first 80%, test on most recent 20% ---
split_idx = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

print(f"Train rows: {len(X_train)}, Test rows: {len(X_test)}")

model = XGBRegressor(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    random_state=42
)
model.fit(X_train, y_train)

preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)
rmse = np.sqrt(mean_squared_error(y_test, preds))

print(f"\n=== Model Performance (+1h horizon) ===")
print(f"MAE:  {mae:.3f} TECU")
print(f"RMSE: {rmse:.3f} TECU")

print("\n--- Sample predictions vs actual ---")
comparison = pd.DataFrame({
    "actual": y_test.values[:10],
    "predicted": preds[:10]
})
print(comparison)

# Feature importance
print("\n--- Feature importance ---")
importance = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
print(importance)

model.save_model("data/xgb_model_1h.json")
print("\nModel saved to data/xgb_model_1h.json")