
import requests
import pandas as pd
from pathlib import Path

url = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    "parameters": "T2M,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN",
    "community": "AG",
    "longitude": 73.58,
    "latitude": 32.43,
    "start": "20240101",
    "end": "20241231",
    "format": "JSON"
}

print("Fetching NASA data...")

response = requests.get(url, params=params, timeout=60)
response.raise_for_status()

data = response.json()

# Extract observations
observations = data["properties"]["parameter"]

# Convert to DataFrame
df = pd.DataFrame(observations)

# Convert date index into a column
df.index.name = "date"
df = df.reset_index()

# Convert dates
df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")

# Replace NASA missing-value indicators
df = df.replace(-999, pd.NA)

# Create output folder
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

# Save CSV
file_path = output_folder / "nasa_power_phalia_2024.csv"
df.to_csv(file_path, index=False)

print("\nNASA data saved successfully!")
print("\nFirst five records:")
print(df.head())

print("\nDataset shape:", df.shape)
print("\nMissing values:")
print(df.isna().sum())

print("\nSaved at:", file_path)
