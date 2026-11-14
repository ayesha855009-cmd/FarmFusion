
import pandas as pd
import matplotlib.pyplot as plt

# Load monthly NASA report
df = pd.read_csv(
    "data/processed/farmfusion_monthly_report.csv"
)

df["date"] = pd.to_datetime(df["date"])

# Create temperature chart
plt.figure(figsize=(10, 5))

plt.plot(
    df["date"],
    df["T2M"],
    marker="o",
    label="Average Temperature"
)

plt.title("Monthly Average Temperature - Phalia (2024)")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()

plt.savefig("data/processed/monthly_temperature.png")
plt.show()

# Create rainfall chart
plt.figure(figsize=(10, 5))

plt.bar(
    df["date"].dt.strftime("%b"),
    df["PRECTOTCORR"]
)

plt.title("Monthly Total Rainfall - Phalia (2024)")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.grid(axis="y")
plt.tight_layout()

plt.savefig("data/processed/monthly_rainfall.png")
plt.show()

print("Both climate charts saved successfully!")
