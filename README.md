# AEGIS — Ionospheric Disturbance Prediction System

ML-based early-warning system forecasting ionospheric disturbances affecting GPS/NavIC accuracy over India.

## Pipeline
1. Data: NOAA/OMNI solar wind, GFZ Kp index, NASA CDDIS RINEX (TEC via georinex)
2. Features: lag-based (1-3h), TEC disturbance target vs rolling baseline
3. Model: XGBoost, multi-horizon (+1h/+3h/+6h)
4. Risk: Green/Yellow/Red classification
5. Serving: Flask API + HTML/Chart.js dashboard

## Setup
See `scripts/` for the full pipeline. Run `python scripts/app.py` then open `scripts/dashboard.html`.

## Stations
IISC (Bangalore), IITK (Kanpur), DRDN (Dehradun)

## Data period
Jan 15-21, 2026, including the Jan 19 G4 geomagnetic storm.