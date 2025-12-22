"""Simple UI helpers for Mercury console (banners, color, prompt)

This module provides minimal utilities used by the console: `display_banner`,
`color_text`, and `prompt`. It's intentionally small and dependency-free.
"""
from __future__ import annotations

import random
import sys
from typing import Optional

BANNERS = [
    r"""
+==========================================+
|    __  ___                               |
|   /  |/  /__  ____________  _________  __|
|  / /|_/ / _ \/ ___/ ___/ / / / ___/ / / /|
| / /  / /  __/ /  / /__/ /_/ / /  / /_/ / |
|/_/  /_/\___/_/   \___/\__,_/_/   \__, /  |
|                                 /____/   |
+==========================================+
""",
    r"""
___  ___                               
|  \/  |                               
| .  . | ___ _ __ ___ _   _ _ __ _   _ 
| |\/| |/ _ \ '__/ __| | | | '__| | | |
| |  | |  __/ | | (__| |_| | |  | |_| |
\_|  |_/\___|_|  \___|\__,_|_|   \__, |
                                  __/ |
                                 |___/ 
""",
    r"""
+==========================================+
|    __  ___                               |
|   /  |/  /__  ____________  _________  __|
|  / /|_/ / _ \/ ___/ ___/ / / / ___/ / / /|
| / /  / /  __/ /  / /__/ /_/ / /  / /_/ / |
|/_/  /_/\___/_/   \___/\__,_/_/   \__, /  |
|                                 /____/   |
+==========================================+
""",
]

HACKER_QUOTES = [
    "Learn, build, defend.",
    "Security is a process, not a product.",
    "Test in isolated labs."
]

COLOR_MAP = {
    'red': '\x1b[31m',
    'green': '\x1b[32m',
    'yellow': '\x1b[33m',
    'blue': '\x1b[34m',
    'magenta': '\x1b[35m',
    'cyan': '\x1b[36m',
    'reset': '\x1b[0m',
}


def display_banner():
    b = random.choice(BANNERS)
    q = random.choice(HACKER_QUOTES)
    print(b)
    print(f"\n  {q}\n")


def color_text(text: str, color: Optional[str] = None) -> str:
    if not color:
        return text
    code = COLOR_MAP.get(color.lower(), '')
    reset = COLOR_MAP.get('reset', '')
    # If stdout is not a tty (e.g., redirected), avoid ANSI sequences
    if not sys.stdout.isatty():
        return text
    return f"{code}{text}{reset}"


def prompt(msg: str = '') -> str:
    try:
        return input(msg)
    except (KeyboardInterrupt, EOFError):
        raise
