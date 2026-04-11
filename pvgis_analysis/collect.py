"""
Data collection: European grid sweep and per-city queries.
"""

import pathlib
import numpy as np
import pandas as pd

from api import get_pvcalc, get_mrcalc
from config import (
    GRID_LAT_MIN, GRID_LAT_MAX,
    GRID_LON_MIN, GRID_LON_MAX,
    GRID_STEP, ALL_CITIES,
)

DATA_DIR = pathlib.Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

GRID_CSV = DATA_DIR / "europe_grid.csv"
CITIES_CSV = DATA_DIR / "cities.csv"


def _extract_pvcalc_fixed(data: dict) -> dict:
    """Pull the fields we need from a fixed-system PVcalc response."""
    totals = data["outputs"]["totals"]["fixed"]
    inputs = data["inputs"]
    return {
        "optimal_tilt":    inputs["mounting_system"]["fixed"]["slope"]["value"],
        "optimal_azimuth": inputs["mounting_system"]["fixed"]["azimuth"]["value"],
        "E_y_fixed":       totals["E_y"],   # kWh/kWp/year
    }


def _extract_pvcalc_tracker(data: dict) -> dict:
    """Pull annual yield from a single-axis inclined tracker PVcalc response."""
    totals = data["outputs"]["totals"]["inclined_axis"]
    return {"E_y_tracker": totals["E_y"]}


def _extract_mrcalc(data: dict) -> dict:
    """Extract monthly horizontal irradiation values (Hh, kWh/m²/month), averaged over all years."""
    months = data["outputs"]["monthly"]
    sums = {}
    counts = {}
    for entry in months:
        m = int(entry["month"])
        sums[m]   = sums.get(m, 0.0)   + entry["H(h)_m"]
        counts[m] = counts.get(m, 0)   + 1
    return {f"irr_month_{m:02d}": sums[m] / counts[m] for m in sorted(sums)}


def collect_europe_grid(force: bool = False) -> pd.DataFrame:
    """
    Sweep a lat/lon grid over Europe, collect fixed and tracker PVcalc data.
    Saves to data/europe_grid.csv. Skips fetch if file already exists.
    """
    if GRID_CSV.exists() and not force:
        print(f"Loading cached grid data from {GRID_CSV}")
        return pd.read_csv(GRID_CSV)

    lats = np.arange(GRID_LAT_MIN, GRID_LAT_MAX + GRID_STEP, GRID_STEP)
    lons = np.arange(GRID_LON_MIN, GRID_LON_MAX + GRID_STEP, GRID_STEP)
    total = len(lats) * len(lons)
    print(f"Collecting grid data: {len(lats)} lats × {len(lons)} lons = {total} points")

    rows = []
    done = 0
    for lat in lats:
        for lon in lons:
            done += 1
            if done % 50 == 0 or done == total:
                print(f"  {done}/{total} ({100*done/total:.0f}%)")

            fixed_data = get_pvcalc(lat, lon, tracking=False)
            if fixed_data is None:
                continue  # No coverage (sea / outside database)

            tracker_data = get_pvcalc(lat, lon, tracking=True)
            if tracker_data is None:
                continue

            row = {"lat": lat, "lon": lon}
            row.update(_extract_pvcalc_fixed(fixed_data))
            row.update(_extract_pvcalc_tracker(tracker_data))
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(GRID_CSV, index=False)
    print(f"Saved {len(df)} valid grid points to {GRID_CSV}")
    return df


def collect_cities(city_list: list[dict] | None = None, force: bool = False) -> pd.DataFrame:
    """
    Query PVcalc (fixed + tracker) and MRcalc for each city.
    Saves to data/cities.csv. Skips fetch if file already exists.
    """
    if city_list is None:
        city_list = ALL_CITIES

    if CITIES_CSV.exists() and not force:
        print(f"Loading cached city data from {CITIES_CSV}")
        return pd.read_csv(CITIES_CSV)

    print(f"Collecting data for {len(city_list)} cities…")
    rows = []
    for i, city in enumerate(city_list, 1):
        lat, lon = city["lat"], city["lon"]
        print(f"  [{i}/{len(city_list)}] {city['city']}, {city['country']}")

        fixed_data   = get_pvcalc(lat, lon, tracking=False)
        tracker_data = get_pvcalc(lat, lon, tracking=True)
        mr_data      = get_mrcalc(lat, lon)

        if fixed_data is None:
            print(f"    WARNING: No PVcalc data for {city['city']}, skipping")
            continue

        row = {
            "city":    city["city"],
            "country": city["country"],
            "lat":     lat,
            "lon":     lon,
        }
        row.update(_extract_pvcalc_fixed(fixed_data))
        if tracker_data is not None:
            row.update(_extract_pvcalc_tracker(tracker_data))
        else:
            row["E_y_tracker"] = None

        if mr_data is not None:
            row.update(_extract_mrcalc(mr_data))

        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(CITIES_CSV, index=False)
    print(f"Saved {len(df)} cities to {CITIES_CSV}")
    return df
