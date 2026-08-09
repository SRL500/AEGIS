import requests
import georinex as gr
import pandas as pd
from pathlib import Path

# Jan 15-21, 2026 = day-of-year 015-021
# This brackets the Jan 19 G4 geomagnetic storm
days = range(15, 22)
year = 2026

# GPS frequencies
f1 = 1575.42e6
f2 = 1227.60e6

# TEC conversion constant
K = 40.3
factor = 1 / (K * (1 / f1**2 - 1 / f2**2)) * 1e-16

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(parents=True, exist_ok=True)

# HTTP session
session = requests.Session()

all_data = []

for doy in days:
    doy_str = f"{doy:03d}"

    filename = (
        f"IISC00IND_R_{year}{doy_str}0000_01D_30S_MO.crx.gz"
    )

    url = (
        f"https://cddis.nasa.gov/archive/gnss/data/daily/"
        f"{year}/{doy_str}/26d/{filename}"
    )

    local_path = data_dir / filename

    print(f"\n=== Day {doy_str} ===")

    # ---------------------------------------------------------
    # DOWNLOAD FILE IF IT DOES NOT ALREADY EXIST
    # ---------------------------------------------------------
    if not local_path.exists():
        print(f"Downloading {filename}...")

        try:
            r = session.get(
                url,
                allow_redirects=True,
                timeout=30
            )

            if r.status_code == 200 and len(r.content) > 100000:
                local_path.write_bytes(r.content)

                print(
                    f"Saved ({len(r.content)} bytes)"
                )

            else:
                print(
                    f"FAILED - status {r.status_code}, "
                    f"size {len(r.content)} - skipping this day"
                )
                continue

        except requests.exceptions.Timeout:
            print(
                f"TIMEOUT on day {doy_str} - skipping"
            )
            continue

        except requests.exceptions.RequestException as e:
            print(
                f"REQUEST ERROR on day {doy_str}: {e} - skipping"
            )
            continue

    else:
        print("Already downloaded, skipping fetch")

    # ---------------------------------------------------------
    # PARSE RINEX OBSERVATION FILE
    # ---------------------------------------------------------
    try:
        print(f"Parsing {filename}...")

        obs = gr.load(
            str(local_path),
            use="G"
        )

        # Calculate Slant TEC
        stec = (
            obs["C2W"] - obs["C1C"]
        ) * factor

        # Average TEC across satellites
        station_tec = stec.mean(
            dim="sv",
            skipna=True
        )

        # Convert to DataFrame
        df = station_tec.to_dataframe(
            name="TEC"
        ).reset_index()

        # Remove missing values
        df = df.dropna()

        # Add station identifier
        df["station"] = "IISC"

        # Store the day's data
        all_data.append(df)

        print(
            f"Parsed {len(df)} TEC rows "
            f"for day {doy_str}"
        )

    except Exception as e:
        print(
            f"PARSE FAILED for day {doy_str}: {e}"
        )
        continue


# -------------------------------------------------------------
# COMBINE ALL DAYS
# -------------------------------------------------------------
if all_data:

    full_df = pd.concat(
        all_data,
        ignore_index=True
    )

    # Sort chronologically
    full_df = full_df.sort_values(
        "time"
    )

    # Save final CSV
    output_file = data_dir / "IISC_TEC_week.csv"

    full_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\n=== DONE: {len(full_df)} total rows "
        f"saved to {output_file} ==="
    )

else:

    print(
        "\nNo data collected - "
        "check errors above"
    )