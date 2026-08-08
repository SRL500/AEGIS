import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/kp_index.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

plt.plot(df["datetime"], df["Kp"])
plt.xlabel("Date")
plt.ylabel("Kp index")
plt.title("Kp Index Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()