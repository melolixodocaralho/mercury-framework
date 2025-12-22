import sys
import os
import subprocess
import importlib
from typing import List


def ensure_requirements(reqfile: str = 'requirements.txt', auto_yes: bool = False) -> None:
    """Read `requirements.txt` and pip-install missing packages.

    This is a best-effort helper for convenience during development. It will
    attempt to import each requirement's top-level module name and install the
    package if import fails. Use `--yes` to auto-accept installations.
    """
    if not os.path.isfile(reqfile):
        return
    try:
        with open(reqfile, 'r', encoding='utf-8') as fh:
            lines = [l.strip() for l in fh if l.strip() and not l.strip().startswith('#')]
    except Exception:
        return

    to_install: List[str] = []
    for pkg in lines:
        # best-effort derive import name from package name (strip version pins)
        im = pkg.split('==')[0].split('>=')[0].split('<=')[0].strip()
        modname = im.replace('-', '_')
        try:
            importlib.import_module(modname)
        except Exception:
            to_install.append(pkg)

    if not to_install:
        return

    print("Missing packages detected:")
    for p in to_install:
        print(" -", p)
    if not auto_yes:
        resp = input("Install missing packages now? [y/N]: ").strip().lower()
        if resp not in ('y', 'yes'):
            print("Skipping installation. You can install packages manually:")
            print(f"{sys.executable} -m pip install {' '.join(to_install)}")
            return

    for p in to_install:
        print(f"Installing {p}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', p])


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(prog='mercury-framework', description='Mercury Framework - Safe educational scaffold')
    parser.add_argument('-c', '--command', help='Execute a single console command and exit')
    parser.add_argument('-s', '--script', help='Execute a file containing console commands (one per line)')
    parser.add_argument('-y', '--yes', action='store_true', help='Automatically accept installing missing dependencies')
    args = parser.parse_args(argv)

    # ensure basic requirements (development/test helpers) are present
    ensure_requirements('requirements.txt', auto_yes=args.yes)

    # now import the console and run (use mercury package)
    from mercury.console import start_console
    if args.command:
        start_console(non_interactive=True, commands=[args.command])
    elif args.script:
        try:
            with open(args.script, 'r', encoding='utf-8') as fh:
                lines = [l.strip() for l in fh if l.strip() and not l.strip().startswith('#')]
        except FileNotFoundError:
            print(f"Script file not found: {args.script}")
            raise SystemExit(2)
        start_console(non_interactive=True, commands=lines)
    else:
        start_console()


if __name__ == '__main__':
    main()
