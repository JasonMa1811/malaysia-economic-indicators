import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def combine_indicators():
    # Load processed files
    fuel = pd.read_csv(PROCESSED_DIR / "fuelprice.csv")
    cpi = pd.read_csv(PROCESSED_DIR / "cpi.csv")
    exchange = pd.read_csv(PROCESSED_DIR / "exchange_rate.csv")
    opr = pd.read_csv(PROCESSED_DIR / "opr.csv")

    # Convert dates
    fuel['date'] = pd.to_datetime(fuel['date'])
    cpi['date'] = pd.to_datetime(cpi['date'])
    exchange['date'] = pd.to_datetime(exchange['date'])
    opr['date'] = pd.to_datetime(opr['date'])

    # Add month column to fuel
    fuel['month'] = fuel['date'].dt.to_period('M').dt.to_timestamp()

    # CPI overall monthly
    cpi_overall = cpi[cpi['division'] == 'overall'].copy()
    cpi_overall['month'] = cpi_overall['date'].dt.to_period('M').dt.to_timestamp()
    cpi_monthly = cpi_overall.groupby('month')['index'].mean().reset_index()
    cpi_monthly.rename(columns={'index': 'cpi_index'}, inplace=True)

    # Exchange rate monthly average
    exchange['month'] = exchange['date'].dt.to_period('M').dt.to_timestamp()
    exchange_monthly = exchange.groupby('month').agg({
        'usd': 'mean',
        'sgd': 'mean',
        'eur': 'mean',
        'gbp': 'mean',
        'jpy': 'mean'
    }).reset_index()

    # OPR forward fill
    opr['month'] = opr['date'].dt.to_period('M').dt.to_timestamp()
    opr_monthly = opr.groupby('month')['new_opr_level'].last().reset_index()
    all_months = fuel[['month']].drop_duplicates().sort_values('month')
    opr_monthly = pd.merge(all_months, opr_monthly, on='month', how='left')
    opr_monthly['new_opr_level'] = opr_monthly['new_opr_level'].ffill()

    # Join all to fuel
    combined = pd.merge(fuel, cpi_monthly, on='month', how='left')
    combined = pd.merge(combined, exchange_monthly, on='month', how='left')
    combined = pd.merge(combined, opr_monthly, on='month', how='left')

    filename = PROCESSED_DIR / "combined_indicators.csv"
    combined.to_csv(filename, index=False)
    print(f"✅ combined — {combined.shape[0]} rows, {combined.shape[1]} columns")
    return combined

if __name__ == "__main__":
    combine_indicators()