import pandas as pd

file_path = "data/processed/nasa_soil_wetness_2024.csv"

df = pd.read_csv(file_path, parse_dates=["date"])

# Calculate monthly average soil wetness
monthly = df.set_index("date").resample("ME").mean()

print("\nMonthly Soil Wetness:")
print(monthly.round(3))

# Save monthly results
monthly.to_csv("data/processed/monthly_soil_wetness_2024.csv")

print("\nMonthly analysis saved successfully!")