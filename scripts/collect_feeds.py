#!/usr/bin/env python3
"""
Collect headlines from public government RSS feeds and write feeds.json + domain_sample.json
for the GovINT SOC dashboard.  Runs daily via GitHub Actions.
"""

from __future__ import annotations

import csv
import json
import random
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "sources.yaml"
DOCS_DATA = ROOT / "docs" / "data"
REPORTS_DIR = ROOT / "reports"
FULL_CSV = ROOT / "current-full.csv"
FEDERAL_CSV = ROOT / "current-federal.csv"
AGENCIES_CSV = ROOT / "agencies-and-subs.csv"

TIMEOUT = 20  # seconds per HTTP request
MAX_ITEMS_PER_FEED = 30
UA = "GovINT-Bot/1.0 (educational; +https://github.com/Personfu/GovINT)"


@dataclass
class FeedItem:
    topic: str
    source: str
    title: str
    link: str
    published: str
    summary: str


def load_config() -> Dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def fetch_rss(url: str) -> Optional[ET.Element]:
    """Download and parse an RSS/Atom feed. Returns the root Element or None."""
    try:
        req = Request(url, headers={"User-Agent": UA})
        with urlopen(req, timeout=TIMEOUT) as resp:
            return ET.fromstring(resp.read())
    except (URLError, ET.ParseError, OSError) as exc:
        print(f"  WARN: {url} -> {exc}")
        return None


def parse_rss_items(root: ET.Element, source_title: str, topic: str) -> List[FeedItem]:
    """Extract items from RSS 2.0 or Atom feeds."""
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items: List[FeedItem] = []

    # RSS 2.0
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        desc = (item.findtext("description") or "").strip()[:300]
        if title:
            items.append(FeedItem(topic=topic, source=source_title, title=title, link=link, published=pub, summary=desc))

    # Atom
    for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
        title = (entry.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
        link_el = entry.find("{http://www.w3.org/2005/Atom}link")
        link = link_el.get("href", "") if link_el is not None else ""
        pub = (entry.findtext("{http://www.w3.org/2005/Atom}updated") or
               entry.findtext("{http://www.w3.org/2005/Atom}published") or "").strip()
        desc = (entry.findtext("{http://www.w3.org/2005/Atom}summary") or "").strip()[:300]
        if title:
            items.append(FeedItem(topic=topic, source=source_title, title=title, link=link, published=pub, summary=desc))

    return items[:MAX_ITEMS_PER_FEED]


def collect_feeds(config: Dict) -> List[Dict]:
    """Iterate over all public_sources and collect feed items."""
    all_items: List[FeedItem] = []
    sources = config.get("public_sources", [])
    print(f"Collecting from {len(sources)} RSS sources...")

    for src in sources:
        if src.get("type") != "rss":
            continue
        url = src.get("url", "")
        title = src.get("title", url)
        topic = src.get("topic", "General")
        print(f"  -> {title}")
        root = fetch_rss(url)
        if root is not None:
            items = parse_rss_items(root, title, topic)
            all_items.extend(items)
            print(f"     {len(items)} items")

    # Sort newest first (best-effort date sort)
    all_items.sort(key=lambda x: x.published, reverse=True)
    return [asdict(i) for i in all_items]


def build_domain_sample(sample_size: int = 200) -> List[Dict[str, str]]:
    """Pick a daily-seeded random sample from current-full.csv."""
    if not FULL_CSV.exists():
        return []
    with FULL_CSV.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return []

    seed = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    rng = random.Random(seed)
    chosen = rows if len(rows) <= sample_size else rng.sample(rows, sample_size)

    return [
        {
            "domain": r.get("Domain name", ""),
            "organization_name": r.get("Organization name", ""),
            "suborganization_name": r.get("Suborganization name", ""),
            "state": r.get("State", ""),
            "domain_type": r.get("Domain type", ""),
        }
        for r in chosen
    ]


def build_topic_summary(config: Dict) -> Dict:
    """Build topic counts from CSVs using keyword matching."""
    from collections import Counter, defaultdict

    topic_rules = {
        name: [kw.lower() for kw in body.get("keywords", [])]
        for name, body in config.get("topics", {}).items()
    }

    def match(text: str) -> str:
        t = text.lower()
        for name, kws in topic_rules.items():
            if any(kw in t for kw in kws):
                return name
        return "GeneralGovernment"

    agency_counts: Counter = Counter()
    if AGENCIES_CSV.exists():
        with AGENCIES_CSV.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.reader(fh)
            next(reader, None)
            for row in reader:
                blob = " ".join(c.strip() for c in row if c.strip())
                agency_counts[match(blob)] += 1

    domain_counts: Counter = Counter()
    org_by_topic: Dict[str, set] = defaultdict(set)
    if FEDERAL_CSV.exists():
        with FEDERAL_CSV.open("r", encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                blob = " ".join(
                    row.get(k, "") for k in ("Organization name", "Suborganization name", "Domain name", "Domain type")
                )
                topic = match(blob)
                domain_counts[topic] += 1
                org_by_topic[topic].add(row.get("Organization name", ""))

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "agency_topic_counts": dict(sorted(agency_counts.items())),
        "federal_domain_topic_counts": dict(sorted(domain_counts.items())),
        "distinct_orgs_by_topic": {t: len(o) for t, o in sorted(org_by_topic.items())},
    }


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    print(f"  Wrote {path}  ({path.stat().st_size:,} bytes)")


def main() -> None:
    config = load_config()

    DOCS_DATA.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. RSS feeds
    feed_items = collect_feeds(config)
    feed_payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "item_count": len(feed_items),
        "items": feed_items,
    }
    write_json(DOCS_DATA / "feeds.json", feed_payload)
    write_json(REPORTS_DIR / "feeds.json", feed_payload)

    # 2. Domain sample
    sample = build_domain_sample(200)
    write_json(DOCS_DATA / "domain_sample.json", sample)
    write_json(REPORTS_DIR / "domain_sample.json", sample)

    # 3. Topic summary
    summary = build_topic_summary(config)
    write_json(DOCS_DATA / "topic_summary.json", summary)
    write_json(REPORTS_DIR / "topic_summary.json", summary)

    print(f"\nDone — {len(feed_items)} feed items, {len(sample)} domain samples.")


if __name__ == "__main__":
    main()
