
import requests
import pandas as pd
import re
from pathlib import Path

print("FARMFUSION - GLOBAL ENVIRONMENTAL DATA")

# Get location details
location = input("Enter location name: ")

latitude = float(input("Enter latitude: "))
longitude = float(input("Enter longitude: "))

start_date = input("Start date (YYYYMMDD): ")
end_date = input("End date (YYYYMMDD): ")

# Validate coordinates
if not -90 <= latitude <= 90:
    raise ValueError("Invalid latitude")

if not -180 <= longitude <= 180:
    raise ValueError("Invalid longitude")

# NASA POWER API
url = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    
"parameters": (
    "T2M,T2M_MAX,T2M_MIN,T2MDEW,"
    "PRECTOTCORR,RH2M,WS10M,"
    "ALLSKY_SFC_SW_DWN,"
    "GWETTOP,GWETROOT,GWETPROF"
),

    "community": "AG",
    "longitude": longitude,
    "latitude": latitude,
   "start": int(start_date.replace("-", "")),
   "end": int(end_date.replace("-", "")),
    "format": "JSON"
}

print("\nFetching NASA environmental data...")

response = requests.get(url, params=params, timeout=60)

if response.status_code != 200:
    print("NASA API error:")
    print(response.text)
    raise SystemExit()

result = response.json()

observations = result["properties"]["parameter"]

# Convert NASA response into DataFrame
df = pd.DataFrame(observations)

df.index.name = "date"
df = df.reset_index()

df["date"] = pd.to_datetime(
    df["date"],
    format="%Y%m%d"
)

df["latitude"] = latitude
df["longitude"] = longitude
df["location"] = location

# Replace NASA missing-value codes
df = df.replace(-999, pd.NA)

# Create safe filename
safe_name = re.sub(
    r"[^a-zA-Z0-9_-]",
    "_",
    location.strip()
)

output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = (
    output_folder /
    f"{safe_name}_nasa_data_{start_date}_{end_date}.csv"
)

df.to_csv(output_file, index=False)

print("\nNASA data retrieved successfully!")
print(df.head())

print("\nDataset shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nSaved to:", output_file)
