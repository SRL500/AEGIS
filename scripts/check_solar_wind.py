import pandas as pd

mag_df = pd.read_csv("data/solar_wind_mag_latest.csv")
speed_df = pd.read_csv("data/solar_wind_speed_latest.csv")

print("Latest magnetic field reading:")
print(mag_df)
print()
print("Latest solar wind speed reading:")
print(speed_df)