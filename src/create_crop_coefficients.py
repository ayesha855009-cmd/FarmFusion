
import pandas as pd
from pathlib import Path

data = [
    {
        "crop_name": "Wheat",
        "crop_scientific_name": "Triticum aestivum",
        "crop_category": "Cereal",
        "kc_initial": 0.30,
        "kc_mid": 1.15,
        "kc_end": 0.25,
        "initial_stage_days": None,
        "development_stage_days": None,
        "mid_stage_days": None,
        "late_stage_days": None,
        "climate_reference": "FAO-56 standard conditions",
        "irrigation_condition": "Not specified",
        "source_name": "FAO Irrigation and Drainage Paper 56",
        "source_url": "https://www.fao.org/4/X0490E/X0490E00.htm",
        "confidence": "Reference baseline"
    }
]

df = pd.DataFrame(data)

output_path = Path("data/processed/global_crop_coefficients.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print("Crop coefficient dataset updated!")
print(df[["crop_name", "kc_initial", "kc_mid", "kc_end"]])
print("Saved to:", output_path)
