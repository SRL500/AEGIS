import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/IISC_TEC_week.csv")
df["time"] = pd.to_datetime(df["time"])

plt.figure(figsize=(14, 5))
plt.plot(df["time"], df["TEC"])
plt.axvline(pd.Timestamp("2026-01-19 19:38:00"), color="red", linestyle="--", label="G4 storm onset")
plt.xlabel("Date")
plt.ylabel("TEC (TECU)")
plt.title("IISC Station TEC — Jan 15-21, 2026 (G4 Storm Week)")
plt.legend()
plt.tight_layout()
plt.show()