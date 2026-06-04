from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="rbi_payment_indicator_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@monthly",
    catchup=False,
    tags=["finsight", "rbi"]
) as dag:

    run_payment_indicators = BashOperator(
        task_id="run_payment_indicators",
        bash_command="""
        cd /opt/project &&
        python -m src.ingestion.rbi_payment_indicator_ingestion
        """
    )