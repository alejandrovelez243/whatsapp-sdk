# Contributing to WhatsApp SDK

¡Gracias por tu interés en contribuir al WhatsApp SDK! / Thank you for your interest in contributing to WhatsApp SDK!

## 🎯 How to Contribute

We welcome contributions from the community! Here are ways you can help:

- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new features
- 🌍 Add translations

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- `uv` package manager (recommended) or `pip`
- Git

### Development Setup

1. **Fork the repository**
   ```bash
   # Click "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/whatsapp-sdk.git
   cd whatsapp-sdk
   ```

3. **Create a virtual environment**
   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Or using venv
   python -m venv .venv
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   # Using uv
   uv pip install -e ".[dev]"

   # Or using pip
   pip install -e ".[dev]"
   ```

5. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

## 📋 Development Workflow

### 1. Create a Feature Branch

```bash
# Create a new branch from main
git checkout -b feature/your-feature-name

# For bug fixes
git checkout -b fix/issue-description

# For documentation
git checkout -b docs/what-you-are-documenting
```

### 2. Make Your Changes

Follow the project structure and conventions defined in `CLAUDE.md`:

- **Services**: All business logic goes in `src/whatsapp_sdk/services/`
- **Models**: Pydantic models in `src/whatsapp_sdk/models/`
- **Tests**: Mirror the source structure in `tests/unit/`
- **SYNCHRONOUS**: This SDK is synchronous - no async/await

### 3. Write Tests FIRST (TDD)

**Tests are mandatory!** We follow Test-Driven Development:

```python
# tests/unit/services/test_your_feature.py
def test_your_feature():
    """Test description."""
    # Write your test first
    assert expected == actual
```

Run tests:
```bash
# Run specific test
uv run pytest tests/unit/services/test_your_feature.py -xvs

# Run all tests with coverage
uv run pytest --cov=whatsapp_sdk

# Run only unit tests
uv run pytest tests/unit/
```

### 4. Follow Code Style

The project uses `ruff` and `black` for code formatting:

```bash
# Format code
uv run ruff format src/ tests/
uv run black src/ tests/

# Check linting
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

### 5. Update Documentation

- Update docstrings for all public methods
- Update README.md if adding new features
- Add examples in `examples/` directory if applicable

### 6. Commit Your Changes

Follow conventional commits format:

```bash
# Features
git commit -m "feat: add template message support"

# Bug fixes
git commit -m "fix: correct webhook signature validation"

# Documentation
git commit -m "docs: update installation instructions"

# Tests
git commit -m "test: add unit tests for media service"

# Refactoring
git commit -m "refactor: simplify message builder logic"

# Performance
git commit -m "perf: optimize batch message sending"

# Chores
git commit -m "chore: update dependencies"
```

### 7. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Description of what and why
- Link to related issue (if any)
- Screenshots/examples (if UI related)

## 📝 Pull Request Guidelines

### PR Title Format
```
<type>(<scope>): <subject>

Types: feat, fix, docs, test, refactor, perf, chore
Scope: messages, media, templates, webhooks, client, etc.
```

Examples:
- `feat(messages): add support for reaction messages`
- `fix(webhooks): validate signature correctly`
- `docs(readme): add usage examples`

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature that would break existing functionality)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass locally
- [ ] Integration tests pass (if applicable)
- [ ] Coverage remains above 80%

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Dependent changes merged

## Related Issues
Fixes #(issue number)
```

## 🧪 Testing Requirements

### Coverage Requirements
- New features must have >90% test coverage
- Overall project coverage must stay above 80%
- All public methods must have tests

### Test Categories

1. **Unit Tests** (`tests/unit/`)
   - Test individual components in isolation
   - Use mocks for external dependencies
   - Must run without network access

2. **Integration Tests** (`tests/integration/`)
   - Test interaction with WhatsApp API
   - Require test credentials
   - May be skipped in CI for external contributors

## 🏗️ Architecture Guidelines

### Follow SOLID Principles

1. **Single Responsibility**: Each class/function does one thing
2. **Open/Closed**: Open for extension, closed for modification
3. **Liskov Substitution**: Derived classes must be substitutable
4. **Interface Segregation**: Don't depend on unused interfaces
5. **Dependency Inversion**: Depend on abstractions

### Project Structure

```
src/whatsapp_sdk/
├── client.py          # Client initialization only
├── services/          # ALL business logic here
│   ├── messages.py    # MessagesService class
│   ├── media.py       # MediaService class
│   └── templates.py   # TemplatesService class
├── models/            # Pydantic models
└── http_client.py     # HTTP client (synchronous)
```

### Important Rules

1. **NO ASYNC**: This SDK is synchronous - no async/await
2. **Pydantic Models**: Always return Pydantic models, never dicts
3. **Service Pattern**: Business logic in services, not in client
4. **Meta API Compliance**: Follow Meta's official documentation
5. **Type Hints**: Use type hints everywhere

## 🔍 Code Review Process

All PRs will be reviewed for:

1. **Functionality**: Does it work as intended?
2. **Tests**: Are there adequate tests?
3. **Documentation**: Is it well documented?
4. **Style**: Does it follow project conventions?
5. **Performance**: Is it efficient?
6. **Security**: Are there any security concerns?

## 🚫 What We Don't Accept

- PRs without tests
- Breaking changes without discussion
- Code that doesn't follow project style
- Features outside the project scope
- Async/await implementations (this is a sync SDK)
- Direct commits to main branch

## 🤝 Community Guidelines

### Be Respectful
- Use welcoming and inclusive language
- Respect differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Communication Channels

- **Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Pull Requests**: Code contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- GitHub contributors page
- CHANGELOG.md (for significant contributions)
- README.md (for major contributors)

## ❓ Questions?

If you have questions, please:
1. Check existing issues and discussions
2. Read the documentation
3. Open a new discussion if needed

---

Thank you for contributing to WhatsApp SDK! 🎉
