"""Airflow DAG for currency rates ETL."""

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from app.etl import run_pipeline


with DAG(
    dag_id="currency_rates_etl",
    description="Загрузка курсов валют из ЦБ РФ",
    start_date=datetime(2026, 5, 30),
    schedule="@daily",
    catchup=False,
    tags=["currency", "etl"],
) as dag:
    run_currency_pipeline = PythonOperator(
        task_id="run_currency_pipeline",
        python_callable=run_pipeline,
    )
