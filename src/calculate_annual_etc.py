
import pandas as pd
from pathlib import Path

# Load NASA data containing ET0
input_file = Path(
    "data/processed/phalia_complete_nasa_data_2023-11-23_2024-12-31_with_eto.csv"
)

df = pd.read_csv(input_file)
df["date"] = pd.to_datetime(df["date"])

# Provisional wheat planting date
planting_date = pd.Timestamp("2023-11-23")

# Reference growth-stage durations
initial_days = 15
development_days = 30
mid_days = 65
late_days = 40

def calculate_crop_values(row):

    days = (row["date"] - planting_date).days
    et0 = row["ET0_mm_day"]

    if days < 0:
        return pd.Series(["Before planting", None, None, days])

    elif days < initial_days:
        stage = "Initial"
        kc = 0.30

    elif days < initial_days + development_days:
        stage = "Crop development"
        progress = (days - initial_days) / development_days
        kc = 0.30 + progress * (1.15 - 0.30)

    elif days < initial_days + development_days + mid_days:
        stage = "Mid-season"
        kc = 1.15

    elif days < initial_days + development_days + mid_days + late_days:
        stage = "Late-season"
        progress = (
            days - initial_days - development_days - mid_days
        ) / late_days
        kc = 1.15 + progress * (0.25 - 1.15)

    else:
        return pd.Series(
            ["Growing season completed", None, None, days]
        )

    etc = et0 * kc

    return pd.Series([stage, kc, etc, days])


# Calculate all dates
df[["growth_stage", "Kc", "ETc_mm_day", "days_after_sowing"]] = (
    df.apply(calculate_crop_values, axis=1)
)

# Save results
output_file = Path(
    "data/processed/phalia_complete_wheat_etc.csv"
)

df.to_csv(output_file, index=False)

print("\nFARMFUSION - ANNUAL WHEAT WATER ANALYSIS")
print("Total records:", len(df))
print("\nGrowth stage distribution:")
print(df["growth_stage"].value_counts())

print("\nFirst five records:")
print(
    df[[
        "date",
        "ET0_mm_day",
        "days_after_sowing",
        "growth_stage",
        "Kc",
        "ETc_mm_day"
    ]].head()
)

print("\nAverage daily ETc during growing season:")
print(round(df["ETc_mm_day"].mean(), 2), "mm/day")

print("\nSaved to:", output_file)
