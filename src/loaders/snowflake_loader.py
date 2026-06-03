import os

import snowflake.connector
from dotenv import load_dotenv

from src.utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class SnowflakeLoader:

    def __init__(self):

        self.connection = snowflake.connector.connect(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            role=os.getenv("SNOWFLAKE_ROLE")
        )

        logger.info("Connected to Snowflake")
    
    def fetch_all(self, query: str):

        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            return cursor.fetchall()

        finally:
            cursor.close()

    def execute(self, query: str):

        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            logger.info("Query executed successfully")

        finally:
            cursor.close()

    def close(self):

        self.connection.close()
        logger.info("Snowflake connection closed")
    def execute_many(self, query: str, data: list):

        cursor = self.connection.cursor()

        try:
            cursor.executemany(query, data)
            logger.info(
                f"Batch inserted {len(data)} rows"
            )

        finally:
            cursor.close()
    
    