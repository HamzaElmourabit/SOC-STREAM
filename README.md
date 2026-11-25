# SOC-STREAM

## Big Data Network Intrusion Detection Platform

SOC-STREAM is a Big Data platform designed to process network traffic
events and detect potential cyberattacks using streaming technologies
and machine learning.

## Architecture

The project uses a Kappa architecture.

### Technologies

- Apache Kafka
- Apache NiFi
- Apache Spark Structured Streaming
- MinIO
- Apache Iceberg
- Great Expectations
- Apache Airflow
- MLflow
- PostgreSQL
- Streamlit
- Grafana
- Docker

## Dataset

Dataset: CIC-IDS2017

Source:
https://www.unb.ca/cic/datasets/ids-2017.html

The raw dataset is stored locally and is not included in this repository.

## Project Structure

- ingestion/: Data ingestion
- streaming/: Stream processing
- storage/: Lakehouse storage
- data_quality/: Data validation
- analytics/: Analytical queries
- ml/: Machine learning
- orchestration/: Workflow orchestration
- dashboard/: Visualization
- monitoring/: Monitoring
- tests/: Project tests

## Project Status

Initial project structure created.
Implementation is in progress.