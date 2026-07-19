# Extends the official Airflow image with the two extra packages
# etl/ needs (pandas, requests). Everything else (Airflow itself,
# its providers, the FAB auth manager) already ships in the base image.
FROM apache/airflow:3.3.0

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
