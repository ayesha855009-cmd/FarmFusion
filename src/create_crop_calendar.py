
import pandas as pd

crops = [
    {
        "crop": "Wheat",
        "season": "Rabi",
        "sowing_start": 10,
        "sowing_end": 12,
        "harvest_start": 4,
        "harvest_end": 5
    },
    {
        "crop": "Rice",
        "season": "Kharif",
        "sowing_start": 6,
        "sowing_end": 7,
        "harvest_start": 10,
        "harvest_end": 11
    },
    {
        "crop": "Cotton",
        "season": "Kharif",
        "sowing_start": 3,
        "sowing_end": 5,
        "harvest_start": 10,
        "harvest_end": 12
    },
    {
        "crop": "Maize",
        "season": "Kharif",
        "sowing_start": 7,
        "sowing_end": 8,
        "harvest_start": 10,
        "harvest_end": 11
    }
]

df = pd.DataFrame(crops)

df.to_csv(
    "data/processed/crop_calendar.csv",
    index=False
)

print("FarmFusion crop calendar created!")
print(df)
