# Changelog

All notable changes to the WhatsApp SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - Unreleased

### Added
- Typing indicator API integration
  - Added `typing_indicator` parameter to `mark_as_read()` method
  - New `send_typing_indicator()` convenience method for showing typing status
  - Typing indicator displays for up to 25 seconds or until a message is sent
  - Comprehensive test coverage for typing indicator functionality

### Improved
- MediaService enhancements and fixes
  - Fixed API endpoint to include v23.0 version prefix for proper WhatsApp Cloud API compliance
  - Added multipart upload support to HTTPClient for file uploads
  - Added binary download support to HTTPClient for media downloads
  - Improved error handling and retry logic for media operations
  - Enhanced reliability for media file operations
  - 100% test coverage for MediaService (32 comprehensive tests covering all scenarios)

## [0.1.0] - 2025-01-07

### Added
- Initial release of WhatsApp Business SDK for Python
- Core client implementation with service-oriented architecture
- Synchronous HTTP client with retry logic and rate limiting
- Comprehensive Pydantic models for type safety
- Service modules:
  - **Messages Service**: Send text, images, documents, audio, video, stickers, location, and contacts
  - **Templates Service**: Manage and send template messages
  - **Media Service**: Upload and manage media files
  - **Webhooks Service**: Handle incoming webhook events with signature validation
  - **Utils**: Phone number formatting and validation utilities
- Support for all WhatsApp message types:
  - Text messages with URL preview
  - Media messages (image, document, audio, video, sticker)
  - Location sharing
  - Contact cards
  - Interactive messages (buttons and lists)
- FastAPI integration support
- Comprehensive error handling with custom exception hierarchy
- Environment-based configuration
- Pre-commit hooks for code quality (ruff, mypy, isort, bandit)
- Unit test suite with pytest
- Python 3.8+ support
- WhatsApp Cloud API v23.0 compatibility

### Security
- HMAC-SHA256 webhook signature validation
- Secure token handling via environment variables
- Input validation on all API methods

[Unreleased]: https://github.com/yourusername/whatsapp-sdk/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/whatsapp-sdk/releases/tag/v0.1.0
