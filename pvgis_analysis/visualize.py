"""
Visualization: all plots saved to figures/.
"""

import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

FIGURES_DIR = pathlib.Path(__file__).parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", font_scale=1.1)


def _save(fig, name: str):
    path = FIGURES_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path}")


# ---------------------------------------------------------------------------
# Q1 / Q2: Tilt map + tilt vs. latitude scatter
# ---------------------------------------------------------------------------

def plot_tilt_map(df: pd.DataFrame):
    """Scatter map of optimal tilt across Europe (colour = tilt angle)."""
    fig, ax = plt.subplots(figsize=(12, 7))

    sc = ax.scatter(
        df["lon"], df["lat"],
        c=df["optimal_tilt"], cmap="plasma",
        s=60, marker="s", linewidths=0,
        vmin=df["optimal_tilt"].min(), vmax=df["optimal_tilt"].max(),
    )
    cbar = fig.colorbar(sc, ax=ax, shrink=0.8)
    cbar.set_label("Optimal tilt angle (°)")

    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("Optimal PV tilt angle across Europe")
    ax.set_xlim(-12, 35)
    ax.set_ylim(34, 73)
    _save(fig, "q1_tilt_map.png")


def plot_tilt_vs_lat(fit_result: dict):
    """Scatter of optimal tilt vs. latitude with linear and quadratic fits."""
    lat  = fit_result["lat"]
    tilt = fit_result["tilt"]
    lin  = fit_result["tilt_pred_lin"]
    quad = fit_result["tilt_pred_quad"]
    r2_l = fit_result["r2_linear"]
    r2_q = fit_result["r2_quad"]
    a, b = fit_result["linear_a"], fit_result["linear_b"]

    lat_sort = np.argsort(lat)
    lat_s  = lat[lat_sort]
    lin_s  = lin[lat_sort]
    quad_s = quad[lat_sort]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(lat, tilt, s=15, alpha=0.4, color="steelblue", label="Grid points")
    ax.plot(lat_s, lin_s,  color="crimson",  lw=2,
            label=f"Linear fit:  tilt = {a:.3f}·lat {'+' if b >= 0 else ''}{b:.2f}°  (R²={r2_l:.3f})")
    ax.plot(lat_s, quad_s, color="darkorange", lw=2, linestyle="--",
            label=f"Quadratic fit  (R²={r2_q:.3f})")

    ax.set_xlabel("Latitude (°N)")
    ax.set_ylabel("Optimal tilt angle (°)")
    ax.set_title("Optimal PV tilt vs. latitude — Europe")
    ax.legend()
    _save(fig, "q2_tilt_vs_lat.png")


# ---------------------------------------------------------------------------
# Q4: Tracker gain map + bar chart by country
# ---------------------------------------------------------------------------

def plot_tracker_gain_map(valid_df: pd.DataFrame):
    """Scatter map of single-axis tracker gain % across Europe."""
    fig, ax = plt.subplots(figsize=(12, 7))

    sc = ax.scatter(
        valid_df["lon"], valid_df["lat"],
        c=valid_df["gain_pct"], cmap="YlOrRd",
        s=60, marker="s", linewidths=0,
        vmin=valid_df["gain_pct"].min(), vmax=valid_df["gain_pct"].max(),
    )
    cbar = fig.colorbar(sc, ax=ax, shrink=0.8)
    cbar.set_label("Tracker gain over fixed tilt (%)")

    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("Single-axis tracker energy gain across Europe")
    ax.set_xlim(-12, 35)
    ax.set_ylim(34, 73)
    _save(fig, "q4_tracker_gain_map.png")


def plot_tracker_gain_by_country(by_country: pd.DataFrame):
    """Horizontal bar chart of mean tracker gain by country."""
    data = by_country[by_country["count"] >= 2].sort_values("mean")

    fig, ax = plt.subplots(figsize=(10, max(6, len(data) * 0.35)))

    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.9, len(data)))
    bars = ax.barh(data.index, data["mean"], color=colors, edgecolor="white")

    # Error bars showing min–max range
    xerr_lo = data["mean"] - data["min"]
    xerr_hi = data["max"] - data["mean"]
    ax.errorbar(
        data["mean"], range(len(data)),
        xerr=[xerr_lo, xerr_hi],
        fmt="none", color="black", capsize=3, lw=1,
    )

    ax.set_xlabel("Mean tracker gain over fixed tilt (%)")
    ax.set_title("Single-axis tracker gain by country\n(error bars = min–max range)")
    ax.axvline(data["mean"].mean(), color="navy", linestyle="--", lw=1.5, label="EU mean")
    ax.legend()
    _save(fig, "q4_tracker_gain_by_country.png")


# ---------------------------------------------------------------------------
# Q5: City comparison
# ---------------------------------------------------------------------------

def plot_city_comparison(df: pd.DataFrame, annual_col: str = "annual_irr"):
    """
    Grouped bar chart of annual solar irradiation per city, grouped and coloured by country.
    Poland reference band highlighted.
    """
    if annual_col not in df.columns:
        print("  annual_irr column not found, skipping city comparison plot")
        return

    df_sorted = df.sort_values(["country", annual_col])
    countries = df_sorted["country"].unique()

    # Assign a colour per country
    palette = sns.color_palette("tab20", len(countries))
    color_map = dict(zip(countries, palette))
    # Highlight Poland
    if "Poland" in color_map:
        color_map["Poland"] = (0.82, 0.10, 0.10)

    fig, ax = plt.subplots(figsize=(18, 7))

    x = 0
    x_ticks = []
    x_labels = []
    group_centers = {}

    for country in sorted(countries):
        group = df_sorted[df_sorted["country"] == country]
        xs = []
        for _, row in group.iterrows():
            ax.bar(x, row[annual_col], color=color_map[country], edgecolor="white", width=0.8)
            xs.append(x)
            x_labels.append(row["city"])
            x_ticks.append(x)
            x += 1
        group_centers[country] = np.mean(xs)
        x += 0.8  # gap between countries

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=75, ha="right", fontsize=8)
    ax.set_ylabel("Annual irradiation (kWh/m²/year)")
    ax.set_title("Annual solar irradiation by city — European comparison")

    # Country labels above the bars
    ymax = df_sorted[annual_col].max()
    for country, cx in group_centers.items():
        ax.text(cx, ymax * 1.01, country, ha="center", va="bottom", fontsize=7.5,
                color=color_map.get(country, "black"), fontweight="bold", rotation=30)

    _save(fig, "q5_city_comparison.png")


def plot_poland_vs_europe(by_country: pd.DataFrame):
    """
    Bar chart comparing country means with Poland highlighted,
    and coefficient of variation shown.
    """
    data = by_country.sort_values("mean", ascending=False)

    colors = ["crimson" if c == "Poland" else "steelblue" for c in data.index]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Left: mean annual irradiation
    axes[0].barh(data.index[::-1], data["mean"][::-1], color=colors[::-1], edgecolor="white")
    axes[0].set_xlabel("Mean annual irradiation (kWh/m²/year)")
    axes[0].set_title("Mean solar energy by country")

    # Right: coefficient of variation (uniformity)
    cv_data = data[data["count"] >= 2].sort_values("cv_pct", ascending=False)
    cv_colors = ["crimson" if c == "Poland" else "steelblue" for c in cv_data.index]
    axes[1].barh(cv_data.index[::-1], cv_data["cv_pct"][::-1], color=cv_colors[::-1], edgecolor="white")
    axes[1].set_xlabel("Coefficient of variation (%)")
    axes[1].set_title("Within-country solar uniformity\n(lower = more uniform)")

    fig.suptitle("European solar energy comparison — Poland highlighted in red", fontsize=13)
    plt.tight_layout()
    _save(fig, "q5_poland_vs_europe.png")
