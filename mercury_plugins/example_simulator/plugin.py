"""
Example safe plugin.

This plugin demonstrates a Mercury-compatible plugin lifecycle.
- setup / cleanup can run outside the sandbox
- run requires MERCURY_SAFE=1
- only attempts local (127.0.0.1) connections
"""

import os
import sys
import socket


def demo_local_connect(host="127.0.0.1", port=9001):
    """Attempt a local-only connection as a safe demo."""
    try:
        s = socket.create_connection((host, port), timeout=1)
        with s:
            s.sendall(b"hello from example_simulator\n")
            resp = s.recv(1024)
            print("[example_simulator] received:", resp.decode(errors="ignore").strip())
    except Exception as e:
        print(
            "[example_simulator] local connect failed (expected if no server):",
            e,
        )


if __name__ == "__main__":
    # Import lifecycle helpers only when executed directly
    from mercury.plugin_api import BasePlugin, dispatch_lifecycle

    class ExamplePlugin(BasePlugin):
        def setup(self):
            print("[example_simulator] setup (no-op)")
            return 0

        def run(self):
            # Enforce sandbox ONLY for runtime execution
            if os.environ.get("MERCURY_SAFE") != "1":
                print(
                    "[example_simulator] must be run via Mercury sandbox "
                    "(set MERCURY_SAFE=1)"
                )
                return 1

            print("[example_simulator] running safe example plugin")

            # Optional simulated device demo
            try:
                from mercury.simulated_device import SimulatedDevice

                d = SimulatedDevice()
                print(d.device_info())
            except Exception:
                print("[example_simulator] no simulated device available")

            # Demonstrate local-only networking
            demo_local_connect()
            return 0

        def cleanup(self):
            print("[example_simulator] cleanup (no-op)")
            return 0

    plugin = ExamplePlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
