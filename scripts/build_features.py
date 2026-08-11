import pandas as pd
import numpy as np

df = pd.read_csv("data/training_dataset_v1.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

# Work per station separately, since lag features shouldn't cross station boundaries
all_features = []

for station, group in df.groupby("station"):
    group = group.sort_values("datetime").reset_index(drop=True)

    # --- Target: TEC "disturbance" = deviation from a rolling baseline ---
    # 6-hour rolling median as a simple "quiet baseline"
    group["TEC_baseline"] = group["TEC"].rolling(window=6, min_periods=3).median()
    group["TEC_disturbance"] = group["TEC"] - group["TEC_baseline"]

    # --- Lag features (t-1h, t-2h, t-3h) ---
    for lag in [1, 2, 3]:
        group[f"TEC_lag{lag}"] = group["TEC"].shift(lag)
        group[f"Bz_lag{lag}"] = group["Bz_GSM"].shift(lag)
        group[f"Kp_lag{lag}"] = group["Kp"].shift(lag)
        group[f"speed_lag{lag}"] = group["speed_kms"].shift(lag)

    # --- Prediction targets: disturbance at t+1h, t+3h, t+6h ---
    group["target_1h"] = group["TEC_disturbance"].shift(-1)
    group["target_3h"] = group["TEC_disturbance"].shift(-3)
    group["target_6h"] = group["TEC_disturbance"].shift(-6)

    all_features.append(group)

features_df = pd.concat(all_features, ignore_index=True)

# Drop rows with missing lag/target data (start/end of each station's series)
features_df = features_df.dropna(subset=[
    "TEC_lag1", "TEC_lag2", "TEC_lag3",
    "Bz_lag1", "Kp_lag1", "target_1h"
])

print(features_df.head(10))
print(f"\nTotal usable rows: {len(features_df)}")
print(f"Columns: {list(features_df.columns)}")

features_df.to_csv("data/features_v1.csv", index=False)
print("\nSaved to data/features_v1.csv")