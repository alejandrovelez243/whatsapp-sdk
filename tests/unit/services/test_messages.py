"""Basic tests for Messages service."""

from unittest.mock import Mock

import pytest

from whatsapp_sdk.config import WhatsAppConfig as Config
from whatsapp_sdk.http_client import HTTPClient
from whatsapp_sdk.models.base import MessageResponse
from whatsapp_sdk.services.messages import MessagesService


class TestMessagesService:
    """Test Messages service functionality."""

    @pytest.fixture
    def mock_http_client(self):
        """Create a mock HTTP client."""
        mock = Mock(spec=HTTPClient)
        return mock

    @pytest.fixture
    def mock_config(self):
        """Create a mock config."""
        return Config(phone_number_id="123456789", access_token="test_token")

    @pytest.fixture
    def messages_service(self, mock_http_client, mock_config):
        """Create a Messages service instance with mocks."""
        return MessagesService(
            http_client=mock_http_client, config=mock_config, phone_number_id="123456789"
        )

    def test_send_text_message(self, messages_service, mock_http_client):
        """Test sending a text message."""
        # Setup mock response
        mock_response = {
            "messaging_product": "whatsapp",
            "contacts": [{"input": "+1234567890", "wa_id": "1234567890"}],
            "messages": [{"id": "wamid.123456"}],
        }
        mock_http_client.post.return_value = mock_response

        # Send message
        response = messages_service.send_text(to="+1234567890", body="Hello, World!")

        # Verify HTTP client was called correctly
        mock_http_client.post.assert_called_once()
        call_args = mock_http_client.post.call_args

        # Check endpoint
        assert "123456789/messages" in call_args[0][0]

        # Check payload
        payload = call_args[1]["json"]
        assert payload["messaging_product"] == "whatsapp"
        assert payload["recipient_type"] == "individual"
        assert payload["to"] == "1234567890"  # Phone number is normalized (digits only)
        assert payload["type"] == "text"
        assert payload["text"]["body"] == "Hello, World!"

        # Check response
        assert isinstance(response, MessageResponse)
        assert response.messages[0].id == "wamid.123456"

    def test_send_text_with_preview_url(self, messages_service, mock_http_client):
        """Test sending text message with URL preview."""
        mock_response = {
            "messaging_product": "whatsapp",
            "contacts": [{"input": "+1234567890", "wa_id": "1234567890"}],
            "messages": [{"id": "wamid.789"}],
        }
        mock_http_client.post.return_value = mock_response

        response = messages_service.send_text(
            to="+1234567890", body="Check this out: https://example.com", preview_url=True
        )

        call_args = mock_http_client.post.call_args
        payload = call_args[1]["json"]

        assert payload["text"]["preview_url"] is True
        assert response.messages[0].id == "wamid.789"

    def test_send_image_message(self, messages_service, mock_http_client):
        """Test sending an image message."""
        mock_response = {
            "messaging_product": "whatsapp",
            "contacts": [{"input": "+1234567890", "wa_id": "1234567890"}],
            "messages": [{"id": "wamid.image123"}],
        }
        mock_http_client.post.return_value = mock_response

        response = messages_service.send_image(
            to="+1234567890", image="https://example.com/image.jpg", caption="Look at this!"
        )

        call_args = mock_http_client.post.call_args
        payload = call_args[1]["json"]

        assert payload["type"] == "image"
        assert payload["image"]["link"] == "https://example.com/image.jpg"
        assert payload["image"]["caption"] == "Look at this!"
        assert response.messages[0].id == "wamid.image123"

    def test_send_location_message(self, messages_service, mock_http_client):
        """Test sending a location message."""
        mock_response = {
            "messaging_product": "whatsapp",
            "contacts": [{"input": "+1234567890", "wa_id": "1234567890"}],
            "messages": [{"id": "wamid.loc456"}],
        }
        mock_http_client.post.return_value = mock_response

        response = messages_service.send_location(
            to="+1234567890",
            latitude=37.7749,
            longitude=-122.4194,
            name="San Francisco",
            address="California, USA",
        )

        call_args = mock_http_client.post.call_args
        payload = call_args[1]["json"]

        assert payload["type"] == "location"
        assert payload["location"]["latitude"] == 37.7749
        assert payload["location"]["longitude"] == -122.4194
        assert payload["location"]["name"] == "San Francisco"
        assert payload["location"]["address"] == "California, USA"
        assert response.messages[0].id == "wamid.loc456"

    def test_mark_as_read(self, messages_service, mock_http_client):
        """Test marking a message as read."""
        mock_response = {
            "messaging_product": "whatsapp",
            "contacts": [],
            "messages": [{"id": "wamid.read123"}],
        }
        mock_http_client.post.return_value = mock_response

        response = messages_service.mark_as_read("wamid.123456")

        call_args = mock_http_client.post.call_args
        payload = call_args[1]["json"]

        assert payload["messaging_product"] == "whatsapp"
        assert payload["status"] == "read"
        assert payload["message_id"] == "wamid.123456"
        assert isinstance(response, MessageResponse)
        assert response.messages[0].id == "wamid.read123"
