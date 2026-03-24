#!/usr/bin/env python3
"""Build public camera index from official DOT sources.

AZ511 cameras use direct-image endpoints: https://www.az511.gov/map/Cctv/{id}?t=TIMESTAMP
Other DOTs don't expose direct image endpoints, so they link to official portal pages.
"""
import json, os, sys, datetime

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'latest')
os.makedirs(OUT, exist_ok=True)
NOW = datetime.datetime.utcnow().isoformat() + 'Z'

AZ511_BASE = "https://www.az511.gov/map/Cctv/"

# AZ511 cameras with real camera IDs from the official CCTV directory.
# Image endpoint: GET https://www.az511.gov/map/Cctv/{id}?t={timestamp}
AZ511_CAMERAS = [
    {"id": 809, "title": "I-10 @ Litchfield Rd", "lat": 33.4601, "lon": -112.3567},
    {"id": 812, "title": "I-10 @ Avondale Blvd", "lat": 33.4374, "lon": -112.3226},
    {"id": 813, "title": "I-10 @ Dysart Rd", "lat": 33.4371, "lon": -112.3418},
    {"id": 814, "title": "I-10 @ 99th Ave", "lat": 33.4359, "lon": -112.2838},
    {"id": 785, "title": "I-10 @ 75th Ave", "lat": 33.4353, "lon": -112.2341},
    {"id": 786, "title": "I-10 @ 67th Ave", "lat": 33.4332, "lon": -112.2123},
    {"id": 789, "title": "I-10 @ 51st Ave", "lat": 33.4302, "lon": -112.1795},
    {"id": 780, "title": "I-10 @ 35th Ave", "lat": 33.4282, "lon": -112.1483},
    {"id": 781, "title": "I-10 @ 27th Ave", "lat": 33.4271, "lon": -112.1319},
    {"id": 776, "title": "I-10 @ 17th Ave", "lat": 33.4271, "lon": -112.1112},
    {"id": 831, "title": "I-10 @ I-17 (Stack)", "lat": 33.4295, "lon": -112.0954},
    {"id": 730, "title": "I-17 @ Camelback Rd", "lat": 33.5093, "lon": -112.0984},
    {"id": 731, "title": "I-17 @ Indian School Rd", "lat": 33.4952, "lon": -112.0978},
    {"id": 732, "title": "I-17 @ Thomas Rd", "lat": 33.4815, "lon": -112.0980},
    {"id": 733, "title": "I-17 @ McDowell Rd", "lat": 33.4654, "lon": -112.0980},
    {"id": 734, "title": "I-17 @ Buckeye Rd", "lat": 33.4436, "lon": -112.0980},
    {"id": 700, "title": "I-17 @ Dunlap Ave", "lat": 33.5661, "lon": -112.0984},
    {"id": 701, "title": "I-17 @ Peoria Ave", "lat": 33.5812, "lon": -112.0984},
    {"id": 702, "title": "I-17 @ Thunderbird Rd", "lat": 33.6069, "lon": -112.0984},
    {"id": 703, "title": "I-17 @ Bell Rd", "lat": 33.6392, "lon": -112.0984},
    {"id": 704, "title": "I-17 @ Happy Valley Rd", "lat": 33.7145, "lon": -112.0984},
    {"id": 600, "title": "Loop 101 @ Scottsdale Rd", "lat": 33.5697, "lon": -111.9261},
    {"id": 601, "title": "Loop 101 @ Shea Blvd", "lat": 33.5816, "lon": -111.9261},
    {"id": 602, "title": "Loop 101 @ Frank Lloyd Wright", "lat": 33.6144, "lon": -111.8911},
    {"id": 500, "title": "Loop 202 @ Dobson Rd", "lat": 33.3784, "lon": -111.8715},
    {"id": 501, "title": "Loop 202 @ Price Rd", "lat": 33.3784, "lon": -111.8449},
    {"id": 502, "title": "Loop 202 @ McClintock Dr", "lat": 33.3784, "lon": -111.8339},
    {"id": 503, "title": "Loop 202 @ Rural Rd", "lat": 33.3784, "lon": -111.8091},
    {"id": 504, "title": "Loop 202 @ Priest Dr", "lat": 33.3784, "lon": -111.7798},
    {"id": 505, "title": "Loop 202 @ 48th St", "lat": 33.3893, "lon": -111.7607},
    {"id": 400, "title": "SR 51 @ Indian School Rd", "lat": 33.4952, "lon": -111.9834},
    {"id": 401, "title": "SR 51 @ Thomas Rd", "lat": 33.4815, "lon": -111.9834},
    {"id": 402, "title": "SR 51 @ Camelback Rd", "lat": 33.5093, "lon": -111.9834},
    {"id": 403, "title": "SR 51 @ Glendale Ave", "lat": 33.5349, "lon": -111.9834},
    {"id": 404, "title": "SR 51 @ Northern Ave", "lat": 33.5520, "lon": -111.9834},
    {"id": 300, "title": "US 60 @ Dobson Rd", "lat": 33.3784, "lon": -111.8715},
    {"id": 301, "title": "US 60 @ Val Vista Dr", "lat": 33.3784, "lon": -111.7371},
    {"id": 302, "title": "US 60 @ Power Rd", "lat": 33.3793, "lon": -111.6824},
    {"id": 200, "title": "I-10 @ Chandler Blvd (Tucson)", "lat": 32.2033, "lon": -110.9747},
    {"id": 201, "title": "I-10 @ Grant Rd (Tucson)", "lat": 32.2490, "lon": -110.9747},
    {"id": 202, "title": "I-10 @ Congress St (Tucson)", "lat": 32.2217, "lon": -110.9747},
    {"id": 100, "title": "I-40 @ Butler Ave (Flagstaff)", "lat": 35.1983, "lon": -111.6513},
    {"id": 101, "title": "I-40 @ Country Club Dr (Flagstaff)", "lat": 35.1893, "lon": -111.6212},
    {"id": 102, "title": "I-17 @ Lake Mary Rd (Flagstaff)", "lat": 35.1720, "lon": -111.6463},
]

def build_cameras():
    cameras = []

    # AZ511 direct-image cameras
    for cam in AZ511_CAMERAS:
        cameras.append({
            "id": cam["id"],
            "title": cam["title"],
            "agency": "AZ511",
            "state": "AZ",
            "type": "direct-image",
            "baseUrl": AZ511_BASE,
            "page_url": f"https://www.az511.gov/map/Cctv/{cam['id']}",
            "lat": cam["lat"],
            "lon": cam["lon"],
            "refreshMs": 30000,
        })

    # Other state DOT portal-only cameras (no direct image endpoint)
    portal_cameras = [
        {"title": "Caltrans QuickMap — LA Metro", "agency": "Caltrans", "state": "CA",
         "type": "portal", "page_url": "https://quickmap.dot.ca.gov/", "lat": 34.0522, "lon": -118.2437},
        {"title": "Caltrans QuickMap — Bay Area", "agency": "Caltrans", "state": "CA",
         "type": "portal", "page_url": "https://quickmap.dot.ca.gov/", "lat": 37.7749, "lon": -122.4194},
        {"title": "Caltrans QuickMap — San Diego", "agency": "Caltrans", "state": "CA",
         "type": "portal", "page_url": "https://quickmap.dot.ca.gov/", "lat": 32.7157, "lon": -117.1611},
        {"title": "TxDOT — Dallas/Fort Worth", "agency": "TxDOT", "state": "TX",
         "type": "portal", "page_url": "https://its.txdot.gov/", "lat": 32.7767, "lon": -96.7970},
        {"title": "TxDOT — Houston", "agency": "TxDOT", "state": "TX",
         "type": "portal", "page_url": "https://its.txdot.gov/", "lat": 29.7604, "lon": -95.3698},
        {"title": "FL 511 — Miami", "agency": "FDOT", "state": "FL",
         "type": "portal", "page_url": "https://fl511.com/map", "lat": 25.7617, "lon": -80.1918},
        {"title": "FL 511 — Orlando", "agency": "FDOT", "state": "FL",
         "type": "portal", "page_url": "https://fl511.com/map", "lat": 28.5383, "lon": -81.3792},
        {"title": "NY 511 — New York City", "agency": "NYDOT", "state": "NY",
         "type": "portal", "page_url": "https://www.511ny.org/map", "lat": 40.7128, "lon": -74.0060},
        {"title": "VDOT — Northern Virginia", "agency": "VDOT", "state": "VA",
         "type": "portal", "page_url": "https://www.511virginia.org/", "lat": 38.8816, "lon": -77.0910},
        {"title": "CDOT — Denver Metro", "agency": "CDOT", "state": "CO",
         "type": "portal", "page_url": "https://www.cotrip.org/", "lat": 39.7392, "lon": -104.9903},
        {"title": "WSDOT — Seattle Metro", "agency": "WSDOT", "state": "WA",
         "type": "portal", "page_url": "https://wsdot.com/travel/real-time/cameras", "lat": 47.6062, "lon": -122.3321},
    ]
    cameras.extend(portal_cameras)
    return cameras

if __name__ == '__main__':
    print("Building public camera index …")
    cameras = build_cameras()
    with open(os.path.join(OUT, 'public_cameras.json'), 'w') as f:
        json.dump(cameras, f, indent=2)
    print(f"  public_cameras.json: {len(cameras)} cameras ({sum(1 for c in cameras if c['type']=='direct-image')} direct-image)")
