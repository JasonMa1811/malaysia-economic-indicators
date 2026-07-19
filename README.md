# Malaysia Economic Indicators Tracker

An automated data pipeline that tracks Malaysia's key economic indicators — fuel prices, CPI inflation, exchange rates and OPR — built with Python, Apache Airflow, PostgreSQL, dbt, and Power BI. Fully containerized: anyone can run the entire stack with two Docker Compose commands.

## 📊 Dashboard Preview
<img width="1367" height="789" alt="image" src="https://github.com/user-attachments/assets/5cd06fce-e914-4f74-95b8-fbce2e124471" />
<<<<<<< Updated upstream


## 🏗️ Architecture
         data.gov.my
               │
         Bank Negara
               │
               ▼
         Python Extract
               │
               ▼
       Data Cleaning
               │
               ▼
      Combined Dataset
               │
               ▼
     Apache Airflow DAG
               │
               ▼
          Power BI
=======

## 🏗️ Architecture

```
data.gov.my / Bank Negara Malaysia (BNM)
              │
              ▼
     Python extract (Airflow)
              │
              ▼
   raw schema  (Postgres — unmodified landing zone)
              │
              ▼
        dbt staging models
     (filtering, COICOP mapping)
              │
              ▼
         dbt marts models
  (daily date spine + forward-fill,
      dbt tests for data quality)
              │
              ▼
   marts.combined_indicators (Postgres)
              │
              ▼
          Power BI
```

This is an **ELT** pipeline, not ETL — raw data lands in Postgres unmodified, and all cleaning/joining logic lives in versioned SQL (dbt), not pandas. Everything runs inside Docker: Airflow orchestrates it, Postgres stores it, dbt transforms it, pgAdmin lets you browse it.

## Data Model

Grain: **one row per calendar day** (2003–present), including weekends. Fuel (weekly), CPI (monthly), and OPR (sporadic) are forward-filled onto every day using a SQL window-function technique ("gaps and islands") — the same approach used to carry exchange rates forward across weekends, when markets are closed and there's no real trading data.

```
date_spine (continuous calendar)
        │
        ├── int_fuel_daily_filled       (weekly → forward-filled daily)
        ├── int_cpi_daily_filled        (monthly → forward-filled daily)
        ├── int_exchange_daily_filled   (weekday → forward-filled through weekends)
        └── int_opr_daily_filled        (sporadic → forward-filled daily)
                        │
                        ▼
             marts.combined_indicators
```
>>>>>>> Stashed changes

## Data Model
```
         Fuel
                 \
         CPI -------> Combined Indicators
                 /
         USD
               /
         OPR
```
          
## 📁 Project Structure
```
├── etl/
│   ├── extract/
│   │   ├── extract_fuel.py           # Fetch fuel prices from data.gov.my
│   │   ├── extract_cpi.py            # Fetch CPI data from data.gov.my
│   │   ├── extract_exchange_rate.py  # Fetch exchange rates from data.gov.my
│   │   └── extract_opr.py            # Fetch OPR decisions from BNM API
│   ├── load/
│   │   └── load_raw_postgres.py      # Land raw CSVs into Postgres, unmodified
│   └── run_pipeline.py               # Orchestrate: extract → load raw → dbt run → dbt test
│
├── dags/
│   └── malaysia_indicators.py        # Airflow DAG (weekdays, 1am UTC)
│
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml                  # Reads connection details from env vars
│   ├── macros/
│   │   └── generate_schema_name.sql  # Clean schema names (staging/marts, not public_staging)
│   └── models/
│       ├── staging/                  # 1:1 cleaning per source, materialized as views
│       └── marts/                    # Daily spine + forward-fill + final join + tests
│
├── data/
│   ├── raw/                          # Raw CSVs (gitignored — regenerates every run)
│   └── processed/                    # Legacy — kept for structure, no longer written to
│
├── dashboard/
│   └── malaysia_indicators.pbix      # Power BI dashboard (reads from marts.combined_indicators)
│
├── pgadmin/
│   └── servers.json                  # Pre-configured Postgres connection for pgAdmin
│
├── docker-compose.yml                # Postgres (x2) + Airflow (4 services) + pgAdmin
├── Dockerfile                        # Airflow image + pandas/requests/dbt
├── requirements.txt
├── .env.example                      # Copy to .env before first run
└── README.md
```

## 🛠️ Tech Stack
- **Python** — Data extraction (API calls only — no transformation logic)
- **PostgreSQL** — Two instances: Airflow's own metadata DB, and a separate data warehouse
- **dbt (data build tool)** — SQL-based transformation layer: staging views, marts, and automated data quality tests
- **Apache Airflow** — Orchestration, weekday scheduling
- **Docker Compose** — Full stack: Postgres ×2, Airflow (api-server/scheduler/dag-processor/triggerer), pgAdmin
- **pgAdmin** — Web-based Postgres browser (`localhost:5050`)
- **Power BI** — Interactive dashboard, connects directly to Postgres
- **data.gov.my API** — Official Malaysia open data (fuel, CPI, exchange rate)
- **BNM API** — Bank Negara Malaysia (OPR decisions)

## 📈 Dashboard Features
- 6 KPI cards — Latest RON95, RON97, Diesel, CPI Index, USD/MYR and OPR
- Fuel Price Trend — RON95, RON97 and Diesel, forward-filled daily
- CPI Inflation Trend — Monthly inflation index, forward-filled daily
- USD/MYR Trend — Daily exchange rate, forward-filled through weekends
- OPR Trend — BNM monetary policy decisions, forward-filled daily
- Interactive date slicer — Filter all visuals by date range

## 🧪 Data Quality
dbt tests run automatically as part of every pipeline execution — `not_null` and `unique` checks on every model's date column. A failed test fails the Airflow task, so bad data never silently reaches the dashboard.

## 🔍 Key Insights
- Diesel prices spiked to RM6.70 in April 2026 despite ringgit strengthening — indicating domestic subsidy removal rather than currency weakness
- USD/MYR peaked at 4.77 in 2024 (weak ringgit) contributing to import cost inflation
- BNM cut OPR from 3.00% to 2.75% in July 2025 to stimulate the economy
- CPI has risen consistently since 2022, driven by Food and Transport categories

## 🐳 Run with Docker

<<<<<<< Updated upstream
### Steps
1. Clone the repo
  ```
  git clone https://github.com/JasonMa1811/malaysia-economic-indicators.git
  cd malaysia-economic-indicators
  ```
2. Install dependencies
  pip install -r requirements.txt

3. Run the pipeline manually
  python etl/run_pipeline.py
  
  This will:
  - Fetch raw data from APIs → saved to data/raw/
  - Clean and transform data → saved to data/processed/
  - Join all datasets → saved to data/processed/combined_indicators.csv

4. Open dashboard
  - Open dashboard/malaysia_indicators.pbix in Power BI Desktop
  - Refresh data source to point to your local data/processed/ folder
=======
The only supported way to run this project — Postgres and dbt are core to the pipeline now, not optional add-ons.

**Prerequisites:** Docker Desktop only (Windows: WSL2 backend, enabled automatically by the installer).

```bash
git clone https://github.com/JasonMa1811/malaysia-economic-indicators.git
cd malaysia-economic-indicators

cp .env.example .env             # local config — see .env.example for what each value does

docker compose up airflow-init   # one-time: creates the Airflow metadata DB + admin user
docker compose up -d             # starts everything: Postgres ×2, Airflow, pgAdmin
```

**Airflow UI** — [http://localhost:8080](http://localhost:8080) (`airflow` / `airflow`). Unpause `malaysia_indicators_pipeline` and trigger it manually, or wait for the weekday 1am UTC schedule.

**pgAdmin** — [http://localhost:5050](http://localhost:5050) (`admin@admin.com` / `admin`) — browse `marts.combined_indicators` directly, or run your own SQL against it.
>>>>>>> Stashed changes

**Power BI** — open `dashboard/malaysia_indicators.pbix`, connect to PostgreSQL at `localhost:5433`, database `malaysia_indicators`, and read from `marts.combined_indicators`.

```bash
docker compose down          # stop everything
docker compose down -v       # stop and wipe all data (fresh start)
```

## 📦 Data Sources
- Fuel Prices: https://data.gov.my/data-catalogue/fuelprice
- CPI Headline: https://data.gov.my/data-catalogue/cpi_headline
- Exchange Rates: https://data.gov.my/data-catalogue/exchangerates_daily_0900
- OPR: https://api.bnm.gov.my/public/opr
