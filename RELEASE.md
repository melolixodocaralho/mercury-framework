Release and packaging

This project uses a standard Python packaging workflow. Use the steps below to
create source and wheel distributions for release.

1) Prepare your environment (recommended in a CI runner)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

2) Build distributions

```powershell
python -m build
```

If you prefer the older commands:

```powershell
python setup.py sdist bdist_wheel
```

3) Verify artifacts in `dist/` and sign if required by your release process.

4) Publish to PyPI (if desired and permitted):

```powershell
python -m pip install --upgrade twine
python -m twine upload dist/*
```

Notes

- Ensure tests pass and CI validates manifests before creating a release.
- Include a clear release changelog and responsible-use reminder in release notes.
