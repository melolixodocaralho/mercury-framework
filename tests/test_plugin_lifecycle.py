import os
import subprocess
import sys
from mercury.plugin_loader import discover_plugins

# Helper function to run plugin commands safely
def run_cmd(path, args):
    env = os.environ.copy()
    env['MERCURY_SAFE'] = '1'  # ensures the plugin runs in safe mode
    p = subprocess.run([sys.executable, path] + args, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr

def test_example_plugin_lifecycle():
    plugins = discover_plugins()
    # Find our plugin
    p = next((p for p in plugins if p['name'] == 'example_simulator'), None)
    assert p is not None, "example_simulator plugin not discovered"

    # Use cross-platform path
    plugin_py = os.path.join(p['path'], 'plugin.py')

    # Run setup
    rc, out, err = run_cmd(plugin_py, ['--setup'])
    print(out, err)
    assert rc == 0, f"Setup failed: {err}"
    assert 'setup' in out.lower()

    # Run main
    rc, out, err = run_cmd(plugin_py, ['--run'])
    print(out, err)
    assert rc == 0, f"Run failed: {err}"
    assert 'running safe example plugin' in out.lower()

    # Run cleanup
    rc, out, err = run_cmd(plugin_py, ['--cleanup'])
    print(out, err)
    assert rc == 0, f"Cleanup failed: {err}"
    assert 'cleanup' in out.lower()
