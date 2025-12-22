"""Safe defensive helpers: local-only port scanner and log monitor.

These tools are intended for defensive research and triage in authorized
environments. They deliberately avoid any offensive capabilities.
"""
from typing import List
import socket
import time


def local_port_scan(host: str = '127.0.0.1', ports: List[int] = None, timeout: float = 0.2) -> List[int]:
    """Scan a short list of ports on localhost and return open ports.

    This function performs TCP connect attempts against `host` for provided
    `ports`. It is intended for triage in lab environments only.
    """
    if ports is None:
        ports = [22, 80, 443, 8000, 8080]
    open_ports = []
    for p in ports:
        try:
            with socket.create_connection((host, p), timeout=timeout):
                open_ports.append(p)
        except Exception:
            continue
    return open_ports


def tail_log(path: str, lines: int = 20) -> List[str]:
    """Return the last `lines` of a text file (simple tail implementation)."""
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as fh:
            all_lines = fh.readlines()
    except Exception:
        return []
    return all_lines[-lines:]
