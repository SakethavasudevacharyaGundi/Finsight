import pandas as pd
from datetime import datetime

from src.loaders.snowflake_loader import (
    SnowflakeLoader
)

from src.loaders.npci_upi_loader import (
    load_dataframe
)

from src.test import (
    download_daily_upi
)

def transform_dataframe(df):

    df = df.copy()

    df = df[
        df["Day"] != "Total"
    ]

    df = df.rename(
        columns={
            "Day": "report_date",
            "Volume (In Mn.)": "volume_mn",
            "Value (In Cr.)": "value_cr"
        }
    )

    df["report_date"] = pd.to_datetime(
    df["report_date"]
    ).dt.strftime("%Y-%m-%d")

    df = df.drop_duplicates(
        subset=["report_date"]
    )

    return df

def backfill_daily_upi():

    all_dfs = []

    for year in range(2021, 2027):

        for month in [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]:

            try:

                print(
                    f"Downloading {month} {year}"
                )

                df = download_daily_upi(
                    month=month,
                    year=year
                )

                df = transform_dataframe(df)

                all_dfs.append(df)

            except Exception as e:

                print(
                    f"Skipping {month} {year}"
                )

    return pd.concat(
        all_dfs,
        ignore_index=True
    )
if __name__ == "__main__":

    backfill = False

    if backfill:

        df = backfill_daily_upi()

    else:

        today = datetime.today()

        df = download_daily_upi(
            month=today.strftime("%B"),
            year=today.year
        )

        df = transform_dataframe(df)

    print(df.head())
    print(df.shape)

    loader = SnowflakeLoader()

    try:

        load_dataframe(
            loader,
            df
        )

    finally:

        loader.close()