import subprocess
from datetime import datetime
from pathlib import Path

from extract.extract_fuel import fetch_fuelprice
from extract.extract_cpi import fetch_cpi
from extract.extract_exchange_rate import fetch_exchange_rate
from extract.extract_opr import fetch_opr
from load.load_raw_postgres import load_raw_to_postgres

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
DBT_DIR = BASE_DIR / "dbt"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# CONFIG
# ============================================
START_YEAR = 2000
END_YEAR = datetime.today().year

extractors = {
    "fuelprice":     lambda: fetch_fuelprice(START_YEAR, END_YEAR),
    "cpi":           lambda: fetch_cpi(START_YEAR, END_YEAR),
    "exchange_rate": lambda: fetch_exchange_rate(START_YEAR, END_YEAR),
    "opr":           lambda: fetch_opr(START_YEAR, END_YEAR),
}

print(f"🗓️ Running pipeline for {START_YEAR} to {END_YEAR}...\n")

# ---- Extract: Python hits the APIs, lands raw CSVs. Unchanged. ----
for name, fetch_func in extractors.items():
    print(f"📦 Extracting {name}...")
    raw_df = fetch_func()
    raw_df.to_csv(RAW_DIR / f"{name}.csv", index=False)
    print(f"✅ Raw — {raw_df.shape[0]} rows\n")

# ---- Load: raw CSVs go straight into Postgres, unmodified. ----
# This is the 'L' in ELT — no cleaning happens here. dbt does that next,
# reading from the `raw` schema this just populated.
print("🐘 Loading raw data into Postgres...")
load_raw_to_postgres()

# ---- Transform: dbt takes over from here (see dbt/models/). ----
# Replaces what used to be etl/transform/transform.py + combine.py —
# those files are still in the repo for reference, but no longer run.
print("\n🏗️  Running dbt transformations...")
subprocess.run(
    ["dbt", "run", "--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)],
    check=True,
)

print("\n🧪 Running dbt tests...")
subprocess.run(
    ["dbt", "test", "--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)],
    check=True,
)

print("\n🎉 Pipeline complete!")
