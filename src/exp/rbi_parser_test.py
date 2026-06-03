import pandas as pd

FILE_PATH = (
    "data/raw/rbi_payment_indicators/"
    "PSSOCT2022D3D2B2B62E8D40CDB7EAD95931FA1756.xlsx"
)

df = pd.read_excel(
    FILE_PATH,
    header=None
)

part1 = df.iloc[1:51]

for idx, row in part1.iterrows():

    metric = str(row[0]).strip()

    if metric.startswith("2.6"):
        print(idx)
        print(row)
        print()