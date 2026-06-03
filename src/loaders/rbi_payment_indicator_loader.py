import logging

logger = logging.getLogger(__name__)


def load_dataframe(
    loader,
    dataframe,
    table_name,
    insert_sql
):

    loader.execute(
        f"TRUNCATE TABLE {table_name}"
    )

    data = list(
        dataframe.itertuples(
            index=False,
            name=None
        )
    )

    loader.execute_many(
        insert_sql,
        data
    )

    logger.info(
        f"Loaded {len(dataframe)} rows into {table_name}"
    )