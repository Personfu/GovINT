#!/usr/bin/env python3
"""Fetch CISA advisories and KEV catalog."""
import json, os, sys, datetime
try:
    import feedparser, requests
except ImportError:
    sys.exit("Missing deps – pip install feedparser requests")

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'latest')
os.makedirs(OUT, exist_ok=True)
NOW = datetime.datetime.utcnow().isoformat() + 'Z'

FEEDS = {
    'cisa_advisories': [
        'https://www.cisa.gov/cybersecurity-advisories/all.xml',
        'https://www.cisa.gov/news.xml',
    ],
}

def parse_feed(url):
    items = []
    try:
        d = feedparser.parse(url)
        for e in d.entries[:50]:
            pub = ''
            if hasattr(e, 'published'):
                pub = e.published
            elif hasattr(e, 'updated'):
                pub = e.updated
            items.append({
                'title': e.get('title', ''),
                'url': e.get('link', ''),
                'published': pub,
                'summary': (e.get('summary', '') or '')[:500],
                'source': 'CISA',
                'tags': ['cybersecurity'],
            })
    except Exception as ex:
        print(f"  WARN: {url}: {ex}", file=sys.stderr)
    return items

def fetch_kev():
    """Fetch CISA Known Exploited Vulnerabilities catalog."""
    items = []
    try:
        r = requests.get('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json', timeout=30)
        r.raise_for_status()
        data = r.json()
        for v in data.get('vulnerabilities', [])[:50]:
            items.append({
                'title': f"{v.get('cveID','')} — {v.get('vendorProject','')} {v.get('product','')}",
                'url': f"https://nvd.nist.gov/vuln/detail/{v.get('cveID','')}",
                'published': v.get('dateAdded', ''),
                'summary': v.get('shortDescription', '')[:500],
                'source': 'CISA-KEV',
                'tags': ['cybersecurity', 'ransomware'] if v.get('knownRansomwareCampaignUse') == 'Known' else ['cybersecurity'],
            })
    except Exception as ex:
        print(f"  WARN KEV: {ex}", file=sys.stderr)
    return items

if __name__ == '__main__':
    print("Fetching CISA advisories …")
    all_items = []
    for url in FEEDS['cisa_advisories']:
        all_items.extend(parse_feed(url))
    with open(os.path.join(OUT, 'cisa_advisories.json'), 'w') as f:
        json.dump({'fetched_at': NOW, 'items': all_items}, f, indent=2)
    print(f"  cisa_advisories.json: {len(all_items)} items")

    print("Fetching CISA KEV …")
    kev_items = fetch_kev()
    with open(os.path.join(OUT, 'cisa_kev.json'), 'w') as f:
        json.dump({'fetched_at': NOW, 'items': kev_items}, f, indent=2)
    print(f"  cisa_kev.json: {len(kev_items)} items")
