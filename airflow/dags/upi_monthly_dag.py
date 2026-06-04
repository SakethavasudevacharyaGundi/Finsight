from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="upi_monthly_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@monthly",
    catchup=False,
    tags=["finsight", "npci"]
) as dag:

    run_upi_monthly = BashOperator(
        task_id="run_upi_monthly",
        bash_command="""
        cd /opt/project &&
        python -m src.ingestion.upi_ingestion
        """
    )