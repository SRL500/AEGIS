import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/Kp_week.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

plt.figure(figsize=(14, 5))
plt.plot(df["datetime"], df["Kp"], marker="o")
plt.axvline(pd.Timestamp("2026-01-19 19:38:00"), color="red", linestyle="--", label="G4 storm onset")
plt.axhline(7, color="orange", linestyle=":", label="G4 threshold (Kp=7-8)")
plt.xlabel("Date")
plt.ylabel("Kp index")
plt.title("Kp Index — Jan 15-21, 2026")
plt.legend()
plt.tight_layout()
plt.show()