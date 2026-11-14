
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

fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharex=True)

# Graph 1: Total soil profile storage
axes[0].plot(
    df["date"],
    df["soil_storage_mm"],
    label="Total profile water storage"
)

axes[0].set_title("Modeled Soil Profile Water Storage")
axes[0].set_ylabel("Water storage (mm)")
axes[0].legend()
axes[0].grid(alpha=0.3)

# Graph 2: Daily unmet crop water demand
axes[1].plot(
    df["date"],
    df["unmet_demand_mm"],
    label="Daily unmet demand"
)

axes[1].set_title("Daily Unmet Wheat Water Demand")
axes[1].set_xlabel("Date")
axes[1].set_ylabel("Unmet demand (mm)")
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()

OUTPUT = (
    BASE_DIR
    / "data"
    / "processed"
    / "daily_water_trends.png"
)

plt.savefig(OUTPUT, dpi=300)
plt.show()

print("Chart saved to:", OUTPUT)
