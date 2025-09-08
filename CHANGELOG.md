# Changelog

All notable changes to the WhatsApp SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-08

### Added
- Typing indicator API integration
  - Added `typing_indicator` parameter to `mark_as_read()` method
  - New `send_typing_indicator()` convenience method for showing typing status
  - Typing indicator displays for up to 25 seconds or until a message is sent
  - Comprehensive test coverage for typing indicator functionality

- Comprehensive test suites for SDK services
  - **MessagesService**: 60 unit tests covering all message types, error handling, and edge cases (96% coverage)
  - **MediaService**: 32 unit tests covering upload, download, and deletion operations (100% coverage)
  - Test fixtures and mock infrastructure for reliable testing
  - Integration with pytest-cov for coverage reporting

- HTTPClient enhancements
  - `upload_multipart()` method for multipart/form-data uploads with proper boundary handling
  - `download_binary()` method for downloading binary content with retry logic
  - Improved error handling with automatic retries and exponential backoff
  - Rate limiting support with configurable request intervals

### Fixed
- MediaService API compliance issues
  - Fixed missing v23.0 version prefix in API endpoints for WhatsApp Cloud API compliance
  - Corrected base URL construction to properly include API version
  - Fixed media upload to use HTTPClient's multipart upload instead of bypassing it
  - Fixed media download to use HTTPClient's binary download with proper authentication

- MessagesService bug fixes
  - Fixed ContactMessage serialization when passing Pydantic models
  - Corrected contact data extraction for proper API payload generation
  - Improved type handling for flexible input formats (Pydantic models, dicts, or simple params)

### Improved
- MediaService reliability and functionality
  - Enhanced file size validation based on media type (image: 5MB, video/audio: 16MB, document: 100MB, sticker: 512KB)
  - Added support for uploading from bytes in memory via `upload_from_bytes()`
  - Improved MIME type detection with fallback handling
  - Better error messages with specific details about failures
  - Atomic file operations with proper cleanup on errors

- Code quality and maintainability
  - Strict adherence to synchronous pattern (no async/await)
  - Consistent use of Pydantic models for type safety
  - Service-oriented architecture with clear separation of concerns
  - Comprehensive docstrings with usage examples
  - Python 3.8+ compatibility maintained

### Changed
- Updated documentation to reflect new features and improvements
- Enhanced README with clearer usage examples
- Improved API documentation with more detailed parameter descriptions

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

[Unreleased]: https://github.com/yourusername/whatsapp-sdk/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/yourusername/whatsapp-sdk/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/yourusername/whatsapp-sdk/releases/tag/v0.1.0
