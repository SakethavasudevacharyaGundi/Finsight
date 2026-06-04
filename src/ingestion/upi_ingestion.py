import glob
import os

import pandas as pd

from src.loaders.snowflake_loader import SnowflakeLoader
from src.utils.logger import get_logger
from src.loaders.npci_upi_monthly_loader import (
    download_monthly_upi
)

logger = get_logger(__name__)


UPI_FOLDER = "data/raw/upi/upi_monthly_stats"


def read_upi_files() -> pd.DataFrame:

    excel_files = glob.glob(
        os.path.join(UPI_FOLDER, "*.xlsx")
    )

    if not excel_files:
        raise FileNotFoundError(
            "No UPI Excel files found"
        )

    logger.info(
        f"Found {len(excel_files)} files"
    )

    dataframes = []

    for file in excel_files:

        df = pd.read_excel(file)

        df["source_file"] = os.path.basename(file)

        dataframes.append(df)

    combined_df = pd.concat(
        dataframes,
        ignore_index=True
    )

    logger.info(
        f"Combined rows: {len(combined_df)}"
    )

    return combined_df


def validate_dataframe(df: pd.DataFrame):

    required_columns = [
        "Month",
        "No. of Banks live on UPI",
        "Volume (In Mn.)",
        "Value (In Cr.)"
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    if df.empty:

        raise ValueError(
            "UPI dataframe is empty"
        )

    logger.info(
        "Validation successful"
    )


def transform_dataframe(df: pd.DataFrame):

    df = df.copy()

    df["Month"] = pd.to_datetime(
        df["Month"],
        format="%B-%Y"
    )

    df["Month"] = df["Month"].dt.strftime("%Y-%m-%d")

    df = df.rename(
        columns={
            "Month": "month",
            "No. of Banks live on UPI": "banks_live",
            "Volume (In Mn.)": "volume_mn",
            "Value (In Cr.)": "value_cr"
        }
    )

    # -------------------------
    # Data Cleaning
    # -------------------------

    df["volume_mn"] = (
        df["volume_mn"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["value_cr"] = (
        df["value_cr"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["banks_live"] = (
        df["banks_live"]
        .fillna(0)
        .astype(int)
    )

    df = df[
        [
            "month",
            "banks_live",
            "volume_mn",
            "value_cr",
            "source_file"
        ]
    ]

    df = df.drop_duplicates(
        subset=["month"]
    )

    df = df.sort_values(
        by="month"
    )

    logger.info(
        f"Rows after deduplication: {len(df)}"
    )

    logger.info(
        f"Date Range: {df['month'].min()} -> {df['month'].max()}"
    )

    return df

def load_upi():

    df = read_upi_files()

    validate_dataframe(df)

    df = transform_dataframe(df)

    loader = SnowflakeLoader()

    try:

        loader.execute(
            """
            TRUNCATE TABLE RAW.UPI_MONTHLY_STATS;
            """
        )

        insert_query = """
        INSERT INTO RAW.UPI_MONTHLY_STATS
        (
            month,
            banks_live,
            volume_mn,
            value_cr,
            source_file
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        records = list(
            df.itertuples(
                index=False,
                name=None
            )
        )

        loader.execute_many(
            insert_query,
            records
        )

        audit_query = f"""
        INSERT INTO RAW.LOAD_AUDIT
        (
            dataset_name,
            file_name,
            rows_loaded,
            load_status
        )
        VALUES
        (
            'UPI_MONTHLY_STATS',
            'MULTIPLE_FILES',
            {len(df)},
            'SUCCESS'
        );
        """

        loader.execute(
            audit_query
        )

        logger.info(
            f"Loaded {len(df)} rows"
        )

    finally:

        loader.close()


if __name__ == "__main__":
    
    download_monthly_upi(
        month=...,
        year=...
    )
    load_upi()