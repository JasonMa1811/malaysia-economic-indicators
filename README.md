# Malaysia Economic Indicators Tracker

An automated ETL pipeline that tracks Malaysia's key economic indicators — fuel prices, CPI inflation, exchange rates and OPR — built with Python, Apache Airflow, and Power BI.

## 📊 Dashboard Preview
<img width="1367" height="789" alt="image" src="https://github.com/user-attachments/assets/5cd06fce-e914-4f74-95b8-fbce2e124471" />


## 🏗️ Architecture
data.gov.my API → Python (Extract) → Raw CSV (data/raw/) → Python Transform (Clean & Join) → Processed CSV (data/processed/) → Airflow (Weekly Schedule) → Power BI (Visualize)

## 📁 Project Structure
```
├── etl/
│   ├── extract/
│   │   ├── extract_fuel.py        # Fetch fuel prices from data.gov.my
│   │   ├── extract_cpi.py         # Fetch CPI data from data.gov.my
│   │   ├── extract_exchange_rate.py # Fetch exchange rates from data.gov.my
│   │   └── extract_opr.py         # Fetch OPR decisions from BNM API
│   ├── transform/
│   │   ├── transform.py           # Clean and filter raw data
│   │   └── combine.py             # Join all datasets into combined table
│   └── run_pipeline.py            # Orchestrate full ETL pipeline
│
├── dags/
│   ├── malaysia_indicators.py     # Dag file for airflow
│
├── data/
│   ├── raw/                       # Raw data from APIs
│   └── processed/                 # Cleaned and combined data
│
├── dashboard/
│   └── malaysia_indicators.pbix   # Power BI dashboard
│
├── requirements.txt
└── README.md
```

## 🛠️ Tech Stack
- **Python** — Data extraction and transformation
- **Apache Airflow** — Weekly pipeline scheduling
- **data.gov.my API** — Official Malaysia open data (fuel, CPI, exchange rate)
- **BNM API** — Bank Negara Malaysia (OPR decisions)
- **Power BI** — Interactive dashboard

## 📈 Dashboard Features
- 6 KPI cards — Latest RON95, RON97, Diesel, CPI Index, USD/MYR and OPR
- Fuel Price Trend — RON95, RON97 and Diesel weekly prices
- CPI Inflation Trend — Monthly inflation index
- USD/MYR Trend — Daily exchange rate aggregated monthly
- OPR Trend — BNM monetary policy decisions
- Interactive date slicer — Filter all visuals by date range

## 🔍 Key Insights
- Diesel prices spiked to RM6.70 in April 2026 despite ringgit strengthening — indicating domestic subsidy removal rather than currency weakness
- USD/MYR peaked at 4.77 in 2024 (weak ringgit) contributing to import cost inflation
- BNM cut OPR from 3.00% to 2.75% in July 2025 to stimulate the economy
- CPI has risen consistently since 2022, driven by Food and Transport categories
## ⚙️ How to Run

### Prerequisites
- Python 3.8+
- Apache Airflow (running on WSL/Linux)
- Power BI Desktop

### Steps
1. Clone the repo
git clone https://github.com/JasonMa1811/malaysia-economic-indicators.git
cd malaysia-economic-indicators

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

### Optional: Schedule with Airflow
1. Install Apache Airflow on WSL/Ubuntu
2. Update PROJECT_PATH in airflow/dags/malaysia_indicators.py
3. Copy DAG file to your Airflow dags folder
4. Start Airflow: airflow standalone
5. Enable malaysia_indicators_pipeline DAG in the UI

## 📦 Data Sources
- Fuel Prices: https://data.gov.my/data-catalogue/fuelprice
- CPI Headline: https://data.gov.my/data-catalogue/cpi_headline
- Exchange Rates: https://data.gov.my/data-catalogue/exchangerates_daily_0900
- OPR: https://api.bnm.gov.my/public/opr
