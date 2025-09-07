# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WhatsApp Business SDK for Python - A comprehensive **SYNCHRONOUS** SDK for WhatsApp Business API following Meta's official Cloud API documentation, designed for production use with enterprise-grade reliability and security.

## CRITICAL: Meta WhatsApp Cloud API Reference

**ALWAYS follow Meta's official documentation**: https://developers.facebook.com/docs/whatsapp/cloud-api

- **Current API Version**: v23.0 (Latest as of 2024)
- **Base URL**: https://graph.facebook.com/v23.0/
- **Documentation**: Every implementation MUST match Meta's official API specs exactly

## Architecture Pattern (STRICT RULES)

### SDK Style: OpenAI/ElevenLabs Pattern - SYNCHRONOUS

**NO ASYNC/AWAIT** - The SDK is synchronous for simplicity:
**NO CONTEXT MANAGERS** - Clean and straightforward:

```python
# ✅ CORRECT - Simple synchronous calls like OpenAI
from whatsapp_sdk import WhatsAppClient

# Simple and clean instantiation
client = WhatsAppClient(
    phone_number_id="123456789",
    access_token="your_token",
    app_secret="your_secret",
    webhook_verify_token="verify_token"
)

# Direct synchronous service calls - NO await!
response = client.messages.send_text(to="+1234567890", body="Hello")
response = client.messages.send_image(to="+1234567890", image="url_or_id")
response = client.templates.send(to="+1234567890", template="welcome")
```

```python
# ❌ WRONG - No async/await, no context managers
async def send():  # NO! Not async
    await client.messages.send_text(...)  # NO await!

async with WhatsAppClient() as client:  # NO context managers!
    client.send_text(...)  # NO!
```

### Project Structure (MANDATORY)

```
src/whatsapp_sdk/
├── __init__.py
├── client.py                 # ONLY client initialization and service wiring
├── config.py                 # Configuration management
├── exceptions.py             # Custom exceptions
├── http_client.py            # SYNCHRONOUS HTTP client with retry logic
├── models/                   # Pydantic models
│   ├── __init__.py
│   ├── base.py              # Base models
│   ├── messages.py          # Message-related models
│   ├── templates.py         # Template models
│   ├── media.py             # Media models
│   └── webhooks.py          # Webhook models
└── services/                 # ALL business logic goes here
    ├── __init__.py
    ├── messages.py          # MessagesService class
    ├── templates.py         # TemplatesService class
    ├── media.py             # MediaService class
    ├── webhooks.py          # WebhooksService class
    └── utils.py             # Shared utilities

tests/
├── unit/                    # Unit tests mirror src structure
│   ├── test_client.py      # Test ONLY client initialization
│   ├── services/           # Service tests
│   │   ├── test_messages.py
│   │   ├── test_media.py
│   │   ├── test_templates.py
│   │   └── test_webhooks.py
│   └── models/             # Model tests
│       ├── test_message_models.py
│       └── test_webhook_models.py
├── integration/            # Integration tests
│   ├── test_message_flow.py
│   └── test_webhook_flow.py
└── fixtures/              # Test fixtures
    └── mock_responses.py
```

## Implementation Rules

### 1. SYNCHRONOUS ONLY (CRITICAL)

**This SDK is SYNCHRONOUS - NO async/await anywhere:**

```python
# ✅ CORRECT - Synchronous methods
class MessagesService:
    def send_text(self, to: str, body: str) -> MessageResponse:
        """Send text message - SYNCHRONOUS."""
        payload = self._build_payload(to, body)
        response = self.http.post(endpoint, json=payload)  # No await!
        return MessageResponse(**response)

# ❌ WRONG - No async methods
class MessagesService:
    async def send_text(self, to: str, body: str) -> MessageResponse:
        """NO! Don't use async."""
        response = await self.http.post(...)  # NO await!
```

### 2. Pydantic-First Development (CRITICAL)

**Users can and SHOULD pass Pydantic models** - This provides documentation and type safety:

```python
from whatsapp_sdk.models import Contact, Name, Phone, TextMessage

# ✅ USERS: Pass Pydantic models for clarity and type safety
contact = Contact(
    name=Name(first_name="John", last_name="Doe"),
    phones=[Phone(phone="+1234567890", type="MOBILE")]
)
response = client.messages.send_contact(to="+123", contacts=[contact])

text_msg = TextMessage(body="Hello", preview_url=True)
response = client.messages.send_text(to="+123", text=text_msg)

# ✅ SDK: Accept Union but convert immediately
def send_contact(
    self, 
    to: str,
    contacts: Union[List[Contact], List[dict]]
) -> MessageResponse:
    # Convert to Pydantic if needed
    if contacts and isinstance(contacts[0], dict):
        contacts_obj = [Contact(**c) for c in contacts]
    else:
        contacts_obj = contacts  # Already Pydantic
    
    # Internal methods ONLY work with Pydantic
    return self._process_contacts(to, contacts_obj)

def _process_contacts(
    self, 
    to: str,
    contacts: List[Contact]  # ONLY Pydantic, no Union
) -> MessageResponse:
    # Full type safety and IDE support
    for contact in contacts:
        print(contact.name.first_name)  # IDE knows all fields
    # ...

# ❌ WRONG - Don't pass dicts internally
def _process_contacts(self, contacts: Union[List[Contact], List[dict]]):
    # Bad: we lose type safety
```

**Benefits of Pydantic models for users:**
- **Documentation**: See exactly what fields are available
- **IDE Support**: Autocomplete shows all options  
- **Validation**: Errors caught before API call
- **Type Safety**: Know exactly what you're sending/receiving

### 3. Service Module Pattern (MANDATORY)

**NEVER put business logic in client.py!**

```python
# ✅ CORRECT - services/messages.py
from whatsapp_sdk.http_client import HTTPClient
from whatsapp_sdk.config import Config
from whatsapp_sdk.models.messages import MessageResponse

class MessagesService:
    """Handle WhatsApp message operations - SYNCHRONOUS."""
    
    def __init__(self, http_client: HTTPClient, config: Config, phone_number_id: str):
        self.http = http_client
        self.config = config
        self.phone_number_id = phone_number_id
    
    def send_text(self, to: str, body: str, **kwargs) -> MessageResponse:
        """Send text message - SYNCHRONOUS, no async!"""
        # Implementation following https://developers.facebook.com/docs/whatsapp/cloud-api/messages/text-messages
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"body": body}
        }
        response = self.http.post(f"v23.0/{self.phone_number_id}/messages", json=payload)
        return MessageResponse(**response)
```

```python
# ✅ CORRECT - client.py (ONLY wiring, NO logic)
from whatsapp_sdk.services.messages import MessagesService
from whatsapp_sdk.services.media import MediaService
from whatsapp_sdk.services.templates import TemplatesService

class WhatsAppClient:
    def __init__(self, phone_number_id: str, access_token: str, **kwargs):
        # Setup HTTP client (synchronous)
        self.http = HTTPClient(access_token=access_token, **kwargs)
        
        # Wire services - NO BUSINESS LOGIC HERE
        self.messages = MessagesService(self.http, self.config, phone_number_id)
        self.media = MediaService(self.http, self.config, phone_number_id)
        self.templates = TemplatesService(self.http, self.config, phone_number_id)
```

### 4. API Response Pattern (CRITICAL)

**ALWAYS return Pydantic models, NEVER raw dicts:**

```python
# ✅ CORRECT - Synchronous with Pydantic response
def send_text(self, to: str, body: str) -> MessageResponse:
    response = self.http.post(endpoint, json=payload)  # No await
    return MessageResponse(**response)  # Pydantic model

# ❌ WRONG
def send_text(self, to: str, body: str) -> dict:
    return self.http.post(endpoint, json=payload)  # NO! Return Pydantic
```

### 5. Flexible Input Pattern (OpenAI Style)

**Accept simple parameters, dicts, or Pydantic models - but ALWAYS convert to Pydantic internally:**

```python
# ✅ CORRECT - Service implementation (SYNCHRONOUS)
from typing import Union, Optional
from whatsapp_sdk.models import TextMessage, ImageMessage, MessageResponse

class MessagesService:
    def send_text(
        self,
        to: str,
        body: Optional[str] = None,
        text: Optional[Union[TextMessage, dict]] = None,
        preview_url: bool = False
    ) -> MessageResponse:
        """
        Flexible input, SYNCHRONOUS execution.
        
        Examples:
            # 1. Simple params (most common)
            client.messages.send_text(to="123", body="Hello")
            
            # 2. Pydantic model
            msg = TextMessage(body="Hello", preview_url=True)
            client.messages.send_text(to="123", text=msg)
            
            # 3. Dict (gets validated and converted to Pydantic)
            client.messages.send_text(to="123", text={"body": "Hello"})
        """
        # ALWAYS convert to Pydantic immediately
        if text is not None:
            if isinstance(text, dict):
                text_obj = TextMessage(**text)  # Validate and convert
            else:
                text_obj = text  # Already Pydantic
        else:
            text_obj = TextMessage(body=body, preview_url=preview_url)
        
        # Now we ONLY work with Pydantic objects
        payload = self._build_text_payload(to, text_obj)
        response = self.http.post(endpoint, json=payload)  # No await!
        return MessageResponse(**response)
```

### 6. Meta API Compliance

Every endpoint implementation MUST:

1. Check Meta's official documentation first
2. Use the correct endpoint format: `v23.0/{phone_number_id}/{resource}`
3. Include all required fields as per Meta's specs
4. Handle Meta's error responses properly
5. Follow Meta's rate limiting guidelines

Key endpoints from Meta's documentation:
- Messages: `POST /v23.0/{phone-number-id}/messages`
- Media Upload: `POST /v23.0/{phone-number-id}/media`
- Media Download: `GET /v23.0/{media-id}`
- Templates: `POST /v23.0/{phone-number-id}/messages` (with template payload)

### 7. Test Organization Rules

```python
# ✅ CORRECT - tests/unit/services/test_messages.py
import pytest
from whatsapp_sdk.services.messages import MessagesService

class TestMessagesService:
    def test_send_text(self):
        # Test the service SYNCHRONOUSLY
        service = MessagesService(mock_http, config, "123")
        response = service.send_text(to="+1234567890", body="Hello")  # No await!
        assert response.message_id

# ❌ WRONG - No async tests for this SDK
async def test_send_text():  # NO! Not async
    response = await service.send_text(...)  # NO await!
```

## Development Workflow

### TDD is MANDATORY

1. Write tests FIRST in `tests/unit/services/test_<feature>.py`
2. Run tests to confirm they fail
3. Implement in `services/<feature>.py`
4. Run tests until green
5. NEVER skip tests

### Commands

```bash
# Run tests
uv run pytest tests/unit/services/test_messages.py -xvs
uv run pytest --cov=whatsapp_sdk

# Quality checks
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run mypy src/
```

## Common Mistakes to AVOID

### ❌ DON'T Do This:

1. Use async/await anywhere in the SDK
2. Put business logic in client.py
3. Use context managers (`with` or `async with`)
4. Return raw dicts from API methods
5. Create tests in root tests/ folder
6. Skip writing tests first
7. Use `client.send_text()` - always `client.messages.send_text()`
8. Implement without checking Meta's documentation
9. Use outdated API versions (must use v23.0)

### ✅ DO This Instead:

1. Keep everything synchronous (no async/await)
2. Keep all logic in services/ modules
3. Use direct instantiation (OpenAI style)
4. Always return Pydantic models
5. Organize tests in proper subdirectories
6. Write tests first (TDD)
7. Access through service attributes
8. Always reference Meta's official docs
9. Use v23.0 for all API calls

## Meta API Key Concepts

### Message Types (from Meta docs)

- Text messages
- Media messages (image, video, audio, document)
- Template messages
- Interactive messages (buttons, lists)
- Location messages
- Contact messages
- Sticker messages

### Required Headers

```python
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
```

### Error Handling

Follow Meta's error response format:

```python
{
    "error": {
        "message": "Error message",
        "type": "OAuthException",
        "code": 190,
        "error_subcode": 460,
        "fbtrace_id": "xxx"
    }
}
```

## Implementation Checklist

When implementing any feature:

- [ ] Check Meta's documentation: https://developers.facebook.com/docs/whatsapp/cloud-api
- [ ] Create service in `services/<feature>.py` (SYNCHRONOUS)
- [ ] Write tests in `tests/unit/services/test_<feature>.py` (SYNCHRONOUS)
- [ ] Create Pydantic models in `models/<feature>.py`
- [ ] Wire service in client.__init__ (dependencies only)
- [ ] Verify against Meta's API specs
- [ ] Use v23.0 in all endpoints
- [ ] Return Pydantic models, never dicts
- [ ] NO async/await anywhere
- [ ] No context managers

## Quick Reference

### Service Template (SYNCHRONOUS)

```python
# services/new_feature.py
from whatsapp_sdk.http_client import HTTPClient
from whatsapp_sdk.config import Config
from whatsapp_sdk.models.new_feature import NewFeatureResponse

class NewFeatureService:
    """Service following Meta's API documentation - SYNCHRONOUS."""
    
    def __init__(self, http_client: HTTPClient, config: Config, phone_number_id: str):
        self.http = http_client
        self.config = config
        self.phone_number_id = phone_number_id
    
    def do_something(self, param: str) -> NewFeatureResponse:
        """
        Synchronous implementation based on Meta's docs.
        Reference: https://developers.facebook.com/docs/whatsapp/cloud-api/...
        """
        endpoint = f"v23.0/{self.phone_number_id}/resource"
        payload = {"messaging_product": "whatsapp", ...}
        response = self.http.post(endpoint, json=payload)  # No await!
        return NewFeatureResponse(**response)
```

### Client Wiring (in client.py)

```python
# Only dependency injection, no logic, no async
self.new_feature = NewFeatureService(self.http, self.config, phone_number_id)
```

## HTTP Client Pattern (SYNCHRONOUS)

```python
# http_client.py - Using httpx in SYNCHRONOUS mode
import httpx
from typing import Dict, Any

class HTTPClient:
    """Synchronous HTTP client."""
    
    def __init__(self, access_token: str, base_url: str = "https://graph.facebook.com"):
        self.client = httpx.Client(  # Not AsyncClient!
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Synchronous POST request."""
        response = self.client.post(endpoint, **kwargs)  # No await!
        response.raise_for_status()
        return response.json()
    
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Synchronous GET request."""
        response = self.client.get(endpoint, **kwargs)  # No await!
        response.raise_for_status()
        return response.json()
```

## Resources

- **Meta WhatsApp Cloud API**: https://developers.facebook.com/docs/whatsapp/cloud-api
- **API Reference**: https://developers.facebook.com/docs/whatsapp/cloud-api/reference
- **Message Types**: https://developers.facebook.com/docs/whatsapp/cloud-api/messages
- **Webhooks**: https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks
- **Error Codes**: https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes