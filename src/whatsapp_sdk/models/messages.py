"""
Message models for WhatsApp SDK.
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import Field, field_validator

from whatsapp_sdk.models.base import (
    Address,
    BaseWhatsAppModel,
    ButtonType,
    Email,
    MessageType,
    Name,
    Organization,
    PhoneNumber,
    RecipientType,
    Url,
)


class Message(BaseWhatsAppModel):
    """Base message model."""

    messaging_product: str = Field(default="whatsapp", description="Messaging product")
    recipient_type: RecipientType = Field(
        default=RecipientType.INDIVIDUAL, description="Recipient type"
    )
    to: str = Field(..., description="Recipient phone number")
    type: MessageType = Field(..., description="Message type")

    @field_validator("to")
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        """Validate phone number format."""
        digits = "".join(filter(str.isdigit, v))
        if len(digits) < 7 or len(digits) > 15:
            raise ValueError(f"Invalid phone number: {v}")
        return digits


class TextMessage(Message):
    """Text message model."""

    type: MessageType = Field(default=MessageType.TEXT, description="Message type")
    text: Dict[str, Union[str, bool]] = Field(..., description="Text content")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: Dict[str, Union[str, bool]]) -> Dict[str, Union[str, bool]]:
        """Validate text content."""
        if "body" not in v:
            raise ValueError("Text message must have a body")
        body = str(v["body"])
        if not body.strip():
            raise ValueError("Message body cannot be empty")
        if len(body) > 4096:
            raise ValueError("Message body cannot exceed 4096 characters")
        return v


class MediaMessage(Message):
    """Base media message model."""

    caption: Optional[str] = Field(None, description="Media caption", max_length=1024)


class ImageMessage(MediaMessage):
    """Image message model."""

    type: MessageType = Field(default=MessageType.IMAGE, description="Message type")
    image: Dict[str, str] = Field(..., description="Image content")

    @field_validator("image")
    @classmethod
    def validate_image(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Validate image content."""
        if "id" not in v and "link" not in v:
            raise ValueError("Image must have either 'id' or 'link'")
        return v


class AudioMessage(MediaMessage):
    """Audio message model."""

    type: MessageType = Field(default=MessageType.AUDIO, description="Message type")
    audio: Dict[str, str] = Field(..., description="Audio content")

    @field_validator("audio")
    @classmethod
    def validate_audio(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Validate audio content."""
        if "id" not in v and "link" not in v:
            raise ValueError("Audio must have either 'id' or 'link'")
        return v


class VideoMessage(MediaMessage):
    """Video message model."""

    type: MessageType = Field(default=MessageType.VIDEO, description="Message type")
    video: Dict[str, str] = Field(..., description="Video content")

    @field_validator("video")
    @classmethod
    def validate_video(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Validate video content."""
        if "id" not in v and "link" not in v:
            raise ValueError("Video must have either 'id' or 'link'")
        return v


class DocumentMessage(MediaMessage):
    """Document message model."""

    type: MessageType = Field(default=MessageType.DOCUMENT, description="Message type")
    document: Dict[str, str] = Field(..., description="Document content")

    @field_validator("document")
    @classmethod
    def validate_document(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Validate document content."""
        if "id" not in v and "link" not in v:
            raise ValueError("Document must have either 'id' or 'link'")
        return v


class LocationMessage(Message):
    """Location message model."""

    type: MessageType = Field(default=MessageType.LOCATION, description="Message type")
    location: Dict[str, Union[str, float]] = Field(..., description="Location content")

    @field_validator("location")
    @classmethod
    def validate_location(cls, v: Dict[str, Union[str, float]]) -> Dict[str, Union[str, float]]:
        """Validate location content."""
        required = ["latitude", "longitude"]
        for field in required:
            if field not in v:
                raise ValueError(f"Location must have '{field}'")

        # Validate latitude and longitude ranges
        lat = float(v["latitude"])
        lon = float(v["longitude"])
        if not -90 <= lat <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= lon <= 180:
            raise ValueError("Longitude must be between -180 and 180")

        return v


class Contact(BaseWhatsAppModel):
    """Contact model."""

    addresses: Optional[List[Address]] = Field(None, description="Addresses")
    birthday: Optional[str] = Field(None, description="Birthday")
    emails: Optional[List[Email]] = Field(None, description="Email addresses")
    name: Name = Field(..., description="Contact name")
    org: Optional[Organization] = Field(None, description="Organization")
    phones: Optional[List[PhoneNumber]] = Field(None, description="Phone numbers")
    urls: Optional[List[Url]] = Field(None, description="URLs")


class ContactMessage(Message):
    """Contact message model."""

    type: MessageType = Field(default=MessageType.CONTACTS, description="Message type")
    contacts: List[Contact] = Field(..., description="Contact list", min_length=1)


class Button(BaseWhatsAppModel):
    """Button model for interactive messages."""

    type: ButtonType = Field(..., description="Button type")
    reply: Optional[Dict[str, str]] = Field(None, description="Reply button data")
    url: Optional[str] = Field(None, description="URL for URL button")
    phone_number: Optional[str] = Field(None, description="Phone number for phone button")


class Section(BaseWhatsAppModel):
    """Section model for list messages."""

    title: Optional[str] = Field(None, description="Section title", max_length=24)
    rows: List[Dict[str, str]] = Field(..., description="Section rows", min_length=1)


class InteractiveMessage(Message):
    """Interactive message model."""

    type: MessageType = Field(default=MessageType.INTERACTIVE, description="Message type")
    interactive: Dict[str, Any] = Field(..., description="Interactive content")

    @field_validator("interactive")
    @classmethod
    def validate_interactive(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate interactive content."""
        if "type" not in v:
            raise ValueError("Interactive message must have a type")
        if "action" not in v:
            raise ValueError("Interactive message must have an action")
        return v


class TemplateMessage(Message):
    """Template message model."""

    type: MessageType = Field(default=MessageType.TEMPLATE, description="Message type")
    template: Dict[str, Any] = Field(..., description="Template content")

    @field_validator("template")
    @classmethod
    def validate_template(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate template content."""
        if "name" not in v:
            raise ValueError("Template must have a name")
        if "language" not in v:
            raise ValueError("Template must have a language")
        return v


class MessageResponse(BaseWhatsAppModel):
    """Message response model."""

    messaging_product: str = Field(..., description="Messaging product")
    contacts: Optional[List[Dict[str, str]]] = Field(None, description="Contact information")
    messages: List[Dict[str, str]] = Field(..., description="Message information")

    @property
    def message_id(self) -> Optional[str]:
        """Get the message ID from the response."""
        if self.messages and len(self.messages) > 0:
            return self.messages[0].get("id")
        return None

    @property
    def recipient(self) -> Optional[str]:
        """Get the recipient from the response."""
        if self.contacts and len(self.contacts) > 0:
            return self.contacts[0].get("wa_id")
        return None

    @property
    def status(self) -> str:
        """Get the status from the response."""
        if self.messages and len(self.messages) > 0:
            return self.messages[0].get("message_status", "sent")
        return "unknown"
