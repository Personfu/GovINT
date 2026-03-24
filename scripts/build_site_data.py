#!/usr/bin/env python3
"""Build site-level aggregated data and archive today's snapshot."""
import json, os, sys, datetime, shutil, glob

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'latest')
ARCHIVE = os.path.join(os.path.dirname(__file__), '..', 'data', 'archive')
TODAY = datetime.date.today().isoformat()

if __name__ == '__main__':
    # Archive today's data
    dest = os.path.join(ARCHIVE, TODAY)
    if not os.path.exists(dest):
        os.makedirs(dest, exist_ok=True)
        for jf in glob.glob(os.path.join(DATA, '*.json')):
            shutil.copy2(jf, dest)
        print(f"Archived {len(os.listdir(dest))} files to data/archive/{TODAY}/")
    else:
        print(f"Archive for {TODAY} already exists, skipping.")
