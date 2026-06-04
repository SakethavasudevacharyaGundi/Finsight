from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

with DAG(
    dag_id="upi_daily_pipeline",
    start_date=datetime(2026, 6, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["finsight"]
) as dag:

    run_upi_daily = BashOperator(
        task_id="run_upi_daily",
        bash_command="""
        cd /opt/project &&
        python -m src.ingestion.npci_upi_daily_ingestion
        """
    )