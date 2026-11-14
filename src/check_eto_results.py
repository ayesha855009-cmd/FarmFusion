
import pandas as pd
from pathlib import Path

file = Path(
    "data/processed/phalia_complete_nasa_data_2023-11-23_2024-12-31_with_eto.csv"
)

df = pd.read_csv(file)
df["date"] = pd.to_datetime(df["date"])

print("ET0 DATA VALIDATION")

print("\nTotal records:", len(df))
print("Missing ET0 values:", df["ET0_mm_day"].isna().sum())
print("Minimum ET0:", df["ET0_mm_day"].min())
print("Maximum ET0:", df["ET0_mm_day"].max())
print("Average ET0:", df["ET0_mm_day"].mean())
print("Negative ET0 values:", (df["ET0_mm_day"] < 0).sum())

# Assumed wheat growing season
season = df[
    (df["date"] >= "2023-11-23") &
    (df["date"] <= "2024-04-20")
]

print("\nWHEAT SEASON ET0")
print("Records:", len(season))
print("Average:", season["ET0_mm_day"].mean())
print("Minimum:", season["ET0_mm_day"].min())
print("Maximum:", season["ET0_mm_day"].max())
