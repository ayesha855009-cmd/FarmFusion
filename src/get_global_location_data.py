
import requests
import pandas as pd

print("FARMFUSION - GLOBAL NASA DATA COLLECTOR")

# Ask the user for farm coordinates
latitude = float(input("Enter latitude: "))
longitude = float(input("Enter longitude: "))

# Validate coordinates
if not -90 <= latitude <= 90:
    raise ValueError("Latitude must be between -90 and 90.")

if not -180 <= longitude <= 180:
    raise ValueError("Longitude must be between -180 and 180.")

start_date = input("Start date (YYYYMMDD): ")
end_date = input("End date (YYYYMMDD): ")

url = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    "parameters": "T2M,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN",
    "community": "AG",
    "longitude": longitude,
    "latitude": latitude,
    "start": start_date,
    "end": end_date,
    "format": "JSON"
}

print("\nFetching NASA data...")

response = requests.get(url, params=params, timeout=60)

if response.status_code != 200:
    print("NASA API error:")
    print(response.text)
    raise SystemExit()

result = response.json()

observations = result["properties"]["parameter"]

df = pd.DataFrame(observations)

df.index.name = "date"
df = df.reset_index()

df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")

df["latitude"] = latitude
df["longitude"] = longitude

df = df.replace(-999, pd.NA)

df.to_csv(
    "data/processed/nasa_global_location_data.csv",
    index=False
)

print("\nNASA data retrieved successfully!")
print(df.head())
print("\nDataset shape:", df.shape)
print("\nSaved successfully!")
