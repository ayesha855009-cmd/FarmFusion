
import pandas as pd
from pathlib import Path

rain_file = Path(
    "data/processed/phalia_nasa_data_20240101_20241231_with_eto.csv"
)

etc_file = Path(
    "data/processed/phalia_wheat_etc_2024.csv"
)

rain = pd.read_csv(rain_file)
etc = pd.read_csv(etc_file)

rain["date"] = pd.to_datetime(rain["date"])
etc["date"] = pd.to_datetime(etc["date"])

# Combine rainfall and crop water demand
df = pd.merge(
    rain[["date", "PRECTOTCORR"]],
    etc[["date", "growth_stage", "ETc_mm_day"]],
    on="date",
    how="inner"
)

# Keep only dates when wheat is actively growing
season = df.dropna(subset=["ETc_mm_day"]).copy()

# Preliminary daily climatic balance
season["rainfall_minus_etc"] = (
    season["PRECTOTCORR"] - season["ETc_mm_day"]
)

print("\nFARMFUSION - WHEAT SEASON WATER ANALYSIS")

print("\nGrowing-season days:", len(season))
print("Total rainfall:", round(season["PRECTOTCORR"].sum(), 2), "mm")
print("Total crop ETc:", round(season["ETc_mm_day"].sum(), 2), "mm")
print(
    "Rainfall minus ETc:",
    round(season["rainfall_minus_etc"].sum(), 2),
    "mm"
)

# Save daily analysis
output = Path(
    "data/processed/phalia_wheat_water_analysis_2024.csv"
)

season.to_csv(output, index=False)

print("\nSaved to:", output)
