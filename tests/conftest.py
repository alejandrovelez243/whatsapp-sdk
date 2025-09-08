"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import os
import sys
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from whatsapp_sdk import WhatsAppClient
from whatsapp_sdk.config import WhatsAppConfig
from whatsapp_sdk.http_client import HTTPClient

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture()
def mock_env(monkeypatch) -> None:
    """Mock environment variables."""

    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "123456789")
    monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "test_token")
    monkeypatch.setenv("WHATSAPP_APP_SECRET", "test_secret")
    monkeypatch.setenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN", "verify_token")


@pytest.fixture()
def mock_http_response() -> Dict[str, Any]:
    """Create a mock HTTP response."""
    return {
        "messaging_product": "whatsapp",
        "contacts": [{"input": "+1234567890", "wa_id": "1234567890"}],
        "messages": [{"id": "wamid.123456"}],
    }


@pytest.fixture()
def mock_config() -> WhatsAppConfig:
    """Create a mock configuration."""

    return WhatsAppConfig(
        phone_number_id="123456789",
        access_token="test_token",
        app_secret="test_secret",
        webhook_verify_token="verify_token",
        base_url="https://graph.facebook.com",
        api_version="v23.0",
    )


@pytest.fixture()
def mock_http_client(mock_http_response) -> Mock:
    """Create a mock HTTP client."""

    mock = Mock(spec=HTTPClient)
    mock.post = Mock(return_value=mock_http_response)
    mock.get = Mock(return_value={"data": [], "paging": {}})
    mock.delete = Mock(return_value={"success": True})
    mock.base_url = "https://graph.facebook.com/v23.0"
    mock.upload_multipart = Mock(return_value={"id": "media_123"})
    mock.download_binary = Mock(return_value=b"fake_binary_data")
    return mock


@pytest.fixture()
def client(mock_config, mock_http_client) -> WhatsAppClient:
    """Create WhatsApp client with mocked dependencies."""

    with patch("whatsapp_sdk.client.HTTPClient", return_value=mock_http_client):
        return WhatsAppClient(
            phone_number_id="123456789",
            access_token="test_token",
        )


@pytest.fixture()
def sample_webhook_payload() -> Dict[str, Any]:
    """Sample webhook payload."""
    return {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "XXXX",
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "16505551234",
                                "phone_number_id": "123456789",
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Test User"},
                                    "wa_id": "16505551234",
                                }
                            ],
                            "messages": [
                                {
                                    "from": "16505551234",
                                    "id": "wamid.test123",
                                    "timestamp": "1669233778",
                                    "type": "text",
                                    "text": {"body": "Hello!"},
                                }
                            ],
                        },
                    }
                ],
            }
        ],
    }
