"""Windows simulation plugin template (benign example)."""
import sys
import os
from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class WindowsSimPlugin(BasePlugin):
    def setup(self):
        print("[windows-sim-template] setup: pre-checks")
        return 0

    def run(self):
        print("[windows-sim-template] run: benign demo for Windows environment")
        return 0

    def cleanup(self):
        print("[windows-sim-template] cleanup")
        return 0


if __name__ == '__main__':
    if os.environ.get('MERCURY_SAFE') != '1':
        print('[windows-sim-template] must be run via Mercury sandbox (MERCURY_SAFE=1)')
        sys.exit(1)
    plugin = WindowsSimPlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
