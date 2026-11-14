
import pandas as pd

# Load combined NASA dataset
df = pd.read_csv(
    "data/processed/farmfusion_nasa_data_2024.csv"
)

df["date"] = pd.to_datetime(df["date"])

# Set date as index
df = df.set_index("date")

# Monthly averages
monthly_avg = df.resample("ME").mean()

# Monthly total rainfall
monthly_rainfall = df["PRECTOTCORR"].resample("ME").sum()

# Replace average rainfall with total rainfall
monthly_avg["PRECTOTCORR"] = monthly_rainfall

# Display results
print("\nFARMFUSION MONTHLY REPORT")
print(monthly_avg.round(2))

# Save report
monthly_avg.to_csv(
    "data/processed/farmfusion_monthly_report.csv"
)

print("\nMonthly report saved successfully!")
