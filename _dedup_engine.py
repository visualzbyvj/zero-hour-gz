# -*- coding: utf-8 -*-
"""Remove duplicate Function IDs from <Engine>, keeping only the last definition per ID.

QLC+ uses the last definition when duplicates exist. This script makes that
explicit and shrinks the file significantly.

Uses XML parsing to identify all Function elements, then string manipulation
to remove earlier duplicates while preserving file formatting.

Usage:
    python _dedup_engine.py            # dedup in place (backs up first)
    python _dedup_engine.py --dry-run  # report only, no write
"""
from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from collections import Counter

from _qlc_helpers import QXW, auto_backup, load_qxw, save_qxw

WS_NS = "http://www.qlcplus.org/Workspace"

# Matches any Function block with flexible indentation
FN_PATTERN = re.compile(
    r'^[ \t]*<Function ID="(\d+)" Type="[^"]*"[^>]*>.*?</Function>[ \t]*\n?',
    re.DOTALL | re.MULTILINE,
)


def dedup(text: str) -> tuple[str, int, int]:
    """Remove duplicate Function blocks, keeping the LAST occurrence of each ID."""
    matches = list(FN_PATTERN.finditer(text))
    id_counts: Counter[int] = Counter()
    for m in matches:
        id_counts[int(m.group(1))] += 1

    dup_ids = {fid for fid, count in id_counts.items() if count > 1}
    if not dup_ids:
        return text, len(matches), 0

    last_seen: dict[int, int] = {}
    for i, m in enumerate(matches):
        last_seen[int(m.group(1))] = i

    to_remove: set[int] = set()
    for i, m in enumerate(matches):
        fid = int(m.group(1))
        if fid in dup_ids and i != last_seen[fid]:
            to_remove.add(i)

    parts: list[str] = []
    prev_end = 0
    for i, m in enumerate(matches):
        if i in to_remove:
            parts.append(text[prev_end:m.start()])
            prev_end = m.end()
    parts.append(text[prev_end:])

    return "".join(parts), len(matches), len(to_remove)


def main() -> None:
    ap = argparse.ArgumentParser(description="Deduplicate Engine Function IDs")
    ap.add_argument("--dry-run", action="store_true", help="Report only, don't write")
    args = ap.parse_args()

    text = load_qxw()
    new_text, total, removed = dedup(text)

    print(f"Total Function blocks matched: {total}")
    print(f"Duplicates removed:            {removed}")
    print(f"Remaining:                     {total - removed}")

    if removed == 0:
        print("No duplicates found.")
        return

    if args.dry_run:
        print("[dry-run] No changes written.")
        return

    # Verify the deduped text still parses as valid XML
    try:
        ET.fromstring(new_text)
    except ET.ParseError as exc:
        print(f"WARNING: Deduped file has XML parse error: {exc}")
        print("Aborting - no changes written. Check the file manually.")
        raise SystemExit(1)

    backup = auto_backup()
    print(f"Backup: {backup}")
    save_qxw(new_text)
    before_kb = len(text.encode("utf-8")) // 1024
    after_kb = len(new_text.encode("utf-8")) // 1024
    print(f"File size: {before_kb} KB -> {after_kb} KB (saved {before_kb - after_kb} KB)")


if __name__ == "__main__":
    main()
