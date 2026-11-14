
import pandas as pd
from pathlib import Path

# Load water-balance scenarios
file = Path("data/processed/soil_water_balance_scenarios.csv")
df = pd.read_csv(file)

events = []

for _, row in df.iterrows():

    dates = str(row["irrigation_dates"]).split(", ")

    dates = [date for date in dates if date.strip()]

    if not dates:
        continue

    # Average irrigation amount per event
    amount_per_event = (
        row["net_irrigation_mm"] / row["irrigation_events"]
    )

    for date in dates:
        events.append({
            "soil_texture": row["soil_texture"],
            "maximum_root_depth_m": row["maximum_root_depth_m"],
            "irrigation_date": date,
            "estimated_irrigation_mm": round(
                amount_per_event, 2
            )
        })

# Create event-level dataset
event_df = pd.DataFrame(events)

output = Path("data/processed/irrigation_events.csv")
event_df.to_csv(output, index=False)

print("FARMFUSION - IRRIGATION EVENTS")
print("\nTotal irrigation events:", len(event_df))
print(event_df.to_string(index=False))
print("\nSaved to:", output)
