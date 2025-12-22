"""Sandbox runner — execute plugins in a subprocess with simple safety checks.

This is NOT a security boundary. It provides a lightweight isolation pattern for
plugins by running them in a separate Python process and enforcing manifest
policies (e.g., `network_policy: local-only`). For real isolation use VMs/containers.
"""
import json
import os
import subprocess
import sys
import threading
from typing import Dict


def run_plugin_subprocess(plugin_path: str, args: list | None = None, timeout: int = 10) -> Dict:
    """Run `plugin.py` under `plugin_path` as subprocess and return stdout/stderr and returncode.

    `args` is a list of CLI args to pass to the plugin (e.g. `['--setup']`).
    The plugin should support the lifecycle flags `--setup`, `--run`, and `--cleanup`.
    An environment variable `MERCURY_SAFE=1` will be set for the subprocess.
    """
    plugin_file = os.path.join(plugin_path, "plugin.py")
    if not os.path.isfile(plugin_file):
        raise FileNotFoundError("plugin.py not found")

    env = os.environ.copy()
    env["MERCURY_SAFE"] = "1"

    # Ensure the project root is on PYTHONPATH so plugins can import `mercury.*`.
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    existing = env.get("PYTHONPATH", "")
    if existing:
        env["PYTHONPATH"] = project_root + os.pathsep + existing
    else:
        env["PYTHONPATH"] = project_root

    if args is None:
        args = ["--run"]

    cmd = [sys.executable, plugin_file] + args
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True)

    timer = threading.Timer(timeout, proc.kill)
    try:
        timer.start()
        out, err = proc.communicate()
    finally:
        timer.cancel()

    return {"returncode": proc.returncode, "stdout": out, "stderr": err}


def validate_manifest_local_only(manifest: Dict) -> bool:
    """Return True if manifest enforces local-only network policy."""
    policy = manifest.get("network_policy", "local-only")
    return policy == "local-only"
