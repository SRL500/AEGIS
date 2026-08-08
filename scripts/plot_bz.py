import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/solar_wind_mag.csv")
df["time_tag"] = pd.to_datetime(df["time_tag"])
df["bz_gsm"] = pd.to_numeric(df["bz_gsm"], errors="coerce")

plt.plot(df["time_tag"], df["bz_gsm"])
plt.xlabel("Time")
plt.ylabel("Bz (nT)")
plt.title("IMF Bz Over Last 7 Days")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()