# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WhatsApp Business SDK for Python - A comprehensive SDK for WhatsApp Business API with FastAPI integration, designed for production use with enterprise-grade reliability and security.

## Architecture Guidelines (CRITICAL)

### SDK Style Pattern - OpenAI/ElevenLabs Pattern
**DO NOT USE CONTEXT MANAGERS** - No `async with` pattern. Follow this style:

```python
# ✅ CORRECT - Direct instantiation
from whatsapp_sdk import WhatsAppClient

client = WhatsAppClient(
    phone_number_id="123",
    access_token="token"
)

# Use services through client
response = await client.messages.send_text(to="+1234567890", body="Hello")
await client.media.upload_image(image_path)
await client.templates.send_template(template_id="welcome")
```

```python
# ❌ WRONG - Don't use context managers
async with WhatsAppClient() as client:  # NO!
    await client.send_text(...)  # NO!
```

### Service Module Structure (STRICT)

**NEVER put everything in client.py!** Each service has its own module:

```
src/whatsapp_sdk/
├── client.py           # ONLY client initialization and service wiring
├── services/           # All business logic goes here!
│   ├── messages.py     # Message sending logic
│   ├── media.py        # Media upload/download
│   ├── templates.py    # Template management
│   ├── webhooks.py     # Webhook processing
│   └── utils.py        # Shared utilities
└── models/            # Pydantic models (already organized)
```

**Service Module Pattern:**
```python
# services/messages.py
class MessagesService:
    def __init__(self, http_client: HTTPClient, config: Config):
        self.http = http_client
        self.config = config
    
    async def send_text(self, to: str, body: str) -> MessageResponse:
        # Implementation here
        pass
```

**Client Wiring Pattern:**
```python
# client.py (ONLY wiring, no business logic!)
from whatsapp_sdk.services.messages import MessagesService
from whatsapp_sdk.services.media import MediaService
from whatsapp_sdk.services.templates import TemplatesService

class WhatsAppClient:
    def __init__(self, ...):
        # Initialize HTTP client
        self.http = HTTPClient(...)
        
        # Wire services (NO business logic here!)
        self.messages = MessagesService(self.http, self.config)
        self.media = MediaService(self.http, self.config)
        self.templates = TemplatesService(self.http, self.config)
        self.webhooks = WebhooksService(self.config)
```

### Test Organization (STRICT)

**NEVER put all tests in root tests/ folder!** Mirror the source structure:

```
tests/
├── unit/                    # Unit tests mirror src structure
│   ├── test_client.py      # Test client initialization only
│   ├── services/           # Service tests
│   │   ├── test_messages.py
│   │   ├── test_media.py
│   │   ├── test_templates.py
│   │   └── test_webhooks.py
│   └── models/            # Model tests
│       ├── test_messages_models.py
│       └── test_webhook_models.py
├── integration/           # Integration tests
│   ├── test_message_flow.py
│   └── test_webhook_flow.py
└── fixtures/             # Shared test fixtures
    └── mock_responses.py
```

### API Response Pattern (STRICT)

**ALWAYS return Pydantic models, NEVER dicts:**

```python
# ✅ CORRECT
async def send_text(...) -> MessageResponse:
    response = await self.http.post(...)
    return MessageResponse(**response)  # Pydantic model

# ❌ WRONG
async def send_text(...) -> dict:
    return await self.http.post(...)  # NO! Never return raw dict
```

## Development Workflow

### TDD Approach (CRITICAL)
**ALWAYS follow Test-Driven Development:**
1. Write tests FIRST (they should fail initially)
2. Run tests to confirm they fail: `uv run pytest tests/unit/services/test_<feature>.py -xvs`
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
uv run pytest tests/unit/services/test_messages.py -xvs  # Run specific test
uv run pytest -k "test_send_text"   # Run specific test
uv run pytest --cov=whatsapp_sdk    # Run with coverage

# Code quality checks (run before committing)
uv run ruff check src/ tests/        # Lint code
uv run ruff format src/ tests/       # Format code
uv run mypy src/                     # Type checking
uv run bandit -r src/                # Security checks
```

## Implementation Checklist

When implementing a new feature:

1. **Service Module First**
   - [ ] Create service class in `services/<feature>.py`
   - [ ] Define interface with type hints
   - [ ] NO business logic in client.py

2. **Test Structure**
   - [ ] Create test in `tests/unit/services/test_<feature>.py`
   - [ ] Write failing tests first (TDD)
   - [ ] Test both success and error cases

3. **Model Definition**
   - [ ] Create Pydantic models in `models/<feature>.py`
   - [ ] Always return models, never dicts
   - [ ] Validate all inputs

4. **Client Wiring**
   - [ ] Wire service in client.__init__
   - [ ] Only pass dependencies, no logic
   - [ ] Keep client.py minimal

## Current Implementation Status

### ✅ Completed
- Project setup and configuration
- HTTP client with retry logic
- Pydantic models structure
- Basic message sending (needs refactoring to services/)

### 🚧 In Progress
- Refactoring messages to services/messages.py
- Organizing tests into proper structure

### ⏳ Pending
- Media service implementation
- Template management service
- Webhook processing service
- Integration tests
- Documentation

## Common Pitfalls to Avoid

1. **DON'T** use context managers (`async with`)
2. **DON'T** put business logic in client.py
3. **DON'T** return raw dicts from API methods
4. **DON'T** create tests in root tests/ folder
5. **DON'T** skip writing tests first (TDD)
6. **DON'T** use `client.send_text()` - use `client.messages.send_text()`

## Service Implementation Template

Use this template when creating new services:

```python
# services/new_feature.py
from typing import Optional
from whatsapp_sdk.http_client import HTTPClient
from whatsapp_sdk.config import Config
from whatsapp_sdk.models.new_feature import NewFeatureResponse

class NewFeatureService:
    """Handle new feature operations."""
    
    def __init__(self, http_client: HTTPClient, config: Config):
        """Initialize service with dependencies."""
        self.http = http_client
        self.config = config
    
    async def do_something(self, param: str) -> NewFeatureResponse:
        """
        Do something with the feature.
        
        Args:
            param: Description
            
        Returns:
            NewFeatureResponse: Pydantic model response
            
        Raises:
            ValidationError: If parameters invalid
            APIError: If API request fails
        """
        # Validate inputs
        self._validate_param(param)
        
        # Make API call
        response = await self.http.post(
            endpoint="...",
            json={...}
        )
        
        # Return Pydantic model
        return NewFeatureResponse(**response)
    
    def _validate_param(self, param: str) -> None:
        """Private validation method."""
        if not param:
            raise ValidationError("Param required")
```

## Pre-Commit Checklist

Before committing any changes:
1. ✅ Tests written first and passing
2. ✅ Service logic in services/ folder
3. ✅ Tests in proper subfolder structure  
4. ✅ Pydantic models returned (no dicts)
5. ✅ No context manager usage
6. ✅ Linting and type checking pass