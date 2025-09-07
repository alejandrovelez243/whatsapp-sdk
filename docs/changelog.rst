Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

Added
~~~~~
- Initial release of WhatsApp SDK Python
- Support for all message types (text, media, location, contacts, interactive)
- Template message management
- Media upload/download functionality
- Webhook handling with signature validation
- Comprehensive type hints with Pydantic models
- Retry logic and rate limiting
- Full test coverage

[0.1.0] - 2024-12-07
--------------------

Added
~~~~~
- Project structure and configuration
- Core HTTP client with retry logic
- Pydantic models for all WhatsApp API types
- Messages service implementation
- Templates service implementation
- Media service implementation
- Webhooks service implementation
- Documentation with Sphinx
- Unit tests
- CI/CD with GitHub Actions
- Pre-commit hooks

Fixed
~~~~~
- N/A (Initial release)

Changed
~~~~~~~
- N/A (Initial release)

Deprecated
~~~~~~~~~~
- N/A (Initial release)

Removed
~~~~~~~
- N/A (Initial release)

Security
~~~~~~~~
- Webhook signature validation
- Secure token handling
