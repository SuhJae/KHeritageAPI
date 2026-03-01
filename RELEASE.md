# Release Logistics

This repository supports release to both GitHub Releases and PyPI from a version tag.

## One-time Setup

1. In GitHub, configure PyPI Trusted Publishing for this repository, or prepare `PYPI_API_TOKEN` secret.
2. Ensure `main` branch is green on CI.

## Standard Release Flow

1. Update `pyproject.toml` version and `kheritageapi/__init__.py::__version__`.
2. Update `CHANGELOG.md`.
3. Commit and push to `main`.
4. Create and push annotated tag:
   - `git tag -a v2.0.0 -m "Release v2.0.0"`
   - `git push origin v2.0.0`
5. GitHub Actions release workflow runs:
   - Test matrix
   - Build + `twine check`
   - Publish to PyPI
   - Create GitHub Release

## Local Preflight (Optional)

```bash
./.venv/bin/python -m unittest discover -s tests -v
./.venv/bin/python -m build
./.venv/bin/python -m twine check dist/*
```
