# 💎 Ethereum EDA Dashboard

**SAP ID:** 70177906  
**Dataset:** `ethereum.csv` (CoinGecko Ethereum History)  
**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Submission Date:** 05-June-2026  

---

## 📁 Project Structure

```
dashboard_project/
├── data/
│   └── ethereum.csv          ← Dataset (DO NOT RENAME)
├── notebooks/
│   └── analysis.ipynb        ← EDA notebook
├── app.py                    ← Main Streamlit dashboard
├── charts.py                 ← All chart functions (10 chart types)
├── filters.py                ← Data loading, cleaning, filtering
├── requirements.txt          ← Python dependencies
└── README.md                 ← This file
```

---

## ⚙️ Installation & Setup

### Step 1 — Clone / Extract the project
```bash
cd dashboard_project
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the dashboard
```bash
streamlit run app.py
```

The dashboard will open automatically at **http://localhost:8501**

---

## 📊 Dataset Overview

| Feature | Description |
|---|---|
| `date` | Trading date |
| `open` | Opening price (USD) |
| `high` | Highest price of the day (USD) |
| `low` | Lowest price of the day (USD) |
| `close` | Closing price (USD) |
| `price` | Daily closing price (USD) |
| `total_volume` | Daily trading volume (USD) |
| `market_cap` | Market capitalization (USD) |
| `price_change_pct` | Daily % price change |
| `rolling_7d_avg` | 7-day moving average |
| `rolling_30d_avg` | 30-day moving average |
| `volatility_7d` | 7-day rolling standard deviation |
| `price_direction` | Bullish / Bearish / Neutral |
| `quarter` | Q1 / Q2 / Q3 / Q4 |
| `day_of_week` | Monday – Sunday |

---

## 📈 Charts Implemented (All 10 Required)

| # | Chart Type | Purpose |
|---|---|---|
| 1 | **Pie Chart** | Price direction distribution (Bullish/Bearish/Neutral) |
| 2 | **Histogram** | Price frequency distribution |
| 3 | **Line Chart** | Price trend with 7-day & 30-day moving averages |
| 4 | **Bar Chart** | Average ETH price by month |
| 5 | **Scatter Plot** | Price vs. daily trading volume |
| 6 | **Box Plot** | Price spread and outliers by quarter |
| 7 | **Heatmap** | Correlation matrix of all numerical features |
| 8 | **Area Chart** | Market cap and volume cumulative trends |
| 9 | **Count Plot** | Record count and avg price by day of week |
| 10 | **Violin Plot** | Price distribution density by quarter |
| ⭐ | **Pair Plot** | Multi-variable relationship (bonus) |

---

## 🔍 Dashboard Filters

| Filter | Type | Description |
|---|---|---|
| Date Range | Date Picker | Filter by start and end date |
| Quarter | Multi-Select | Q1, Q2, Q3, Q4 |
| Price Range | Range Slider | Min–Max price filter |
| Price Direction | Multi-Select | Bullish / Bearish / Neutral |
| Day of Week | Multi-Select | Monday–Sunday |
| Search | Text Input | Filter by keyword in date column |
| Reset | Button | Clears all filters |

> All filters are **dynamically linked** — every chart updates simultaneously.

---

## 💡 Key Insights

1. **ETH Price Trend**: Ethereum prices rose significantly from ~$1,800 in mid-2023 to ~$3,500 by mid-2024, driven by the ETH ETF anticipation.
2. **Bullish Bias**: More bullish days than bearish over the period, confirming the overall uptrend.
3. **Volume-Price Relationship**: Higher trading volume correlates with price spikes and dips (high volatility days).
4. **Market Cap**: Market cap closely tracks price due to near-constant circulating supply (~120M ETH).
5. **Q4 Strength**: Q4 historically shows higher average prices — classic crypto seasonality pattern.
6. **Day-of-Week Effect**: Weekend trading shows slightly lower volume but similar price levels.
7. **Volatility**: 7-day rolling volatility peaks coincide with major market events.

---

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| Python 3.x | Core language |
| Pandas | Data loading, cleaning, filtering |
| NumPy | Numerical operations |
| Matplotlib | Chart creation |
| Seaborn | Statistical visualizations |
| Streamlit | Interactive dashboard frontend |

---

*EDA Dashboard Project · SAP ID: 70177906 · Exploratory Data Analysis*
