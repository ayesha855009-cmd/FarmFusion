
import pandas as pd

file_path = (
    "data/processed/phalia_nasa_data_20240101_20241231_with_eto.csv"
)

df = pd.read_csv(file_path)

print("RAINFALL DATA CHECK")

print("\nRainfall column available:")
print("PRECTOTCORR" in df.columns)

if "PRECTOTCORR" in df.columns:
    rainfall = df["PRECTOTCORR"]

    print("\nMissing values:", rainfall.isna().sum())
    print("Minimum rainfall:", rainfall.min())
    print("Maximum rainfall:", rainfall.max())
    print("Average daily rainfall:", rainfall.mean())
    print("Total annual rainfall:", rainfall.sum())

    print("\nFirst five rainfall records:")
    print(rainfall.head())
