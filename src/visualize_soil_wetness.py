import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/processed/monthly_soil_wetness_2024.csv"
)

plt.figure(figsize=(10, 5))

plt.plot(df["date"], df["GWETTOP"], marker="o", label="Surface")
plt.plot(df["date"], df["GWETROOT"], marker="o", label="Root zone")
plt.plot(df["date"], df["GWETPROF"], marker="o", label="Full profile")

plt.title("Monthly Soil Wetness - Phalia (2024)")
plt.xlabel("Month")
plt.ylabel("Soil Wetness (0–1)")
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()

plt.savefig("data/processed/soil_wetness_chart.png")
plt.show()