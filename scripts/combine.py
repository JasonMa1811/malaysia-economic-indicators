import pandas as pd
import os

save_path = r"C:\Users\JasonMa\Documents\MEGA\Portfolio\project_1\data"

# Load both files
fuel = pd.read_csv(os.path.join(save_path, "fuelprice_20260714.csv"))
cpi = pd.read_csv(os.path.join(save_path, "cpi_20260714.csv"))

# Convert dates
fuel['date'] = pd.to_datetime(fuel['date'])
cpi['date'] = pd.to_datetime(cpi['date'])

# Filter fuel to level only (remove change_weekly rows)
fuel = fuel[fuel['series_type'] == 'level'].copy()

# Add month column to fuel
fuel['month'] = fuel['date'].dt.to_period('M').dt.to_timestamp()

# Filter CPI to overall only
cpi_overall = cpi[cpi['division'] == 'overall'].copy()

# Aggregate CPI to monthly
cpi_overall['month'] = cpi_overall['date'].dt.to_period('M').dt.to_timestamp()
cpi_monthly = cpi_overall.groupby('month')['index'].mean().reset_index()
cpi_monthly.rename(columns={'index': 'cpi_index'}, inplace=True)

# Left join — keep all fuel rows, match CPI where available
combined = pd.merge(fuel, cpi_monthly, on='month', how='left')

# Save
filename = os.path.join(save_path, "combined_indicators.csv")
combined.to_csv(filename, index=False)
print(f"✅ Done! {combined.shape[0]} rows, {combined.shape[1]} columns")
print(combined.head(10))