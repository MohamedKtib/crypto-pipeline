from datetime import datetime
from io import StringIO

import pandas as pd
from airflow.sdk import dag, task

from src.extract import extract_prices
from src.transform import transform_prices
from src.load import load_prices

@dag(
    dag_id="crypto_pipeline",
    schedule="@hourly",
    start_date=datetime(2026, 10, 1),
    catchup=False,
    default_args={"retries": 2}
)
def crypto_pipeline():
    @task
    def extract():
        return extract_prices()
    @task
    def transform(raw):
        df = transform_prices(raw)
        return df.to_json(orient="records", date_format="iso")
    @task
    def load(payload):
        df = pd.read_json(StringIO(payload), orient="records")
        df["last_updated"] = pd.to_datetime(df["last_updated"], utc=True)
        df["fetched_at"] = pd.to_datetime(df["fetched_at"], utc=True)
        load_prices(df)
    
    load(transform(extract()))

crypto_pipeline()