import pandas as pd
import numpy as np

df = pd.read_csv("data/features_v1.csv")

# Simple percentile-based thresholds using target_1h magnitude
disturbance = df["target_1h"].abs()
yellow_threshold = disturbance.quantile(0.75)
red_threshold = disturbance.quantile(0.90)

print(f"Yellow threshold: {yellow_threshold:.2f} TECU")
print(f"Red threshold: {red_threshold:.2f} TECU")

def classify(value):
    v = abs(value)
    if v >= red_threshold:
        return "Red"
    elif v >= yellow_threshold:
        return "Yellow"
    else:
        return "Green"

df["risk_1h"] = df["target_1h"].apply(classify)
print(df["risk_1h"].value_counts())

df.to_csv("data/features_with_risk.csv", index=False)
print("Saved data/features_with_risk.csv")