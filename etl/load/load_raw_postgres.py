import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

DB_USER = os.environ.get("POSTGRES_DATA_USER", "malaysia")
DB_PASSWORD = os.environ.get("POSTGRES_DATA_PASSWORD", "malaysia")
DB_HOST = os.environ.get("POSTGRES_DATA_HOST", "localhost")
DB_PORT = os.environ.get("POSTGRES_DATA_PORT", "5433")
DB_NAME = os.environ.get("POSTGRES_DATA_DB", "malaysia_indicators")

TABLES = ["fuelprice", "cpi", "exchange_rate", "opr"]


def get_engine():
    conn_str = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(conn_str)


def load_raw_to_postgres():
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

    for name in TABLES:
        csv_path = RAW_DIR / f"{name}.csv"
        if not csv_path.exists():
            print(f"⚠️  Skipping {name} — {csv_path} not found")
            continue

        df = pd.read_csv(csv_path)

        # CASCADE drop first, not pandas' plain if_exists='replace'.
        # From the 2nd run onward, dbt's staging views depend on these raw
        # tables, so a plain DROP TABLE fails with "DependentObjectsStillExist".
        # CASCADE also drops those dependent views — harmless, since
        # `dbt run` recreates every view from scratch on each run anyway.
        with engine.begin() as conn:
            conn.execute(text(f'DROP TABLE IF EXISTS raw."{name}" CASCADE'))

        df.to_sql(name, engine, schema="raw", if_exists="append", index=False)
        print(f"✅ Loaded raw.{name} — {df.shape[0]} rows")


if __name__ == "__main__":
    load_raw_to_postgres()
