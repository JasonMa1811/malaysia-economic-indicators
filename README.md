# Malaysia Economic Indicators Tracker

An automated data pipeline that tracks Malaysia's key economic indicators — fuel prices, CPI inflation, exchange rates and OPR — built with Python, Apache Airflow, PostgreSQL, dbt, and Power BI. Fully containerized: anyone can run the entire stack with two Docker Compose commands.

## 📊 Dashboard Preview
<img width="1367" height="789" alt="image" src="https://github.com/user-attachments/assets/5cd06fce-e914-4f74-95b8-fbce2e124471" />
<img width="2093" height="1181" alt="image" src="https://github.com/user-attachments/assets/2eb8e0d0-7484-4990-8df6-495e0f13c169" />

## 🏗️ Architecture

```
data.gov.my / Bank Negara Malaysia (BNM)
              │
              ▼  Python — API calls
        Extract (raw CSVs)
              │
              ▼  Python — pandas/SQLAlchemy
      raw schema (Postgres)
              │
              ▼  dbt — SQL
     staging views (Postgres)
     (filtering, COICOP mapping)
              │
              ▼  dbt — SQL
      marts tables (Postgres)
  (daily date spine + forward-fill, dbt tests for data quality)
              │
              ▼
   marts.combined_indicators
              │
              ▼
          Power BI
```

Two different tools save data into Postgres, at two different stages: **Python** lands the raw, unmodified data (`raw` schema) — dbt has no involvement here. **dbt** then reads that raw data and saves its own transformed output back into Postgres (`staging` and `marts` schemas) — dbt never touches the original CSVs directly, only what Python already loaded.

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
                        │
                        ▼
              marts.monthly_changes
       (monthly snapshot + MoM/YoY % change, via LAG window functions — powers the Insights page in Power BI)
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
│                                        + monthly_changes.sql (MoM/YoY %, powers Insights page)
│
├── data/
│   ├── raw/                          # Raw CSVs (gitignored — regenerates every run)
│   └── processed/                    # Legacy — kept for structure, no longer written to
│
├── dashboard/
│   └── malaysia_indicators.pbix      # Power BI dashboard (reads from marts.combined_indicators)
│
├── pgadmin/
│   └── servers.json                  # Intended to auto-load the Postgres connection in pgAdmin — see note below, doesn't fire in Desktop Mode
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

**Page 1 — Overview** (monitoring: what's happening now)
- 6 KPI cards — Latest RON95, RON97, Diesel, CPI Index, USD/MYR and OPR
- Fuel Price Trend — RON95, RON97 and Diesel, forward-filled daily
- CPI Inflation Trend — Monthly inflation index, forward-filled daily
- USD/MYR Trend — Daily exchange rate, forward-filled through weekends
- OPR Trend — BNM monetary policy decisions, forward-filled daily
- Interactive date slicer — Filter all visuals by date range

**Page 2 — Insights** (analysis: why, and so what)
- 3 insight cards, each pairing a small supporting chart with a written Observation → Interpretation, reading from `marts.monthly_changes`:
  - **Diesel subsidy shock** — Diesel vs USD/MYR (% change), correctly scaled so the divergence between a policy-driven spike and currency movement is visible
  - **Inflation holding steady** — CPI year-over-year growth, showing the fuel shock hasn't yet fed through to headline inflation
  - **Currency and rates diverged** — USD/MYR vs OPR on a secondary axis, showing rate hikes alone didn't defend the ringgit in real time
- Biggest Monthly Moves table — every month ranked by size of move, backing the insight cards with the full underlying data rather than just the headline claim

## 🧪 Data Quality
dbt tests run automatically as part of every pipeline execution — `not_null` and `unique` checks on every model's date column. A failed test fails the Airflow task, so bad data never silently reaches the dashboard.

## 🔍 Key Insights
- **Diesel subsidy shock**: diesel rose 81.6% month-over-month in March 2026 — the largest single-month move of any indicator tracked, isolated to diesel and not mirrored in the exchange rate, consistent with a targeted subsidy cut rather than global oil prices
- **Inflation holding steady**: CPI year-over-year growth stayed within a narrow 1.4%-2.0% band through mid-2026, even after the diesel spike — the fuel shock hasn't visibly reached headline inflation yet
- **Currency and rates diverged**: the ringgit weakened through 2022-2023 even as OPR rose from 1.75% to 3.00%; it only strengthened after rates had peaked, and BNM's later cut to 2.75% (July 2025) came only after that recovery

## 🐳 Run with Docker

The only supported way to run this project — Postgres and dbt are core to the pipeline now, not optional add-ons.

**Prerequisites:** Docker Desktop (Windows: WSL2 backend, enabled automatically by the installer), and [Git](https://git-scm.com/downloads) available from your command line.

> **Docker Desktop must be open and running** before any `docker compose` command below — not just installed. Look for the whale icon 🐳 in your system tray showing "Docker Desktop is running." If a command fails with `failed to connect to the docker API` / `dockerDesktopLinuxEngine: The system cannot find the file specified`, this is why — open Docker Desktop, wait ~30-60 seconds, then retry.

> **No Git installed?** GitHub Desktop's bundled git is **not** the same as having `git` available in PowerShell/terminal — if `git clone` says `'git' is not recognized`, that's why. Fastest fix on Windows, straight from PowerShell:
> ```powershell
> winget install --id Git.Git -e --source winget
> ```
> Close and reopen your terminal afterward so it picks up the new `git` command. Alternatively, install [Git for Windows](https://git-scm.com/downloads) manually, or skip the command line entirely: on the repo's GitHub page, click **Code → Download ZIP**, extract it, and open a terminal in that extracted folder to continue from step 2 below.

### Steps

1. **Clone the repo**
   ```bash
   git clone https://github.com/JasonMa1811/malaysia-economic-indicators.git
   cd malaysia-economic-indicators
   ```

2. **Set up local config**
   ```bash
   cp .env.example .env
   ```
   See `.env.example` for what each value does — safe local-dev defaults, no editing required to just get running.

3. **One-time Airflow setup** — creates the metadata database and admin login
   ```bash
   docker compose up airflow-init
   ```

4. **Start everything** — Postgres ×2, Airflow (4 services), pgAdmin
   ```bash
   docker compose up -d
   ```

5. **Open the Airflow UI** — [http://localhost:8080](http://localhost:8080) (`airflow` / `airflow`). Unpause `malaysia_indicators_pipeline` and trigger it manually, or wait for the weekday 1am UTC schedule.

6. **Open pgAdmin** — [http://localhost:5050](http://localhost:5050) (`admin@admin.com` / `admin`) — browse `marts.combined_indicators` directly, or run your own SQL against it.

   > **First-time pgAdmin setup required:** pgAdmin's config runs in "Desktop Mode" (no login-per-user), and dbt's auto-import of `pgadmin/servers.json` doesn't fire under that mode — a known pgAdmin quirk, not a bug in this repo. So on first use, the server list will be empty. Add it once, manually:
   > 1. Click **Add New Server**
   > 2. General tab → Name: anything, e.g. `Malaysia Indicators`
   > 3. Connection tab → Host: `postgres-data` (not `localhost` — pgAdmin talks to it over the internal Docker network), Port: `5432`, Maintenance database: `malaysia_indicators`, Username: `malaysia`, Password: `malaysia`
   > 4. Save, and tick "Save Password" so it's not needed again
   >
   > This only needs doing once per pgAdmin container — the connection persists across restarts via its own Docker volume.

7. **Open the dashboard** — `dashboard/malaysia_indicators.pbix` in Power BI Desktop, connect to PostgreSQL at `localhost:5433`, database `malaysia_indicators`, reading from `marts.combined_indicators`.

### Stopping

```bash
docker compose down          # stop everything
docker compose down -v       # stop and wipe all data (fresh start)
```

> **Windows/WSL2 users:** Docker Desktop runs everything inside a WSL2 Linux VM, which can hold onto several GB of RAM even after `docker compose down`. To fully release it: `wsl --shutdown` (this also closes any open WSL terminals — reopen them after). To cap how much RAM Docker's allowed to use in the first place instead of shutting it down each time, add a `.wslconfig` file in your Windows user folder — see the [WSL2 settings docs](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#wslconfig).

## 📦 Data Sources
- Fuel Prices: https://data.gov.my/data-catalogue/fuelprice
- CPI Headline: https://data.gov.my/data-catalogue/cpi_headline
- Exchange Rates: https://data.gov.my/data-catalogue/exchangerates_daily_0900
- OPR: https://api.bnm.gov.my/public/opr
