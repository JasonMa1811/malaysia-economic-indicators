# extract_cpi.py
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_cpi(start_year=None, end_year=None):
    all_data = []
    limit = 5000
    offset = 0

    params = f"id=cpi_headline&limit={limit}"
    if start_year:
        params += f"&date_start={start_year}-01-01@date"
    if end_year:
        params += f"&date_end={end_year}-12-31@date"

    while True:
        url = f"https://api.data.gov.my/data-catalogue?{params}&offset={offset}"
        response = requests.get(url)
        data = response.json()

        if not data:
            break

        all_data.extend(data)

        if len(data) < limit:
            break

        offset += limit
        time.sleep(1)

    df = pd.DataFrame(all_data)
    df['date'] = pd.to_datetime(df['date'])
    return df

if __name__ == "__main__":
    df = fetch_cpi(start_year=None, end_year=None)
    filename = RAW_DIR / "cpi.csv"
    df.to_csv(filename, index=False)
    print(f"✅ cpi — {df.shape[0]} rows, {df.shape[1]} columns")