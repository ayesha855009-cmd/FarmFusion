
import pandas as pd
from pathlib import Path

# ==========================================
# 1. LOAD DATASETS
# ==========================================

wheat_file = Path("data/processed/phalia_complete_wheat_etc.csv")
soil_file = Path("data/processed/global_soil_properties.csv")
crop_file = Path("data/processed/global_crop_water_parameters.csv")

df = pd.read_csv(wheat_file)
soils = pd.read_csv(soil_file)
crop = pd.read_csv(crop_file)

df["date"] = pd.to_datetime(df["date"])
# ==========================================
# SOIL LAYER STRUCTURE
# ==========================================

soil_layers = [
    {"top": 0.00, "bottom": 0.15},
    {"top": 0.15, "bottom": 0.30},
    {"top": 0.30, "bottom": 0.60},
    {"top": 0.60, "bottom": 1.00},
    {"top": 1.00, "bottom": 1.50}
]

print("\nSOIL LAYER STRUCTURE")

for layer in soil_layers:
    thickness = layer["bottom"] - layer["top"]

    print(
        f'{layer["top"]:.2f}–{layer["bottom"]:.2f} m'
        f' | Thickness: {thickness:.2f} m'
    )
# ==========================================
# 2. SELECT WHEAT GROWING SEASON
# ==========================================

sowing_date = pd.Timestamp("2023-11-23")
harvest_date = pd.Timestamp("2024-04-20")

df = df[
    (df["date"] >= sowing_date) &
    (df["date"] <= harvest_date)
].copy()

df = df.sort_values("date")

# ==========================================
# 3. CROP WATER PARAMETERS
# ==========================================

p_at_5 = float(
    crop.loc[0, "depletion_fraction_at_5mm_day"]
)

# ==========================================
# 4. ROOT-DEPTH AND INITIAL MOISTURE SCENARIOS
# ==========================================

maximum_root_depths = [1.0, 1.5]

# Hypothetical initial depletion scenarios
initial_depletion_fractions = [0.0, 0.30, 0.60]

# Provisional root-growth assumptions
initial_root_depth = 0.15
root_growth_days = 45

# ==========================================
# 5. RESULT STORAGE
# ==========================================

results = []
irrigation_records = []

# ==========================================
# 6. RUN WATER-BALANCE SCENARIOS
# ==========================================

for _, soil in soils.iterrows():

    available_water = float(
        soil["available_water_mm_per_m"]
    )

    for maximum_root_depth in maximum_root_depths:

        for initial_depletion_fraction in initial_depletion_fractions:

            # Initial root-zone available water
            initial_taw = (
                available_water * initial_root_depth
            )

            # Initial soil-water depletion
            initial_depletion = (
                initial_taw * initial_depletion_fraction
            )

            depletion = initial_depletion

            total_irrigation = 0.0
            total_drainage = 0.0

            irrigation_events = 0
            irrigation_dates = []

            total_rainfall = 0.0
            total_etc = 0.0

            # ======================================
            # DAILY SIMULATION
            # ======================================

            for _, day in df.iterrows():

                # Calculate growing root depth
                days_after_sowing = (
                    day["date"] - sowing_date
                ).days

                growth_fraction = min(
                    days_after_sowing / root_growth_days,
                    1.0
                )

                root_depth = (
                    initial_root_depth
                    + (maximum_root_depth - initial_root_depth)
                    * growth_fraction
                )

                # Total available water
                taw = available_water * root_depth

                # Daily rainfall and crop water use
                rainfall = max(
                    float(day["PRECTOTCORR"]), 0
                )

                etc = max(
                    float(day["ETc_mm_day"]), 0
                )

                total_rainfall += rainfall
                total_etc += etc

                # Readily available water fraction
                p = max(
                    0.1,
                    min(0.8, p_at_5 + 0.04 * (5 - etc))
                )

                raw = p * taw

                # Update soil-water depletion
                depletion = depletion - rainfall + etc

                # Drainage when storage exceeds field capacity
                drainage = 0.0

                if depletion < 0:

                    drainage = -depletion
                    total_drainage += drainage

                    depletion = 0.0

                # Irrigation trigger
                if depletion > raw:

                    irrigation_amount = depletion

                    total_irrigation += irrigation_amount
                    irrigation_events += 1

                    irrigation_date = day["date"].strftime(
                        "%Y-%m-%d"
                    )

                    irrigation_dates.append(irrigation_date)

                    # Record simulated irrigation event
                    irrigation_records.append({
                        "soil_texture": soil["soil_texture"],
                        "maximum_root_depth_m": maximum_root_depth,
                        "initial_depletion_fraction": initial_depletion_fraction,
                        "irrigation_date": irrigation_date,
                        "irrigation_amount_mm": round(
                            irrigation_amount, 2
                        )
                    })

                    # Restore depletion to zero
                    depletion = 0.0

            # ======================================
            # 7. WATER-BALANCE RESIDUAL
            # ======================================

            residual = (
                total_rainfall
                + total_irrigation
                + depletion
                - total_etc
                - total_drainage
                - initial_depletion
            )

            # ======================================
            # 8. SAVE SCENARIO SUMMARY
            # ======================================

            results.append({

                "soil_texture": soil["soil_texture"],

                "maximum_root_depth_m": maximum_root_depth,

                "initial_depletion_fraction": initial_depletion_fraction,

                "initial_depletion_mm": round(
                    initial_depletion, 2
                ),

                "initial_TAW_mm": round(
                    initial_taw, 2
                ),

                "TAW_max_mm": round(
                    available_water * maximum_root_depth, 2
                ),

                "total_rainfall_mm": round(
                    total_rainfall, 2
                ),

                "total_ETc_mm": round(
                    total_etc, 2
                ),

                "net_irrigation_mm": round(
                    total_irrigation, 2
                ),

                "irrigation_events": irrigation_events,

                "irrigation_dates": ", ".join(
                    irrigation_dates
                ),

                "drainage_mm": round(
                    total_drainage, 2
                ),

                "final_depletion_mm": round(
                    depletion, 2
                ),

                "water_balance_residual_mm": round(
                    residual, 4
                )
            })

# ==========================================
# 9. SAVE SCENARIO CSV
# ==========================================

result_df = pd.DataFrame(results)

output = Path(
    "data/processed/soil_water_balance_scenarios.csv"
)

result_df.to_csv(output, index=False)

# ==========================================
# 10. SAVE IRRIGATION EVENT CSV
# ==========================================

event_df = pd.DataFrame(irrigation_records)

event_output = Path(
    "data/processed/irrigation_events.csv"
)

event_df.to_csv(event_output, index=False)

# ==========================================
# 11. DISPLAY RESULTS
# ==========================================

print("FARMFUSION - GROWING ROOT WATER BALANCE")

print("\nTotal scenarios:", len(result_df))

print("\nScenario results:")
print(result_df.to_string(index=False))

print(
    "\nMaximum absolute residual:",
    result_df["water_balance_residual_mm"].abs().max()
)

print(
    "\nTotal recorded irrigation events:",
    len(event_df)
)

print("\nIrrigation event records:")
print(event_df.to_string(index=False))

print("\nSaved scenario results to:", output)
print("Saved irrigation events to:", event_output)
