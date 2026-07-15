import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent  
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

division_map = {
    'overall': 'Overall',
    '01': 'Food & Non-Alcoholic Beverages',
    '02': 'Alcoholic Beverages & Tobacco',
    '03': 'Clothing & Footwear',
    '04': 'Housing, Water, Electricity & Gas',
    '05': 'Furnishings & Household Equipment',
    '06': 'Health',
    '07': 'Transport',
    '08': 'Communication',
    '09': 'Recreation & Culture',
    '10': 'Education',
    '11': 'Restaurants & Hotels',
    '12': 'Miscellaneous Goods & Services',
    '13': 'Insurance & Financial Services'
}

def transform_fuelprice(df):
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['series_type'] == 'level'].copy()
    df = df.drop(columns=['series_type'])
    return df

def transform_cpi(df):
    df['date'] = pd.to_datetime(df['date'])
    df['division_name'] = df['division'].map(division_map)
    return df

def transform_exchange_rate(df):
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['rate_type'] == 'middle'].copy()
    df = df.drop(columns=['rate_type'])
    return df

def transform_opr(df):
    df['date'] = pd.to_datetime(df['date'])
    df = df.drop_duplicates(subset=['date']).reset_index(drop=True)
    return df

if __name__ == "__main__":
    datasets = {
        "fuelprice": transform_fuelprice,
        "cpi": transform_cpi,
        "exchange_rate": transform_exchange_rate,
        "opr": transform_opr,
    }

    for name, transform_func in datasets.items():
        # Find latest raw file - handle both with and without date suffix
        files = list(RAW_DIR.glob(f"{name}*.csv"))
        
        if not files:
            print(f"❌ No raw file found for {name}")
            continue

        latest_file = max(files, key=lambda x: x.stat().st_mtime)
        df = pd.read_csv(latest_file)
        df = transform_func(df)

        filename = PROCESSED_DIR / f"{name}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ {name} — {df.shape[0]} rows, {df.shape[1]} columns")

    print("\n🎉 Transform complete!")