import requests
import pandas as pd

# NOTE: NOAA changed their endpoints in 2026 — these "summary" URLs
# return only the SINGLE latest reading, not a time series.
# Good enough to prove the pipeline works; we'll need a different
# source for historical backfill later.

mag_url = "https://services.swpc.noaa.gov/products/summary/solar-wind-mag-field.json"
speed_url = "https://services.swpc.noaa.gov/products/summary/solar-wind-speed.json"

mag_response = requests.get(mag_url)
speed_response = requests.get(speed_url)

print("Mag status:", mag_response.status_code)
print("Speed status:", speed_response.status_code)

mag_data = mag_response.json()   # list containing one dict
speed_data = speed_response.json()

print("Mag data:", mag_data)
print("Speed data:", speed_data)

mag_df = pd.DataFrame(mag_data)
speed_df = pd.DataFrame(speed_data)

mag_df.to_csv("data/solar_wind_mag_latest.csv", index=False)
speed_df.to_csv("data/solar_wind_speed_latest.csv", index=False)
print("Saved latest readings to data/")