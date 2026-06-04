from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="rbi_dpi_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@monthly",
    catchup=False,
    tags=["finsight", "rbi"]
) as dag:

    run_rbi_dpi = BashOperator(
        task_id="run_rbi_dpi",
        bash_command="""
        cd /opt/project &&
        python -m src.ingestion.rbi_dpi_ingestion
        """
    )