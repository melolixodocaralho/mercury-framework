#!/usr/bin/env python3
"""Create a release ZIP of the repository suitable for extracting on a clean folder.

Excludes: .git, .venv, dist (optional), __pycache__, .pytest_cache

Output: dist/mercury-framework-release.zip
"""
from __future__ import annotations
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)
EXCLUDE_DIRS = {'.git', '.venv', 'dist', '__pycache__', '.pytest_cache'}
OUT_ZIP = OUT / 'mercury-framework-release.zip'
print(f"Creating release zip: {OUT_ZIP}")

with zipfile.ZipFile(OUT_ZIP, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(ROOT):
        # adjust dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            full = Path(root) / f
            # skip files in excluded directories (also skip the output zip itself)
            if any(part in EXCLUDE_DIRS for part in full.relative_to(ROOT).parts):
                continue
            if full == OUT_ZIP:
                continue
            arcname = full.relative_to(ROOT)
            z.write(full, arcname)

print('Release zip created:', OUT_ZIP)
