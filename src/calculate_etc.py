
import pandas as pd
from datetime import datetime
from pathlib import Path

# Load NASA data
file_path = Path(
    "data/processed/phalia_nasa_data_20240101_20241231_with_eto.csv"
)

df = pd.read_csv(file_path)
df["date"] = pd.to_datetime(df["date"])

# Wheat test planting date
planting_date = datetime(2023, 11, 23)

# Reference growth-stage durations (days)
initial_days = 15
development_days = 30
mid_days = 65
late_days = 40

# Select date for testing
date_input = input("Enter date (YYYY-MM-DD): ")
test_date = pd.to_datetime(date_input)

result = df[df["date"] == test_date]

if result.empty:
    print("Date not found in NASA dataset.")
    raise SystemExit

# Detect growth stage automatically
days_after_sowing = (test_date - planting_date).days

if days_after_sowing < 0:
    print("Date is before planting.")
    raise SystemExit

if days_after_sowing < initial_days:
    stage = "Initial"
    kc = 0.30

elif days_after_sowing < initial_days + development_days:
    stage = "Crop development"
    progress = (
        days_after_sowing - initial_days
    ) / development_days
    kc = 0.30 + progress * (1.15 - 0.30)

elif days_after_sowing < initial_days + development_days + mid_days:
    stage = "Mid-season"
    kc = 1.15

elif days_after_sowing < initial_days + development_days + mid_days + late_days:
    stage = "Late-season"
    progress = (
        days_after_sowing - initial_days - development_days - mid_days
    ) / late_days
    kc = 1.15 + progress * (0.25 - 1.15)

else:
    print("Growing season completed.")
    raise SystemExit

# Calculate crop evapotranspiration
et0 = result.iloc[0]["ET0_mm_day"]
etc = et0 * kc

print("\nFARMFUSION - CROP WATER ANALYSIS")
print("Crop: Wheat")
print("Date:", test_date.date())
print("Days after sowing:", days_after_sowing)
print("Growth stage:", stage)
print("ET0:", round(et0, 2), "mm/day")
print("Kc:", round(kc, 3))
print("Estimated ETc:", round(etc, 2), "mm/day")
