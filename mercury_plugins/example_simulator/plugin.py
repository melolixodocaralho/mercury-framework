"""Example safe plugin.

This plugin reads `MERCURY_SAFE` env var as a lightweight check, prints device info
when invoked with `--run` and demonstrates connecting to `127.0.0.1` only as a safe demo.
"""
import os
import sys
import socket


def demo_local_connect(host="127.0.0.1", port=9001):
    try:
        s = socket.create_connection((host, port), timeout=1)
        with s:
            s.sendall(b"hello from example_simulator\n")
            resp = s.recv(1024)
            print("[example_simulator] received:", resp.decode(errors="ignore").strip())
    except Exception as e:
        print("[example_simulator] local connect failed (expected if no server):", e)


if __name__ == "__main__":
    # simple safety check
    if os.environ.get("MERCURY_SAFE") != "1":
        print("[example_simulator] must be run via Mercury sandbox (MERCURY_SAFE=1)")
        sys.exit(1)

    # support lifecycle hooks: --setup, --run, --cleanup
    from mercury.plugin_api import BasePlugin, dispatch_lifecycle

    class ExamplePlugin(BasePlugin):
        def setup(self):
            print("[example_simulator] setup (no-op)")
            return 0

        def run(self):
            print("[example_simulator] running safe example plugin")
            # print a tiny simulated device info if available via import
            try:
                from mercury.simulated_device import SimulatedDevice
                d = SimulatedDevice()
                print(d.device_info())
            except Exception:
                print("[example_simulator] no simulated device available")
            # attempt local connect to show how a plugin could demonstrate network flows
            demo_local_connect()
            return 0

        def cleanup(self):
            print("[example_simulator] cleanup (no-op)")
            return 0

    plugin = ExamplePlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
