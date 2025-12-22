Release notes for Mercury Framework

This release packages the Mercury Framework safe educational scaffold.

What's included:
- Core `mercury` package with console, sandbox, plugin loader, and simulated devices.
- `mercury_plugins` directory with templates and example plugins.
- Packaging scripts:
  - `scripts/build_windows_installer.ps1` (zip + install helper, optional SFX)
  - `scripts/build_msi.ps1` (WiX-based MSI builder; requires WiX Toolset)
  - `scripts/prepare_unix_packages.py` (source tarball + PKGBUILD, optional .deb on Linux)
  - `scripts/create_release_zip.py` (creates `dist/mercury-framework-release.zip`)

Notes:
- This repository intentionally contains only benign simulation code and demos.
- The MSI builder assumes Python is installed on target machines; bundling Python would require extra steps.
