Malaysia Economic Indicators Tracker

An automated data pipeline that tracks Malaysia's fuel prices and CPI inflation trends, built with Python, Apache Airflow, and Power BI.

## 📊 Dashboard Preview
<img width="2028" height="1062" alt="malaysia_indicators" src="https://github.com/user-attachments/assets/a23aba25-a2e2-4a91-ac2e-64cd3d9a3cee" />

## 🏗️ Architecture
data.gov.my API → Python (Extract) → Airflow (Schedule) → CSV → Power BI (Visualize)

## 📁 Project Structure
```
├── scripts/
│   ├── extract.py          # Fetch data from data.gov.my API
│   └── combine.py          # Transform and join datasets
├── data/
│   ├── fuelprice.csv       # Raw weekly fuel prices
│   ├── cpi.csv             # Raw monthly CPI by division
│   └── combined_indicators.csv  # Cleaned combined dataset
├── dashboard/
│   └── malaysia_indicators.pbix  # Power BI dashboard
└── README.md
```

## 🛠️ Tech Stack
- **Python** — Data extraction and transformation
- **Apache Airflow** — Weekly pipeline scheduling
- **data.gov.my API** — Official Malaysia open data
- **Power BI** — Interactive dashboard

## 📈 Dashboard Features
- **Page 1: Fuel Price Trend** — RON95, RON97 and Diesel price trends from 2017
- **Page 2: CPI Inflation** — Malaysia inflation by category (Food, Transport, Housing etc.)
- **Page 3: Overview** — Combined view of fuel prices and CPI side by side

## 🔍 Key Insights
- RON95 remained subsidised at RM2.05 for extended periods before subsidy removal in 2024
- Diesel prices spiked significantly in 2024 following targeted subsidy removal
- CPI has been consistently rising, with Food & Transport categories showing the steepest increases

## ⚙️ How to Run
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run extract script: `python scripts/extract.py`
4. Set up Airflow DAG for weekly scheduling
5. Open `dashboard/malaysia_indicators.pbix` in Power BI Desktop

## 📦 Data Sources
- [Fuel Prices — data.gov.my](https://data.gov.my/data-catalogue/fuelprice)
- [CPI Headline — data.gov.my](https://data.gov.my/data-catalogue/cpi_headline)
