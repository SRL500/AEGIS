import json

with open("data/delta_checker_results.json") as f:
    results = json.load(f)

def classify_risk(pred, confidence):
    magnitude = abs(pred)
    if magnitude > 8 and confidence > 0.5:
        return "Red"
    elif magnitude > 3:
        return "Yellow"
    else:
        return "Green"

def generate_action(station, risk, horizon):
    if risk == "Red":
        return f"{station.title()} region: RED risk in {horizon}. Recommend conventional ILS backup readiness for approach/landing operations."
    elif risk == "Yellow":
        return f"{station.title()} region: YELLOW risk in {horizon}. Monitor GAGAN augmentation status; degraded accuracy possible during approach."
    else:
        return f"{station.title()} region: GREEN. Nominal conditions expected in {horizon}."

final_output = []
for r in results:
    risk = classify_risk(r["xgb_pred_latest"], r["confidence"])
    action = generate_action(r["station"], risk, r["horizon"])
    r["risk"] = risk
    r["action"] = action
    final_output.append(r)
    print(f"{r['station']:12s} +{r['horizon']:3s} | Risk: {risk:6s} | {action}")

with open("data/final_forecast_output.json", "w") as f:
    json.dump(final_output, f, indent=2)

print("\nSaved to data/final_forecast_output.json")