import pandas as pd

df = pd.read_csv(
    "data/processed/phalia_nasa_data_20240101_20241231_with_eto.csv"
)

print("Rows:", len(df))
print("Missing ET0:", df["ET0_mm_day"].isna().sum())
print("Negative ET0:", (df["ET0_mm_day"] < 0).sum())
print("Minimum ET0:", df["ET0_mm_day"].min())
print("Maximum ET0:", df["ET0_mm_day"].max())