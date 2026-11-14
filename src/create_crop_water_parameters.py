
import pandas as pd
from pathlib import Path

data = [
    {
        "crop_name": "Wheat",
        "root_depth_min_m": 1.0,
        "root_depth_max_m": 1.5,
        "depletion_fraction_at_5mm_day": 0.55,
        "source": "FAO-56",
        "confidence": "Reference range - field conditions may differ"
    }
]

df = pd.DataFrame(data)

output = Path(
    "data/processed/global_crop_water_parameters.csv"
)

df.to_csv(output, index=False)

print("CROP WATER PARAMETERS CREATED")
print(df.to_string(index=False))
print("\nSaved to:", output)
