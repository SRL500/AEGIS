import requests
import pandas as pd

url = "https://kp.gfz.de/app/json/"
params = {
    "start": "2026-06-01T00:00:00Z",
    "end": "2026-07-01T00:00:00Z",
    "index": "Kp",
    "status": "def"
}

response = requests.get(url, params=params)
data = response.json()

print(data.keys())
print(data["datetime"][:5])
print(data["Kp"][:5])

df = pd.DataFrame({
    "datetime": data["datetime"],
    "Kp": data["Kp"]
})
df["datetime"] = pd.to_datetime(df["datetime"])
df.to_csv("data/kp_index.csv", index=False)
print(f"Saved {len(df)} rows to data/kp_index.csv")