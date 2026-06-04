from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from datetime import datetime

with DAG(
    dag_id="finsight_master_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@monthly",
    catchup=False,
    tags=["finsight"]
) as dag:

    start = EmptyOperator(
        task_id="start"
    )

    trigger_rbi_dpi = TriggerDagRunOperator(
        task_id="trigger_rbi_dpi",
        trigger_dag_id="rbi_dpi_pipeline"
    )

    trigger_payment_indicators = TriggerDagRunOperator(
        task_id="trigger_payment_indicators",
        trigger_dag_id="rbi_payment_indicator_pipeline"
    )

    trigger_upi_monthly = TriggerDagRunOperator(
        task_id="trigger_upi_monthly",
        trigger_dag_id="upi_monthly_pipeline"
    )

    end = EmptyOperator(
        task_id="end"
    )

    (
        start
        >> trigger_rbi_dpi
        >> trigger_payment_indicators
        >> trigger_upi_monthly
        >> end
    )