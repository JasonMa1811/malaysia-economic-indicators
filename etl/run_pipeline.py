from extract.extract_fuel import fetch_fuelprice
from extract.extract_cpi import fetch_cpi
from extract.extract_exchange_rate import fetch_exchange_rate
from extract.extract_opr import fetch_opr
from transform.transform import transform_fuelprice, transform_cpi, transform_exchange_rate, transform_opr
from transform.combine import combine_indicators
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# CONFIG
# ============================================
START_YEAR = 2000
END_YEAR = datetime.today().year

datasets = {
    "fuelprice":     (lambda: fetch_fuelprice(START_YEAR, END_YEAR),     transform_fuelprice),
    "cpi":           (lambda: fetch_cpi(START_YEAR, END_YEAR),           transform_cpi),
    "exchange_rate": (lambda: fetch_exchange_rate(START_YEAR, END_YEAR), transform_exchange_rate),
    "opr":           (lambda: fetch_opr(START_YEAR, END_YEAR),           transform_opr),
}

print(f"🗓️ Running pipeline for {START_YEAR} to {END_YEAR}...\n")

for name, (fetch_func, transform_func) in datasets.items():
    print(f"📦 Extracting {name}...")
    raw_df = fetch_func()
    raw_df.to_csv(RAW_DIR / f"{name}.csv", index=False)
    print(f"✅ Raw — {raw_df.shape[0]} rows")

    print(f"🔄 Transforming {name}...")
    processed_df = transform_func(raw_df)
    processed_df.to_csv(PROCESSED_DIR / f"{name}.csv", index=False)
    print(f"✅ Processed — {processed_df.shape[0]} rows\n")

# after all extract + transform steps
print("\n🔗 Combining datasets...")
combine_indicators()

print("🎉 Pipeline complete!")