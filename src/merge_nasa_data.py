import pandas as pd

# Load both NASA datasets
climate = pd.read_csv(
    "data/processed/nasa_power_phalia_2024.csv"
)

soil = pd.read_csv(
    "data/processed/nasa_soil_wetness_2024.csv"
)

# Convert dates into datetime format
climate["date"] = pd.to_datetime(climate["date"])
soil["date"] = pd.to_datetime(soil["date"])

# Merge using date
combined = pd.merge(
    climate,
    soil,
    on="date",
    how="inner"
)

# Sort by date
combined = combined.sort_values("date")

# Save combined dataset
combined.to_csv(
    "data/processed/farmfusion_nasa_data_2024.csv",
    index=False
)

print("Combined NASA dataset created!")
print("\nFirst five rows:")
print(combined.head())

print("\nDataset shape:", combined.shape)
print("\nMissing values:")
print(combined.isnull().sum())