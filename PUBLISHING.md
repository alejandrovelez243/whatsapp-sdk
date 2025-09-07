# Publishing to PyPI Guide

## Prerequisites

1. **PyPI Account**: Create accounts at:
   - [PyPI](https://pypi.org/account/register/)
   - [Test PyPI](https://test.pypi.org/account/register/) (for testing)

2. **API Tokens**: Generate tokens for both:
   - PyPI: Account Settings → API tokens → Add API token
   - Test PyPI: Same process on test.pypi.org

## Step 1: GitHub Repository Setup

### 1.1 Create Repository
```bash
# Initialize git if not already done
git init

# Add remote
git remote add origin https://github.com/alejandrovelez243/whatsapp-sdk.git

# Create main branch
git branch -M main

# Push initial commit
git add .
git commit -m "Initial commit: WhatsApp SDK Python"
git push -u origin main
```

### 1.2 Create develop branch
```bash
git checkout -b develop
git push -u origin develop
```

### 1.3 Add Secrets to GitHub

Go to: Settings → Secrets and variables → Actions

Add these secrets:
- `PYPI_TOKEN`: Your PyPI API token
- `TEST_PYPI_TOKEN`: Your Test PyPI API token

### 1.4 Branch Protection Rules

Go to: Settings → Branches → Add rule

For `main` branch:
- ✅ Require a pull request before merging
- ✅ Require approvals (1)
- ✅ Dismiss stale pull request approvals
- ✅ Require status checks to pass (lint, test, security)
- ✅ Require branches to be up to date
- ✅ Include administrators

For `develop` branch:
- ✅ Require status checks to pass
- ✅ Require branches to be up to date

## Step 2: Local Development Setup

### 2.1 Install Development Dependencies
```bash
# Using uv
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Or using pip
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2.2 Install Pre-commit Hooks
```bash
pre-commit install
pre-commit run --all-files  # Test that it works
```

### 2.3 Run Quality Checks
```bash
# Format code
black src/ tests/
ruff format src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/

# Run tests
pytest tests/ --cov=whatsapp_sdk
```

## Step 3: Publishing Process

### 3.1 Test on Test PyPI First

```bash
# Build the package
python -m build

# Check the build
twine check dist/*

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation
pip install -i https://test.pypi.org/simple/ whatsapp-sdk
```

### 3.2 Version Management

Update version in `pyproject.toml`:
```toml
version = "0.1.1"  # Increment as needed
```

### 3.3 Create a Release

```bash
# Ensure you're on main
git checkout main
git pull origin main

# Create a tag
git tag -a v0.1.0 -m "Release version 0.1.0"

# Push the tag
git push origin v0.1.0
```

### 3.4 GitHub Release

1. Go to Releases → Create a new release
2. Choose the tag you just created
3. Title: `v0.1.0 - Initial Release`
4. Description: Add changelog
5. ✅ Set as latest release
6. Publish release

The GitHub Action will automatically:
- Build the package
- Run all tests
- Publish to PyPI

## Step 4: Manual Publishing (if needed)

```bash
# Build
python -m build

# Upload to PyPI
twine upload dist/*
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backward compatible
- **PATCH** (0.0.1): Bug fixes, backward compatible

Examples:
- `0.1.0` → `0.1.1`: Bug fix
- `0.1.1` → `0.2.0`: New feature
- `0.2.0` → `1.0.0`: Breaking change

## Checklist Before Publishing

- [ ] All tests pass: `pytest tests/`
- [ ] Code is formatted: `black src/ tests/`
- [ ] No linting errors: `ruff check src/ tests/`
- [ ] Type checking passes: `mypy src/`
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Version number is incremented
- [ ] Test on Test PyPI first

## Common Issues

### 1. Package Name Taken
If `whatsapp-sdk` is taken, try:
- `whatsapp-sdk`
- `whatsapp-business-sdk`
- `whatsapp-cloud-sdk`

### 2. Build Errors
```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Rebuild
python -m build
```

### 3. Upload Errors
```bash
# Check PyPI token is correct
echo $PYPI_TOKEN

# Try with username/password
twine upload dist/* --username __token__ --password $PYPI_TOKEN
```

## Maintenance

### Weekly Tasks
- Update dependencies: `pip list --outdated`
- Check security: `safety check`
- Review open issues

### Monthly Tasks
- Review and merge dependabot PRs
- Update documentation
- Check for deprecated features

### Per Release
- Update CHANGELOG.md
- Test all examples
- Update README if needed

## Resources

- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)
- [Python Packaging User Guide](https://packaging.python.org/)

---

## Quick Commands Reference

```bash
# Development
uv pip install -e ".[dev]"     # Install in dev mode
pytest tests/                   # Run tests
black src/ tests/               # Format code
ruff check src/ tests/          # Lint
mypy src/                       # Type check

# Building
python -m build                 # Build package
twine check dist/*              # Check build

# Publishing
twine upload --repository testpypi dist/*  # Test PyPI
twine upload dist/*                         # PyPI

# Git
git tag -a v0.1.0 -m "Message"  # Create tag
git push origin v0.1.0          # Push tag
```
