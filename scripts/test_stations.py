import requests

session = requests.Session()
year = 2026
doy = "015"

candidates = ["HYDE00IND", "IITK00IND", "DRDN00IND"]

for code in candidates:
    filename = f"{code}_R_{year}{doy}0000_01D_30S_MO.crx.gz"
    url = f"https://cddis.nasa.gov/archive/gnss/data/daily/{year}/{doy}/26d/{filename}"
    r = session.head(url, allow_redirects=True, timeout=20)
    print(f"{code}: status {r.status_code}")