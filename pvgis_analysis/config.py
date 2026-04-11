"""
Configuration: grid bounds, city lists, API constants.
"""

# Europe grid sweep: lat 35-72°N, lon -11 to 32°E, 2° step
GRID_LAT_MIN = 35
GRID_LAT_MAX = 72
GRID_LON_MIN = -11
GRID_LON_MAX = 32
GRID_STEP = 2

# Poland bounding box (for filtering grid points)
POLAND_LAT_MIN = 49.0
POLAND_LAT_MAX = 54.9
POLAND_LON_MIN = 14.1
POLAND_LON_MAX = 24.2

# Standard PV system parameters
PV_PARAMS = {
    "peakpower": 1,
    "loss": 14,
    "pvtechchoice": "crystSi",
    "mountingplace": "free",
    "outputformat": "json",
}

# Polish cities for Q5
POLISH_CITIES = [
    {"city": "Warsaw",    "country": "Poland", "lat": 52.23, "lon": 21.01},
    {"city": "Kraków",    "country": "Poland", "lat": 50.06, "lon": 19.94},
    {"city": "Gdańsk",    "country": "Poland", "lat": 54.35, "lon": 18.65},
    {"city": "Wrocław",   "country": "Poland", "lat": 51.11, "lon": 17.04},
    {"city": "Poznań",    "country": "Poland", "lat": 52.41, "lon": 16.93},
    {"city": "Łódź",      "country": "Poland", "lat": 51.77, "lon": 19.46},
    {"city": "Lublin",    "country": "Poland", "lat": 51.25, "lon": 22.57},
    {"city": "Białystok", "country": "Poland", "lat": 53.13, "lon": 23.16},
    {"city": "Rzeszów",   "country": "Poland", "lat": 50.04, "lon": 22.00},
    {"city": "Szczecin",  "country": "Poland", "lat": 53.43, "lon": 14.55},
]

# European comparison cities for Q5
EUROPEAN_CITIES = [
    {"city": "Rome",      "country": "Italy",       "lat": 41.90, "lon": 12.50},
    {"city": "Milan",     "country": "Italy",       "lat": 45.47, "lon": 9.19},
    {"city": "Palermo",   "country": "Italy",       "lat": 38.12, "lon": 13.36},
    {"city": "Madrid",    "country": "Spain",       "lat": 40.42, "lon": -3.70},
    {"city": "Barcelona", "country": "Spain",       "lat": 41.39, "lon": 2.15},
    {"city": "Seville",   "country": "Spain",       "lat": 37.39, "lon": -5.99},
    {"city": "London",    "country": "UK",          "lat": 51.51, "lon": -0.13},
    {"city": "Manchester","country": "UK",          "lat": 53.48, "lon": -2.24},
    {"city": "Edinburgh", "country": "UK",          "lat": 55.95, "lon": -3.19},
    {"city": "Stockholm", "country": "Sweden",      "lat": 59.33, "lon": 18.07},
    {"city": "Malmö",     "country": "Sweden",      "lat": 55.60, "lon": 13.00},
    {"city": "Oslo",      "country": "Norway",      "lat": 59.91, "lon": 10.75},
    {"city": "Athens",    "country": "Greece",      "lat": 37.98, "lon": 23.73},
    {"city": "Thessaloniki","country": "Greece",    "lat": 40.64, "lon": 22.94},
    {"city": "Lisbon",    "country": "Portugal",    "lat": 38.72, "lon": -9.14},
    {"city": "Porto",     "country": "Portugal",    "lat": 41.16, "lon": -8.63},
    {"city": "Paris",     "country": "France",      "lat": 48.85, "lon": 2.35},
    {"city": "Marseille", "country": "France",      "lat": 43.30, "lon": 5.37},
    {"city": "Berlin",    "country": "Germany",     "lat": 52.52, "lon": 13.40},
    {"city": "Munich",    "country": "Germany",     "lat": 48.14, "lon": 11.58},
    {"city": "Vienna",    "country": "Austria",     "lat": 48.21, "lon": 16.37},
    {"city": "Prague",    "country": "Czechia",     "lat": 50.08, "lon": 14.44},
    {"city": "Budapest",  "country": "Hungary",     "lat": 47.50, "lon": 19.04},
    {"city": "Bucharest", "country": "Romania",     "lat": 44.43, "lon": 26.10},
    {"city": "Helsinki",  "country": "Finland",     "lat": 60.17, "lon": 24.94},
    {"city": "Amsterdam", "country": "Netherlands", "lat": 52.37, "lon": 4.90},
    {"city": "Brussels",  "country": "Belgium",     "lat": 50.85, "lon": 4.35},
    {"city": "Zurich",    "country": "Switzerland", "lat": 47.38, "lon": 8.54},
    {"city": "Valletta",  "country": "Malta",       "lat": 35.90, "lon": 14.51},
    {"city": "Nicosia",   "country": "Cyprus",      "lat": 35.17, "lon": 33.36},
]

ALL_CITIES = POLISH_CITIES + EUROPEAN_CITIES
