
import pandas as pd
from pathlib import Path

# Load datasets
wheat_file = Path("data/processed/phalia_complete_wheat_etc.csv")
soil_file = Path("data/processed/global_soil_properties.csv")
crop_file = Path("data/processed/global_crop_water_parameters.csv")

df = pd.read_csv(wheat_file)
soils = pd.read_csv(soil_file)
crop = pd.read_csv(crop_file)

df["date"] = pd.to_datetime(df["date"])

# Select wheat growing season
sowing_date = pd.Timestamp("2023-11-23")

df = df[
    (df["date"] >= sowing_date) &
    (df["date"] <= "2024-04-20")
].copy()

df = df.sort_values("date")

# Select Loam soil
soil = soils[soils["soil_texture"] == "Loam"].iloc[0]

available_water = float(soil["available_water_mm_per_m"])
p_at_5 = float(crop.loc[0, "depletion_fraction_at_5mm_day"])

# Provisional root-growth assumptions
initial_root_depth = 0.15
maximum_root_depth = 1.0
root_growth_days = 45

depletion = 0.0
records = []

for _, day in df.iterrows():

    days_after_sowing = (day["date"] - sowing_date).days

    # Gradually increase root depth
    growth_fraction = min(days_after_sowing / root_growth_days, 1)

    root_depth = (
        initial_root_depth
        + (maximum_root_depth - initial_root_depth) * growth_fraction
    )

    # Calculate available water in the current root zone
    taw = available_water * root_depth

    rainfall = max(float(day["PRECTOTCORR"]), 0)
    etc = max(float(day["ETc_mm_day"]), 0)

    p = max(0.1, min(0.8, p_at_5 + 0.04 * (5 - etc)))
    raw = p * taw

    # Daily soil-water balance
    depletion = depletion - rainfall + etc

    drainage = 0.0

    if depletion < 0:
        drainage = -depletion
        depletion = 0.0

    irrigation = 0.0

    if depletion > raw:
        irrigation = depletion
        depletion = 0.0

    records.append({
        "date": day["date"],
        "days_after_sowing": days_after_sowing,
        "root_depth_m": root_depth,
        "TAW_mm": taw,
        "rainfall_mm": rainfall,
        "ETc_mm": etc,
        "RAW_mm": raw,
        "irrigation_mm": irrigation,
        "drainage_mm": drainage,
        "soil_depletion_mm": depletion,
        "GWETROOT": day["GWETROOT"]
    })

# Save daily records
trace = pd.DataFrame(records)

output = Path("data/processed/loam_wheat_daily_water_trace.csv")
trace.to_csv(output, index=False)

print("FARMFUSION - GROWING ROOT WATER TRACE")
print("\nTotal days:", len(trace))
print("Initial root depth:", round(trace.iloc[0]["root_depth_m"], 2), "m")
print("Final root depth:", round(trace.iloc[-1]["root_depth_m"], 2), "m")
print("Irrigation days:", (trace["irrigation_mm"] > 0).sum())
print("Total irrigation:", round(trace["irrigation_mm"].sum(), 2), "mm")

print("\nIrrigation schedule:")
print(
    trace.loc[
        trace["irrigation_mm"] > 0,
        ["date", "root_depth_m", "ETc_mm", "RAW_mm", "irrigation_mm"]
    ].to_string(index=False)
)

print("\nSaved to:", output)
