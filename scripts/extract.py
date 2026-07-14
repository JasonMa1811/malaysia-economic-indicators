import requests
import pandas as pd
import os
from datetime import datetime

save_path = r"C:\Users\JasonMa\Documents\MEGA\Portfolio\project_1\data"

# Division mapping
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

def fetch_data(dataset_id):
    url = f"https://api.data.gov.my/data-catalogue?id={dataset_id}&limit=9999"
    response = requests.get(url)
    df = pd.DataFrame(response.json())
    return df

def process_fuelprice(df):
    df['date'] = pd.to_datetime(df['date'])
    return df

def process_cpi(df):
    df['date'] = pd.to_datetime(df['date'])
    # Map division codes to names
    df['division_name'] = df['division'].map(division_map)
    return df


# Create folder if not exists
os.makedirs(save_path, exist_ok=True)
today = datetime.today().strftime('%Y%m%d')

# Fetch and process each dataset
datasets = {
    "fuelprice": ("fuelprice", process_fuelprice),
    "cpi": ("cpi_headline", process_cpi)
}

for output_name, (dataset_id, process_func) in datasets.items():
    df = fetch_data(dataset_id)
    df = process_func(df)
    filename = os.path.join(save_path, f"{output_name}_{today}.csv")
    df.to_csv(filename, index=False)
    print(f"✅ Done! {output_name} — {df.shape[0]} rows, {df.shape[1]} columns")