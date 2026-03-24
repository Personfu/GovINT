#!/usr/bin/env python3
"""Build public camera index from official DOT sources."""
import json, os, sys, datetime

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'latest')
os.makedirs(OUT, exist_ok=True)
NOW = datetime.datetime.utcnow().isoformat() + 'Z'

# Static directory of known official public camera pages.
# These are official .gov or state DOT camera portals.
CAMERAS = [
    {"camera_name": "AZ 511 — Phoenix Metro", "agency": "Arizona DOT", "state": "AZ",
     "page_url": "https://www.az511.gov/map/Cctv", "lat": 33.4484, "lon": -112.0740},
    {"camera_name": "AZ 511 — Tucson", "agency": "Arizona DOT", "state": "AZ",
     "page_url": "https://www.az511.gov/map/Cctv", "lat": 32.2226, "lon": -110.9747},
    {"camera_name": "AZ 511 — I-10 West", "agency": "Arizona DOT", "state": "AZ",
     "page_url": "https://www.az511.gov/map/Cctv", "lat": 33.0, "lon": -113.0},
    {"camera_name": "AZ 511 — I-17 North", "agency": "Arizona DOT", "state": "AZ",
     "page_url": "https://www.az511.gov/map/Cctv", "lat": 34.5, "lon": -112.0},
    {"camera_name": "AZ 511 — Flagstaff", "agency": "Arizona DOT", "state": "AZ",
     "page_url": "https://www.az511.gov/map/Cctv", "lat": 35.1983, "lon": -111.6513},
    {"camera_name": "Caltrans QuickMap — LA Metro", "agency": "California DOT", "state": "CA",
     "page_url": "https://quickmap.dot.ca.gov/", "lat": 34.0522, "lon": -118.2437},
    {"camera_name": "Caltrans QuickMap — Bay Area", "agency": "California DOT", "state": "CA",
     "page_url": "https://quickmap.dot.ca.gov/", "lat": 37.7749, "lon": -122.4194},
    {"camera_name": "Caltrans QuickMap — San Diego", "agency": "California DOT", "state": "CA",
     "page_url": "https://quickmap.dot.ca.gov/", "lat": 32.7157, "lon": -117.1611},
    {"camera_name": "TxDOT — Dallas/Fort Worth", "agency": "Texas DOT", "state": "TX",
     "page_url": "https://its.txdot.gov/", "lat": 32.7767, "lon": -96.7970},
    {"camera_name": "TxDOT — Houston", "agency": "Texas DOT", "state": "TX",
     "page_url": "https://its.txdot.gov/", "lat": 29.7604, "lon": -95.3698},
    {"camera_name": "TxDOT — Austin", "agency": "Texas DOT", "state": "TX",
     "page_url": "https://its.txdot.gov/", "lat": 30.2672, "lon": -97.7431},
    {"camera_name": "FL 511 — Miami", "agency": "Florida DOT", "state": "FL",
     "page_url": "https://fl511.com/map", "lat": 25.7617, "lon": -80.1918},
    {"camera_name": "FL 511 — Orlando", "agency": "Florida DOT", "state": "FL",
     "page_url": "https://fl511.com/map", "lat": 28.5383, "lon": -81.3792},
    {"camera_name": "FL 511 — Tampa", "agency": "Florida DOT", "state": "FL",
     "page_url": "https://fl511.com/map", "lat": 27.9506, "lon": -82.4572},
    {"camera_name": "NY 511 — New York City", "agency": "New York DOT", "state": "NY",
     "page_url": "https://www.511ny.org/map", "lat": 40.7128, "lon": -74.0060},
    {"camera_name": "NY 511 — Albany", "agency": "New York DOT", "state": "NY",
     "page_url": "https://www.511ny.org/map", "lat": 42.6526, "lon": -73.7562},
    {"camera_name": "VDOT — Northern Virginia", "agency": "Virginia DOT", "state": "VA",
     "page_url": "https://www.511virginia.org/", "lat": 38.8816, "lon": -77.0910},
    {"camera_name": "CDOT — Denver Metro", "agency": "Colorado DOT", "state": "CO",
     "page_url": "https://www.cotrip.org/", "lat": 39.7392, "lon": -104.9903},
    {"camera_name": "CDOT — I-70 Mountain Corridor", "agency": "Colorado DOT", "state": "CO",
     "page_url": "https://www.cotrip.org/", "lat": 39.6, "lon": -106.0},
    {"camera_name": "WSDOT — Seattle Metro", "agency": "Washington DOT", "state": "WA",
     "page_url": "https://wsdot.com/travel/real-time/cameras", "lat": 47.6062, "lon": -122.3321},
]

if __name__ == '__main__':
    print("Building public camera index …")
    with open(os.path.join(OUT, 'public_cameras.json'), 'w') as f:
        json.dump(CAMERAS, f, indent=2)
    print(f"  public_cameras.json: {len(CAMERAS)} cameras")
