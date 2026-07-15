import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

def fetch_opr(start_year=None, end_year=None):
    if end_year is None:
        end_year = datetime.today().year

    headers = {"Accept": "application/vnd.BNM.API.v1+json"}
    all_data = []
    start_time = time.time()

    for year in range(start_year, end_year + 1):
        url = f"https://api.bnm.gov.my/public/opr/year/{year}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ {year} — API error {response.status_code}")
            continue

        data = response.json().get('data', [])
        all_data.extend(data)
        print(f"✅ {year} — {len(data)} decisions")
        time.sleep(0.5)

    df = pd.DataFrame(all_data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    # Remove duplicates
    df = df.drop_duplicates(subset=['date']).reset_index(drop=True)

    total_time = round(time.time() - start_time, 1)
    print(f"\n✅ Done! {df.shape[0]} rows in {total_time}s")
    return df

if __name__ == "__main__":
    df = fetch_opr(start_year=None, end_year=None)
    filename = RAW_DIR / "opr.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved!")
    print(df)