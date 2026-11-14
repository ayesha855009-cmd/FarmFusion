
import pandas as pd

# Load NASA dataset
df = pd.read_csv("data/processed/nasa_power_phalia_2024.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

print("NASA DATA ANALYSIS")
print("------------------")

# Basic dataset information
print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

# Statistical analysis
print("\nStatistical summary:")
print(df.describe())

# Average temperature
print("\nAverage temperature:")
print(df["T2M"].mean())

# Total annual rainfall
print("\nTotal rainfall:")
print(df["PRECTOTCORR"].sum())

# Average humidity
print("\nAverage humidity:")
print(df["RH2M"].mean())

# Average solar radiation
print("\nAverage solar radiation:")
print(df["ALLSKY_SFC_SW_DWN"].mean())
