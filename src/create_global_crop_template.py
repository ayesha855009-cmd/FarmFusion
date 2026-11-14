
import pandas as pd

columns = [
    "country_iso3",
    "region_name",
    "region_code",
    "agroecological_zone",
    "crop_name",
    "season_name",
    "production_system",
    "sowing_start_month",
    "sowing_start_day",
    "sowing_end_month",
    "sowing_end_day",
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

df.to_csv(
    "data/processed/global_crop_calendar.csv",
    index=False
)

print("Global crop calendar template created!")
print("Columns:", len(columns))
print(df.columns.tolist())
