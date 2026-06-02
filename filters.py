"""
filters.py — Filter & Data Processing Functions
EDA Dashboard Project | SAP ID: 70177906
Dataset: CoinGecko Ethereum History
"""

import pandas as pd
import numpy as np


def load_data(filepath: str = "data/ethereum.csv") -> pd.DataFrame:
    """Load and return the Ethereum dataset."""
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the Ethereum dataset.
    - Drop rows with null prices
    - Ensure correct dtypes
    - Add derived columns
    """
    df = df.copy()

    # Drop rows where core financial columns are missing
    df.dropna(subset=["price", "total_volume", "market_cap"], inplace=True)

    # Ensure date is datetime
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"])

    # Fill rolling averages NaN (first rows) with price
    for col in ["rolling_7d_avg", "rolling_30d_avg", "volatility_7d"]:
        if col in df.columns:
            df[col] = df[col].fillna(df["price"])

    # Add useful derived columns if not present
    if "month" not in df.columns:
        df["month"] = df["date"].dt.month_name()
    if "year" not in df.columns:
        df["year"] = df["date"].dt.year
    if "quarter" not in df.columns:
        df["quarter"] = df["date"].dt.quarter.map(
            {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}
        )
    if "day_of_week" not in df.columns:
        df["day_of_week"] = df["date"].dt.day_name()
    if "price_change_pct" not in df.columns:
        df["price_change_pct"] = df["price"].pct_change() * 100

    # Categorize daily return
    df["price_direction"] = df["price_change_pct"].apply(
        lambda x: "Bullish" if x > 0 else ("Bearish" if x < 0 else "Neutral")
    )

    # Volume category
    vol_mean = df["total_volume"].mean()
    vol_std = df["total_volume"].std()
    df["volume_category"] = pd.cut(
        df["total_volume"],
        bins=[0, vol_mean - vol_std, vol_mean + vol_std, float("inf")],
        labels=["Low", "Medium", "High"],
    )

    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# ─── Filter Functions ─────────────────────────────────────────────────────────

def filter_by_date(df: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    """Filter DataFrame by date range."""
    return df[(df["date"] >= pd.Timestamp(start_date)) & (df["date"] <= pd.Timestamp(end_date))]


def filter_by_quarter(df: pd.DataFrame, quarters: list) -> pd.DataFrame:
    """Filter by selected quarters (e.g. ['Q1', 'Q3'])."""
    if not quarters:
        return df
    return df[df["quarter"].isin(quarters)]


def filter_by_price_range(df: pd.DataFrame, min_price: float, max_price: float) -> pd.DataFrame:
    """Filter by price range."""
    return df[(df["price"] >= min_price) & (df["price"] <= max_price)]


def filter_by_direction(df: pd.DataFrame, directions: list) -> pd.DataFrame:
    """Filter by price direction: Bullish / Bearish / Neutral."""
    if not directions:
        return df
    return df[df["price_direction"].isin(directions)]


def filter_by_day_of_week(df: pd.DataFrame, days: list) -> pd.DataFrame:
    """Filter by selected days of the week."""
    if not days:
        return df
    return df[df["day_of_week"].isin(days)]


def search_by_date_text(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """Filter rows where date string contains keyword (e.g. '2024', 'March')."""
    if not keyword.strip():
        return df
    keyword_lower = keyword.lower()
    mask = df["date"].astype(str).str.lower().str.contains(keyword_lower, na=False)
    return df[mask]


def apply_all_filters(
    df: pd.DataFrame,
    start_date=None,
    end_date=None,
    quarters=None,
    price_min=None,
    price_max=None,
    directions=None,
    days=None,
    search_keyword="",
) -> pd.DataFrame:
    """Apply all active filters and return filtered DataFrame."""
    filtered = df.copy()

    if start_date and end_date:
        filtered = filter_by_date(filtered, start_date, end_date)

    if quarters:
        filtered = filter_by_quarter(filtered, quarters)

    if price_min is not None and price_max is not None:
        filtered = filter_by_price_range(filtered, price_min, price_max)

    if directions:
        filtered = filter_by_direction(filtered, directions)

    if days:
        filtered = filter_by_day_of_week(filtered, days)

    if search_keyword:
        filtered = search_by_date_text(filtered, search_keyword)

    return filtered


# ─── Summary / KPI Helpers ────────────────────────────────────────────────────

def get_kpis(df: pd.DataFrame) -> dict:
    """Return a dict of key KPI metrics from the filtered dataset."""
    if df.empty:
        return {}
    return {
        "total_records": len(df),
        "avg_price": df["price"].mean(),
        "max_price": df["price"].max(),
        "min_price": df["price"].min(),
        "avg_volume_b": df["total_volume"].mean() / 1e9,
        "max_volume_b": df["total_volume"].max() / 1e9,
        "avg_market_cap_b": df["market_cap"].mean() / 1e9,
        "bullish_days": (df["price_direction"] == "Bullish").sum(),
        "bearish_days": (df["price_direction"] == "Bearish").sum(),
        "date_range_start": df["date"].min().strftime("%b %d, %Y"),
        "date_range_end": df["date"].max().strftime("%b %d, %Y"),
        "total_return_pct": (
            (df["price"].iloc[-1] - df["price"].iloc[0]) / df["price"].iloc[0] * 100
            if len(df) > 1 else 0
        ),
    }
