"""Mercury interactive console — single-entry REPL with module commands and help.

This console mirrors the original project console but uses the `mercury` package
and `mercury_plugins` directory. It enforces local-only plugin manifests and
runs plugins inside the Mercury sandbox subprocess (sets `MERCURY_SAFE=1`).
"""
from __future__ import annotations

import shlex
import textwrap
import os
from typing import Optional, List

from .ui import display_banner, color_text, prompt
from .plugin_loader import discover_plugins
from .sandbox import run_plugin_subprocess, validate_manifest_local_only
from .simulated_device import SimulatedDevice
from .simulated_contacts import sample_contacts
from .simulated_sensors import sensor_readings
from .simulated_storage import storage_listing
from .benign_demo import EchoServer

from pathlib import Path
try:
    import readline  # type: ignore
except Exception:
    readline = None


class MercuryConsole:
    def __init__(self):
        self.prompt = color_text("mercury> ", "green")
        self.device = SimulatedDevice()
        self.echo_server: Optional[EchoServer] = None
        self.plugins = discover_plugins()
        self.current_plugin: Optional[dict] = None
        # setup completion and history
        self._setup_readline()

    def _setup_readline(self):
        histfile = Path.home() / ".mercury_history"
        try:
            if readline:
                # build completions from commands and plugin names
                commands = [
                    'help', 'banner', 'modules', 'info', 'run', 'sim', 'echo', 'analyze', 'logparse', 'exit', 'quit'
                ]
                plugin_names = [p['name'] for p in self.plugins]
                words = commands + plugin_names

                def completer(text, state):
                    options = [w for w in words if w.startswith(text)]
                    if state < len(options):
                        return options[state]
                    return None

                readline.set_completer(completer)
                readline.parse_and_bind('tab: complete')
                # read history
                try:
                    readline.read_history_file(str(histfile))
                except Exception:
                    pass
                import atexit

                def save_hist():
                    try:
                        readline.write_history_file(str(histfile))
                    except Exception:
                        pass

                atexit.register(save_hist)
        except Exception:
            pass

    def start(self):
        display_banner()
        print(color_text("Type 'help' for commands. Be safe and use test environments only.", "yellow"))
        while True:
            try:
                line = prompt(self.prompt)
            except (KeyboardInterrupt, EOFError):
                print()
                self.do_exit([])
                break
            if not line:
                continue
            args = shlex.split(line)
            cmd = args[0].lower()
            handler = getattr(self, f"do_{cmd}", None)
            if handler:
                try:
                    handler(args[1:])
                except Exception as e:
                    print(color_text(f"Error: {e}", "red"))
            else:
                print(color_text(f"Unknown command: {cmd}. Type 'help' for a list.", "red"))

    def execute_line(self, line: str):
        """Execute a single console line (used by non-interactive mode)."""
        if not line:
            return
        args = shlex.split(line)
        cmd = args[0].lower()
        handler = getattr(self, f"do_{cmd}", None)
        if handler:
            handler(args[1:])
        else:
            print(color_text(f"Unknown command: {cmd}. Type 'help' for a list.", "red"))

    # Basic commands
    def do_help(self, argv: List[str]):
        """help [command]  - Show help. If command provided, show command-specific help."""
        if argv:
            cmd = argv[0].lower()
            method = getattr(self, f"help_{cmd}", None)
            if method:
                method()
            else:
                print(color_text("No help available for that command.", "yellow"))
            return
        print(textwrap.dedent(
            """
            Mercury console commands (safe, educational):

            help [command]         - Show this help or command-specific help
            banner [n]             - Show a banner (n optional: 1-3)
            modules                - List discovered plugin templates and plugins
            info <plugin>          - Show manifest info for a plugin
            run <plugin> [phases]  - Run plugin lifecycle phases (phases: setup,run,cleanup)
            sim <what>             - Show simulated data (device|contacts|sensors|storage)
            echo start|stop|send   - Control local echo server for demos
            analyze manifest <path>- Analyze an AndroidManifest.xml (static only)
            logparse <file>        - Run simple suspicious log parser on a file
            exit|quit              - Exit the console
            """
        ))

    def help_run(self):
        print(textwrap.dedent(
            """
            run <plugin> [phases]

            Run a plugin discovered under `mercury_plugins/` in the sandbox. Phases
            is a comma-separated list containing any of: setup, run, cleanup

            Examples:
              run example_simulator run
              run android-sim-template setup,run,cleanup
            """
        ))

    # Banner
    def do_banner(self, argv: List[str]):
        """banner [n] - Show a random or numbered banner (1-3)."""
        n = None
        if argv:
            try:
                idx = int(argv[0]) - 1
                if idx in (0, 1, 2):
                    # map to the existing themes by name
                    themes = [None, None, None]
                    # display_banner accepts theme name or None; we'll call display_banner multiple times
                    # but we just call it here to keep behavior simple
                    pass
            except Exception:
                pass
        display_banner()

    # Modules
    def do_modules(self, argv: List[str]):
        """modules - list discovered plugins/templates"""
        self.plugins = discover_plugins()
        if not self.plugins:
            print(color_text("No plugins found under mercury_plugins/", "yellow"))
            return
        print(color_text("Discovered plugins:", "cyan"))
        for p in self.plugins:
            m = p.get("manifest", {})
            print(f" - {m.get('name')} : {m.get('description', '')}")

    def do_info(self, argv: List[str]):
        """info <plugin> - show manifest and responsible use info for a plugin"""
        if not argv:
            print("Usage: info <plugin_name>")
            return
        name = argv[0]
        found = next((p for p in self.plugins if p['name'] == name), None)
        if not found:
            print(color_text("Plugin not found", "red"))
            return
        m = found.get('manifest', {})
        print(color_text(f"Name: {m.get('name')}", "cyan"))
        print(f"Version: {m.get('version')}")
        print(f"Description: {m.get('description')}")
        print(color_text("Responsible use:", "yellow"))
        print(textwrap.indent(str(m.get('responsible_use', 'N/A')), '  '))

    def do_run(self, argv: List[str]):
        """run <plugin> [phases] - run plugin lifecycle phases in sandbox (setup, run, cleanup)"""
        if not argv:
            print("Usage: run <plugin_name> [phases]")
            return
        name = argv[0]
        phases = []
        if len(argv) > 1:
            phases = argv[1].split(',')
        found = next((p for p in self.plugins if p['name'] == name), None)
        if not found:
            print(color_text("Plugin not found", "red"))
            return
        manifest = found.get('manifest', {})
        if not validate_manifest_local_only(manifest):
            print(color_text("Plugin rejected: manifest must declare network_policy: local-only", "red"))
            return
        argmap = {'setup': '--setup', 'run': '--run', 'cleanup': '--cleanup'}
        args = [argmap[p] for p in phases if p in argmap]
        if not args:
            args = ['--run']
        print(color_text(f"Running {name} with args: {args}", "cyan"))
        res = run_plugin_subprocess(found['path'], args=args, timeout=20)
        print(color_text("--- stdout ---", "green"))
        print(res.get('stdout', ''))
        if res.get('stderr'):
            print(color_text("--- stderr ---", "red"))
            print(res.get('stderr'))

    # Simulated data
    def do_sim(self, argv: List[str]):
        """sim <device|contacts|sensors|storage> - show simulated data for demos"""
        if not argv:
            print("Usage: sim <device|contacts|sensors|storage>")
            return
        what = argv[0]
        if what == 'device':
            print(self.device.device_info())
        elif what == 'contacts':
            for c in sample_contacts():
                print(f"- {c.name} | {c.phone} | {c.email}")
        elif what == 'sensors':
            print(sensor_readings())
        elif what == 'storage':
            for f in storage_listing():
                print(f"- {f}")
        else:
            print("Unknown sim target")

    # Echo server controls
    def do_echo(self, argv: List[str]):
        """echo start|stop|send <message> - control local echo server for demos"""
        if not argv:
            print("Usage: echo start|stop|send <message>")
            return
        cmd = argv[0]
        if cmd == 'start':
            if self.echo_server and self.echo_server._thread and self.echo_server._thread.is_alive():
                print("Echo server already running")
            else:
                self.echo_server = EchoServer(host='127.0.0.1', port=8000)
                self.echo_server.start()
                print(color_text('Echo server started on 127.0.0.1:8000', 'green'))
        elif cmd == 'stop':
            if self.echo_server:
                self.echo_server.stop()
                self.echo_server = None
                print('Echo server stopped')
            else:
                print('No running echo server')
        elif cmd == 'send':
            if len(argv) < 2:
                print('Usage: echo send <message>')
                return
            msg = ' '.join(argv[1:])
            try:
                from .benign_demo import echo_client_send
                resp = echo_client_send(msg, host='127.0.0.1', port=8000)
                print('Received:', resp)
            except Exception as e:
                print(color_text(f'Failed to send to echo server: {e}', 'red'))
        else:
            print('Unknown echo command')

    # Static analysis & detection
    def do_analyze(self, argv: List[str]):
        """analyze manifest <path> - run static manifest analyzer (requires extracted AndroidManifest.xml)"""
        if len(argv) < 2 or argv[0] != 'manifest':
            print('Usage: analyze manifest <path_to_AndroidManifest.xml>')
            return
        path = Path(argv[1])
        if not path.exists():
            print('File not found:', path)
            return
        try:
            from ..tools.apk_manifest_analyzer import analyze_manifest, pretty_print
        except Exception:
            # fallback import style
            from tools.apk_manifest_analyzer import analyze_manifest, pretty_print
        report = analyze_manifest(path)
        pretty_print(report)

    def do_logparse(self, argv: List[str]):
        """logparse <file> - run simple suspicious log parser and print matches"""
        if not argv:
            print('Usage: logparse <file>')
            return
        path = Path(argv[0])
        if not path.exists():
            print('File not found:', path)
            return
        text = path.read_text(encoding='utf-8', errors='replace')
        # Import the log parser dynamically so the import resolves whether
        # `detection` is a top-level package or available via different
        # package layouts (avoids static analyzer false-positives).
        import importlib
        mod = None
        for candidate in ("detection.log_parser", "mercury.detection.log_parser"):
            try:
                mod = importlib.import_module(candidate)
                break
            except Exception:
                continue
        if mod is None:
            print(color_text('Log parser module not available', 'red'))
            return
        matches = getattr(mod, 'find_suspicious_lines')(text)
        if not matches:
            print(color_text('No suspicious lines found', 'green'))
            return
        print(color_text('Suspicious lines found:', 'yellow'))
        for m in matches:
            print(' -', m)

    def do_exit(self, argv: List[str]):
        """exit - exit the console"""
        print(color_text('Goodbye — stay ethical.', 'cyan'))
        if self.echo_server:
            try:
                self.echo_server.stop()
            except Exception:
                pass
        raise SystemExit(0)

    def do_quit(self, argv: List[str]):
        self.do_exit(argv)


def start_console(non_interactive: bool = False, commands: Optional[List[str]] = None):
    """Start the Mercury console.

    If `non_interactive` is True, `commands` (list of lines) will be executed
    sequentially and the function will return without entering the interactive
    REPL. This supports `run.py -c` and `-s` script mode.
    """
    c = MercuryConsole()
    if non_interactive:
        commands = commands or []
        for line in commands:
            try:
                c.execute_line(line)
            except SystemExit:
                # allow scripts to exit early
                break
        return
    c.start()


if __name__ == '__main__':
    start_console()
