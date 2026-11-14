
import requests
import pandas as pd
from pathlib import Path

url = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    "parameters": "GWETTOP,GWETROOT,GWETPROF",
    "community": "AG",
    "longitude": 73.58,
    "latitude": 32.43,
    "start": "20240101",
    "end": "20241231",
    "format": "JSON"
}

print("Fetching NASA soil-wetness data...")

response = requests.get(url, params=params, timeout=60)
print("Status code:", response.status_code)

if response.status_code != 200:
    print("NASA error details:")
    print(response.text)
    exit()

result = response.json()



observations = result["properties"]["parameter"]

df = pd.DataFrame(observations)
df.index.name = "date"
df = df.reset_index()

df["date"] = pd.to_datetime(
    df["date"], format="%Y%m%d"
)

df = df.replace(-999, float("nan"))

output = Path("data/processed")
output.mkdir(parents=True, exist_ok=True)

file_path = output / "nasa_soil_wetness_2024.csv"

df.to_csv(file_path, index=False)

print("\nSoil-wetness data retrieved!")
print(df.head())
print("\nDataset shape:", df.shape)
print("\nMissing values:")
print(df.isna().sum())
print("\nSaved:", file_path)
