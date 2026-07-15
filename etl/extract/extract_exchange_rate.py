import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

def fetch_exchange_rate_by_year(year):
    all_data = []
    limit = 5000
    offset = 0

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    while True:
        url = (
            f"https://api.data.gov.my/data-catalogue"
            f"?id=exchangerates_daily_0900"
            f"&limit={limit}"
            f"&offset={offset}"
            f"&date_start={start_date}@date"
            f"&date_end={end_date}@date"
        )
        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ API error: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        all_data.extend(data)
        if len(data) < limit:
            break

        offset += limit

    return all_data

def fetch_exchange_rate(start_year=None, end_year=None):
    if end_year is None:
        end_year = datetime.today().year

    all_data = []
    start_time = time.time()

    # Fetch year by year
    for year in range(start_year, end_year + 1):
        print(f"Fetching {year}...")
        year_data = fetch_exchange_rate_by_year(year)
        all_data.extend(year_data)
        print(f"  ✅ {year} — {len(year_data)} rows")
        time.sleep(0.5)  # small delay between years

    df = pd.DataFrame(all_data)
    df['date'] = pd.to_datetime(df['date'])
    # df = df[df['rate_type'] == 'middle'].copy()
    # df = df[['date', 'usd', 'sgd', 'eur', 'gbp', 'jpy']].copy()
    df = df.sort_values('date').reset_index(drop=True)

    total_time = round(time.time() - start_time, 1)
    print(f"\n✅ Done! {df.shape[0]} rows in {total_time}s")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")

    return df

if __name__ == "__main__":

    df = fetch_exchange_rate(start_year=None, end_year=None)

    # filename = RAW_DIR / f"exchange_rate_{start_year}_{end_year}.csv"
    filename = RAW_DIR / f"exchange_rate.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved to {filename}")