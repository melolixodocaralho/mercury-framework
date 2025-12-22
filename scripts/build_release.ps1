# PowerShell helper to create a release build (source & wheel) in Windows
# Run from repository root.

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install build
python -m build
Write-Host "Build complete. Artifacts in dist/"
