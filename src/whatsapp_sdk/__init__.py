"""
WhatsApp Business SDK for Python

A comprehensive Python SDK for WhatsApp Business API with FastAPI integration.
"""

from whatsapp_sdk.client import WhatsAppClient
from whatsapp_sdk.config import Config
from whatsapp_sdk.exceptions import (
    APIError,
    AuthenticationError,
    MediaError,
    RateLimitError,
    TemplateError,
    ValidationError,
    WhatsAppError,
)

__version__ = "0.1.0"
__author__ = "Alejandro Velez"
__email__ = "alejandro-243@hotmail.com"

__all__ = [
    "APIError",
    "AuthenticationError",
    "Config",
    "MediaError",
    "RateLimitError",
    "TemplateError",
    "ValidationError",
    "WhatsAppClient",
    "WhatsAppError",
]
