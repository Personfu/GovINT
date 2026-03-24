#!/usr/bin/env python3
"""Build topic-focused datasets from the repository source CSV files."""

from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "sources.yaml"
AGENCIES_PATH = ROOT / "agencies-and-subs.csv"
FEDERAL_PATH = ROOT / "current-federal.csv"
FULL_PATH = ROOT / "current-full.csv"
REPORTS_DIR = ROOT / "reports"
DOCS_DATA_DIR = ROOT / "docs" / "data"


@dataclass
class TopicRule:
    name: str
    keywords: List[str]


def load_config() -> Dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def normalize(value: Optional[str]) -> str:
    return (value or "").strip().lower()


def match_topic(text_blob: str, topic_rules: Iterable[TopicRule]) -> str:
    lowered = normalize(text_blob)
    if not lowered:
        return "GeneralGovernment"

    for rule in topic_rules:
        if any(keyword in lowered for keyword in rule.keywords):
            return rule.name

    return "GeneralGovernment"


def ensure_dirs() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def parse_agencies(topic_rules: Iterable[TopicRule]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with AGENCIES_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        _ = next(reader, None)
        for row in reader:
            agency = row[0].strip() if len(row) > 0 and row[0] else ""
            bureau = row[1].strip() if len(row) > 1 and row[1] else ""
            blob = f"{agency} {bureau}"
            topic = match_topic(blob, topic_rules)
            rows.append(
                {
                    "agency": agency,
                    "bureau": bureau,
                    "topic": topic,
                }
            )
    return rows


def parse_domains(topic_rules: Iterable[TopicRule]) -> List[Dict[str, str]]:
    rows = read_csv_rows(FEDERAL_PATH)
    enriched: List[Dict[str, str]] = []
    for row in rows:
        org = row.get("Organization name", "")
        sub = row.get("Suborganization name", "")
        domain = row.get("Domain name", "")
        dom_type = row.get("Domain type", "")
        blob = f"{org} {sub} {domain} {dom_type}"
        topic = match_topic(blob, topic_rules)

        enriched.append(
            {
                "domain": domain,
                "domain_type": dom_type,
                "organization_name": org,
                "suborganization_name": sub,
                "topic": topic,
            }
        )
    return enriched


def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_random_sample(sample_size: int = 150) -> List[Dict[str, str]]:
    all_rows = read_csv_rows(FULL_PATH)
    if not all_rows:
        return []

    # Seed by date to produce one deterministic "random" sample per day.
    seed_value = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    rng = random.Random(seed_value)

    chosen = all_rows if len(all_rows) <= sample_size else rng.sample(all_rows, sample_size)

    out: List[Dict[str, str]] = []
    for row in chosen:
        out.append(
            {
                "domain": row.get("Domain name", ""),
                "organization_name": row.get("Organization name", ""),
                "suborganization_name": row.get("Suborganization name", ""),
                "state": row.get("State", ""),
                "domain_type": row.get("Domain type", ""),
            }
        )
    return out


def summarize_topics(
    agency_rows: List[Dict[str, str]],
    domain_rows: List[Dict[str, str]],
) -> Dict:
    agency_counts = Counter(row["topic"] for row in agency_rows)
    domain_counts = Counter(row["topic"] for row in domain_rows)

    by_topic_orgs: Dict[str, set] = defaultdict(set)
    for row in domain_rows:
        by_topic_orgs[row["topic"]].add(row["organization_name"])

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "agency_topic_counts": dict(sorted(agency_counts.items())),
        "federal_domain_topic_counts": dict(sorted(domain_counts.items())),
        "distinct_orgs_by_topic": {
            topic: len(orgs)
            for topic, orgs in sorted(by_topic_orgs.items())
        },
    }


def main() -> None:
    config = load_config()
    topic_rules = [
        TopicRule(name=name, keywords=[k.lower() for k in body.get("keywords", [])])
        for name, body in config.get("topics", {}).items()
    ]

    ensure_dirs()

    agency_rows = parse_agencies(topic_rules)
    domain_rows = parse_domains(topic_rules)
    random_sample = build_random_sample(sample_size=150)
    topic_summary = summarize_topics(agency_rows, domain_rows)

    write_csv(
        REPORTS_DIR / "agencies_topics.csv",
        ["agency", "bureau", "topic"],
        agency_rows,
    )
    write_csv(
        REPORTS_DIR / "federal_domains_topics.csv",
        ["domain", "domain_type", "organization_name", "suborganization_name", "topic"],
        domain_rows,
    )
    write_csv(
        REPORTS_DIR / "daily_random_domain_sample.csv",
        ["domain", "organization_name", "suborganization_name", "state", "domain_type"],
        random_sample,
    )

    with (REPORTS_DIR / "topic_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(topic_summary, handle, indent=2)

    with (DOCS_DATA_DIR / "topic_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(topic_summary, handle, indent=2)

    print("Built dataset reports:")
    print(f"- {REPORTS_DIR / 'agencies_topics.csv'}")
    print(f"- {REPORTS_DIR / 'federal_domains_topics.csv'}")
    print(f"- {REPORTS_DIR / 'daily_random_domain_sample.csv'}")
    print(f"- {REPORTS_DIR / 'topic_summary.json'}")


if __name__ == "__main__":
    main()
