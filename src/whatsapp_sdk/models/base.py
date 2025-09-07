"""
Base models and enums for WhatsApp SDK.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MessageType(str, Enum):
    """Message types supported by WhatsApp."""

    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    TEMPLATE = "template"
    INTERACTIVE = "interactive"
    LOCATION = "location"
    CONTACTS = "contacts"
    STICKER = "sticker"
    REACTION = "reaction"


class RecipientType(str, Enum):
    """Recipient types."""

    INDIVIDUAL = "individual"
    GROUP = "group"


class ComponentType(str, Enum):
    """Template component types."""

    HEADER = "header"
    BODY = "body"
    FOOTER = "footer"
    BUTTONS = "buttons"


class ParameterType(str, Enum):
    """Template parameter types."""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"
    CURRENCY = "currency"
    DATE_TIME = "date_time"


class ButtonType(str, Enum):
    """Button types for interactive messages."""

    REPLY = "reply"
    URL = "url"
    PHONE_NUMBER = "phone_number"
    QUICK_REPLY = "quick_reply"


class InteractiveType(str, Enum):
    """Interactive message types."""

    BUTTON = "button"
    LIST = "list"
    PRODUCT = "product"
    PRODUCT_LIST = "product_list"


class MediaType(str, Enum):
    """Media types."""

    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    STICKER = "sticker"


class StatusType(str, Enum):
    """Message status types."""

    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class WebhookField(str, Enum):
    """Webhook field types."""

    MESSAGES = "messages"
    MESSAGING_PRODUCT = "messaging_product"
    METADATA = "metadata"
    CONTACTS = "contacts"
    STATUSES = "statuses"
    ERRORS = "errors"


class BaseWhatsAppModel(BaseModel):
    """Base model for all WhatsApp models."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        populate_by_name=True,
        use_enum_values=True,
        json_encoders={
            Enum: lambda v: v.value,
        },
    )


class PhoneNumber(BaseWhatsAppModel):
    """Phone number model."""

    phone: str = Field(..., description="Phone number")
    type: Optional[str] = Field(None, description="Phone number type")
    wa_id: Optional[str] = Field(None, description="WhatsApp ID")


class Name(BaseWhatsAppModel):
    """Name model for contacts."""

    formatted_name: str = Field(..., description="Full name")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    middle_name: Optional[str] = Field(None, description="Middle name")
    suffix: Optional[str] = Field(None, description="Name suffix")
    prefix: Optional[str] = Field(None, description="Name prefix")


class Address(BaseWhatsAppModel):
    """Address model for contacts."""

    street: Optional[str] = Field(None, description="Street address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    zip: Optional[str] = Field(None, description="ZIP code")
    country: Optional[str] = Field(None, description="Country")
    country_code: Optional[str] = Field(None, description="Country code")
    type: Optional[str] = Field(None, description="Address type")


class Email(BaseWhatsAppModel):
    """Email model for contacts."""

    email: str = Field(..., description="Email address")
    type: Optional[str] = Field(None, description="Email type")


class Url(BaseWhatsAppModel):
    """URL model for contacts."""

    url: str = Field(..., description="URL")
    type: Optional[str] = Field(None, description="URL type")


class Organization(BaseWhatsAppModel):
    """Organization model for contacts."""

    company: Optional[str] = Field(None, description="Company name")
    department: Optional[str] = Field(None, description="Department")
    title: Optional[str] = Field(None, description="Job title")
