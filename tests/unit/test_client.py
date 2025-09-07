"""Basic tests for WhatsApp SDK client."""

from unittest.mock import patch

import pytest

from whatsapp_sdk import WhatsAppClient


class TestWhatsAppClient:
    """Test WhatsApp client initialization and configuration."""

    def test_client_initialization_with_params(self):
        """Test client can be initialized with direct parameters."""
        client = WhatsAppClient(phone_number_id="123456789", access_token="test_token")

        assert client.config.phone_number_id == "123456789"
        assert client.config.access_token == "test_token"
        assert client.messages is not None
        assert client.media is not None
        assert client.templates is not None
        assert client.webhooks is not None

    def test_client_initialization_with_config(self):
        """Test client can be initialized with all parameters."""
        client = WhatsAppClient(
            phone_number_id="987654321", access_token="another_token", api_version="v23.0"
        )

        assert client.config.phone_number_id == "987654321"
        assert client.config.access_token == "another_token"
        assert client.config.api_version == "v23.0"

    def test_client_initialization_with_optional_params(self):
        """Test client initialization with all optional parameters."""
        client = WhatsAppClient(
            phone_number_id="123456789",
            access_token="test_token",
            app_secret="secret",
            webhook_verify_token="verify_token",
            api_version="v23.0",
            timeout=60,
            max_retries=5,
            rate_limit=100,
        )

        assert client.config.app_secret == "secret"
        assert client.config.webhook_verify_token == "verify_token"
        assert client.config.timeout == 60
        assert client.config.max_retries == 5
        assert client.config.rate_limit == 100

    @patch.dict(
        "os.environ",
        {"WHATSAPP_PHONE_NUMBER_ID": "env_phone_id", "WHATSAPP_ACCESS_TOKEN": "env_token"},
    )
    def test_client_from_env(self):
        """Test client can be initialized from environment variables."""
        client = WhatsAppClient.from_env()

        assert client.config.phone_number_id == "env_phone_id"
        assert client.config.access_token == "env_token"

    def test_client_services_are_initialized(self):
        """Test all services are properly initialized."""
        client = WhatsAppClient(phone_number_id="123456789", access_token="test_token")

        # Check all services exist
        assert hasattr(client, "messages")
        assert hasattr(client, "media")
        assert hasattr(client, "templates")
        assert hasattr(client, "webhooks")

        # Check services are not None
        assert client.messages is not None
        assert client.media is not None
        assert client.templates is not None
        assert client.webhooks is not None

    def test_client_base_url_configuration(self):
        """Test base URL is properly configured."""
        client = WhatsAppClient(
            phone_number_id="123456789", access_token="test_token", api_version="v23.0"
        )

        expected_base_url = "https://graph.facebook.com"
        assert client.config.base_url == expected_base_url
        assert client.config.api_version == "v23.0"

    def test_client_raises_on_missing_required_params(self):
        """Test client raises error when required parameters are missing."""
        with pytest.raises(TypeError):
            WhatsAppClient()  # Missing required parameters

        with pytest.raises(TypeError):
            WhatsAppClient(phone_number_id="123456789")  # Missing access_token

        with pytest.raises(TypeError):
            WhatsAppClient(access_token="token")  # Missing phone_number_id
