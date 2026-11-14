
import pandas as pd
from pathlib import Path

folder = Path("data/processed")

files = list(folder.glob("*_nasa_data_*.csv"))

if not files:
    raise FileNotFoundError("No NASA dataset found.")

latest_file = max(files, key=lambda f: f.stat().st_mtime)

df = pd.read_csv(latest_file)

print("Checking:", latest_file.name)

print("\nAvailable columns:")
print(df.columns.tolist())

required_columns = [
    "date", "T2M", "T2M_MAX", "T2M_MIN",
    "PRECTOTCORR", "RH2M", "WS10M",
    "ALLSKY_SFC_SW_DWN",
    "GWETTOP", "GWETROOT", "GWETPROF"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    print("\nMissing columns:", missing_columns)
    print("Please check the NASA downloader.")
else:
    print("\nAll required columns found!")

    print("\nDataset shape:", df.shape)

    print("\nMissing values:")
    print(df[required_columns].isnull().sum())

    print("\nFirst five rows:")
    print(df[required_columns].head())
