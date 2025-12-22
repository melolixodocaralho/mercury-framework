"""Plugin template demonstrating setup/run/cleanup lifecycle.

Copy this folder and update `manifest.json` for new plugins. Plugins must
include tests and a `responsible_use` field in the manifest.
"""
import sys
import os
from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class TemplatePlugin(BasePlugin):
    def setup(self):
        print("[plugin_template] setup: prepare simulation environment")
        return 0

    def run(self):
        print("[plugin_template] run: perform local-only demo action")
        # do only localhost operations or simulated operations here
        return 0

    def cleanup(self):
        print("[plugin_template] cleanup: teardown")
        return 0


if __name__ == '__main__':
    if os.environ.get('MERCURY_SAFE') != '1':
        print('[plugin_template] must be run via Mercury sandbox (MERCURY_SAFE=1)')
        sys.exit(1)
    plugin = TemplatePlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
