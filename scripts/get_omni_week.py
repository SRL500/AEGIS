import requests
import pandas as pd

year = 2026
url = f"https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/omni2_{year}.dat"

print("Downloading OMNI2 hourly file for", year, "...")
r = requests.get(url, timeout=60)
print("Status:", r.status_code)

lines = r.text.strip().split("\n")
print(f"Total lines in file: {len(lines)}")

rows = []
for line in lines:
    parts = line.split()
    yr = int(parts[0])
    day = int(parts[1])
    hour = int(parts[2])
    bz_gsm = float(parts[16])      # word 17
    speed = float(parts[24])       # word 25
    kp10 = int(parts[38])          # word 39

    # Only keep day-of-year 15-21 (our storm week)
    if 15 <= day <= 21:
        rows.append({
            "year": yr, "day": day, "hour": hour,
            "Bz_GSM": bz_gsm, "speed_kms": speed, "Kp": kp10 / 10.0
        })

df = pd.DataFrame(rows)

# Convert year/day/hour into a real datetime
df["datetime"] = pd.to_datetime(df["year"].astype(str), format="%Y") + \
                  pd.to_timedelta(df["day"] - 1, unit="D") + \
                  pd.to_timedelta(df["hour"], unit="h")

# Replace fill values with NaN (999.9 = missing Bz, 9999 = missing speed)
df.loc[df["Bz_GSM"] > 900, "Bz_GSM"] = None
df.loc[df["speed_kms"] > 9000, "speed_kms"] = None

df = df[["datetime", "Bz_GSM", "speed_kms", "Kp"]]

print(df.head(10))
print(f"\nTotal rows: {len(df)}")

df.to_csv("data/OMNI_week.csv", index=False)
print("Saved to data/OMNI_week.csv")