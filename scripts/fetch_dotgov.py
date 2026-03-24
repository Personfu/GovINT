#!/usr/bin/env python3
"""Build .gov domain summary from CSV files in repo root."""
import csv, json, os, sys, datetime, random

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'latest')
ROOT = os.path.join(os.path.dirname(__file__), '..')
os.makedirs(OUT, exist_ok=True)
NOW = datetime.datetime.utcnow().isoformat() + 'Z'

def load_csv(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

if __name__ == '__main__':
    print("Building .gov domain summary …")
    full = load_csv(os.path.join(ROOT, 'current-full.csv'))
    fed = load_csv(os.path.join(ROOT, 'current-federal.csv'))

    type_counts = {}
    state_counts = {}
    for r in full:
        dt = r.get('Domain Type', r.get('domain_type', 'Unknown'))
        type_counts[dt] = type_counts.get(dt, 0) + 1
        st = r.get('State', r.get('state', ''))
        if st:
            state_counts[st] = state_counts.get(st, 0) + 1

    # random sample of 200
    sample_rows = random.sample(full, min(200, len(full)))
    sample = []
    for r in sample_rows:
        sample.append({
            'domain': r.get('Domain Name', r.get('domain_name', '')),
            'type': r.get('Domain Type', r.get('domain_type', '')),
            'agency': r.get('Agency', r.get('agency', '')),
            'state': r.get('State', r.get('state', '')),
        })

    summary = {
        'fetched_at': NOW,
        'total': len(full),
        'federal': len(fed),
        'non_federal': len(full) - len(fed),
        'states_count': len(state_counts),
        'type_counts': dict(sorted(type_counts.items(), key=lambda x: -x[1])[:15]),
        'state_counts': dict(sorted(state_counts.items(), key=lambda x: -x[1])[:20]),
        'sample': sample,
    }
    with open(os.path.join(OUT, 'gov_domains_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"  gov_domains_summary.json: {summary['total']} domains, {len(sample)} sample")
