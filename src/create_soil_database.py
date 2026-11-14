
import pandas as pd
from pathlib import Path

soil_data = [
    ["Sand", 0.13, 0.06],
    ["Loamy sand", 0.16, 0.08],
    ["Sandy loam", 0.22, 0.10],
    ["Loam", 0.31, 0.15],
    ["Silt loam", 0.33, 0.13],
    ["Silt", 0.33, 0.09],
    ["Sandy clay loam", 0.32, 0.20],
    ["Clay loam", 0.39, 0.23],
    ["Silty clay loam", 0.44, 0.23],
    ["Sandy clay", 0.39, 0.27],
    ["Silty clay", 0.50, 0.32],
    ["Clay", 0.54, 0.39]
]

df = pd.DataFrame(
    soil_data,
    columns=[
        "soil_texture",
        "field_capacity",
        "wilting_point"
    ]
)

# Calculate available water capacity
df["available_water_capacity"] = (
    df["field_capacity"] - df["wilting_point"]
)

# Convert m3/m3 to mm of available water per metre of soil
df["available_water_mm_per_m"] = (
    df["available_water_capacity"] * 1000
)

df["unit"] = "m3/m3"
df["source"] = "FAO AquaCrop default soil characteristics"
df["confidence"] = "Reference estimate - not field measured"

output = Path("data/processed/global_soil_properties.csv")

df.to_csv(output, index=False)

print("GLOBAL SOIL DATABASE CREATED")
print("\n", df.to_string(index=False))
print("\nSaved to:", output)
