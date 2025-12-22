from mercury.plugin_loader import discover_plugins, load_manifest
import os

def test_discover_example_plugin():
    plugins = discover_plugins()
    names = [p['name'] for p in plugins]
    assert 'example_simulator' in names, "example_simulator plugin not found in discovery"

def test_manifest_local_only():
    plugins = discover_plugins()
    p = next((p for p in plugins if p['name'] == 'example_simulator'), None)
    assert p is not None, "example_simulator plugin not found"

    manifest = load_manifest(p['path'])
    assert manifest.get('network_policy') == 'local-only', "network_policy is not 'local-only'"
