import subprocess
import sys


def test_import_cli_module():
    # ensure cli module can be imported without running interactive loop
    code = 'import mercury.cli; print("OK")'
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert p.returncode == 0
    assert "OK" in p.stdout
