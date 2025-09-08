"""Tests for Messages Service."""


from __future__ import annotations

import pytest

from whatsapp_sdk.models import (
    ImageMessage,
    TextMessage,
)
from whatsapp_sdk.services.messages import MessagesService


class TestMessagesService:
    """Test messages service functionality."""

    @pytest.fixture()
    def messages_service(self, mock_http_client, mock_config):
        """Create messages service with mocked dependencies."""
        return MessagesService(
            http_client=mock_http_client,
            config=mock_config,
            phone_number_id="123456789",
        )

    def test_send_text_simple(self, messages_service, mock_http_client):
        """Test sending simple text message."""
        _ = messages_service.send_text("+1234567890", "Hello, World!")

        # Verify HTTP client was called correctly
        mock_http_client.post.assert_called_once()
        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["messaging_product"] == "whatsapp"
        assert payload["to"] == "1234567890"
        assert payload["type"] == "text"
        assert payload["text"]["body"] == "Hello, World!"
        assert payload["text"]["preview_url"] is False

    def test_send_text_with_preview(self, messages_service, mock_http_client):
        """Test sending text message with URL preview."""
        _ = messages_service.send_text(
            "+1234567890",
            "Check out https://example.com",
            preview_url=True,
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["text"]["body"] == "Check out https://example.com"
        assert payload["text"]["preview_url"] is True

    def test_send_text_with_model(self, messages_service, mock_http_client):
        """Test sending text message using TextMessage model."""
        msg = TextMessage(body="Hello from model!", preview_url=True)
        _ = messages_service.send_text("+1234567890", text=msg)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["text"]["body"] == "Hello from model!"
        assert payload["text"]["preview_url"] is True

    def test_send_text_with_dict(self, messages_service, mock_http_client):
        """Test sending text message using dict."""
        text_dict = {"body": "Hello from dict!", "preview_url": False}
        _ = messages_service.send_text("+1234567890", text=text_dict)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["text"]["body"] == "Hello from dict!"
        assert payload["text"]["preview_url"] is False

    def test_send_text_no_content_error(self, messages_service):
        """Test sending text without content raises error."""
        with pytest.raises(ValueError) as exc_info:
            messages_service.send_text("+1234567890")

        assert "Must provide either 'body' or 'text'" in str(exc_info.value)

    def test_send_image_with_url(self, messages_service, mock_http_client):
        """Test sending image with URL."""
        _ = messages_service.send_image(
            "+1234567890",
            "https://example.com/image.jpg",
            caption="Test image",
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "image"
        assert payload["image"]["link"] == "https://example.com/image.jpg"
        assert payload["image"]["caption"] == "Test image"

    def test_send_image_with_media_id(self, messages_service, mock_http_client):
        """Test sending image with media ID."""
        _ = messages_service.send_image(
            "+1234567890",
            "media_id_123",
            caption="Test image",
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "image"
        assert payload["image"]["id"] == "media_id_123"
        assert payload["image"]["caption"] == "Test image"

    def test_send_image_with_model(self, messages_service, mock_http_client):
        """Test sending image using ImageMessage model."""
        img = ImageMessage(link="https://example.com/pic.jpg", caption="Nice!")
        _ = messages_service.send_image("+1234567890", img)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["image"]["link"] == "https://example.com/pic.jpg"
        assert payload["image"]["caption"] == "Nice!"

    def test_send_location(self, messages_service, mock_http_client):
        """Test sending location message."""
        _ = messages_service.send_location(
            "+1234567890",
            37.4847,
            -122.1477,
            name="Meta Headquarters",
            address="1 Hacker Way, Menlo Park, CA",
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "location"
        assert payload["location"]["latitude"] == 37.4847
        assert payload["location"]["longitude"] == -122.1477
        assert payload["location"]["name"] == "Meta Headquarters"
        assert payload["location"]["address"] == "1 Hacker Way, Menlo Park, CA"

    def test_mark_as_read(self, messages_service, mock_http_client):
        """Test marking message as read."""
        _ = messages_service.mark_as_read("wamid.123456")

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["messaging_product"] == "whatsapp"
        assert payload["status"] == "read"
        assert payload["message_id"] == "wamid.123456"

    def test_format_phone_number(self, messages_service):
        """Test phone number formatting."""
        # Test various formats
        assert messages_service._format_phone_number("+1234567890") == "1234567890"
        assert messages_service._format_phone_number("1234567890") == "1234567890"
        assert messages_service._format_phone_number("+1-234-567-890") == "1234567890"
        assert messages_service._format_phone_number("(123) 456-7890") == "1234567890"

    def test_format_phone_number_invalid_length(self, messages_service):
        """Test phone number validation for length."""
        # Too short
        with pytest.raises(ValueError) as exc_info:
            messages_service._format_phone_number("12345")
        assert "Invalid phone number length" in str(exc_info.value)

        # Too long
        with pytest.raises(ValueError) as exc_info:
            messages_service._format_phone_number("1234567890123456")
        assert "Invalid phone number length" in str(exc_info.value)

    def test_send_document(self, messages_service, mock_http_client):
        """Test sending document message."""
        _ = messages_service.send_document(
            "+1234567890",
            "https://example.com/document.pdf",
            caption="Important document",
            filename="document.pdf",
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "document"
        assert payload["document"]["link"] == "https://example.com/document.pdf"
        assert payload["document"]["caption"] == "Important document"
        assert payload["document"]["filename"] == "document.pdf"

    def test_send_audio(self, messages_service, mock_http_client):
        """Test sending audio message."""
        _ = messages_service.send_audio(
            "+1234567890",
            "https://example.com/audio.mp3",
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "audio"
        assert payload["audio"]["link"] == "https://example.com/audio.mp3"

    def test_send_video(self, messages_service, mock_http_client):
        """Test sending video message."""
        _ = messages_service.send_video(
            "+1234567890",
            "https://example.com/video.mp4",
            caption="Check this out!",
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "video"
        assert payload["video"]["link"] == "https://example.com/video.mp4"
        assert payload["video"]["caption"] == "Check this out!"

    def test_send_sticker(self, messages_service, mock_http_client):
        """Test sending sticker message."""
        _ = messages_service.send_sticker(
            "+1234567890",
            "https://example.com/sticker.webp",
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "sticker"
        assert payload["sticker"]["link"] == "https://example.com/sticker.webp"
