import logging

logger = logging.getLogger(__name__)


def load_dataframe(
    loader,
    dataframe
):

    data = list(
        dataframe.itertuples(
            index=False,
            name=None
        )
    )

    loader.execute_many(
        """
        INSERT INTO RAW.UPI_DAILY_STATS
        (
            REPORT_DATE,
            VOLUME_MN,
            VALUE_CR
        )
        VALUES (%s,%s,%s)
        """,
        data
    )

    logger.info(
        f"Loaded {len(dataframe)} rows"
    )