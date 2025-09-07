# Contributing to WhatsApp SDK Python

Thank you for your interest in contributing to WhatsApp SDK Python! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Process](#development-process)
- [Environment Setup](#environment-setup)
- [Style Guides](#style-guides)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### 🐛 Reporting Bugs

Before creating a bug report, please check that a similar issue doesn't already exist.

**To report a bug:**

1. Use the bug issue template
2. Include a clear and descriptive title
3. Provide detailed steps to reproduce the problem
4. Include minimal example code that reproduces the issue
5. Describe expected behavior vs actual behavior
6. Include logs, screenshots if applicable
7. Mention your environment (Python version, OS, etc.)

### 💡 Suggesting Enhancements

1. First check existing issues and the roadmap
2. Open an issue using the feature request template
3. Clearly explain the problem it solves
4. Provide usage examples
5. If possible, suggest an implementation

### 🔧 Contributing Code

1. **Fork the repository**
2. **Create a branch** from `develop`:
   ```bash
   git checkout -b feature/amazing-feature
   # or
   git checkout -b fix/bug-description
   ```

3. **Set up your development environment**:
   ```bash
   # Clone your fork
   git clone https://github.com/your-username/whatsapp-sdk-python.git
   cd whatsapp-sdk-python

   # Install with uv (recommended)
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e ".[dev]"

   # Or with pip
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Development Process

### 1. Test-Driven Development (TDD)

**MANDATORY**: Write tests FIRST

```python
# 1. Write the test first in tests/unit/services/test_feature.py
def test_new_feature():
    service = FeatureService(...)
    result = service.do_something("param")
    assert result.success is True

# 2. Run the test (should fail)
pytest tests/unit/services/test_feature.py -xvs

# 3. Implement the functionality in src/whatsapp_sdk/services/feature.py

# 4. Run the test until it passes
```

### 2. Code Rules

#### ⚠️ CRITICAL: NO ASYNC/AWAIT

This SDK is **SYNCHRONOUS**. Don't use `async/await` anywhere:

```python
# ✅ CORRECT
def send_message(self, to: str, body: str) -> MessageResponse:
    response = self.http.post(endpoint, json=payload)
    return MessageResponse(**response)

# ❌ INCORRECT
async def send_message(self, to: str, body: str) -> MessageResponse:
    response = await self.http.post(endpoint, json=payload)
    return MessageResponse(**response)
```

#### 📦 Service Structure

**NEVER** put business logic in `client.py`:

```python
# ✅ CORRECT: services/messages.py
class MessagesService:
    def send_text(self, to: str, body: str) -> MessageResponse:
        # All logic here

# client.py only wires services
self.messages = MessagesService(...)

# ❌ INCORRECT: NO pongas lógica en client.py
class WhatsAppClient:
    def send_text(self, ...):  # NO! DON'T put logic in client.py
```

#### 🔍 Always Return Pydantic Models

```python
# ✅ CORRECT
def get_media(self, media_id: str) -> MediaResponse:
    data = self.http.get(f"/{media_id}")
    return MediaResponse(**data)  # Pydantic model

# ❌ INCORRECT
def get_media(self, media_id: str) -> dict:
    return self.http.get(f"/{media_id}")  # DON'T return dicts
```

### 3. Code Quality

Before committing, run:

```bash
# Formatting
black src/ tests/
ruff format src/ tests/

# Linting
ruff check src/ tests/

# Type checking
mypy src/

# Tests
pytest tests/ --cov=whatsapp_sdk

# All together
make quality  # If you have Makefile
```

## Style Guides

- **Python**: We follow PEP 8 with 100 character lines
- **Commits**: Conventional Commits
  - `feat:` New feature
  - `fix:` Bug fix
  - `docs:` Documentation changes
  - `test:` Add or modify tests
  - `refactor:` Refactoring without functional changes
  - `chore:` Maintenance tasks
- **Docstrings**: Google style
- **Type hints**: Required in all public functions

## Pull Request Process

1. **Update your branch** with the latest changes from `develop`:
   ```bash
   git fetch upstream
   git rebase upstream/develop
   ```

2. **Ensure all tests pass**:
   ```bash
   pytest tests/
   ```

3. **Update documentation** if necessary

4. **Create the Pull Request**:
   - Use a descriptive title
   - Reference any related issue (#123)
   - Describe the changes made
   - Include screenshots if there are visual changes
   - Mark the checklist in the PR template

5. **Review Process**:
   - At least 1 approval required
   - All CI checks must pass
   - No conflicts with the base branch
   - Test coverage must not decrease

### PR Checklist

- [ ] I have read the contribution guidelines
- [ ] My code follows the project style
- [ ] I have added tests that prove my fix/feature
- [ ] All tests pass locally
- [ ] I have updated documentation if necessary
- [ ] My code is SYNCHRONOUS (no async/await)
- [ ] I have followed the service structure
- [ ] I return Pydantic models, not dicts

## Branch Structure

- `main` - Production branch, stable
- `develop` - Development branch, for integration
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates
- `release/*` - Release preparation

## Versioning

We follow [Semantic Versioning](https://semver.org/):
- MAJOR: Backward incompatible changes
- MINOR: New backward compatible functionality
- PATCH: Backward compatible bug fixes

## Communication

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussions
- **Discord/Slack**: [Coming soon]

## Recognition

All contributors will be added to the README! 🌟

## License

By contributing, you agree that your contributions will be licensed under the same MIT License as the project.

---

Questions? Open an issue or contact us.

Thank you for making WhatsApp SDK Python better! 💚
