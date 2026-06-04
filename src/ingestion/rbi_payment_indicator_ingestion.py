import re
import pandas as pd
from datetime import datetime
import glob
import os

from src.utils.logger import get_logger

logger = get_logger(__name__)
from datetime import datetime
import pandas as pd
from src.loaders.rbi_payment_indicator_downloader import (
    download_new_files
)


def parse_period(year_value, month_value):

    if pd.isna(year_value):
        return None

    year_text = str(year_value).strip()

    # Example: 2021\nFebruary
    if "\n" in year_text:

        year, month = year_text.split("\n")

        for fmt in ("%B %Y", "%b %Y"):

            try:
                return datetime.strptime(
                    f"{month.strip()} {year.strip()}",
                    fmt
                ).date()

            except ValueError:
                pass

    # Skip FY columns
    if year_text.upper().startswith("FY"):
        return None

    if pd.isna(month_value):
        return None

    month_text = str(month_value).strip()

    for fmt in ("%B %Y", "%b %Y"):

        try:
            return datetime.strptime(
                f"{month_text} {year_text}",
                fmt
            ).date()

        except ValueError:
            pass

    return None



class RBIPaymentIndicatorParser:

    def __init__(self, file_path: str):

        self.file_path = file_path

        self.df = pd.read_excel(
        file_path,
        header=None
    )
    
    def get_metric_column(self):

        for col in self.df.columns:

            non_null_count = self.df[col].notna().sum()

            if non_null_count > 20:
                return col

        return 1

    def extract_sections(self):

        sections = {}

        for idx, row in self.df.iterrows():

            row_text = " ".join(
                str(x)
                for x in row.values
                if pd.notna(x)
            ).strip()

            if row_text.startswith("PART IV"):
                sections["PART_IV"] = idx

            elif row_text.startswith("PART III"):
                sections["PART_III"] = idx

            elif row_text.startswith("PART II"):
                sections["PART_II"] = idx

            elif row_text.startswith("PART I"):
                sections["PART_I"] = idx

        return sections
    def is_metric_row(self, value):

        if pd.isna(value):
            return False

        value = str(value).strip()

        return bool(
            re.match(
                r"^\d+(\.\d+)*\s+",
                value
            )
        )
    def extract_metrics(self):

        sections = self.extract_sections()

        part1 = self.df.iloc[
            sections["PART_I"]:
            sections["PART_II"]
        ]

        metrics = []

        for _, row in part1.iterrows():

            metric_col = self.get_metric_column()

            metric = row[metric_col]

            if self.is_metric_row(metric):

                metrics.append(
                    str(metric).strip()
                )

        return metrics
    def build_period_map(self, section_start):

        header_years = self.df.iloc[section_start + 2]
        header_months = self.df.iloc[section_start + 3]

        period_map = {}

        for col in self.df.columns:

            period = parse_period(
                header_years[col],
                header_months[col]
            )

            if period is not None:
                period_map[col] = period

        return period_map
    
    def parse_volume_value_section(
        self,
        start_row,
        end_row
    ):

        period_map = self.build_period_map(
            start_row
        )

        section_df = self.df.iloc[
            start_row:end_row
        ]

        records = []

        for _, row in section_df.iterrows():

            metric_col = self.get_metric_column()

            metric = row[metric_col]

            if not self.is_metric_row(metric):
                continue

            metric = str(metric).strip()

            metric_code = metric.split()[0]

            metric_name = metric.replace(
                metric_code,
                "",
                1
            ).strip()

            volume_cols = sorted(
                period_map.keys()
            )

            value_cols = [
                col + len(volume_cols)
                for col in volume_cols
            ]

            for volume_col, value_col in zip(
                volume_cols,
                value_cols
            ):

                if value_col not in row.index:
                    continue

                records.append(
                    {
                        "report_period": period_map[
                            volume_col
                        ],
                        "metric_code": metric_code,
                        "metric_name": metric_name,
                        "volume_lakh": row[
                            volume_col
                        ],
                        "value_crore": row[
                            value_col
                        ]
                    }
                )

        return pd.DataFrame(records)
    def parse_transactions(self):

        sections = self.extract_sections()

        part1 = self.df.iloc[
            sections["PART_I"]:
            sections["PART_II"]
        ]

        return self.parse_volume_value_section(
            sections["PART_I"],
            sections["PART_II"]
        )
    def parse_channels(self):

        sections = self.extract_sections()

        return self.parse_volume_value_section(
            sections["PART_II"],
            sections["PART_III"]
        )
    def parse_infrastructure(self):

        sections = self.extract_sections()

        period_map = (
            self.build_infrastructure_period_map(
                sections["PART_III"]
            )
        )
        end_row = sections.get(
            "PART_IV",
            len(self.df)
        )

        infra_df = self.df.iloc[
            sections["PART_III"]:
            end_row
        ]

        records = []

        for _, row in infra_df.iterrows():

            metric_col = self.get_metric_column()
            metric = row[metric_col]

            if not self.is_metric_row(metric):
                continue

            metric = str(metric).strip()

            metric_code = metric.split()[0]

            metric_name = metric.replace(
                metric_code,
                "",
                1
            ).strip()

            for col in sorted(period_map.keys()):

                if col not in row.index:
                    continue

                metric_value = row[col]

                if pd.isna(metric_value):
                    continue

                value = row[col]

                if pd.isna(value):
                    continue

                if str(value).strip() in [
                    "-",
                    "--",
                    ""
                ]:
                    continue

                records.append(
                    {
                        "report_period": str(period_map[col]),
                        "metric_code": metric_code,
                        "metric_name": metric_name,
                        "metric_value": float(value)
                    }
                )


        return pd.DataFrame(records)
    def build_infrastructure_period_map(
        self,
        section_start
    ):

        header_years = self.df.iloc[
            section_start + 1
        ]

        header_months = self.df.iloc[
            section_start + 2
        ]

        period_map = {}

        # Baseline snapshot column
        if (
            len(header_years) > 2
            and pd.notna(header_years[2])
        ):

            period_map[2] = (
                str(header_years[2])
                .strip()
                .upper()
                .replace(" ", "_")
            )

        # Dynamic monthly columns

        for col in self.df.columns:

            if col == 2:
                continue

            period = parse_period(
                header_years[col],
                header_months[col]
            )

            if period is not None:

                period_map[col] = period

        return period_map
    def parse_frauds(self):

        sections = self.extract_sections()

        if "PART_IV" not in sections:

            logger.info(
                "PART IV not present"
            )

            return pd.DataFrame(
                columns=[
                    "report_period",
                    "fraud_volume_lakh",
                    "fraud_value_crore"
                ]
            )

        fraud_df = self.df.iloc[
            sections["PART_IV"] + 2:
        ]

        records = []

        for _, row in fraud_df.iterrows():

            period = row[0]

            if pd.isna(period):
                continue

            period = str(period).strip()

            try:

                report_period = datetime.strptime(
                    period,
                    "%B %Y"
                ).date()

            except Exception:
                continue

            records.append(
                {
                    "report_period": report_period,
                    "fraud_volume_lakh": row[1],
                    "fraud_value_crore": row[2]
                }
            )

        return pd.DataFrame(records)

    def process_single_file(self):

        sections = self.extract_sections()


        tx = self.parse_transactions()


        ch = self.parse_channels()


        infra = self.parse_infrastructure()


        fraud = self.parse_frauds()


        return {
            "transactions": tx,
            "channels": ch,
            "infrastructure": infra,
            "frauds": fraud
        }   
def process_all_files():

    files = glob.glob(
        "data/raw/rbi_payment_indicators/*.xlsx"
    )

    logger.info(
        f"Found {len(files)} files"
    )

    all_transactions = []
    all_channels = []
    all_infrastructure = []
    all_frauds = []

    for file in files:

        try:

            logger.info(
                f"Processing {os.path.basename(file)}"
            )

            parser = RBIPaymentIndicatorParser(
                file
            )

            results = parser.process_single_file()

            all_transactions.append(
                results["transactions"]
            )

            all_channels.append(
                results["channels"]
            )

            all_infrastructure.append(
                results["infrastructure"]
            )

            all_frauds.append(
                results["frauds"]
            )

        except Exception:

            logger.exception(
                f"FAILED: {os.path.basename(file)}"
            )

    transactions_df = (
        pd.concat(
            all_transactions,
            ignore_index=True
        )
        if all_transactions
        else pd.DataFrame()
    )

    channels_df = (
        pd.concat(
            all_channels,
            ignore_index=True
        )
        if all_channels
        else pd.DataFrame()
    )

    infrastructure_df = (
        pd.concat(
            all_infrastructure,
            ignore_index=True
        )
        if all_infrastructure
        else pd.DataFrame()
    )

    frauds_df = (
        pd.concat(
            all_frauds,
            ignore_index=True
        )
        if all_frauds
        else pd.DataFrame()
    )

    # Deduplicate overlapping RBI periods

    infrastructure_df = (
        infrastructure_df
        .drop_duplicates(
            subset=[
                "report_period",
                "metric_code"
            ]
        )
        .reset_index(drop=True)
    )

    frauds_df = (
        frauds_df
        .drop_duplicates(
            subset=[
                "report_period"
            ]
        )
        .reset_index(drop=True)
    )

    logger.info(
        f"Transactions: {len(transactions_df)}"
    )

    logger.info(
        f"Channels: {len(channels_df)}"
    )

    logger.info(
        f"Infrastructure: {len(infrastructure_df)}"
    )

    logger.info(
        f"Frauds: {len(frauds_df)}"
    )

    return {
        "transactions": transactions_df,
        "channels": channels_df,
        "infrastructure": infrastructure_df,
        "frauds": frauds_df
    }
if __name__ == "__main__":
    
    new_files = download_new_files()
    results = process_all_files()

    from src.loaders.snowflake_loader import (
        SnowflakeLoader
    )

    from src.loaders.rbi_payment_indicator_loader import (
        load_dataframe
    )

    loader = SnowflakeLoader()

    try:

        load_dataframe(
            loader,
            results["transactions"],
            "RAW.RBI_PAYMENT_TRANSACTIONS",
            """
            INSERT INTO RAW.RBI_PAYMENT_TRANSACTIONS
            (
                REPORT_PERIOD,
                METRIC_CODE,
                METRIC_NAME,
                VOLUME_LAKH,
                VALUE_CRORE
            )
            VALUES (%s,%s,%s,%s,%s)
            """
        )

        load_dataframe(
            loader,
            results["channels"],
            "RAW.RBI_PAYMENT_CHANNELS",
            """
            INSERT INTO RAW.RBI_PAYMENT_CHANNELS
            (
                REPORT_PERIOD,
                METRIC_CODE,
                METRIC_NAME,
                VOLUME_LAKH,
                VALUE_CRORE
            )
            VALUES (%s,%s,%s,%s,%s)
            """
        )

        load_dataframe(
            loader,
            results["infrastructure"],
            "RAW.RBI_PAYMENT_INFRASTRUCTURE",
            """
            INSERT INTO RAW.RBI_PAYMENT_INFRASTRUCTURE
            (
                REPORT_PERIOD,
                METRIC_CODE,
                METRIC_NAME,
                METRIC_VALUE
            )
            VALUES (%s,%s,%s,%s)
            """
        )

        load_dataframe(
            loader,
            results["frauds"],
            "RAW.RBI_PAYMENT_FRAUDS",
            """
            INSERT INTO RAW.RBI_PAYMENT_FRAUDS
            (
                REPORT_PERIOD,
                FRAUD_VOLUME_LAKH,
                FRAUD_VALUE_CRORE
            )
            VALUES (%s,%s,%s)
            """
        )

        logger.info(
            "RBI Payment Indicators load completed successfully"
        )

    finally:

        loader.close()