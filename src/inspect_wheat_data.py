import pandas as pd

df = pd.read_csv(
    "data/processed/phalia_complete_wheat_etc.csv"
)

print(df.columns.tolist())