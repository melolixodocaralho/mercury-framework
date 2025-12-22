# Mercury Framework (Safe Educational Scaffold)

Mercury Framework is an educational scaffold for security researchers and pentesters.

It provides a modular, plugin-friendly CLI and harmless simulated device components so contributors can learn about workflows safely in isolated labs and emulators.

**Author:** voltsparx  
**Contact:** voltsparx@gmail.com

IMPORTANT: This repository contains ONLY harmless simulation code and benign network demos. It does NOT include implants, malware, or tools for unauthorized access. Use only in authorized test environments, with explicit consent, and in accordance with laws and organizational policies.

Quick start

- Create a Python virtual environment and install:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

- Run the CLI:

```powershell
python run.py
```

What this scaffold provides

- A menu-driven CLI with three rotating banner designs.
 - A `mercury.simulated_device` module with harmless stubs (fake SMS, fake gallery, fake camera feed, device info).
- Benign local-network demo modules for learning network flows.
- CONTRIBUTING, SECURITY, and RESPONSIBLE_USE guidance to maintain safe, ethical usage.
 - A set of safe plugin templates for Android, Windows, macOS, Linux, network and forensic simulations under `mercury_plugins/templates/`.
 - A sandbox example (Dockerfile) under `sandbox/` to run plugin subprocesses in a container for isolated testing.
 - A manifest validation script `tools/check_manifests.py` and a CI workflow stub that validates manifests and runs tests.
 - Lab setup guidance in `LAB_SETUP.md` describing isolated VMs, Android AVD setup, and consent checklists.

Packaging & Installers

- Platform installer scripts are included under `scripts/`:
	- `scripts/build_windows_installer.ps1` — creates a distributable ZIP and `install.ps1` helper for Windows.
	- `scripts/build_msi.ps1` — WiX-based MSI builder (requires WiX Toolset on Windows).
	- `scripts/build_debian.sh` — build a `.deb` package on Debian/Ubuntu hosts.
	- `scripts/build_arch.sh` — prepare PKGBUILD and optionally run `makepkg` on Arch.
	- `scripts/build_macos_installer.sh` — macOS `.pkg` and `.dmg` creator (requires Xcode CLT).

See `INSTALL.md` for detailed instructions on building and installing per-platform packages.

Responsible use & license

- This project is provided under the MIT license. By using this software you accept responsibility to use it only for lawful, authorized research and testing.
- See `RESPONSIBLE_USE.md` and `SECURITY.md` for guidelines and contact policy.

UI and plugin templates

 - Use `Plugins` from the CLI to discover local plugin folders under `mercury_plugins/`.
 - Copy the templates in `mercury_plugins/templates/` to create new safe plugins. Every plugin must include `manifest.json` and declare `network_policy` and `responsible_use`.

CI and manifest checks

- The CI workflow runs `tools/check_manifests.py` to ensure all plugins include required fields. Plugins that lack required metadata will fail CI.

Screenshot (terminal)

```
Mercury Framework (safe educational scaffold)
	Learn, build, defend.

Select an option:

1) Simulated device (view fake SMS, gallery, camera)
2) Benign network demos (local echo)
3) Plugins directory (list available plugins)
4) About / Responsible Use
5) Exit

Enter choice number:
```

Contributing

Contributions are welcome. Please read `CONTRIBUTING.md` and follow the repository's safety rules.
