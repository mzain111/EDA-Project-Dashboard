"""
app.py — Main Streamlit Dashboard Application
EDA Dashboard Project | SAP ID: 70177906
Dataset: CoinGecko Ethereum History (ethereum.csv)
Course: Exploratory Data Analysis
Instructor: Ali Hassan Sherazi
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")

from filters import load_data, clean_data, apply_all_filters, get_kpis
from charts import (
    chart_pie_direction,
    chart_histogram_price,
    chart_line_price_trend,
    chart_bar_monthly_avg,
    chart_scatter_price_volume,
    chart_box_price_by_quarter,
    chart_heatmap_correlation,
    chart_area_market_cap,
    chart_count_day_of_week,
    chart_violin_price_quarter,
    chart_pairplot,
)

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ethereum EDA Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0D1117; color: #E6EDF3; }
    .main .block-container { padding-top: 1rem; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #21262D;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #161B22 0%, #1C2128 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 10px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #627EEA;
        font-family: 'Courier New', monospace;
    }
    .kpi-label {
        font-size: 0.75rem;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }
    .kpi-delta { font-size: 0.85rem; margin-top: 4px; }
    .positive { color: #26A69A; }
    .negative { color: #EF5350; }

    /* Section headers */
    .section-title {
        color: #627EEA;
        font-size: 1.1rem;
        font-weight: 700;
        border-bottom: 2px solid #21262D;
        padding-bottom: 8px;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Dashboard title */
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #627EEA, #F7931A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Courier New', monospace;
        letter-spacing: 3px;
    }
    .dashboard-subtitle {
        color: #8B949E;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }

    /* Chart containers */
    .chart-container {
        background: #161B22;
        border: 1px solid #21262D;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 12px;
    }

    /* Streamlit metric overrides */
    [data-testid="metric-container"] {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 12px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #627EEA, #8B6FD4);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        width: 100%;
    }

    /* Filter labels */
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stDateInput label, .stTextInput label, .stCheckbox label {
        color: #8B949E !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
</style>
""", unsafe_allow_html=True)


# ─── Load & Clean Data ────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    df = load_data("data/ethereum.csv")
    df = clean_data(df)
    return df

df_raw = get_data()

# ─── SIDEBAR FILTERS ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💎 ETH Dashboard")
    st.markdown("---")
    st.markdown("### ⚙️ FILTERS")

    # 1. Date Range Filter
    st.markdown("**📅 Date Range**")
    min_date = df_raw["date"].min().date()
    max_date = df_raw["date"].max().date()
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        start_date = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
    with col_d2:
        end_date = st.date_input("To", value=max_date, min_value=min_date, max_value=max_date)

    st.markdown("---")

    # 2. Quarter Multi-Select
    st.markdown("**📊 Quarter**")
    all_quarters = sorted(df_raw["quarter"].unique())
    selected_quarters = st.multiselect(
        "Select Quarter(s)", all_quarters, default=all_quarters, label_visibility="collapsed"
    )

    st.markdown("---")

    # 3. Numerical Range Slider — Price
    st.markdown("**💰 Price Range (USD)**")
    price_min_val = float(df_raw["price"].min())
    price_max_val = float(df_raw["price"].max())
    price_range = st.slider(
        "Price range", price_min_val, price_max_val,
        (price_min_val, price_max_val), step=50.0, label_visibility="collapsed"
    )

    st.markdown("---")

    # 4. Multi-Select — Price Direction
    st.markdown("**📈 Price Direction**")
    directions = st.multiselect(
        "Direction", ["Bullish", "Bearish", "Neutral"],
        default=["Bullish", "Bearish", "Neutral"], label_visibility="collapsed"
    )

    st.markdown("---")

    # 5. Multi-Select — Day of Week
    st.markdown("**📆 Day of Week**")
    all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    selected_days = st.multiselect(
        "Days", all_days, default=all_days, label_visibility="collapsed"
    )

    st.markdown("---")

    # 6. Search / Text Filter
    st.markdown("**🔍 Search by Date**")
    search_kw = st.text_input(
        "Keyword (e.g. '2024', 'March')", value="", label_visibility="collapsed",
        placeholder="e.g. 2024, March..."
    )

    st.markdown("---")

    # Reset Button
    if st.button("🔄 Reset All Filters"):
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='color:#8B949E;font-size:0.72rem;text-align:center;'>"
        "SAP ID: 70177906<br>Dataset: ethereum.csv<br>EDA — Ali Hassan Sherazi"
        "</div>",
        unsafe_allow_html=True,
    )


# ─── Apply Filters ────────────────────────────────────────────────────────────
df = apply_all_filters(
    df_raw,
    start_date=start_date,
    end_date=end_date,
    quarters=selected_quarters if selected_quarters else None,
    price_min=price_range[0],
    price_max=price_range[1],
    directions=directions if directions else None,
    days=selected_days if selected_days else None,
    search_keyword=search_kw,
)

kpis = get_kpis(df)

# ─── DASHBOARD HEADER ─────────────────────────────────────────────────────────
st.markdown(
    '<div class="dashboard-title">⬡ ETHEREUM ANALYTICS DASHBOARD</div>'
    '<div class="dashboard-subtitle">Exploratory Data Analysis · CoinGecko ETH History · SAP 70177906</div>',
    unsafe_allow_html=True,
)
st.markdown("")

if df.empty:
    st.warning("⚠️ No data matches the current filters. Please adjust your selections.")
    st.stop()

# ─── KPI SUMMARY CARDS ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)

def kpi_card(col, value, label, delta=None, delta_label=""):
    with col:
        delta_html = ""
        if delta is not None:
            cls = "positive" if delta >= 0 else "negative"
            sign = "▲" if delta >= 0 else "▼"
            delta_html = f'<div class="kpi-delta {cls}">{sign} {abs(delta):.1f}% {delta_label}</div>'
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-label">{label}</div>'
            f'{delta_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

kpi_card(c1, f"${kpis.get('avg_price', 0):,.0f}", "Avg Price (USD)")
kpi_card(c2, f"${kpis.get('max_price', 0):,.0f}", "All-Time High")
kpi_card(c3, f"${kpis.get('min_price', 0):,.0f}", "All-Time Low")
kpi_card(c4, f"${kpis.get('avg_market_cap_b', 0):,.0f}B", "Avg Market Cap")
kpi_card(c5, f"{kpis.get('total_records', 0):,}", "Trading Days",
         delta=kpis.get('total_return_pct', 0), delta_label="Return")
kpi_card(c6, f"{kpis.get('bullish_days', 0)} / {kpis.get('bearish_days', 0)}", "Bull / Bear Days")

st.markdown("")

# ─── ROW 1: Line Chart + Pie Chart ────────────────────────────────────────────
st.markdown('<div class="section-title">📈 Price Trends & Distribution</div>', unsafe_allow_html=True)
col_l, col_r = st.columns([3, 1])

with col_l:
    st.markdown("**ETH Price Over Time with Moving Averages**")
    st.pyplot(chart_line_price_trend(df), use_container_width=True)

with col_r:
    st.markdown("**Daily Price Direction**")
    st.pyplot(chart_pie_direction(df), use_container_width=True)

# ─── ROW 2: Area Chart ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Market Cap & Volume Trends</div>', unsafe_allow_html=True)
st.pyplot(chart_area_market_cap(df), use_container_width=True)

# ─── ROW 3: Histogram + Bar Chart ─────────────────────────────────────────────
st.markdown('<div class="section-title">📉 Frequency & Monthly Analysis</div>', unsafe_allow_html=True)
col3a, col3b = st.columns(2)
with col3a:
    st.markdown("**Price Frequency Histogram**")
    st.pyplot(chart_histogram_price(df), use_container_width=True)
with col3b:
    st.markdown("**Average Price by Month**")
    st.pyplot(chart_bar_monthly_avg(df), use_container_width=True)

# ─── ROW 4: Scatter + Box Plot ────────────────────────────────────────────────
st.markdown('<div class="section-title">🔬 Relationships & Spread Analysis</div>', unsafe_allow_html=True)
col4a, col4b = st.columns(2)
with col4a:
    st.markdown("**Price vs Volume Scatter**")
    st.pyplot(chart_scatter_price_volume(df), use_container_width=True)
with col4b:
    st.markdown("**Price Spread by Quarter (Box Plot)**")
    st.pyplot(chart_box_price_by_quarter(df), use_container_width=True)

# ─── ROW 5: Heatmap ───────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🌡️ Correlation Heatmap</div>', unsafe_allow_html=True)
st.pyplot(chart_heatmap_correlation(df), use_container_width=True)

# ─── ROW 6: Count Plot + Violin Plot ──────────────────────────────────────────
st.markdown('<div class="section-title">🎻 Weekly Patterns & Price Density</div>', unsafe_allow_html=True)
col6a, col6b = st.columns(2)
with col6a:
    st.markdown("**Records & Avg Price by Day of Week**")
    st.pyplot(chart_count_day_of_week(df), use_container_width=True)
with col6b:
    st.markdown("**Price Distribution by Quarter (Violin)**")
    st.pyplot(chart_violin_price_quarter(df), use_container_width=True)

# ─── BONUS: Pair Plot ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">⭐ Bonus — Pair Plot Analysis</div>', unsafe_allow_html=True)
with st.expander("Show Pair Plot (may take a moment to render)"):
    sample_df = df.sample(min(300, len(df)), random_state=42)
    st.pyplot(chart_pairplot(sample_df), use_container_width=True)

# ─── RAW DATA TABLE ───────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Filtered Data Preview</div>', unsafe_allow_html=True)
display_cols = ["date", "open", "high", "low", "close", "price",
                "total_volume", "market_cap", "price_change_pct",
                "price_direction", "quarter", "day_of_week",
                "rolling_7d_avg", "rolling_30d_avg"]
display_cols = [c for c in display_cols if c in df.columns]

col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.markdown(f"**Showing {len(df):,} records** from {kpis.get('date_range_start','')} to {kpis.get('date_range_end','')}")
with col_t2:
    st.download_button(
        "⬇️ Download Filtered CSV",
        data=df[display_cols].to_csv(index=False).encode("utf-8"),
        file_name="ethereum_filtered.csv",
        mime="text/csv",
    )

st.dataframe(
    df[display_cols].sort_values("date", ascending=False).head(50),
    use_container_width=True,
    height=300,
)

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#8B949E;font-size:0.8rem;'>"
    "EDA Dashboard · SAP ID: 70177906 · Dataset: ethereum.csv · "
    "Course: Exploratory Data Analysis · Instructor: Ali Hassan Sherazi"
    "</div>",
    unsafe_allow_html=True,
)
