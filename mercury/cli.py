"""Mercury CLI (safe educational scaffold)

Provides a small menu-driven CLI with three rotating banners and simple options
that operate only on simulated devices and benign demos.
"""
import random
import textwrap
from .simulated_device import SimulatedDevice
from .plugin_loader import discover_plugins, load_manifest
from .sandbox import run_plugin_subprocess, validate_manifest_local_only
from .ui import display_banner, prompt
from .benign_demo import EchoServer, echo_client_send

BANNERS = [
    r"""
 __  __  _____ _____  ____  ____  _____
|  \/  |/ ____|  __ \|  _ \|  _ \|  __ \
| \  / | |  __| |__) | |_) | |_) | |__) |
| |\/| | | |_ |  _  /|  _ <|  _ <|  _  /
| |  | | |__| | | \ \| |_) | |_) | | \ \
|_|  |_|\_____|_|  \_\____/|____/|_|  \_\
""",
    r"""
 __  __  _____  _____ _____ _     _____
|  \/  |/ ____|/ ____|_   _| |   |  __ \
| \  / | (___ | |      | | | |   | |__) |
| |\/| |\___ \| |      | | | |   |  ___/
| |  | |____) | |____ _| |_| |___| |
|_|  |_|_____/ \_____|_____|_____|_|
""",
    r"""
 __  __  ______ _____  _____  _____
|  \/  |/ ____|  __ \|  __ \|  __ \
| \  / | |  __| |__) | |  | | |__) |
| |\/| | | |_ |  _  /| |  | |  _  /
| |  | | |__| | | \ \| |__| | | \ \
|_|  |_|\_____|_|  \_\\____/|_|  \_\
""",
]

HACKER_QUOTES = [
    "Information wants to be free.",
    "Security is not a product, but a process.",
    "Learn, build, defend.",
]


def print_banner():
    banner = random.choice(BANNERS)
    quote = random.choice(HACKER_QUOTES)
    print(banner)
    print(f"\n  {quote}\n")


def main():
    display_banner()
    print("Mercury Framework (safe educational scaffold)")
    print("Author: voltsparx <voltsparx@gmail.com>\n")

    device = SimulatedDevice()

    while True:
        menu = textwrap.dedent(
            """
            Select an option:

            1) Simulated device (view fake SMS, gallery, camera)
            2) Benign network demos (local echo)
            3) Plugins directory (list available plugins)
            4) About / Responsible Use
            5) Exit
            """
        )
        print(menu)
        choice = prompt("Enter choice number: ").strip()
        if choice == "1":
            handle_simulated(device)
        elif choice == "2":
            handle_benign_network()
        elif choice == "3":
            plugins = discover_plugins()
            if not plugins:
                print("Plugins: (none installed). Add plugins under mercury_plugins/ with a manifest.")
            else:
                print("Available plugins:")
                for i, p in enumerate(plugins, start=1):
                    m = p.get("manifest", {})
                    print(f"{i}) {m.get('name')} - {m.get('description', '')}")
                    sel = prompt("Enter plugin number to run (or press Enter to cancel): ").strip()
                if sel:
                    try:
                        idx = int(sel) - 1
                        chosen = plugins[idx]
                        manifest = chosen.get("manifest", {})
                        if not validate_manifest_local_only(manifest):
                            print("Plugin rejected: manifest must declare 'network_policy': 'local-only'")
                        else:
                            # prompt for lifecycle phases
                            print("Choose lifecycle phases to run (comma-separated):")
                            print("  1) setup")
                            print("  2) run")
                            print("  3) cleanup")
                            phases = prompt("Enter choices (e.g. 2 or 1,2,3) [default: 2]: ").strip()
                            if not phases:
                                phases = "2"
                            choice_map = {"1": "--setup", "2": "--run", "3": "--cleanup"}
                            args = []
                            for token in [p.strip() for p in phases.split(',') if p.strip()]:
                                if token in choice_map:
                                    args.append(choice_map[token])
                            if not args:
                                args = ["--run"]
                            print(f"Running plugin {manifest.get('name')} in sandbox with args: {args}...")
                            res = run_plugin_subprocess(chosen.get("path"), args=args, timeout=12)
                            print("--- plugin stdout ---")
                            print(res.get("stdout", ""))
                            if res.get("stderr"):
                                print("--- plugin stderr ---")
                                print(res.get("stderr"))
                    except Exception as e:
                        print("Failed to run plugin:", e)
        elif choice == "4":
            print_responsible_use()
        elif choice == "5":
            print("Goodbye — stay ethical.")
            break
        else:
            print("Invalid choice, try again.")


def handle_simulated(device: SimulatedDevice):
    while True:
        submenu = textwrap.dedent(
            """
            Simulated device menu:
            1) Show device info
            2) Show fake SMS messages
            3) Show fake gallery entries
            4) Show fake camera frame (ASCII)
            5) Back
            """
        )
        print(submenu)
        c = input("Enter choice: ").strip()
        if c == "1":
            print(device.device_info())
        elif c == "2":
            for m in device.fake_sms():
                print(f"- {m}")
        elif c == "3":
            for g in device.fake_gallery():
                print(f"- {g}")
        elif c == "4":
            print(device.fake_camera_frame())
        elif c == "5":
            break
        else:
            print("Invalid choice")


def handle_benign_network():
    server: EchoServer | None = None
    while True:
        print("\nBenign network demos (local-only):")
        print("1) Start local echo server (127.0.0.1:8000)")
        print("2) Send test message to local echo server")
        print("3) Stop local echo server")
        print("4) Back")
        sel = prompt("Enter choice: ").strip()
        if sel == "1":
            if server is None:
                server = EchoServer(host="127.0.0.1", port=8000)
                server.start()
                print("Local echo server started on 127.0.0.1:8000")
            else:
                print("Echo server already running")
        elif sel == "2":
            msg = prompt("Enter message to send: ")
            try:
                resp = echo_client_send(msg, host="127.0.0.1", port=8000)
                print("Received:", resp)
            except Exception as e:
                print("Failed to send/receive:", e)
        elif sel == "3":
            if server:
                server.stop()
                server = None
                print("Echo server stopped")
            else:
                print("No server is running")
        elif sel == "4":
            if server:
                server.stop()
            break
        else:
            print("Invalid choice")


def print_responsible_use():
    print(textwrap.dedent(
        """
        Responsible use:
        - Use this framework only for authorized testing and learning in isolated labs.
        - Do NOT use it to access or exfiltrate data from systems you do not own or have explicit permission to test.
        - Review `RESPONSIBLE_USE.md` and `SECURITY.md` for more details.
        """
    ))


if __name__ == "__main__":
    main()
