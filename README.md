# PERSONFU // Arizona Public Intel Wiki

> An open-source OSINT dashboard and research wiki focused on Arizona government, defense, infrastructure, border security, cyber threats, and documented anomalies — built from public federal data feeds.

**Live site:** [personfu.github.io/GovINT](https://personfu.github.io/GovINT/)

---

## What This Is

A static website that aggregates publicly available U.S. government data into a browsable, cross-referenced intelligence wiki with a cyberpunk desert aesthetic. All data comes from official `.gov` sources, FOIA-released documents, and verified public records.

**This is not** a news site, conspiracy platform, or intelligence agency. It is an educational OSINT research tool.

## Content Pillars

| Pillar | Description |
|--------|-------------|
| **Cyber** | CISA advisories, KEV catalog, FBI/DOJ cyber press, DHS news |
| **Government** | 15,000+ `.gov` domains, agency profiles, CRS reports |
| **Defense** | Fort Huachuca, Davis-Monthan AFB, Luke AFB, Yuma Proving Ground |
| **Infrastructure** | Weather alerts, transportation, Palo Verde, CAP canal, dams |
| **Borders** | CBP technology corridor, Tucson/Yuma sectors, public cameras |
| **Anomalies** | Phoenix Lights, Sedona, documented UAP events with reliability labels |
| **Documents** | Declassified materials, CRS reports, FOIA releases |

## Reliability System

Every claim carries a reliability badge (1–10 scale):

- **Verified** (10) — Official government source, directly confirmed
- **Official** (9) — Published by a government agency
- **Confirmed** (8) — Multiple credible sources agree
- **Credible** (7) — Reputable source, not independently confirmed
- **Probable** (6) — Likely true based on available evidence
- **Possible** (5) — Plausible but unconfirmed
- **Speculative** (4) — Based on limited or indirect evidence
- **Disputed** (3) — Conflicting accounts exist
- **Folklore** (2) — Community tradition, not evidence-based
- **Unresolved** (1) — Insufficient evidence to assess

## Architecture

```
├── index.html              # Mission Control homepage
├── *.html                  # Portal pages (cyber, defense, borders, etc.)
├── content/                # Deep-dive dossier pages
├── assets/
│   ├── css/fllc-govint.css # Cosmic desert cyberpunk theme
│   └── js/                 # Vanilla JS modules (no frameworks)
├── config/sources.yaml     # RSS feed and API source definitions
├── data/
│   ├── latest/             # Auto-updated JSON from daily pipeline
│   ├── wiki/               # Static reference data (agencies, places, timelines)
│   └── archive/            # Historical snapshots
├── scripts/                # Python data collection pipeline
└── .github/workflows/      # Daily automated collection (GitHub Actions)
```

## Data Pipeline

A GitHub Actions workflow runs daily at 11:17 UTC and collects from:

- **CISA** — Advisories and Known Exploited Vulnerabilities catalog
- **FBI** — Cyber division press releases
- **DOJ** — Cybercrime prosecution announcements
- **DHS** — News and operational updates
- **FAA/NWS** — Aviation alerts, weather warnings
- **GSA** — `.gov` domain registry (15,000+ domains)
- **State DOTs** — Public traffic camera feeds

All data is fetched from official government RSS feeds and APIs. No scraping. No private data.

## Local Development

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run individual collectors
python scripts/fetch_cisa.py
python scripts/fetch_fbi.py
python scripts/build_daily_brief.py

# Serve locally
python -m http.server 8000
```

## Security

- All external data is HTML-escaped before rendering to prevent XSS
- External resources (Leaflet) loaded with `crossorigin="anonymous"`
- No cookies, no tracking, no analytics, no user data collection
- All links to external sites use `rel="noopener"`
- Content Security Policy headers recommended for production deployment

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is released under [CC0 1.0 Universal](LICENSE) — public domain dedication. You can copy, modify, and distribute this work without asking permission.

Data sourced from U.S. government public records is not subject to copyright under 17 U.S.C. § 105.
