from datetime import datetime, timedelta
import os
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

# Add src/ directory to PYTHONPATH so Airflow can import modules
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from scraper import scrape_flip
from cleaner import clean_data
from loader import load_to_sqlite

default_args = {
    "owner": "student",
    "retries": 2,
    "retry_delay": timedelta(minutes=3)
}

with DAG(
    dag_id="flip_books_pipeline",
    description="ETL pipeline: flip.kz books → clean → SQLite",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",  # no more than once per day
    catchup=False,
    default_args=default_args,
) as dag:

    scrape_task = PythonOperator(
        task_id="scrape_data",
        python_callable=scrape_flip
    )

    clean_task = PythonOperator(
        task_id="clean_data",
        python_callable=clean_data
    )

    load_task = PythonOperator(
        task_id="load_to_db",
        python_callable=load_to_sqlite
    )

    scrape_task >> clean_task >> load_task
