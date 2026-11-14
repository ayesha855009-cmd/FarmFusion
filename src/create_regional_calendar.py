
import pandas as pd
from pathlib import Path

columns = [
    "country_iso3",
    "region_name",
    "agroecological_zone",
    "crop_name",
    "season_name",
    "planting_start_month",
    "planting_start_day",
    "planting_end_month",
    "planting_end_day",
    "initial_stage_days",
    "development_stage_days",
    "mid_stage_days",
    "late_stage_days",
    "harvest_start_month",
    "harvest_start_day",
    "harvest_end_month",
    "harvest_end_day",
    "source_name",
    "source_url",
    "reference_year",
    "confidence"
]

df = pd.DataFrame(columns=columns)

output_path = Path(
    "data/processed/regional_crop_calendar.csv"
)

output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print("Regional crop calendar created!")
print("Columns:", len(df.columns))
print("Saved to:", output_path)
