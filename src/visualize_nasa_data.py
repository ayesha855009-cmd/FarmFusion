
import pandas as pd
import matplotlib.pyplot as plt

# Load NASA data
df = pd.read_csv("data/processed/nasa_power_phalia_2024.csv")

df["date"] = pd.to_datetime(df["date"])

# Calculate monthly averages and rainfall totals
df["month"] = df["date"].dt.month

monthly = df.groupby("month").agg({
    "T2M": "mean",
    "PRECTOTCORR": "sum",
    "RH2M": "mean",
    "ALLSKY_SFC_SW_DWN": "mean"
})

# Create dashboard charts
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Temperature
axes[0, 0].plot(monthly.index, monthly["T2M"], marker="o")
axes[0, 0].set_title("Monthly Average Temperature")
axes[0, 0].set_ylabel("Temperature (°C)")

# Rainfall
axes[0, 1].bar(monthly.index, monthly["PRECTOTCORR"])
axes[0, 1].set_title("Monthly Rainfall")
axes[0, 1].set_ylabel("Rainfall (mm)")

# Humidity
axes[1, 0].plot(monthly.index, monthly["RH2M"], marker="o")
axes[1, 0].set_title("Monthly Average Humidity")
axes[1, 0].set_ylabel("Humidity (%)")

# Solar radiation
axes[1, 1].plot(
    monthly.index,
    monthly["ALLSKY_SFC_SW_DWN"],
    marker="o"
)
axes[1, 1].set_title("Monthly Solar Radiation")
axes[1, 1].set_ylabel("MJ/m²/day")

for ax in axes.flat:
    ax.set_xlabel("Month")
    ax.grid(True, alpha=0.3)

plt.tight_layout()

# Save visualization
plt.savefig("data/processed/nasa_climate_analysis.png", dpi=120)

plt.show()
