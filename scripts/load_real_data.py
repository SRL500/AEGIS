import pandas as pd

df = pd.read_excel("data/model_ready_data.xlsx")

print("Shape:", df.shape)
print("\nDate range:", df["timestamp"].min(), "to", df["timestamp"].max())
print("\nColumns:")
print(list(df.columns))
print("\nMissing values per column (top 10):")
print(df.isnull().sum().sort_values(ascending=False).head(10))

df.to_csv("data/model_ready_data.csv", index=False)
print("\nSaved as CSV for faster loading later")