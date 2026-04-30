# -*- coding: utf-8 -*-
"""Compare / preview changes to the showfile.

Default mode (no flags):
    Unified text diff between the newest backup and the current showfile.

--dry-run mode:
    1. Copy the current showfile to a temp file.
    2. Run _rebuild_all.py --no-post on the temp copy.
    3. Show semantic diff (via _what_changed.semantic_diff) between original and rebuilt copy.
    4. Delete temp -- the current showfile is untouched.

Usage:
    python _preview_changes.py                    # text diff vs backup
    python _preview_changes.py <a.qxw> <b.qxw>   # text diff between explicit files
    python _preview_changes.py --dry-run          # rebuild on temp + semantic diff
    python _preview_changes.py -n 200             # limit text diff lines
"""
from __future__ import annotations

import argparse
import difflib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _qlc_helpers import BACKUP_DIR, QXW
from _what_changed import semantic_diff

ROOT = Path(__file__).resolve().parent.parent


def latest_backup() -> Path | None:
    if not BACKUP_DIR.is_dir():
        return None
    files = sorted(BACKUP_DIR.glob("*.qxw"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def text_diff(left: Path, right: Path, n: int) -> None:
    a = left.read_text(encoding="utf-8", errors="replace").splitlines()
    b = right.read_text(encoding="utf-8", errors="replace").splitlines()
    diff = difflib.unified_diff(
        a, b,
        fromfile=str(left),
        tofile=str(right),
        lineterm="",
    )
    lines = list(diff)
    if n and n > 0:
        lines = lines[:n]
        if len(lines) == n:
            lines.append(f"... (truncated to {n} lines; use -n 0 for full)")
    if not lines:
        print("No textual differences.")
        return
    print("\n".join(lines))


def dry_run() -> None:
    """Copy showfile to temp, run rebuild on it, show semantic diff, delete temp."""
    if not QXW.is_file():
        raise SystemExit(f"Showfile not found: {QXW}")

    rebuild_script = ROOT / "_rebuild_all.py"
    if not rebuild_script.is_file():
        raise SystemExit("_rebuild_all.py not found; cannot dry-run rebuild")

    with tempfile.TemporaryDirectory(prefix="qxw_dryrun_") as tmpdir:
        tmp_qxw = Path(tmpdir) / QXW.name
        shutil.copy2(QXW, tmp_qxw)
        print(f"[dry-run] Copied showfile to temp: {tmp_qxw}")
        print(f"[dry-run] Running rebuild on temp copy (--no-post)...")

        result = subprocess.run(
            [sys.executable, str(rebuild_script), "--no-post", "--qxw", str(tmp_qxw)],
            capture_output=False,
            text=True,
        )

        if result.returncode != 0:
            print(f"[dry-run] Rebuild exited with code {result.returncode}")
            # Still show diff of whatever was produced
        else:
            print("[dry-run] Rebuild complete.")

        print()
        semantic_diff(QXW, tmp_qxw, label_a="current", label_b="after-rebuild")
        # temp dir auto-deleted on exit


def main() -> None:
    ap = argparse.ArgumentParser(description="Preview / diff QLC+ workspace changes")
    ap.add_argument("left", nargs="?", help="Older / reference .qxw (default: newest backup)")
    ap.add_argument("right", nargs="?", help="Newer .qxw (default: main showfile)")
    ap.add_argument("-n", type=int, default=400, help="Max text diff lines to print (0 = unlimited)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Rebuild on temp copy and show semantic diff; does not modify files")
    args = ap.parse_args()

    if args.dry_run:
        dry_run()
        return

    right = Path(args.right) if args.right else QXW
    if args.left:
        left = Path(args.left)
    else:
        lb = latest_backup()
        if lb is None:
            raise SystemExit("No .qxw backups in _Showfile_Backups; pass explicit paths.")
        left = lb

    if not left.is_file() or not right.is_file():
        raise SystemExit("Both paths must exist.")

    text_diff(left, right, args.n)


if __name__ == "__main__":
    main()
