# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take the security of WhatsApp SDK Python seriously. If you have discovered a security vulnerability, we appreciate your help in disclosing it to us in a responsible manner.

### How to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **alejandro-243@hotmail.com**

### What to Include

Please include the following information:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- **Initial Response**: Within 48 hours
- **Assessment**: Within 1 week
- **Resolution**: Varies based on complexity, typically 2-4 weeks

### What to Expect

1. **Acknowledgment**: We'll acknowledge receipt of your vulnerability report
2. **Assessment**: We'll assess the vulnerability and determine its impact
3. **Communication**: We'll keep you informed about our progress
4. **Fix**: We'll work on a fix and coordinate with you on disclosure
5. **Credit**: We'll credit you for the discovery (unless you prefer to remain anonymous)

## Security Best Practices

When using WhatsApp SDK Python, follow these security best practices:

### 1. Protect Your Credentials

Never hardcode credentials in your source code:

```python
# ❌ WRONG - Never do this
client = WhatsAppClient(
    access_token="EAABxxxxx",  # Hardcoded token
    app_secret="abc123"         # Hardcoded secret
)

# ✅ CORRECT - Use environment variables
import os
client = WhatsAppClient(
    access_token=os.getenv("WHATSAPP_ACCESS_TOKEN"),
    app_secret=os.getenv("WHATSAPP_APP_SECRET")
)
```

### 2. Validate Webhook Signatures

Always validate webhook signatures to ensure requests are from WhatsApp:

```python
from fastapi import HTTPException

@app.post("/webhook")
async def handle_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    # Always validate the signature
    if not client.webhooks.verify_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Process webhook...
```

### 3. Use HTTPS

Always use HTTPS for:
- Webhook endpoints
- Media URLs
- API communications

### 4. Rate Limiting

Implement rate limiting to prevent abuse:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/webhook")
@limiter.limit("100/minute")
async def handle_webhook(request: Request):
    # Handle webhook...
```

### 5. Input Validation

Always validate and sanitize user input:

```python
# Use Pydantic models for validation
from whatsapp_sdk.models import TextMessage

try:
    message = TextMessage(body=user_input)  # Pydantic validates
    client.messages.send_text(to=phone, text=message)
except ValidationError as e:
    # Handle invalid input
    logger.error(f"Invalid input: {e}")
```

### 6. Logging and Monitoring

- Log security events (failed authentications, invalid signatures)
- Monitor for unusual patterns
- Never log sensitive data (tokens, passwords, personal information)

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log security events
logger.info(f"Webhook received from IP: {request.client.host}")
logger.warning(f"Invalid signature from IP: {request.client.host}")
```

### 7. Keep Dependencies Updated

Regularly update dependencies to patch security vulnerabilities:

```bash
# Check for outdated packages
pip list --outdated

# Update packages
pip install --upgrade whatsapp-sdk
```

## Security Features

WhatsApp SDK Python includes several security features:

1. **Automatic Token Redaction**: Tokens are automatically redacted in logs
2. **Signature Validation**: Built-in webhook signature validation
3. **Type Safety**: Pydantic models prevent injection attacks
4. **HTTPS Enforcement**: API calls use HTTPS by default
5. **No Credential Storage**: SDK never stores credentials to disk

## Compliance

This SDK helps you maintain compliance with:

- **GDPR**: No automatic data collection or storage
- **WhatsApp Business API Terms**: Follows official API guidelines
- **Data Protection**: Supports encryption and secure communication

## Additional Resources

- [WhatsApp Business API Security](https://developers.facebook.com/docs/whatsapp/api/security)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)

---

Thank you for helping keep WhatsApp SDK Python and its users safe! 🔐
