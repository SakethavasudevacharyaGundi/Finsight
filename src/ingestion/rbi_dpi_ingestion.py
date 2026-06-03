import os

import pandas as pd

from src.loaders.snowflake_loader import SnowflakeLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)


def validate_dataframe(df: pd.DataFrame):

    required_columns = [
        "Period",
        "DPI_Value"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError(
            "DPI file is empty"
        )

    logger.info(
        f"Validation passed. Rows: {len(df)}"
    )


def load_rbi_dpi():

    file_path = "data/raw/rbi_dpi.csv"

    logger.info(
        f"Reading file: {file_path}"
    )

    df = pd.read_csv(file_path)

    validate_dataframe(df)

    loader = SnowflakeLoader()

    try:

        loader.execute(
            """
            TRUNCATE TABLE RAW.RBI_DPI;
            """
        )

        for _, row in df.iterrows():

            period = row["Period"]
            dpi_value = row["DPI_Value"]

            query = f"""
            INSERT INTO RAW.RBI_DPI
            (
                period,
                dpi_value,
                source_file
            )
            VALUES
            (
                '{period}-01',
                {dpi_value},
                'rbi_dpi.csv'
            );
            """

            loader.execute(query)

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
            'RBI_DPI',
            'rbi_dpi.csv',
            {len(df)},
            'SUCCESS'
        );
        """

        loader.execute(audit_query)

        logger.info(
            f"Loaded {len(df)} rows into RAW.RBI_DPI"
        )

    finally:
        loader.close()


if __name__ == "__main__":
    load_rbi_dpi()