import requests
import pandas as pd

url = "https://kp.gfz.de/app/json/"
params = {
    "start": "2026-01-15T00:00:00Z",
    "end": "2026-01-22T00:00:00Z",
    "index": "Kp",
    "status": "def"
}

response = requests.get(url, params=params, timeout=30)
data = response.json()

print("Status:", response.status_code)
print("Keys:", data.keys())

df = pd.DataFrame({
    "datetime": data["datetime"],
    "Kp": data["Kp"]
})
df["datetime"] = pd.to_datetime(df["datetime"])

print(df)
df.to_csv("data/Kp_week.csv", index=False)
print(f"\nSaved {len(df)} rows to data/Kp_week.csv")