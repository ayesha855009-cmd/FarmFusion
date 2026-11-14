
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FILE = BASE_DIR / "data" / "processed" / "all_36_scenario_summary.csv"
df = pd.read_csv(FILE)

# Create scenario labels
df["scenario"] = (
    df["soil_texture"] + " - " + df["moisture_scenario"]
)

# Plot extracted and unmet water
plt.figure(figsize=(16, 8))

plt.bar(
    df["scenario"],
    df["water_extracted_mm"],
    label="Water extracted"
)

plt.bar(
    df["scenario"],
    df["unmet_demand_mm"],
    bottom=df["water_extracted_mm"],
    label="Unmet demand"
)

plt.title("Crop Water Demand: Extracted Water vs Unmet Demand")
plt.xlabel("Soil and Moisture Scenario")
plt.ylabel("Water Depth (mm)")
plt.xticks(rotation=90, fontsize=8)
plt.legend()
plt.tight_layout()

OUTPUT = BASE_DIR / "data" / "processed" / "water_demand_comparison.png"

plt.savefig(OUTPUT, dpi=300)
plt.show()

print("Chart saved to:", OUTPUT)
