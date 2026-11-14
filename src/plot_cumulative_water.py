
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "layered_daily_simulation_sandy_loam_wet.csv"
)

df = pd.read_csv(FILE)
df["date"] = pd.to_datetime(df["date"])

# Calculate cumulative rainfall and crop-water demand
df["cumulative_rainfall_mm"] = df["rainfall_mm"].cumsum()
df["cumulative_etc_mm"] = df["ETc_mm"].cumsum()

# Create the chart
plt.figure(figsize=(14, 7))

plt.plot(
    df["date"],
    df["cumulative_rainfall_mm"],
    label="Cumulative rainfall",
    linewidth=2
)

plt.plot(
    df["date"],
    df["cumulative_etc_mm"],
    label="Cumulative crop-water demand (ETc)",
    linewidth=2
)

plt.title("Cumulative Rainfall vs Crop-Water Demand")
plt.xlabel("Date")
plt.ylabel("Cumulative water (mm)")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()

OUTPUT = (
    BASE_DIR
    / "data"
    / "processed"
    / "cumulative_water_comparison.png"
)

plt.savefig(OUTPUT, dpi=300)
plt.show()

print("Chart saved to:", OUTPUT)
