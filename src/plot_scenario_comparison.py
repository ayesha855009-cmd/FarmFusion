
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load scenario summary
FILE = BASE_DIR / "data" / "processed" / "all_36_scenario_summary.csv"
df = pd.read_csv(FILE)

# Create a comparison chart
plt.figure(figsize=(14, 7))

for moisture in ["Wet", "Moderate", "Dry"]:
    subset = df[df["moisture_scenario"] == moisture]

    plt.plot(
        subset["soil_texture"],
        subset["unmet_demand_mm"],
        marker="o",
        label=moisture
    )

plt.title("Simulated Unmet Wheat Water Demand by Soil and Moisture Scenario")
plt.xlabel("Soil Texture")
plt.ylabel("Unmet Crop Water Demand (mm)")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Initial Moisture")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

# Save chart
OUTPUT = BASE_DIR / "data" / "processed" / "unmet_demand_comparison.png"
plt.savefig(OUTPUT, dpi=300)

plt.show()

print("Chart saved to:", OUTPUT)
