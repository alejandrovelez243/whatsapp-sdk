"""WhatsApp Business SDK for Python.

A comprehensive, synchronous SDK for the WhatsApp Business API.
"""

__version__ = "0.1.0"

from .client import WhatsAppClient
from .config import WhatsAppConfig
from .exceptions import (
    WhatsAppError,
    WhatsAppAPIError,
    WhatsAppAuthenticationError,
    WhatsAppRateLimitError,
    WhatsAppValidationError,
    WhatsAppWebhookError,
    WhatsAppMediaError,
    WhatsAppTimeoutError,
    WhatsAppConfigError,
)

# Import all models for convenience
from .models import (
    # Base models
    BaseResponse,
    Contact,
    Error,
    ErrorResponse,
    Message,
    MessageResponse,
    PaginationCursor,
    PaginationInfo,
    # Message models
    TextMessage,
    ImageMessage,
    DocumentMessage,
    AudioMessage,
    VideoMessage,
    StickerMessage,
    LocationMessage,
    InteractiveMessage,
    TemplateMessage,
    ReactionMessage,
    MessageStatus,
    # Contact models
    Name,
    Phone,
    Email,
    Address,
    Organization,
    ContactMessage,
    # Template models
    Template,
    TemplateButton,
    TemplateComponent,
    TemplateParameter,
    TemplateResponse,
    # Media models
    MediaUploadResponse,
    MediaURLResponse,
    MediaDeleteResponse,
    # Webhook models
    WebhookEvent,
    WebhookMessage,
    WebhookStatus,
    WebhookVerification,
)

__all__ = [
    # Main client
    "WhatsAppClient",
    "WhatsAppConfig",
    # Exceptions
    "WhatsAppError",
    "WhatsAppAPIError",
    "WhatsAppAuthenticationError",
    "WhatsAppRateLimitError",
    "WhatsAppValidationError",
    "WhatsAppWebhookError",
    "WhatsAppMediaError",
    "WhatsAppTimeoutError",
    "WhatsAppConfigError",
    # Models (most common ones)
    "TextMessage",
    "ImageMessage",
    "DocumentMessage",
    "AudioMessage",
    "VideoMessage",
    "LocationMessage",
    "InteractiveMessage",
    "TemplateMessage",
    "ContactMessage",
    "MessageResponse",
    "WebhookEvent",
    "WebhookMessage",
]