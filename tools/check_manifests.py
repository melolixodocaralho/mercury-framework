"""Validate plugin manifests for required fields used by CI.

Checks that all manifests under `mercury_plugins/` include `name`, `version`,
`network_policy`, and `responsible_use`.

Exit code 0 on success, non-zero on failure.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
PLUGINS_DIR = os.path.join(ROOT, "mercury_plugins")

required = ["name", "version", "network_policy", "responsible_use"]

failed = []
for entry in sorted(os.listdir(PLUGINS_DIR)):
    pdir = os.path.join(PLUGINS_DIR, entry)
    if not os.path.isdir(pdir):
        continue
    manifest_path = os.path.join(pdir, "manifest.json")
    if not os.path.isfile(manifest_path):
        failed.append(f"{entry}: manifest.json missing")
        continue
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            m = json.load(f)
    except Exception as e:
        failed.append(f"{entry}: manifest parse error: {e}")
        continue
    for r in required:
        if r not in m:
            failed.append(f"{entry}: missing '{r}' in manifest")

if failed:
    print("Manifest validation failed:")
    for f in failed:
        print(" -", f)
    sys.exit(2)
print("All plugin manifests validated.")
sys.exit(0)
