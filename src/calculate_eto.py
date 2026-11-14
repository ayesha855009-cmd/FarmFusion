
import math
import requests
import pandas as pd
from pathlib import Path

print("FARMFUSION - REFERENCE EVAPOTRANSPIRATION")

# Find the latest global NASA dataset
folder = Path("data/processed")
files = [
    f for f in folder.glob("*_nasa_data_*.csv")
    if not f.stem.endswith("_with_eto")
]
if not files:
    raise FileNotFoundError("No NASA dataset found.")

file_path = max(files, key=lambda f: f.stat().st_mtime)
df = pd.read_csv(file_path)

# Check required variables
required = [
    "date", "T2M_MAX", "T2M_MIN",
    "T2MDEW", "WS10M", "ALLSKY_SFC_SW_DWN",
    "latitude", "longitude"
]

missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(
        f"Missing columns: {missing}. "
        "Update and rerun your NASA downloader."
    )

# Get coordinates
latitude = float(df["latitude"].iloc[0])
longitude = float(df["longitude"].iloc[0])

# Retrieve elevation from a global digital elevation model
elevation_url = "https://api.open-meteo.com/v1/elevation"

response = requests.get(
    elevation_url,
    params={
        "latitude": latitude,
        "longitude": longitude
    },
    timeout=30
)

response.raise_for_status()
elevation = float(response.json()["elevation"][0])

print(f"\nLocation: {df['location'].iloc[0]}")
print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")
print(f"Estimated elevation: {elevation} metres")

# FAO-56 calculations

def saturation_vapour_pressure(temp):
    return 0.6108 * math.exp(
        (17.27 * temp) / (temp + 237.3)
    )


def calculate_eto(row):

    tmax = row["T2M_MAX"]
    tmin = row["T2M_MIN"]
    tdew = row["T2MDEW"]
    ws10 = row["WS10M"]
    rs = row["ALLSKY_SFC_SW_DWN"]

    tmean = (tmax + tmin) / 2

    # Atmospheric vapour pressure
    es = (
        saturation_vapour_pressure(tmax)
        + saturation_vapour_pressure(tmin)
    ) / 2

    ea = saturation_vapour_pressure(tdew)

    # Slope of vapour pressure curve
    delta = (
        4098 * saturation_vapour_pressure(tmean)
        / (tmean + 237.3) ** 2
    )

    # Atmospheric pressure and psychrometric constant
    pressure = 101.3 * (
        (293 - 0.0065 * elevation) / 293
    ) ** 5.26

    gamma = 0.000665 * pressure

    # Convert wind speed from 10m to 2m
    u2 = ws10 * 4.87 / math.log(67.8 * 10 - 5.42)

    # Solar geometry
    day = row["date"].day_of_year
    lat_rad = math.radians(latitude)

    dr = 1 + 0.033 * math.cos(2 * math.pi * day / 365)

    solar_declination = 0.409 * math.sin(
        2 * math.pi * day / 365 - 1.39
    )

    sunset_angle = math.acos(
        max(-1, min(
            1,
            -math.tan(lat_rad) * math.tan(solar_declination)
        ))
    )

    ra = (
        24 * 60 / math.pi
        * 0.0820
        * dr
        * (
            sunset_angle * math.sin(lat_rad)
            * math.sin(solar_declination)
            + math.cos(lat_rad)
            * math.cos(solar_declination)
            * math.sin(sunset_angle)
        )
    )

    # Clear-sky radiation
    rso = (0.75 + 0.00002 * elevation) * ra

    if rso <= 0:
        return float("nan")

    # Net radiation
    rns = 0.77 * rs

    cloud_factor = min(
    1.0,
    max(0.05, 1.35 * (rs / rso) - 0.35)
)

    rnl = (
        4.903e-9
        * (
            (tmax + 273.16) ** 4
            + (tmin + 273.16) ** 4
        ) / 2
        * (0.34 - 0.14 * math.sqrt(max(ea, 0)))
        * cloud_factor
    )

    rn = rns - rnl

    # Daily soil heat flux assumed to be zero
    g = 0

    # FAO-56 Penman-Monteith equation
    eto = (
        0.408 * delta * (rn - g)
        + gamma * (900 / (tmean + 273))
        * u2 * (es - ea)
    ) / (
        delta + gamma * (1 + 0.34 * u2)
    )

    return eto


# Convert required columns to numeric
numeric_columns = [
    "T2M_MAX", "T2M_MIN", "T2MDEW",
    "WS10M", "ALLSKY_SFC_SW_DWN"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["date"] = pd.to_datetime(df["date"])

df = df.dropna(subset=required)

# Calculate daily reference evapotranspiration
df["ET0_mm_day"] = df.apply(calculate_eto, axis=1)

# Save results
output_file = file_path.with_name(
    file_path.stem + "_with_eto.csv"
)

df.to_csv(output_file, index=False)

print("\nET0 calculation completed!")
print(df[["date", "ET0_mm_day"]].head())

print("\nAverage daily ET0:")
print(round(df["ET0_mm_day"].mean(), 2), "mm/day")

print("\nSaved to:", output_file)
