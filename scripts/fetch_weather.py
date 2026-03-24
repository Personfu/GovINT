#!/usr/bin/env python3
"""Fetch NWS / NOAA weather alerts."""
import json, os, sys, datetime
try:
    import requests
except ImportError:
    sys.exit("Missing deps – pip install requests")

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'latest')
os.makedirs(OUT, exist_ok=True)
NOW = datetime.datetime.utcnow().isoformat() + 'Z'

ALERTS_URL = 'https://api.weather.gov/alerts/active?status=actual&message_type=alert'

if __name__ == '__main__':
    print("Fetching NWS weather alerts …")
    items = []
    try:
        headers = {'User-Agent': 'GOVINT-FLLC/1.0 (educational research)', 'Accept': 'application/geo+json'}
        r = requests.get(ALERTS_URL, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        for f in data.get('features', [])[:50]:
            p = f.get('properties', {})
            items.append({
                'title': p.get('headline', p.get('event', '')),
                'url': p.get('web', '') or f"https://alerts.weather.gov/search?id={p.get('id','')}",
                'published': p.get('sent', ''),
                'summary': (p.get('description', '') or '')[:500],
                'source': 'NWS',
                'tags': ['weather', 'public-safety'],
                'severity': p.get('severity', ''),
                'area': p.get('areaDesc', ''),
            })
    except Exception as ex:
        print(f"  WARN: {ex}", file=sys.stderr)

    with open(os.path.join(OUT, 'weather_alerts.json'), 'w') as f:
        json.dump({'fetched_at': NOW, 'items': items}, f, indent=2)
    print(f"  weather_alerts.json: {len(items)} items")
