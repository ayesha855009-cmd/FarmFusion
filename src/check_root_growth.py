
import pandas as pd

file = "data/processed/loam_wheat_daily_water_trace.csv"

df = pd.read_csv(file)

check_days = [0, 15, 30, 45, 60, 90, 120, 149]

print("FARMFUSION - ROOT GROWTH CHECK")

print(
    df.iloc[check_days][
        ["date", "days_after_sowing", "root_depth_m", "TAW_mm"]
    ].to_string(index=False)
)
