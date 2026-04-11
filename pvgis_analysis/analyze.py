"""
Analysis functions for all 5 research questions.
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
from config import POLAND_LAT_MIN, POLAND_LAT_MAX, POLAND_LON_MIN, POLAND_LON_MAX


# ---------------------------------------------------------------------------
# Q1: Optimal tilt range across Europe + dominant geographic parameter
# ---------------------------------------------------------------------------

def tilt_range_analysis(df: pd.DataFrame) -> dict:
    """
    Report the range of optimal tilt angles across Europe and determine
    whether latitude or longitude is the dominant driver.
    """
    tilt = df["optimal_tilt"]

    r_lat, p_lat = stats.pearsonr(df["lat"], tilt)
    r_lon, p_lon = stats.pearsonr(df["lon"], tilt)

    dominant = "latitude" if abs(r_lat) > abs(r_lon) else "longitude"

    result = {
        "tilt_min":   tilt.min(),
        "tilt_max":   tilt.max(),
        "tilt_mean":  tilt.mean(),
        "tilt_std":   tilt.std(),
        "r_lat":      r_lat,
        "p_lat":      p_lat,
        "r_lon":      r_lon,
        "p_lon":      p_lon,
        "dominant":   dominant,
    }

    print("\n=== Q1: Optimal Tilt Range Across Europe ===")
    print(f"  Min tilt:  {tilt.min():.1f}°")
    print(f"  Max tilt:  {tilt.max():.1f}°")
    print(f"  Mean tilt: {tilt.mean():.1f}° ± {tilt.std():.1f}°")
    print(f"  Pearson r with latitude:  {r_lat:.4f}  (p={p_lat:.2e})")
    print(f"  Pearson r with longitude: {r_lon:.4f}  (p={p_lon:.2e})")
    print(f"  → Dominant geographic parameter: {dominant.upper()}")

    return result


# ---------------------------------------------------------------------------
# Q2: Mathematical relationship between latitude and optimal tilt
# ---------------------------------------------------------------------------

def _linear(x, a, b):
    return a * x + b

def _quadratic(x, a, b, c):
    return a * x**2 + b * x + c

def fit_tilt_model(df: pd.DataFrame) -> dict:
    """
    Fit linear and quadratic models of optimal_tilt as a function of latitude.
    Report coefficients and R².
    """
    lat = df["lat"].values
    tilt = df["optimal_tilt"].values

    # Linear fit via scipy curve_fit
    popt_lin, _ = curve_fit(_linear, lat, tilt)
    tilt_pred_lin = _linear(lat, *popt_lin)
    ss_res = np.sum((tilt - tilt_pred_lin) ** 2)
    ss_tot = np.sum((tilt - tilt.mean()) ** 2)
    r2_lin = 1 - ss_res / ss_tot

    # Quadratic fit
    popt_quad, _ = curve_fit(_quadratic, lat, tilt)
    tilt_pred_quad = _quadratic(lat, *popt_quad)
    ss_res_q = np.sum((tilt - tilt_pred_quad) ** 2)
    r2_quad = 1 - ss_res_q / ss_tot

    result = {
        "linear_a":  popt_lin[0],
        "linear_b":  popt_lin[1],
        "r2_linear": r2_lin,
        "quad_a":    popt_quad[0],
        "quad_b":    popt_quad[1],
        "quad_c":    popt_quad[2],
        "r2_quad":   r2_quad,
        "lat":       lat,
        "tilt":      tilt,
        "tilt_pred_lin":  tilt_pred_lin,
        "tilt_pred_quad": tilt_pred_quad,
    }

    a, b = popt_lin
    sign_b = "+" if b >= 0 else "-"
    print("\n=== Q2: Mathematical Relationship (Latitude → Optimal Tilt) ===")
    print(f"  Linear model:    tilt = {a:.4f} × lat {sign_b} {abs(b):.2f}°   R² = {r2_lin:.4f}")
    qa, qb, qc = popt_quad
    print(f"  Quadratic model: tilt = {qa:.5f} × lat² + {qb:.4f} × lat + {qc:.2f}°   R² = {r2_quad:.4f}")
    print(f"  Rule of thumb for comparison: tilt ≈ lat × 0.76 + 3.1  (Gunerhan & Hepbasli 2007)")

    return result


# ---------------------------------------------------------------------------
# Q3: Optimal tilt for Poland
# ---------------------------------------------------------------------------

def poland_optimal_tilt(grid_df: pd.DataFrame, city_df: pd.DataFrame | None = None) -> dict:
    """
    Report optimal tilt for Poland from the grid, and optionally from city data.
    """
    poland_mask = (
        (grid_df["lat"] >= POLAND_LAT_MIN) & (grid_df["lat"] <= POLAND_LAT_MAX) &
        (grid_df["lon"] >= POLAND_LON_MIN) & (grid_df["lon"] <= POLAND_LON_MAX)
    )
    poland = grid_df[poland_mask]

    mean_tilt = poland["optimal_tilt"].mean()
    std_tilt  = poland["optimal_tilt"].std()
    min_tilt  = poland["optimal_tilt"].min()
    max_tilt  = poland["optimal_tilt"].max()

    result = {
        "mean": mean_tilt,
        "std":  std_tilt,
        "min":  min_tilt,
        "max":  max_tilt,
        "n":    len(poland),
    }

    print("\n=== Q3: Optimal Tilt for Poland ===")
    print(f"  Grid points in Poland: {len(poland)}")
    print(f"  Optimal tilt: {mean_tilt:.1f}° ± {std_tilt:.1f}°  (range {min_tilt:.1f}° – {max_tilt:.1f}°)")

    if city_df is not None and "country" in city_df.columns:
        pl_cities = city_df[city_df["country"] == "Poland"][["city", "optimal_tilt"]]
        if not pl_cities.empty:
            print("  By city:")
            for _, row in pl_cities.iterrows():
                print(f"    {row['city']:12s}  {row['optimal_tilt']:.1f}°")

    return result


# ---------------------------------------------------------------------------
# Q4: Tracker gain across Europe
# ---------------------------------------------------------------------------

def _assign_country(lat: float, lon: float) -> str:
    """Very rough country assignment from bounding boxes for grid points."""
    boxes = {
        "Norway":      [(57, 71, 4, 31)],
        "Sweden":      [(55, 69, 10, 24)],
        "Finland":     [(59, 70, 20, 32)],
        "UK":          [(50, 59, -8, 2)],
        "Ireland":     [(51, 55, -10, -6)],
        "Portugal":    [(37, 42, -9, -6)],
        "Spain":       [(36, 44, -9, 4)],
        "France":      [(42, 51, -5, 8)],
        "Germany":     [(47, 55, 6, 15)],
        "Netherlands": [(51, 53, 4, 7)],
        "Belgium":     [(50, 51, 2, 6)],
        "Switzerland": [(46, 48, 6, 10)],
        "Austria":     [(46, 49, 9, 17)],
        "Italy":       [(37, 47, 6, 19)],
        "Greece":      [(35, 42, 20, 28)],
        "Turkey":      [(36, 42, 26, 36)],
        "Poland":      [(49, 55, 14, 24)],
        "Czechia":     [(48, 51, 12, 19)],
        "Slovakia":    [(48, 49, 17, 22)],
        "Hungary":     [(45, 48, 16, 23)],
        "Romania":     [(43, 48, 22, 30)],
        "Bulgaria":    [(41, 44, 22, 29)],
        "Serbia":      [(42, 46, 19, 23)],
        "Croatia":     [(42, 46, 13, 19)],
        "Denmark":     [(54, 57, 8, 15)],
        "Estonia":     [(57, 60, 21, 28)],
        "Latvia":      [(55, 58, 21, 28)],
        "Lithuania":   [(53, 57, 21, 27)],
        "Belarus":     [(51, 56, 23, 32)],
        "Ukraine":     [(44, 52, 22, 40)],
    }
    for country, regions in boxes.items():
        for (la0, la1, lo0, lo1) in regions:
            if la0 <= lat <= la1 and lo0 <= lon <= lo1:
                return country
    return "Other"


def tracker_gain_analysis(df: pd.DataFrame) -> dict:
    """
    Compute single-axis tracker gain over fixed-tilt system.
    Report range, top countries, and Poland value.
    """
    valid = df.dropna(subset=["E_y_fixed", "E_y_tracker"]).copy()
    valid["gain_pct"] = (valid["E_y_tracker"] - valid["E_y_fixed"]) / valid["E_y_fixed"] * 100
    valid["country"] = valid.apply(lambda r: _assign_country(r["lat"], r["lon"]), axis=1)

    by_country = (
        valid[valid["country"] != "Other"]
        .groupby("country")["gain_pct"]
        .agg(["mean", "min", "max", "count"])
        .sort_values("mean", ascending=False)
    )

    poland_mask = (
        (valid["lat"] >= POLAND_LAT_MIN) & (valid["lat"] <= POLAND_LAT_MAX) &
        (valid["lon"] >= POLAND_LON_MIN) & (valid["lon"] <= POLAND_LON_MAX)
    )
    poland_gain = valid[poland_mask]["gain_pct"]

    result = {
        "gain_min":      valid["gain_pct"].min(),
        "gain_max":      valid["gain_pct"].max(),
        "gain_mean":     valid["gain_pct"].mean(),
        "by_country":    by_country,
        "poland_gain":   poland_gain.mean() if not poland_gain.empty else None,
        "valid_df":      valid,
    }

    print("\n=== Q4: Single-Axis Tracker Gain vs. Fixed Tilt ===")
    print(f"  Europe-wide gain range: {valid['gain_pct'].min():.1f}% – {valid['gain_pct'].max():.1f}%")
    print(f"  Europe-wide mean gain:  {valid['gain_pct'].mean():.1f}%")
    print(f"  Poland mean gain:       {poland_gain.mean():.1f}%" if not poland_gain.empty else "  Poland: no data")
    print("\n  Top 10 countries by mean tracker gain:")
    print(by_country.head(10).to_string(
        formatters={"mean": "{:.1f}%".format, "min": "{:.1f}%".format, "max": "{:.1f}%".format}
    ))

    return result


# ---------------------------------------------------------------------------
# Q5: City comparison — solar availability
# ---------------------------------------------------------------------------

def city_comparison(df: pd.DataFrame) -> dict:
    """
    Compare annual solar energy availability across European cities.
    Assess within-country uniformity, with focus on Poland vs. other countries.
    """
    month_cols = [c for c in df.columns if c.startswith("irr_month_")]

    if month_cols:
        df = df.copy()
        df["annual_irr"] = df[month_cols].sum(axis=1)
    else:
        df = df.copy()
        df["annual_irr"] = df["E_y_fixed"]   # fallback

    by_country = (
        df.groupby("country")["annual_irr"]
        .agg(["mean", "std", "min", "max", "count"])
        .sort_values("mean", ascending=False)
    )

    # Coefficient of variation as uniformity metric
    by_country["cv_pct"] = (by_country["std"] / by_country["mean"] * 100).round(2)

    poland_row = by_country.loc["Poland"] if "Poland" in by_country.index else None
    poland_cities = df[df["country"] == "Poland"][["city", "annual_irr"]].sort_values("annual_irr")

    result = {
        "by_country":    by_country,
        "poland_cities": poland_cities,
        "df":            df,
    }

    print("\n=== Q5: Solar Energy Availability — City Comparison ===")
    print("\n  Annual irradiation by country (kWh/m²/year):")
    print(by_country[["mean", "std", "cv_pct", "min", "max"]].to_string(
        formatters={
            "mean":   "{:.0f}".format,
            "std":    "{:.0f}".format,
            "cv_pct": "{:.1f}%".format,
            "min":    "{:.0f}".format,
            "max":    "{:.0f}".format,
        }
    ))

    if poland_row is not None:
        cv = poland_row["cv_pct"]
        print(f"\n  Poland CV: {cv:.1f}% → ", end="")
        if cv < 5:
            print("very uniform solar conditions across the country")
        elif cv < 10:
            print("moderately uniform solar conditions")
        else:
            print("notable regional variation in solar conditions")

        print("\n  Polish cities ranked by annual irradiation:")
        for _, row in poland_cities.iterrows():
            print(f"    {row['city']:12s}  {row['annual_irr']:.0f} kWh/m²/year")

    return result
