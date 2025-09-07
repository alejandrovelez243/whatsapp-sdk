# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WhatsApp Business SDK for Python - A comprehensive SDK for WhatsApp Business API with FastAPI integration, designed for production use with enterprise-grade reliability and security.

## Development Workflow

### TDD Approach (CRITICAL)
**ALWAYS follow Test-Driven Development:**
1. Write tests FIRST (they should fail initially)
2. Run tests to confirm they fail: `uv run pytest tests/test_<feature>.py -xvs`
3. Implement the minimum code to make tests pass
4. Refactor while keeping tests green
5. Never skip to implementation without tests

### Essential Commands

```bash
# Environment setup
uv sync                              # Install dependencies
uv sync --extra dev                  # Install with dev dependencies
uv sync --extra fastapi              # Install with FastAPI support

# Running tests (TDD workflow)
uv run pytest                        # Run all tests
uv run pytest tests/test_client.py -xvs  # Run specific test file with verbose output
uv run pytest -k "test_send_text"   # Run specific test
uv run pytest --cov=whatsapp_sdk    # Run with coverage
uv run pytest --cov-report=html     # Generate HTML coverage report

# Code quality checks (run before committing)
uv run ruff check src/ tests/        # Lint code
uv run ruff format src/ tests/       # Format code
uv run mypy src/                     # Type checking
uv run bandit -r src/                # Security checks

# Pre-commit hooks
pre-commit install                   # Setup hooks (one-time)
pre-commit run --all-files          # Run all hooks manually

# Building and packaging
uv build                             # Build package
uv publish                           # Publish to PyPI (requires credentials)
```

## Architecture & Implementation Status

### Core Structure
```
src/whatsapp_sdk/
├── client.py        # ✅ Basic implementation (send_text, send_image)
├── config.py        # ✅ Complete with env loading
├── exceptions.py    # ✅ Exception hierarchy defined
├── http_client.py   # ✅ HTTP client with retry logic
├── models/          # ✅ Pydantic models created
│   ├── base.py      # Base models
│   ├── messages.py  # Message models
│   ├── templates.py # Template models
│   └── webhooks.py  # Webhook models
└── [services]/      # ⏳ Pending implementation
    ├── messages/    # Message service
    ├── templates/   # Template management
    ├── media/       # Media handling
    └── webhooks/    # Webhook processing
```

### Implementation Progress (from TASKS.md)
- **Phase 1**: Foundation ✅ (Project setup, core client, models)
- **Phase 2**: Messaging Features 🚧 (Basic text/image implemented)
- **Phase 3**: Template Management ⏳ (Pending)
- **Phase 4**: Webhook Integration ⏳ (Pending)
- **Phase 5**: Media Management ⏳ (Pending)
- **Phase 6**: Advanced Features ⏳ (Pending)
- **Phase 7**: Testing ⏳ (No tests written yet)
- **Phase 8**: Documentation ⏳ (Pending)

## Key Technical Decisions

### Dependencies & Tools
- **Package Manager**: UV (not pip/poetry) - all commands use `uv run`
- **HTTP Client**: httpx (async-first, not requests)
- **Validation**: Pydantic v2 (strict type checking)
- **Testing**: pytest with pytest-asyncio for async tests
- **Linting**: ruff (replaces flake8, black, isort)
- **Type Checking**: mypy with strict mode
- **Security**: bandit for vulnerability scanning

### API Design Principles
- **Async-First**: All API methods are async (use `await`)
- **Type Safety**: Full type hints with Pydantic models
- **Error Handling**: Custom exception hierarchy (WhatsAppError base)
- **Validation**: Input validation before API calls
- **FastAPI Integration**: Native support with dependency injection

## Critical Implementation Notes

### WhatsApp API Specifics
- **API Version**: v18.0 (update in client.py if needed)
- **Phone Format**: Strip to digits only, validate 7-15 length
- **Message Limits**: Text: 4096 chars, Caption: 1024 chars
- **Rate Limiting**: 80 calls/second default (configurable)
- **Webhook Security**: HMAC-SHA256 signature validation required

### Testing Requirements
- **Coverage Target**: 90% minimum
- **Test Structure**: Mirror src/ structure in tests/
- **Mock Strategy**: Use pytest-mock for external API calls
- **Async Testing**: Use pytest-asyncio fixtures
- **Integration Tests**: Separate from unit tests

### Deployment Preparation
- **Version Management**: Follow semantic versioning (0.1.0 currently)
- **PyPI Package**: Name is "whatsapp-sdk"
- **Build System**: Uses uv_build backend
- **Python Support**: 3.8+ (ensure compatibility)
- **Documentation**: MkDocs with Material theme configured

## Common Development Tasks

### Adding a New Message Type
1. Create test file: `tests/test_messages_<type>.py`
2. Write failing tests for the new message type
3. Add Pydantic model in `models/messages.py`
4. Implement method in `client.py` or service class
5. Run tests until green
6. Update API documentation

### Implementing a Service Module
1. Create test file: `tests/test_<service>.py`
2. Write interface tests (what the service should do)
3. Create service class in `src/whatsapp_sdk/<service>/`
4. Wire service into WhatsAppClient.__init__
5. Implement methods following TDD
6. Add integration tests

### Webhook Handler Implementation
1. Write tests for webhook payload parsing
2. Test signature validation thoroughly
3. Create FastAPI router example in `examples/`
4. Implement webhook models validation
5. Add event routing logic
6. Document security requirements

## Environment Variables

Required for running the SDK:
```bash
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_APP_SECRET=your_app_secret       # For webhook validation
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_token  # For webhook setup
```

## Pre-Commit Checklist

Before committing any changes:
1. ✅ All tests pass: `uv run pytest`
2. ✅ Coverage maintained: `uv run pytest --cov=whatsapp_sdk`
3. ✅ Linting clean: `uv run ruff check src/ tests/`
4. ✅ Types check: `uv run mypy src/`
5. ✅ Security scan: `uv run bandit -r src/`
6. ✅ Pre-commit hooks: `pre-commit run --all-files`

## Current Priorities (from TASKS.md)

1. **Immediate**: Complete Phase 2 messaging features with tests
2. **Next**: Implement webhook processing (Phase 4)
3. **Then**: Template management (Phase 3)
4. **Finally**: Documentation and examples (Phase 8)

## Resources

- **Project Docs**: See `claude_docs/` for PRD, Technical Spec, API Design
- **Task Tracking**: `claude_docs/TASKS.md` for detailed task breakdown
- **WhatsApp API**: https://developers.facebook.com/docs/whatsapp
- **FastAPI Integration**: Priority for webhook handling