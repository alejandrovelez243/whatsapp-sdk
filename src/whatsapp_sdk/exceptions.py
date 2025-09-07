"""
Exception classes for WhatsApp SDK.
"""

from typing import Any, Dict, Optional


class WhatsAppError(Exception):
    """Base exception for all WhatsApp SDK errors."""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, code={self.code!r})"


class APIError(WhatsAppError):
    """Error from WhatsApp API."""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, code, details)
        self.status_code = status_code

    @classmethod
    def from_response(cls, response: Dict[str, Any]) -> "APIError":
        """Create APIError from API response."""
        error = response.get("error", {})
        return cls(
            message=error.get("message", "Unknown API error"),
            code=error.get("code"),
            status_code=error.get("error_subcode"),
            details=error.get("error_data", {}),
        )


class AuthenticationError(WhatsAppError):
    """Authentication failed."""

    pass


class ValidationError(WhatsAppError):
    """Data validation failed."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Any = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details=details)
        self.field = field
        self.value = value


class RateLimitError(WhatsAppError):
    """Rate limit exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details=details)
        self.retry_after = retry_after


class MediaError(WhatsAppError):
    """Media operation failed."""

    def __init__(
        self,
        message: str,
        media_type: Optional[str] = None,
        media_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details=details)
        self.media_type = media_type
        self.media_id = media_id


class TemplateError(WhatsAppError):
    """Template operation failed."""

    def __init__(
        self,
        message: str,
        template_name: Optional[str] = None,
        template_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, details=details)
        self.template_name = template_name
        self.template_id = template_id


class WebhookError(WhatsAppError):
    """Webhook processing failed."""

    pass


class NetworkError(WhatsAppError):
    """Network-related error."""

    pass
