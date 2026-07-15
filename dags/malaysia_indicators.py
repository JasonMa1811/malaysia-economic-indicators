from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Update PROJECT_PATH to match your local project directory
PROJECT_PATH = "/mnt/c/Users/JasonMa/Documents/Portfolio/malaysia-economic-indicators"

with DAG(
    dag_id='malaysia_indicators_pipeline',
    description='Malaysia Economic Indicators ETL Pipeline',
    schedule='@weekly',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['malaysia', 'portfolio']
) as dag:

    run_pipeline = BashOperator(
        task_id='run_pipeline',
        bash_command=f'cd {PROJECT_PATH} && python etl/run_pipeline.py'
    )