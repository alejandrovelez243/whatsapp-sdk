"""Pytest configuration and shared fixtures."""

import os
import sys
from unittest.mock import Mock

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture
def mock_http_response():
    """Create a mock HTTP response."""
    return {
        "messaging_product": "whatsapp",
        "contacts": [{"input": "+1234567890", "wa_id": "1234567890"}],
        "messages": [{"id": "wamid.123456"}],
    }


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    from whatsapp_sdk.config import WhatsAppConfig

    return WhatsAppConfig(
        phone_number_id="123456789", access_token="test_token", api_version="v23.0"
    )


@pytest.fixture
def mock_http_client():
    """Create a mock HTTP client."""
    from whatsapp_sdk.http_client import HTTPClient

    mock = Mock(spec=HTTPClient)
    mock.post = Mock()
    mock.get = Mock()
    mock.delete = Mock()
    return mock
