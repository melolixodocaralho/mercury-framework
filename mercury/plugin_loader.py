"""Plugin loader for Mercury — safe, metadata-driven discovery.

Plugins live under `mercury_plugins/<plugin_name>/` and must include a
`manifest.json` with required fields and a `plugin.py` file exposing a
`run()` entrypoint for demonstration purposes.
"""
import json
import os
from typing import Dict, List

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PLUGINS_DIR = os.path.join(ROOT, "mercury_plugins")


class PluginError(Exception):
    pass


def discover_plugins() -> List[Dict]:
    """Return a list of plugin metadata dicts discovered under `mercury_plugins`.

    Each plugin metadata contains keys: name, path, manifest (dict).
    """
    plugins = []
    if not os.path.isdir(PLUGINS_DIR):
        return plugins

    for name in sorted(os.listdir(PLUGINS_DIR)):
        pdir = os.path.join(PLUGINS_DIR, name)
        if not os.path.isdir(pdir):
            continue
        manifest_path = os.path.join(pdir, "manifest.json")
        if not os.path.isfile(manifest_path):
            continue
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception as e:
            # skip malformed manifests
            continue
        # basic validation
        if "name" not in manifest or "version" not in manifest:
            continue
        plugins.append({"name": manifest.get("name"), "path": pdir, "manifest": manifest})
    return plugins


def load_manifest(plugin_path: str) -> Dict:
    manifest_path = os.path.join(plugin_path, "manifest.json")
    if not os.path.isfile(manifest_path):
        raise PluginError("manifest.json not found")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    return manifest
