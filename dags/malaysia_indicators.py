from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from pathlib import Path

# Resolved relative to this file, so it works unchanged whether Airflow is
# running natively (WSL) or in Docker (project mounted at /opt/airflow/project) —
# dags/malaysia_indicators.py -> parent.parent is always the project root.
PROJECT_PATH = Path(__file__).resolve().parent.parent

with DAG(
    dag_id='malaysia_indicators_pipeline',
    description='Malaysia Economic Indicators ETL Pipeline',
    # schedule='@weekly',
    schedule='0 1 * * 1-5',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['malaysia', 'portfolio']
) as dag:

    run_pipeline = BashOperator(
        task_id='run_pipeline',
        bash_command=f'cd {PROJECT_PATH} && python3 etl/run_pipeline.py'
    )