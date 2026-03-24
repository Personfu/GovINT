#!/usr/bin/env python3
"""Fetch FAA / NTSB / aviation notices."""
import json, os, sys, datetime
try:
    import feedparser
except ImportError:
    sys.exit("Missing deps – pip install feedparser")

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'latest')
os.makedirs(OUT, exist_ok=True)
NOW = datetime.datetime.utcnow().isoformat() + 'Z'

FEEDS = [
    ('https://www.faa.gov/newsroom/rss', 'FAA'),
    ('https://www.ntsb.gov/news/press-releases/_layouts/ntsb.recsearch/GetRSSFeed.ashx', 'NTSB'),
]

def parse_feed(url, source):
    items = []
    try:
        d = feedparser.parse(url, agent='Mozilla/5.0 (compatible; GOVINT/1.0)')
        for e in d.entries[:25]:
            pub = getattr(e, 'published', '') or getattr(e, 'updated', '')
            items.append({
                'title': e.get('title', ''),
                'url': e.get('link', ''),
                'published': pub,
                'summary': (e.get('summary', '') or '')[:500],
                'source': source,
                'tags': ['aviation', 'transportation'],
            })
    except Exception as ex:
        print(f"  WARN: {url}: {ex}", file=sys.stderr)
    return items

if __name__ == '__main__':
    print("Fetching aviation feeds …")
    items = []
    for url, src in FEEDS:
        items.extend(parse_feed(url, src))
    with open(os.path.join(OUT, 'aviation_alerts.json'), 'w') as f:
        json.dump({'fetched_at': NOW, 'items': items}, f, indent=2)
    print(f"  aviation_alerts.json: {len(items)} items")
