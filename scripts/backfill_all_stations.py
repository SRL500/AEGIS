import requests
import georinex as gr
import pandas as pd
from pathlib import Path

stations = ["IISC00IND", "IITK00IND", "DRDN00IND"]
days = range(15, 22)  # Jan 15-21, 2026
year = 2026

f1 = 1575.42e6
f2 = 1227.60e6
K = 40.3
factor = 1 / (K * (1/f1**2 - 1/f2**2)) * 1e-16

session = requests.Session()
all_data = []

for station in stations:
    station_short = station[:4]
    for doy in days:
        doy_str = f"{doy:03d}"
        filename = f"{station}_R_{year}{doy_str}0000_01D_30S_MO.crx.gz"
        url = f"https://cddis.nasa.gov/archive/gnss/data/daily/{year}/{doy_str}/26d/{filename}"
        local_path = Path(f"data/{filename}")

        print(f"\n=== {station_short} Day {doy_str} ===")

        if not local_path.exists():
            print(f"Downloading {filename}...")
            try:
                r = session.get(url, allow_redirects=True, timeout=30)
                if r.status_code == 200 and len(r.content) > 100000:
                    local_path.write_bytes(r.content)
                    print(f"Saved ({len(r.content)} bytes)")
                else:
                    print(f"FAILED - status {r.status_code}, size {len(r.content)} - skipping")
                    continue
            except requests.exceptions.Timeout:
                print(f"TIMEOUT on {station_short} day {doy_str} - skipping")
                continue
            except requests.exceptions.RequestException as e:
                print(f"REQUEST ERROR: {e} - skipping")
                continue
        else:
            print("Already downloaded, skipping fetch")

        try:
            obs = gr.load(str(local_path), use="G")
            stec = (obs["C2W"] - obs["C1C"]) * factor
            station_tec = stec.mean(dim="sv", skipna=True)
            df = station_tec.to_dataframe(name="TEC").reset_index()
            df = df.dropna()
            df["station"] = station_short
            all_data.append(df)
            print(f"Parsed {len(df)} TEC rows")
        except Exception as e:
            print(f"PARSE FAILED: {e}")
            continue

if all_data:
    full_df = pd.concat(all_data, ignore_index=True)
    full_df = full_df.sort_values(["station", "time"])
    full_df.to_csv("data/AllStations_TEC_week.csv", index=False)
    print(f"\n=== DONE: {len(full_df)} total rows saved to data/AllStations_TEC_week.csv ===")
else:
    print("\nNo data collected")