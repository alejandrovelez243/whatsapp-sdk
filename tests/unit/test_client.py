"""Tests for WhatsApp Client."""


from __future__ import annotations

import pytest

from whatsapp_sdk import WhatsAppClient, WhatsAppConfig


class TestWhatsAppClient:
    """Test WhatsApp client initialization and configuration."""

    def test_client_initialization(self):
        """Test client initialization with required parameters."""
        client = WhatsAppClient(
            phone_number_id="123456789",
            access_token="test_token",
        )

        assert client.phone_number_id == "123456789"
        assert client.config.access_token == "test_token"
        assert client.config.base_url == "https://graph.facebook.com"
        assert client.config.api_version == "v23.0"

    def test_client_with_all_parameters(self):
        """Test client initialization with all parameters."""
        app_secret = "secret"  # nosec B105  # Test secret for unit tests
        verify_token = "verify"  # nosec B105  # Test token for unit tests
        client = WhatsAppClient(
            phone_number_id="123456789",
            access_token="test_token",
            app_secret=app_secret,
            webhook_verify_token=verify_token,
            base_url="https://custom.api.com",
            api_version="v20.0",
            timeout=60,
            max_retries=5,
            rate_limit=100,
        )

        assert client.phone_number_id == "123456789"
        assert client.config.access_token == "test_token"
        assert client.config.app_secret == app_secret
        assert client.config.webhook_verify_token == verify_token
        assert client.config.base_url == "https://custom.api.com"
        assert client.config.api_version == "v20.0"
        assert client.config.timeout == 60
        assert client.config.max_retries == 5
        assert client.config.rate_limit == 100

    def test_client_services_initialization(self):
        """Test that all services are properly initialized."""
        client = WhatsAppClient(
            phone_number_id="123456789",
            access_token="test_token",
        )

        assert hasattr(client, "messages")
        assert hasattr(client, "templates")
        assert hasattr(client, "media")
        assert hasattr(client, "webhooks")

    def test_from_env_success(self, mock_env):
        """Test creating client from environment variables."""
        client = WhatsAppClient.from_env()

        assert client.phone_number_id == "123456789"
        assert client.config.access_token == "test_token"
        assert client.config.app_secret == "test_secret"
        assert client.config.webhook_verify_token == "verify_token"

    def test_from_env_missing_required(self):
        """Test from_env raises error when required env vars are missing."""
        with pytest.raises(ValueError) as exc_info:
            WhatsAppClient.from_env()

        assert "WHATSAPP_PHONE_NUMBER_ID" in str(exc_info.value)

    def test_from_env_partial_missing(self, monkeypatch):
        """Test from_env with only phone number ID missing."""
        monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "test_token")

        with pytest.raises(ValueError) as exc_info:
            WhatsAppClient.from_env()

        assert "WHATSAPP_PHONE_NUMBER_ID" in str(exc_info.value)

    def test_from_env_with_custom_values(self, monkeypatch):
        """Test from_env with custom timeout and retries."""
        monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "123456789")
        monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "test_token")
        monkeypatch.setenv("WHATSAPP_TIMEOUT", "45")
        monkeypatch.setenv("WHATSAPP_MAX_RETRIES", "10")
        monkeypatch.setenv("WHATSAPP_RATE_LIMIT", "200")

        client = WhatsAppClient.from_env()

        assert client.config.timeout == 45
        assert client.config.max_retries == 10
        assert client.config.rate_limit == 200


class TestWhatsAppConfig:
    """Test WhatsApp configuration."""

    def test_config_initialization(self):
        """Test configuration with required parameters."""
        config = WhatsAppConfig(
            phone_number_id="123456789",
            access_token="test_token",
        )

        assert config.phone_number_id == "123456789"
        assert config.access_token == "test_token"
        assert config.base_url == "https://graph.facebook.com"
        assert config.api_version == "v23.0"
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.rate_limit == 80

    def test_config_with_all_parameters(self):
        """Test configuration with all parameters."""
        config = WhatsAppConfig(
            phone_number_id="123456789",
            access_token="test_token",
            app_secret="secret",
            webhook_verify_token="verify",
            base_url="https://custom.api.com",
            api_version="v20.0",
            timeout=60,
            max_retries=5,
            rate_limit=100,
        )

        assert config.phone_number_id == "123456789"
        assert config.access_token == "test_token"
        assert config.app_secret == "secret"
        assert config.webhook_verify_token == "verify"
        assert config.base_url == "https://custom.api.com"
        assert config.api_version == "v20.0"
        assert config.timeout == 60
        assert config.max_retries == 5
        assert config.rate_limit == 100
