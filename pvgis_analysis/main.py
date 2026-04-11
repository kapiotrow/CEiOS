"""
Main orchestrator — runs all 5 analyses end-to-end.

Usage:
    python main.py              # full run (fetches data if not cached)
    python main.py --force      # re-fetch all data even if cached
    python main.py --analyze-only  # skip collection, use existing CSVs
"""

import argparse
import sys

from collect import collect_europe_grid, collect_cities
from analyze import (
    tilt_range_analysis,
    fit_tilt_model,
    poland_optimal_tilt,
    tracker_gain_analysis,
    city_comparison,
)
from visualize import (
    plot_tilt_map,
    plot_tilt_vs_lat,
    plot_tracker_gain_map,
    plot_tracker_gain_by_country,
    plot_city_comparison,
    plot_poland_vs_europe,
)
from config import ALL_CITIES


def main(force: bool = False, analyze_only: bool = False):
    # ------------------------------------------------------------------ #
    # 1. Data collection                                                   #
    # ------------------------------------------------------------------ #
    print("=" * 60)
    print("PVGIS SOLAR ANALYSIS")
    print("=" * 60)

    if analyze_only:
        from pathlib import Path
        from collect import GRID_CSV, CITIES_CSV
        import pandas as pd
        if not GRID_CSV.exists() or not CITIES_CSV.exists():
            print("ERROR: --analyze-only requires existing data files.")
            print(f"  Expected: {GRID_CSV}")
            print(f"           {CITIES_CSV}")
            sys.exit(1)
        print("\n[1/2] Loading existing data (--analyze-only)…")
        grid_df   = pd.read_csv(GRID_CSV)
        cities_df = pd.read_csv(CITIES_CSV)
    else:
        print("\n[1/2] Collecting data from PVGIS API…")
        grid_df   = collect_europe_grid(force=force)
        cities_df = collect_cities(ALL_CITIES, force=force)

    print(f"\n  Grid points loaded:  {len(grid_df)}")
    print(f"  Cities loaded:       {len(cities_df)}")

    # ------------------------------------------------------------------ #
    # 2. Analysis                                                          #
    # ------------------------------------------------------------------ #
    print("\n[2/2] Running analysis…")

    # Q1 — tilt range & dominant geographic parameter
    q1 = tilt_range_analysis(grid_df)

    # Q2 — mathematical model
    q2 = fit_tilt_model(grid_df)

    # Q3 — Poland optimal tilt
    q3 = poland_optimal_tilt(grid_df, cities_df)

    # Q4 — tracker gain
    q4 = tracker_gain_analysis(grid_df)

    # Q5 — city solar comparison
    # Compute annual_irr column before passing to analysis
    month_cols = [c for c in cities_df.columns if c.startswith("irr_month_")]
    if month_cols:
        cities_df["annual_irr"] = cities_df[month_cols].sum(axis=1)
    else:
        cities_df["annual_irr"] = cities_df["E_y_fixed"]
    q5 = city_comparison(cities_df)

    # ------------------------------------------------------------------ #
    # 3. Plots                                                             #
    # ------------------------------------------------------------------ #
    print("\n[3/3] Generating figures…")

    plot_tilt_map(grid_df)
    plot_tilt_vs_lat(q2)
    plot_tracker_gain_map(q4["valid_df"])
    plot_tracker_gain_by_country(q4["by_country"])
    plot_city_comparison(cities_df)
    plot_poland_vs_europe(q5["by_country"])

    # ------------------------------------------------------------------ #
    # 4. Summary                                                           #
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("SUMMARY OF FINDINGS")
    print("=" * 60)

    print(f"\nQ1  Optimal tilt range across Europe: "
          f"{q1['tilt_min']:.0f}° – {q1['tilt_max']:.0f}°  "
          f"(mean {q1['tilt_mean']:.1f}°)")
    print(f"    Dominant geographic parameter: {q1['dominant'].upper()} "
          f"(r={q1['r_lat']:.3f}) vs. longitude (r={q1['r_lon']:.3f})")

    a, b = q2["linear_a"], q2["linear_b"]
    print(f"\nQ2  Best-fit model: tilt = {a:.3f} × lat {'+' if b >= 0 else ''}{b:.2f}°  "
          f"(R² = {q2['r2_linear']:.4f})")

    print(f"\nQ3  Poland optimal tilt: {q3['mean']:.1f}° ± {q3['std']:.1f}°")

    print(f"\nQ4  Tracker gain range (Europe): "
          f"{q4['gain_min']:.1f}% – {q4['gain_max']:.1f}%  "
          f"(mean {q4['gain_mean']:.1f}%)")
    if q4["poland_gain"] is not None:
        print(f"    Poland tracker gain: {q4['poland_gain']:.1f}%")
    top5 = q4["by_country"]["mean"].head(5)
    print("    Top 5 countries by tracker gain:")
    for country, val in top5.items():
        print(f"      {country:20s}  {val:.1f}%")

    print(f"\nQ5  Country solar comparison saved — see figures/q5_*.png")

    print("\nAll figures saved to figures/")
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PVGIS solar analysis")
    parser.add_argument("--force", action="store_true",
                        help="Re-fetch all API data even if cached")
    parser.add_argument("--analyze-only", action="store_true",
                        help="Skip data collection, use existing CSVs")
    args = parser.parse_args()
    main(force=args.force, analyze_only=args.analyze_only)
