
import pandas as pd
from pathlib import Path

file_path = Path(
    "data/processed/regional_crop_calendar.csv"
)

df = pd.read_csv(file_path)

new_record = {
    "country_iso3": "PAK",
    "region_name": "Central Punjab",
    "agroecological_zone": "Not yet classified",
    "crop_name": "Wheat",
    "season_name": "Rabi",
    "planting_start_month": 11,
    "planting_start_day": 1,
    "planting_end_month": 12,
    "planting_end_day": 15,
    "initial_stage_days": None,
    "development_stage_days": None,
    "mid_stage_days": None,
    "late_stage_days": None,
    "harvest_start_month": None,
    "harvest_start_day": None,
    "harvest_end_month": None,
    "harvest_end_day": None,
    "source_name": "Pakistan Wheat Policy Analysis 2023-24",
    "source_url": "https://api.gov.pk/SiteImage/Policy/Wheat%20Policy%20Analysis%20For%202023-24%20Crop.pdf",
    "reference_year": "2023-24",
    "confidence": "Official sowing window; Phalia regional mapping provisional"
}

df = pd.concat(
    [df, pd.DataFrame([new_record])],
    ignore_index=True
)

df.to_csv(file_path, index=False)

print("First regional crop record added!")
print(df[["country_iso3", "region_name", "crop_name",
          "season_name"]])
print("Total records:", len(df))
