"""
Webhook models for WhatsApp SDK.
"""

from typing import Any, Dict, List, Optional

from pydantic import Field

from whatsapp_sdk.models.base import BaseWhatsAppModel, MessageType, StatusType


class WebhookMetadata(BaseWhatsAppModel):
    """Webhook metadata model."""

    display_phone_number: str = Field(..., description="Display phone number")
    phone_number_id: str = Field(..., description="Phone number ID")


class TextContent(BaseWhatsAppModel):
    """Text content in incoming message."""

    body: str = Field(..., description="Message text body")


class MediaContent(BaseWhatsAppModel):
    """Media content in incoming message."""

    id: str = Field(..., description="Media ID")
    mime_type: Optional[str] = Field(None, description="MIME type")
    sha256: Optional[str] = Field(None, description="SHA256 hash")
    caption: Optional[str] = Field(None, description="Media caption")
    filename: Optional[str] = Field(None, description="Filename for documents")


class LocationContent(BaseWhatsAppModel):
    """Location content in incoming message."""

    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    name: Optional[str] = Field(None, description="Location name")
    address: Optional[str] = Field(None, description="Location address")
    url: Optional[str] = Field(None, description="Location URL")


class ContactContent(BaseWhatsAppModel):
    """Contact content in incoming message."""

    name: Dict[str, str] = Field(..., description="Contact name")
    phones: Optional[List[Dict[str, str]]] = Field(None, description="Phone numbers")
    emails: Optional[List[Dict[str, str]]] = Field(None, description="Email addresses")
    addresses: Optional[List[Dict[str, str]]] = Field(None, description="Addresses")
    org: Optional[Dict[str, str]] = Field(None, description="Organization")
    urls: Optional[List[Dict[str, str]]] = Field(None, description="URLs")


class InteractiveContent(BaseWhatsAppModel):
    """Interactive content in incoming message."""

    type: str = Field(..., description="Interactive type")
    button_reply: Optional[Dict[str, str]] = Field(None, description="Button reply")
    list_reply: Optional[Dict[str, str]] = Field(None, description="List reply")


class ReactionContent(BaseWhatsAppModel):
    """Reaction content in incoming message."""

    message_id: str = Field(..., description="Message ID being reacted to")
    emoji: str = Field(..., description="Reaction emoji")


class Context(BaseWhatsAppModel):
    """Message context (for replies)."""

    from_: str = Field(..., alias="from", description="Original sender")
    id: str = Field(..., description="Original message ID")
    forwarded: Optional[bool] = Field(None, description="Is forwarded")
    frequently_forwarded: Optional[bool] = Field(None, description="Is frequently forwarded")


class IncomingMessage(BaseWhatsAppModel):
    """Incoming message model."""

    id: str = Field(..., description="Message ID")
    from_: str = Field(..., alias="from", description="Sender phone number")
    timestamp: str = Field(..., description="Message timestamp")
    type: MessageType = Field(..., description="Message type")
    context: Optional[Context] = Field(None, description="Message context")

    # Content fields based on message type
    text: Optional[TextContent] = Field(None, description="Text content")
    image: Optional[MediaContent] = Field(None, description="Image content")
    video: Optional[MediaContent] = Field(None, description="Video content")
    audio: Optional[MediaContent] = Field(None, description="Audio content")
    voice: Optional[MediaContent] = Field(None, description="Voice note content")
    document: Optional[MediaContent] = Field(None, description="Document content")
    sticker: Optional[MediaContent] = Field(None, description="Sticker content")
    location: Optional[LocationContent] = Field(None, description="Location content")
    contacts: Optional[List[ContactContent]] = Field(None, description="Contacts content")
    interactive: Optional[InteractiveContent] = Field(None, description="Interactive content")
    reaction: Optional[ReactionContent] = Field(None, description="Reaction content")
    errors: Optional[List[Dict[str, Any]]] = Field(None, description="Message errors")

    @property
    def content(self) -> Optional[Any]:
        """Get the message content based on type."""
        content_map = {
            MessageType.TEXT: self.text,
            MessageType.IMAGE: self.image,
            MessageType.VIDEO: self.video,
            MessageType.AUDIO: self.audio,
            MessageType.DOCUMENT: self.document,
            MessageType.STICKER: self.sticker,
            MessageType.LOCATION: self.location,
            MessageType.CONTACTS: self.contacts,
            MessageType.INTERACTIVE: self.interactive,
            MessageType.REACTION: self.reaction,
        }
        return content_map.get(self.type)

    @property
    def is_reply(self) -> bool:
        """Check if message is a reply."""
        return self.context is not None


class MessageStatus(BaseWhatsAppModel):
    """Message status update model."""

    id: str = Field(..., description="Message ID")
    status: StatusType = Field(..., description="Message status")
    timestamp: str = Field(..., description="Status timestamp")
    recipient_id: str = Field(..., description="Recipient ID")
    conversation: Optional[Dict[str, Any]] = Field(None, description="Conversation details")
    pricing: Optional[Dict[str, Any]] = Field(None, description="Pricing information")
    errors: Optional[List[Dict[str, Any]]] = Field(None, description="Status errors")


class ContactInfo(BaseWhatsAppModel):
    """Contact information in webhook."""

    profile: Dict[str, str] = Field(..., description="Contact profile")
    wa_id: str = Field(..., description="WhatsApp ID")


class WebhookValue(BaseWhatsAppModel):
    """Webhook value containing the actual data."""

    messaging_product: str = Field(..., description="Messaging product")
    metadata: WebhookMetadata = Field(..., description="Metadata")
    contacts: Optional[List[ContactInfo]] = Field(None, description="Contact information")
    messages: Optional[List[IncomingMessage]] = Field(None, description="Incoming messages")
    statuses: Optional[List[MessageStatus]] = Field(None, description="Status updates")
    errors: Optional[List[Dict[str, Any]]] = Field(None, description="Errors")


class WebhookChange(BaseWhatsAppModel):
    """Webhook change event."""

    value: WebhookValue = Field(..., description="Change value")
    field: str = Field(..., description="Change field")


class WebhookEntry(BaseWhatsAppModel):
    """Webhook entry."""

    id: str = Field(..., description="Entry ID")
    changes: List[WebhookChange] = Field(..., description="Changes")


class WebhookPayload(BaseWhatsAppModel):
    """Main webhook payload model."""

    object: str = Field(..., description="Object type (always 'whatsapp_business_account')")
    entry: List[WebhookEntry] = Field(..., description="Webhook entries")


class WebhookEvent(BaseWhatsAppModel):
    """Processed webhook event."""

    raw_payload: WebhookPayload = Field(..., description="Raw webhook payload")
    messages: List[IncomingMessage] = Field(default_factory=list, description="Incoming messages")
    statuses: List[MessageStatus] = Field(default_factory=list, description="Status updates")
    errors: List[Dict[str, Any]] = Field(default_factory=list, description="Errors")

    @classmethod
    def from_payload(cls, payload: WebhookPayload) -> "WebhookEvent":
        """Create WebhookEvent from raw payload."""
        messages = []
        statuses = []
        errors = []

        for entry in payload.entry:
            for change in entry.changes:
                if change.value.messages:
                    messages.extend(change.value.messages)
                if change.value.statuses:
                    statuses.extend(change.value.statuses)
                if change.value.errors:
                    errors.extend(change.value.errors)

        return cls(
            raw_payload=payload,
            messages=messages,
            statuses=statuses,
            errors=errors,
        )

    @property
    def has_messages(self) -> bool:
        """Check if event contains messages."""
        return len(self.messages) > 0

    @property
    def has_statuses(self) -> bool:
        """Check if event contains status updates."""
        return len(self.statuses) > 0

    @property
    def has_errors(self) -> bool:
        """Check if event contains errors."""
        return len(self.errors) > 0
