import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/OMNI_week.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

axes[0].plot(df["datetime"], df["Bz_GSM"])
axes[0].axvline(pd.Timestamp("2026-01-19 19:38:00"), color="red", linestyle="--", label="G4 storm onset")
axes[0].set_ylabel("Bz GSM (nT)")
axes[0].legend()
axes[0].set_title("IMF Bz — Jan 15-21, 2026")

axes[1].plot(df["datetime"], df["Kp"], marker="o")
axes[1].axvline(pd.Timestamp("2026-01-19 19:38:00"), color="red", linestyle="--")
axes[1].set_ylabel("Kp index")
axes[1].set_xlabel("Date")

plt.tight_layout()
plt.show()