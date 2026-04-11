"""
PVGIS API client with disk caching and rate limiting.
"""

import json
import time
import hashlib
import pathlib
import requests

BASE_URL = "https://re.jrc.ec.europa.eu/api/v5_3"
CACHE_DIR = pathlib.Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# Stay well under the 30 req/s limit
_MIN_INTERVAL = 1 / 25  # seconds between requests
_last_call_time = 0.0


def _rate_limit():
    global _last_call_time
    elapsed = time.monotonic() - _last_call_time
    wait = _MIN_INTERVAL - elapsed
    if wait > 0:
        time.sleep(wait)
    _last_call_time = time.monotonic()


def _cache_path(endpoint: str, params: dict) -> pathlib.Path:
    # Convert numpy scalars to native Python types so json.dumps works
    native = {k: v.item() if hasattr(v, "item") else v for k, v in params.items()}
    key = json.dumps(native, sort_keys=True)
    digest = hashlib.md5(key.encode()).hexdigest()[:12]
    return CACHE_DIR / f"{endpoint}_{digest}.json"


def _fetch(endpoint: str, params: dict, retries: int = 5) -> dict:
    cache_file = _cache_path(endpoint, params)
    if cache_file.exists():
        with cache_file.open() as f:
            return json.load(f)

    url = f"{BASE_URL}/{endpoint}"
    backoff = 2.0
    for attempt in range(retries):
        _rate_limit()
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code in (429, 503):
                print(f"  Rate limited ({response.status_code}), waiting {backoff:.1f}s…")
                time.sleep(backoff)
                backoff *= 2
                continue
            if response.status_code == 400:
                raise requests.HTTPError(response=response)
            response.raise_for_status()
            data = response.json()
            with cache_file.open("w") as f:
                json.dump(data, f)
            return data
        except requests.HTTPError:
            raise  # 400 = no coverage, 4xx errors — don't retry
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise
            print(f"  Request error: {e}, retrying in {backoff:.1f}s…")
            time.sleep(backoff)
            backoff *= 2

    raise RuntimeError(f"Failed after {retries} attempts: {endpoint} {params}")


def get_pvcalc(lat: float, lon: float, tracking: bool = False) -> dict | None:
    """
    Query PVcalc for a location.
    Returns parsed JSON or None if PVGIS has no data for this point (e.g. ocean).
    tracking=False → fixed optimal tilt.
    tracking=True  → single-axis inclined tracker with optimal axis inclination.
                     Use totals["inclined_axis"]["E_y"] from the response.
    """
    params = {
        "lat": round(lat, 4),
        "lon": round(lon, 4),
        "peakpower": 1,
        "loss": 14,
        "pvtechchoice": "crystSi",
        "mountingplace": "free",
        "outputformat": "json",
    }
    if tracking:
        params["inclined_axis"] = 1
        params["optimalinclination"] = 1
    else:
        params["optimalangles"] = 1

    try:
        return _fetch("PVcalc", params)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 400:
            # No data for this point (sea, no coverage)
            return None
        raise


def get_mrcalc(lat: float, lon: float) -> dict | None:
    """
    Query MRcalc for monthly radiation at a location.
    Returns parsed JSON or None if no data available.
    """
    params = {
        "lat": round(lat, 4),
        "lon": round(lon, 4),
        "outputformat": "json",
        "horirrad": 1,
        "optrad": 1,
    }
    try:
        return _fetch("MRcalc", params)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 400:
            return None
        raise
