"""
Pydantic models for WhatsApp SDK.
"""

from whatsapp_sdk.models.base import MessageType, RecipientType
from whatsapp_sdk.models.messages import (
    AudioMessage,
    ContactMessage,
    DocumentMessage,
    ImageMessage,
    InteractiveMessage,
    LocationMessage,
    MediaMessage,
    Message,
    MessageResponse,
    TemplateMessage,
    TextMessage,
    VideoMessage,
)
from whatsapp_sdk.models.templates import (
    Component,
    ComponentType,
    Template,
    TemplateCategory,
    TemplateComponent,
    TemplateParameter,
    TemplateStatus,
)
from whatsapp_sdk.models.webhooks import (
    IncomingMessage,
    MessageStatus,
    WebhookChange,
    WebhookEntry,
    WebhookEvent,
    WebhookMetadata,
    WebhookPayload,
    WebhookValue,
)

__all__ = [
    "AudioMessage",
    "Component",
    "ComponentType",
    "ContactMessage",
    "DocumentMessage",
    "ImageMessage",
    "IncomingMessage",
    "InteractiveMessage",
    "LocationMessage",
    "MediaMessage",
    # Messages
    "Message",
    "MessageResponse",
    "MessageStatus",
    # Base
    "MessageType",
    "RecipientType",
    # Templates
    "Template",
    "TemplateCategory",
    "TemplateComponent",
    "TemplateMessage",
    "TemplateParameter",
    "TemplateStatus",
    "TextMessage",
    "VideoMessage",
    "WebhookChange",
    "WebhookEntry",
    "WebhookEvent",
    "WebhookMetadata",
    # Webhooks
    "WebhookPayload",
    "WebhookValue",
]
