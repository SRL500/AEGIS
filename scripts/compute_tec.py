import georinex as gr
import numpy as np
import pandas as pd

print("Loading GPS data...")
obs = gr.load(
    "data/IISC_2026_001.crx.gz",
    use="G",
    tlim=["2026-01-01T00:00:00", "2026-01-01T01:00:00"]
)

# Frequencies (Hz)
f1 = 1575.42e6
f2 = 1227.60e6

# Constant for the STEC formula
K = 40.3
factor = 1 / (K * (1/f1**2 - 1/f2**2)) * 1e-16

# Compute STEC per satellite per epoch
c1 = obs["C1C"]
c2 = obs["C2W"]
stec = (c2 - c1) * factor

print("\n--- STEC sample (TECU) ---")
print(stec)

# Convert to a clean DataFrame: rows = time, columns = satellites
df = stec.to_dataframe(name="STEC").reset_index()
df = df.dropna()

print(f"\nComputed {len(df)} STEC values")
print(df.head(10))

df.to_csv("data/IISC_STEC_sample.csv", index=False)
print("\nSaved to data/IISC_STEC_sample.csv")