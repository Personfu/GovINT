#!/usr/bin/env python3
"""Fetch FBI cyber and law enforcement notices."""
import json, os, sys, datetime
try:
    import feedparser
except ImportError:
    sys.exit("Missing deps – pip install feedparser")

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'latest')
os.makedirs(OUT, exist_ok=True)
NOW = datetime.datetime.utcnow().isoformat() + 'Z'

FEEDS = [
    'https://www.fbi.gov/feeds/fbi-news',
    'https://www.fbi.gov/feeds/fbi-cyber',
]

def parse_feed(url, source='FBI'):
    items = []
    try:
        d = feedparser.parse(url, agent='Mozilla/5.0 (compatible; GOVINT/1.0)')
        for e in d.entries[:30]:
            pub = getattr(e, 'published', '') or getattr(e, 'updated', '')
            items.append({
                'title': e.get('title', ''),
                'url': e.get('link', ''),
                'published': pub,
                'summary': (e.get('summary', '') or '')[:500],
                'source': source,
                'tags': ['law-enforcement', 'cybersecurity'],
            })
    except Exception as ex:
        print(f"  WARN: {url}: {ex}", file=sys.stderr)
    return items

if __name__ == '__main__':
    print("Fetching FBI feeds …")
    items = []
    for url in FEEDS:
        items.extend(parse_feed(url))
    with open(os.path.join(OUT, 'fbi_cyber.json'), 'w') as f:
        json.dump({'fetched_at': NOW, 'items': items}, f, indent=2)
    print(f"  fbi_cyber.json: {len(items)} items")
