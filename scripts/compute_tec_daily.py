import georinex as gr
import numpy as np
import pandas as pd

print("Loading full day, GPS only...")
obs = gr.load("data/IISC_2026_001.crx.gz", use="G")

f1 = 1575.42e6
f2 = 1227.60e6
K = 40.3
factor = 1 / (K * (1/f1**2 - 1/f2**2)) * 1e-16

stec = (obs["C2W"] - obs["C1C"]) * factor

# Average across all visible satellites per epoch -> one TEC value per timestamp
station_tec = stec.mean(dim="sv", skipna=True)

df = station_tec.to_dataframe(name="TEC").reset_index()
df = df.dropna()
df["station"] = "IISC"

print(df.head(10))
print(f"\nTotal rows: {len(df)}")

df.to_csv("data/IISC_TEC_daily.csv", index=False)
print("Saved data/IISC_TEC_daily.csv")