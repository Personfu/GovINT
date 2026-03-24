#!/usr/bin/env python3
"""Build daily intelligence brief from all collected data."""
import json, os, sys, datetime, glob

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'latest')
REPORTS = os.path.join(os.path.dirname(__file__), '..', 'data', 'reports')
os.makedirs(REPORTS, exist_ok=True)
NOW = datetime.datetime.utcnow().isoformat() + 'Z'
TODAY = datetime.date.today().isoformat()

if __name__ == '__main__':
    print("Building daily brief …")
    source_counts = {}
    category_counts = {}
    all_items = []

    for jf in glob.glob(os.path.join(DATA, '*.json')):
        try:
            with open(jf) as f:
                data = json.load(f)
            items = data.get('items', []) if isinstance(data, dict) else []
            for item in items:
                src = item.get('source', 'Unknown')
                source_counts[src] = source_counts.get(src, 0) + 1
                for tag in item.get('tags', []):
                    category_counts[tag] = category_counts.get(tag, 0) + 1
                all_items.append(item)
        except Exception:
            pass

    # pick notable items — most recent with longest summaries
    notable = sorted(all_items, key=lambda x: len(x.get('summary', '')), reverse=True)[:10]
    notable_out = [{'title': n.get('title',''), 'url': n.get('url',''), 'source': n.get('source','')} for n in notable]

    brief = {
        'date': TODAY,
        'fetched_at': NOW,
        'total_items': len(all_items),
        'summary': f"GOVINT collected {len(all_items)} items from {len(source_counts)} sources on {TODAY}.",
        'source_counts': dict(sorted(source_counts.items(), key=lambda x: -x[1])),
        'category_counts': dict(sorted(category_counts.items(), key=lambda x: -x[1])),
        'notable': notable_out,
    }
    with open(os.path.join(REPORTS, 'daily_brief.json'), 'w') as f:
        json.dump(brief, f, indent=2)
    print(f"  daily_brief.json: {brief['total_items']} items from {len(source_counts)} sources")
