
import pandas as pd

file = "data/processed/phalia_complete_wheat_etc.csv"

df = pd.read_csv(file)
df["date"] = pd.to_datetime(df["date"])

season = df[
    (df["date"] >= "2023-11-23") &
    (df["date"] <= "2024-04-20")
]

print("FARMFUSION - SOIL WATER DATA CHECK")

print("\nGrowing season records:", len(season))

print("\nTotal rainfall:")
print(round(season["PRECTOTCORR"].sum(), 2), "mm")

print("\nTotal crop water use:")
print(round(season["ETc_mm_day"].sum(), 2), "mm")

print("\nRoot-zone soil wetness:")
print("Average:", round(season["GWETROOT"].mean(), 3))
print("Minimum:", round(season["GWETROOT"].min(), 3))
print("Maximum:", round(season["GWETROOT"].max(), 3))

print("\nMissing values:")
print(season[
    ["PRECTOTCORR", "ETc_mm_day", "GWETROOT"]
].isna().sum())
