"""
charts.py — Chart & Visualization Functions
EDA Dashboard Project | SAP ID: 70177906
Dataset: CoinGecko Ethereum History

All 10 required chart types:
  1. Pie Chart       – Price direction distribution
  2. Histogram       – Price frequency distribution
  3. Line Chart      – Price trend over time
  4. Bar Chart       – Avg price by month
  5. Scatter Plot    – Price vs Volume
  6. Box Plot        – Price spread by quarter
  7. Heatmap         – Correlation matrix
  8. Area Chart      – Cumulative market cap over time
  9. Count Plot      – Day-of-week frequency
  10. Violin Plot    – Price distribution by quarter
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np

# ─── Global Style ─────────────────────────────────────────────────────────────
PALETTE_MAIN  = "#627EEA"   # Ethereum blue
PALETTE_SEC   = "#F7931A"   # Gold accent
PALETTE_POS   = "#26A69A"   # Bullish green
PALETTE_NEG   = "#EF5350"   # Bearish red
PALETTE_NEU   = "#78909C"   # Neutral grey
BG_COLOR      = "#0D1117"
PANEL_COLOR   = "#161B22"
TEXT_COLOR    = "#E6EDF3"
GRID_COLOR    = "#21262D"

ETH_PALETTE   = [PALETTE_MAIN, PALETTE_SEC, PALETTE_POS, PALETTE_NEG,
                 "#9B59B6", "#1ABC9C", "#E67E22", "#3498DB"]

def _apply_dark_style(fig, ax_or_axes, title: str = ""):
    """Apply consistent dark crypto-style theme to any figure."""
    fig.patch.set_facecolor(BG_COLOR)
    axes = ax_or_axes if isinstance(ax_or_axes, (list, np.ndarray)) else [ax_or_axes]
    for ax in np.array(axes).flatten():
        ax.set_facecolor(PANEL_COLOR)
        ax.tick_params(colors=TEXT_COLOR, labelsize=9)
        ax.xaxis.label.set_color(TEXT_COLOR)
        ax.yaxis.label.set_color(TEXT_COLOR)
        for spine in ax.spines.values():
            spine.set_color(GRID_COLOR)
        ax.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.7)
        if title:
            ax.set_title(title, color=TEXT_COLOR, fontsize=13, fontweight="bold", pad=12)
    return fig


# ─── 1. PIE CHART ─────────────────────────────────────────────────────────────
def chart_pie_direction(df: pd.DataFrame):
    """Pie chart: Bullish / Bearish / Neutral day distribution."""
    counts = df["price_direction"].value_counts()
    colors = [PALETTE_POS if x == "Bullish" else PALETTE_NEG if x == "Bearish" else PALETTE_NEU
              for x in counts.index]

    fig, ax = plt.subplots(figsize=(6, 5))
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops={"edgecolor": BG_COLOR, "linewidth": 2},
        pctdistance=0.80,
    )
    for t in texts:
        t.set_color(TEXT_COLOR); t.set_fontsize(11)
    for at in autotexts:
        at.set_color(TEXT_COLOR); at.set_fontsize(9); at.set_fontweight("bold")
    ax.set_title("Daily Price Direction Distribution", color=TEXT_COLOR,
                 fontsize=13, fontweight="bold", pad=15)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    plt.tight_layout()
    return fig


# ─── 2. HISTOGRAM ─────────────────────────────────────────────────────────────
def chart_histogram_price(df: pd.DataFrame):
    """Histogram: Frequency distribution of ETH closing price."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["price"], bins=30, color=PALETTE_MAIN, edgecolor=BG_COLOR,
            alpha=0.85, linewidth=0.8)
    ax.axvline(df["price"].mean(), color=PALETTE_SEC, linewidth=2,
               linestyle="--", label=f"Mean: ${df['price'].mean():,.0f}")
    ax.axvline(df["price"].median(), color=PALETTE_POS, linewidth=2,
               linestyle=":", label=f"Median: ${df['price'].median():,.0f}")
    ax.set_xlabel("Price (USD)", color=TEXT_COLOR)
    ax.set_ylabel("Frequency (Days)", color=TEXT_COLOR)
    legend = ax.legend(facecolor=PANEL_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    _apply_dark_style(fig, ax, "ETH Price Frequency Distribution")
    plt.tight_layout()
    return fig


# ─── 3. LINE CHART ────────────────────────────────────────────────────────────
def chart_line_price_trend(df: pd.DataFrame):
    """Line chart: ETH price over time with 7-day and 30-day moving averages."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date"], df["price"], color=PALETTE_MAIN, linewidth=1.2,
            alpha=0.7, label="Daily Close")
    if "rolling_7d_avg" in df.columns:
        ax.plot(df["date"], df["rolling_7d_avg"], color=PALETTE_SEC,
                linewidth=1.8, label="7-Day MA")
    if "rolling_30d_avg" in df.columns:
        ax.plot(df["date"], df["rolling_30d_avg"], color=PALETTE_POS,
                linewidth=2, label="30-Day MA")
    ax.set_xlabel("Date", color=TEXT_COLOR)
    ax.set_ylabel("Price (USD)", color=TEXT_COLOR)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)
    legend = ax.legend(facecolor=PANEL_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    _apply_dark_style(fig, ax, "Ethereum Price Trend Over Time")
    plt.tight_layout()
    return fig


# ─── 4. BAR CHART ─────────────────────────────────────────────────────────────
def chart_bar_monthly_avg(df: pd.DataFrame):
    """Bar chart: Average ETH price by month."""
    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    monthly = df.groupby("month")["price"].mean().reindex(
        [m for m in month_order if m in df["month"].unique()]
    ).reset_index()
    monthly.columns = ["month", "avg_price"]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(monthly["month"], monthly["avg_price"],
                  color=PALETTE_MAIN, edgecolor=BG_COLOR, linewidth=0.8)
    for bar, val in zip(bars, monthly["avg_price"]):
        bar.set_color(plt.cm.Blues(0.4 + 0.6 * (val - monthly["avg_price"].min()) /
                                   (monthly["avg_price"].max() - monthly["avg_price"].min() + 1)))
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
                f"${val:,.0f}", ha="center", va="bottom",
                color=TEXT_COLOR, fontsize=8, fontweight="bold")
    ax.set_xlabel("Month", color=TEXT_COLOR)
    ax.set_ylabel("Average Price (USD)", color=TEXT_COLOR)
    plt.xticks(rotation=35, ha="right")
    _apply_dark_style(fig, ax, "Average ETH Price by Month")
    plt.tight_layout()
    return fig


# ─── 5. SCATTER PLOT ──────────────────────────────────────────────────────────
def chart_scatter_price_volume(df: pd.DataFrame):
    """Scatter plot: Price vs Daily Volume colored by quarter."""
    quarters = df["quarter"].unique()
    colors_map = dict(zip(sorted(quarters), ETH_PALETTE))

    fig, ax = plt.subplots(figsize=(8, 5))
    for q in sorted(quarters):
        sub = df[df["quarter"] == q]
        ax.scatter(sub["total_volume"] / 1e9, sub["price"],
                   c=colors_map[q], label=q, alpha=0.6, s=25, edgecolors="none")
    ax.set_xlabel("Daily Volume (Billion USD)", color=TEXT_COLOR)
    ax.set_ylabel("Price (USD)", color=TEXT_COLOR)
    legend = ax.legend(title="Quarter", facecolor=PANEL_COLOR, edgecolor=GRID_COLOR,
                       labelcolor=TEXT_COLOR, title_fontsize=9)
    legend.get_title().set_color(TEXT_COLOR)
    _apply_dark_style(fig, ax, "ETH Price vs Daily Trading Volume")
    plt.tight_layout()
    return fig


# ─── 6. BOX PLOT ──────────────────────────────────────────────────────────────
def chart_box_price_by_quarter(df: pd.DataFrame):
    """Box plot: ETH price spread by quarter."""
    fig, ax = plt.subplots(figsize=(8, 5))
    quarters_sorted = sorted(df["quarter"].unique())
    data_by_q = [df[df["quarter"] == q]["price"].values for q in quarters_sorted]

    bp = ax.boxplot(data_by_q, labels=quarters_sorted, patch_artist=True,
                    medianprops={"color": PALETTE_SEC, "linewidth": 2},
                    whiskerprops={"color": TEXT_COLOR},
                    capprops={"color": TEXT_COLOR},
                    flierprops={"markerfacecolor": PALETTE_NEG, "marker": "o",
                                "markersize": 4, "alpha": 0.5})
    for patch, color in zip(bp["boxes"], ETH_PALETTE):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
        patch.set_edgecolor(TEXT_COLOR)
    ax.set_xlabel("Quarter", color=TEXT_COLOR)
    ax.set_ylabel("Price (USD)", color=TEXT_COLOR)
    _apply_dark_style(fig, ax, "ETH Price Distribution by Quarter (Box Plot)")
    plt.tight_layout()
    return fig


# ─── 7. HEATMAP ───────────────────────────────────────────────────────────────
def chart_heatmap_correlation(df: pd.DataFrame):
    """Heatmap: Correlation matrix of numerical features."""
    num_cols = ["price", "open", "high", "low", "total_volume", "market_cap",
                "price_change_pct", "rolling_7d_avg", "rolling_30d_avg", "volatility_7d"]
    num_cols = [c for c in num_cols if c in df.columns]
    corr = df[num_cols].corr()

    labels = {
        "price": "Price", "open": "Open", "high": "High", "low": "Low",
        "total_volume": "Volume", "market_cap": "Mkt Cap",
        "price_change_pct": "Chg%", "rolling_7d_avg": "MA-7",
        "rolling_30d_avg": "MA-30", "volatility_7d": "Volatility"
    }
    corr.index = [labels.get(c, c) for c in corr.index]
    corr.columns = [labels.get(c, c) for c in corr.columns]

    fig, ax = plt.subplots(figsize=(9, 7))
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap=cmap,
                center=0, ax=ax, linewidths=0.5, linecolor=BG_COLOR,
                annot_kws={"size": 8, "color": TEXT_COLOR},
                cbar_kws={"shrink": 0.8})
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)
    ax.set_title("Feature Correlation Heatmap", color=TEXT_COLOR,
                 fontsize=13, fontweight="bold", pad=12)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(PANEL_COLOR)
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color=TEXT_COLOR)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT_COLOR)
    plt.xticks(rotation=35, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    return fig


# ─── 8. AREA CHART ────────────────────────────────────────────────────────────
def chart_area_market_cap(df: pd.DataFrame):
    """Area chart: Market cap and volume over time."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    ax1.fill_between(df["date"], df["market_cap"] / 1e9, alpha=0.6,
                     color=PALETTE_MAIN, label="Market Cap (B USD)")
    ax1.plot(df["date"], df["market_cap"] / 1e9, color=PALETTE_MAIN, linewidth=1)
    ax1.set_ylabel("Market Cap (B USD)", color=TEXT_COLOR)
    ax1.legend(facecolor=PANEL_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

    ax2.fill_between(df["date"], df["total_volume"] / 1e9, alpha=0.6,
                     color=PALETTE_SEC, label="Daily Volume (B USD)")
    ax2.plot(df["date"], df["total_volume"] / 1e9, color=PALETTE_SEC, linewidth=1)
    ax2.set_ylabel("Volume (B USD)", color=TEXT_COLOR)
    ax2.set_xlabel("Date", color=TEXT_COLOR)
    ax2.legend(facecolor=PANEL_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)

    fig.suptitle("Market Cap & Volume Trends (Area Chart)",
                 color=TEXT_COLOR, fontsize=13, fontweight="bold", y=1.01)
    _apply_dark_style(fig, [ax1, ax2])
    plt.tight_layout()
    return fig


# ─── 9. COUNT PLOT ────────────────────────────────────────────────────────────
def chart_count_day_of_week(df: pd.DataFrame):
    """Count plot: Records and avg price by day of week."""
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    day_counts = df["day_of_week"].value_counts().reindex(day_order).fillna(0)
    day_avg    = df.groupby("day_of_week")["price"].mean().reindex(day_order)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    colors = [ETH_PALETTE[i % len(ETH_PALETTE)] for i in range(len(day_order))]
    ax1.bar(day_order, day_counts.values, color=colors, edgecolor=BG_COLOR, linewidth=0.8)
    ax1.set_xlabel("Day of Week", color=TEXT_COLOR)
    ax1.set_ylabel("Count (Days)", color=TEXT_COLOR)
    ax1.set_title("Record Count by Day of Week", color=TEXT_COLOR,
                  fontsize=12, fontweight="bold")
    plt.setp(ax1.get_xticklabels(), rotation=35, ha="right")

    ax2.bar(day_order, day_avg.values, color=colors, edgecolor=BG_COLOR, linewidth=0.8)
    ax2.set_xlabel("Day of Week", color=TEXT_COLOR)
    ax2.set_ylabel("Avg Price (USD)", color=TEXT_COLOR)
    ax2.set_title("Average ETH Price by Day of Week", color=TEXT_COLOR,
                  fontsize=12, fontweight="bold")
    plt.setp(ax2.get_xticklabels(), rotation=35, ha="right")

    _apply_dark_style(fig, [ax1, ax2])
    plt.tight_layout()
    return fig


# ─── 10. VIOLIN PLOT ──────────────────────────────────────────────────────────
def chart_violin_price_quarter(df: pd.DataFrame):
    """Violin plot: Price distribution and density by quarter."""
    fig, ax = plt.subplots(figsize=(9, 5))
    quarters = sorted(df["quarter"].unique())
    data_by_q = [df[df["quarter"] == q]["price"].values for q in quarters]

    parts = ax.violinplot(data_by_q, positions=range(len(quarters)),
                          showmeans=True, showmedians=True, showextrema=True)
    for i, (pc, color) in enumerate(zip(parts["bodies"], ETH_PALETTE)):
        pc.set_facecolor(color)
        pc.set_alpha(0.65)
        pc.set_edgecolor(TEXT_COLOR)
        pc.set_linewidth(0.8)
    for part in ["cmedians", "cmeans", "cbars", "cmins", "cmaxes"]:
        if part in parts:
            parts[part].set_color(TEXT_COLOR)
            parts[part].set_linewidth(1.2)

    ax.set_xticks(range(len(quarters)))
    ax.set_xticklabels(quarters)
    ax.set_xlabel("Quarter", color=TEXT_COLOR)
    ax.set_ylabel("Price (USD)", color=TEXT_COLOR)
    _apply_dark_style(fig, ax, "ETH Price Distribution by Quarter (Violin)")
    plt.tight_layout()
    return fig


# ─── BONUS: Pair Plot ─────────────────────────────────────────────────────────
def chart_pairplot(df: pd.DataFrame):
    """Bonus pair plot for selected numerical features."""
    cols = ["price", "total_volume", "market_cap", "price_change_pct"]
    cols = [c for c in cols if c in df.columns]
    sub = df[cols + ["price_direction"]].copy()
    sub["total_volume"] = sub["total_volume"] / 1e9
    sub["market_cap"]   = sub["market_cap"]   / 1e9
    sub.columns = ["Price", "Volume(B)", "Mkt Cap(B)", "Chg%", "Direction"]

    palette = {"Bullish": PALETTE_POS, "Bearish": PALETTE_NEG, "Neutral": PALETTE_NEU}
    g = sns.pairplot(sub, hue="Direction", palette=palette,
                     plot_kws={"alpha": 0.5, "s": 15},
                     diag_kind="kde", corner=True)
    g.figure.patch.set_facecolor(BG_COLOR)
    for ax in g.axes.flatten():
        if ax:
            ax.set_facecolor(PANEL_COLOR)
            ax.tick_params(colors=TEXT_COLOR, labelsize=7)
            ax.xaxis.label.set_color(TEXT_COLOR)
            ax.yaxis.label.set_color(TEXT_COLOR)
            for spine in ax.spines.values():
                spine.set_color(GRID_COLOR)
    g.figure.suptitle("Pair Plot — Key ETH Features", color=TEXT_COLOR,
                       fontsize=13, fontweight="bold", y=1.02)
    return g.figure
