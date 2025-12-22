"""APK Manifest Analyzer (safe, static analysis only)

This tool analyzes an Android `AndroidManifest.xml` file (extracted from an APK)
and reports potentially interesting fields that defenders may want to review.

Usage (after extracting APK with `apktool` or similar):

python tools/apk_manifest_analyzer.py path/to/AndroidManifest.xml

This script does NOT process APKs directly and does not perform dynamic actions.
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def analyze_manifest(path: Path) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    ns = {'android': 'http://schemas.android.com/apk/res/android'}

    pkg = root.attrib.get('package')
    version_code = root.attrib.get('{http://schemas.android.com/apk/res/android}versionCode')
    version_name = root.attrib.get('{http://schemas.android.com/apk/res/android}versionName')

    permissions = [p.attrib.get('{http://schemas.android.com/apk/res/android}name') for p in root.findall('uses-permission')]

    activities = []
    for a in root.findall('application/activity'):
        name = a.attrib.get('{http://schemas.android.com/apk/res/android}name')
        exported = a.attrib.get('{http://schemas.android.com/apk/res/android}exported')
        activities.append({'name': name, 'exported': exported})

    receivers = [r.attrib.get('{http://schemas.android.com/apk/res/android}name') for r in root.findall('application/receiver')]
    services = [s.attrib.get('{http://schemas.android.com/apk/res/android}name') for s in root.findall('application/service')]

    return {
        'package': pkg,
        'version_code': version_code,
        'version_name': version_name,
        'permissions': permissions,
        'activities': activities,
        'receivers': receivers,
        'services': services,
    }


def pretty_print(report: dict):
    print(f"Package: {report.get('package')}")
    print(f"Version: {report.get('version_name')} (code {report.get('version_code')})")
    print('\nPermissions:')
    for p in report.get('permissions', []):
        print(' -', p)
    print('\nActivities:')
    for a in report.get('activities', []):
        print(' -', a.get('name'), 'exported=', a.get('exported'))
    print('\nReceivers:')
    for r in report.get('receivers', []):
        print(' -', r)
    print('\nServices:')
    for s in report.get('services', []):
        print(' -', s)


def main():
    if len(sys.argv) != 2:
        print('Usage: python tools/apk_manifest_analyzer.py path/to/AndroidManifest.xml')
        sys.exit(2)
    path = Path(sys.argv[1])
    if not path.exists():
        print('File not found:', path)
        sys.exit(2)
    report = analyze_manifest(path)
    pretty_print(report)


if __name__ == '__main__':
    main()
