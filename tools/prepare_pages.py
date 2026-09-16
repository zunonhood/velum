#!/usr/bin/env python3
"""Prepare the static site for GitHub project Pages under /velum/."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "frontend" / "site"
TARGET = ROOT / ".pages"
TEXT_SUFFIXES = {".html", ".js", ".mjs", ".json", ".css"}
REPLACEMENTS = (
    (b"/_assets/", b"/velum/_assets/"),
    (b"path:`/docs", b"path:`/velum/docs"),
    (b"path:`/tracks", b"path:`/velum/tracks"),
)

if TARGET.exists():
    shutil.rmtree(TARGET)
shutil.copytree(SOURCE, TARGET)

changed = 0
for path in TARGET.rglob("*"):
    if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
        continue
    data = path.read_bytes()
    updated = data
    for old, new in REPLACEMENTS:
        updated = updated.replace(old, new)
    if updated != data:
        path.write_bytes(updated)
        changed += 1

print(f"Prepared {TARGET} for /velum/ ({changed} files rewritten)")