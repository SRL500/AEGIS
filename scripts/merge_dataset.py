import pandas as pd

# --- Load TEC data (30-second resolution, 3 stations) ---
tec = pd.read_csv("data/AllStations_TEC_week.csv")
tec["time"] = pd.to_datetime(tec["time"])

# Round down to the hour, then average TEC per station per hour
tec["datetime"] = tec["time"].dt.floor("h")
tec_hourly = tec.groupby(["station", "datetime"])["TEC"].mean().reset_index()

print("TEC hourly sample:")
print(tec_hourly.head())
print(f"TEC hourly rows: {len(tec_hourly)}")

# --- Load OMNI data (already hourly: Bz, speed, Kp) ---
omni = pd.read_csv("data/OMNI_week.csv")
omni["datetime"] = pd.to_datetime(omni["datetime"])

print("\nOMNI sample:")
print(omni.head())
print(f"OMNI rows: {len(omni)}")

# --- Merge: each station's hourly TEC gets matched with that hour's space weather ---
merged = tec_hourly.merge(omni, on="datetime", how="inner")

print("\n=== MERGED DATASET ===")
print(merged.head(10))
print(f"\nTotal merged rows: {len(merged)}")
print(f"Stations present: {merged['station'].unique()}")
print(f"Date range: {merged['datetime'].min()} to {merged['datetime'].max()}")

# Check for missing values
print("\nMissing values per column:")
print(merged.isnull().sum())

merged.to_csv("data/training_dataset_v1.csv", index=False)
print("\nSaved to data/training_dataset_v1.csv")