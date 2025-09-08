"""Tests for Messages Service."""


from __future__ import annotations

import pytest

from whatsapp_sdk.models import (
    AudioMessage,
    Contact,
    ContactMessage,
    DocumentMessage,
    ImageMessage,
    InteractiveMessage,
    MessageResponse,
    Name,
    Phone,
    StickerMessage,
    TextMessage,
    VideoMessage,
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

    def test_send_sticker_with_media_id(self, messages_service, mock_http_client):
        """Test sending sticker with media ID."""
        _ = messages_service.send_sticker("+1234567890", "sticker_id_123")

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "sticker"
        assert payload["sticker"]["id"] == "sticker_id_123"

    def test_send_sticker_with_model(self, messages_service, mock_http_client):
        """Test sending sticker using StickerMessage model."""
        sticker = StickerMessage(link="https://example.com/animated.webp")
        _ = messages_service.send_sticker("+1234567890", sticker)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["sticker"]["link"] == "https://example.com/animated.webp"

    def test_send_sticker_invalid_parameter(self, messages_service):
        """Test sending sticker with invalid parameter type."""
        with pytest.raises(ValueError) as exc_info:
            messages_service.send_sticker("+1234567890", 123)
        assert "Invalid sticker parameter type" in str(exc_info.value)

    # ========================================================================
    # DOCUMENT MESSAGE TESTS
    # ========================================================================

    def test_send_document_with_media_id(self, messages_service, mock_http_client):
        """Test sending document with media ID."""
        _ = messages_service.send_document(
            "+1234567890",
            "doc_id_123",
            caption="Important file"
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "document"
        assert payload["document"]["id"] == "doc_id_123"
        assert payload["document"]["caption"] == "Important file"

    def test_send_document_with_model(self, messages_service, mock_http_client):
        """Test sending document using DocumentMessage model."""
        doc = DocumentMessage(
            link="https://example.com/report.pdf",
            filename="report.pdf",
            caption="Monthly report"
        )
        _ = messages_service.send_document("+1234567890", doc)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["document"]["link"] == "https://example.com/report.pdf"
        assert payload["document"]["filename"] == "report.pdf"
        assert payload["document"]["caption"] == "Monthly report"

    def test_send_document_with_dict(self, messages_service, mock_http_client):
        """Test sending document using dict parameter."""
        doc_dict = {
            "id": "doc_456",
            "caption": "Shared document"
        }
        _ = messages_service.send_document("+1234567890", doc_dict)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["document"]["id"] == "doc_456"
        assert payload["document"]["caption"] == "Shared document"

    def test_send_document_invalid_parameter(self, messages_service):
        """Test sending document with invalid parameter type."""
        with pytest.raises(ValueError) as exc_info:
            messages_service.send_document("+1234567890", [])
        assert "Invalid document parameter type" in str(exc_info.value)

    # ========================================================================
    # AUDIO MESSAGE TESTS
    # ========================================================================

    def test_send_audio_with_media_id(self, messages_service, mock_http_client):
        """Test sending audio with media ID."""
        _ = messages_service.send_audio("+1234567890", "audio_id_123")

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "audio"
        assert payload["audio"]["id"] == "audio_id_123"

    def test_send_audio_with_model(self, messages_service, mock_http_client):
        """Test sending audio using AudioMessage model."""
        audio = AudioMessage(link="https://example.com/voice.mp3")
        _ = messages_service.send_audio("+1234567890", audio)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["audio"]["link"] == "https://example.com/voice.mp3"

    def test_send_audio_with_dict(self, messages_service, mock_http_client):
        """Test sending audio using dict parameter."""
        audio_dict = {"id": "audio_789"}
        _ = messages_service.send_audio("+1234567890", audio_dict)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["audio"]["id"] == "audio_789"

    def test_send_audio_invalid_parameter(self, messages_service):
        """Test sending audio with invalid parameter type."""
        with pytest.raises(ValueError) as exc_info:
            messages_service.send_audio("+1234567890", None)
        assert "Invalid audio parameter type" in str(exc_info.value)

    # ========================================================================
    # VIDEO MESSAGE TESTS
    # ========================================================================

    def test_send_video_with_media_id(self, messages_service, mock_http_client):
        """Test sending video with media ID."""
        _ = messages_service.send_video(
            "+1234567890",
            "video_id_123",
            caption="Great video!"
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "video"
        assert payload["video"]["id"] == "video_id_123"
        assert payload["video"]["caption"] == "Great video!"

    def test_send_video_with_model(self, messages_service, mock_http_client):
        """Test sending video using VideoMessage model."""
        video = VideoMessage(
            link="https://example.com/demo.mp4",
            caption="Product demo"
        )
        _ = messages_service.send_video("+1234567890", video)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["video"]["link"] == "https://example.com/demo.mp4"
        assert payload["video"]["caption"] == "Product demo"

    def test_send_video_with_dict(self, messages_service, mock_http_client):
        """Test sending video using dict parameter."""
        video_dict = {
            "link": "https://example.com/tutorial.mp4",
            "caption": "Tutorial video"
        }
        _ = messages_service.send_video("+1234567890", video_dict)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["video"]["link"] == "https://example.com/tutorial.mp4"
        assert payload["video"]["caption"] == "Tutorial video"

    def test_send_video_no_caption(self, messages_service, mock_http_client):
        """Test sending video without caption."""
        _ = messages_service.send_video(
            "+1234567890",
            "https://example.com/clip.mp4"
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["video"]["link"] == "https://example.com/clip.mp4"
        assert "caption" not in payload["video"]

    def test_send_video_invalid_parameter(self, messages_service):
        """Test sending video with invalid parameter type."""
        with pytest.raises(ValueError) as exc_info:
            messages_service.send_video("+1234567890", 123.45)
        assert "Invalid video parameter type" in str(exc_info.value)

    # ========================================================================
    # LOCATION MESSAGE TESTS - Enhanced
    # ========================================================================

    def test_send_location_without_name(self, messages_service, mock_http_client):
        """Test sending location without name and address."""
        _ = messages_service.send_location(
            "+1234567890",
            40.7128,
            -74.0060
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "location"
        assert payload["location"]["latitude"] == 40.7128
        assert payload["location"]["longitude"] == -74.0060
        assert "name" not in payload["location"]
        assert "address" not in payload["location"]

    def test_send_location_with_name_only(self, messages_service, mock_http_client):
        """Test sending location with name but no address."""
        _ = messages_service.send_location(
            "+1234567890",
            40.7589,
            -73.9851,
            name="Times Square"
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["location"]["name"] == "Times Square"
        assert "address" not in payload["location"]

    def test_send_location_negative_coordinates(self, messages_service, mock_http_client):
        """Test sending location with negative coordinates."""
        _ = messages_service.send_location(
            "+1234567890",
            -33.8688,
            151.2093,
            name="Sydney Opera House"
        )

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["location"]["latitude"] == -33.8688
        assert payload["location"]["longitude"] == 151.2093

    # ========================================================================
    # CONTACT MESSAGE TESTS
    # ========================================================================

    def test_send_contact_single(self, messages_service, mock_http_client):
        """Test sending single contact."""
        contact = Contact(
            name=Name(
                formatted_name="John Doe",
                first_name="John",
                last_name="Doe"
            ),
            phones=[Phone(phone="+1234567890", type="MOBILE")]
        )
        _ = messages_service.send_contact("+1234567890", [contact])

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "contacts"
        assert len(payload["contacts"]) == 1
        assert payload["contacts"][0]["name"]["formatted_name"] == "John Doe"
        assert payload["contacts"][0]["phones"][0]["phone"] == "+1234567890"

    def test_send_contact_multiple(self, messages_service, mock_http_client):
        """Test sending multiple contacts."""
        contact1 = Contact(
            name=Name(formatted_name="Alice Smith", first_name="Alice"),
            phones=[Phone(phone="+1111111111", type="HOME")]
        )
        contact2 = Contact(
            name=Name(formatted_name="Bob Jones", first_name="Bob"),
            phones=[Phone(phone="+2222222222", type="WORK")]
        )
        _ = messages_service.send_contact("+1234567890", [contact1, contact2])

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert len(payload["contacts"]) == 2
        assert payload["contacts"][0]["name"]["formatted_name"] == "Alice Smith"
        assert payload["contacts"][1]["name"]["formatted_name"] == "Bob Jones"

    def test_send_contact_with_contact_message(self, messages_service, mock_http_client):
        """Test sending contact using ContactMessage model."""
        contact = Contact(
            name=Name(formatted_name="Test Contact"),
            phones=[Phone(phone="+9876543210")]
        )
        contact_message = ContactMessage(contacts=[contact])
        _ = messages_service.send_contact("+1234567890", contact_message)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        # The service now properly serializes ContactMessage to dict format
        assert len(payload["contacts"]) == 1
        assert payload["contacts"][0]["name"]["formatted_name"] == "Test Contact"
        assert payload["contacts"][0]["phones"][0]["phone"] == "+9876543210"

    def test_send_contact_with_dict(self, messages_service, mock_http_client):
        """Test sending contact using dict parameter."""
        contact_dict = {
            "contacts": [
                {
                    "name": {"formatted_name": "Dict Contact"},
                    "phones": [{"phone": "+5555555555"}]
                }
            ]
        }
        _ = messages_service.send_contact("+1234567890", contact_dict)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["contacts"][0]["name"]["formatted_name"] == "Dict Contact"

    def test_send_contact_invalid_parameter(self, messages_service):
        """Test sending contact with invalid parameter type."""
        with pytest.raises(ValueError) as exc_info:
            messages_service.send_contact("+1234567890", "invalid")
        assert "Invalid contacts parameter type" in str(exc_info.value)

    # ========================================================================
    # INTERACTIVE MESSAGE TESTS
    # ========================================================================

    def test_send_interactive_button_message(self, messages_service, mock_http_client):
        """Test sending interactive button message."""
        interactive_dict = {
            "type": "button",
            "body": {"text": "Choose an option:"},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "1", "title": "Yes"}},
                    {"type": "reply", "reply": {"id": "2", "title": "No"}}
                ]
            }
        }
        _ = messages_service.send_interactive("+1234567890", interactive_dict)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["type"] == "interactive"
        assert payload["interactive"]["type"] == "button"
        assert payload["interactive"]["body"]["text"] == "Choose an option:"
        assert len(payload["interactive"]["action"]["buttons"]) == 2

    def test_send_interactive_list_message(self, messages_service, mock_http_client):
        """Test sending interactive list message."""
        interactive_dict = {
            "type": "list",
            "body": {"text": "Select from menu:"},
            "action": {
                "button": "Menu",
                "sections": [
                    {
                        "title": "Main Courses",
                        "rows": [
                            {"id": "pizza", "title": "Pizza", "description": "Delicious pizza"}
                        ]
                    }
                ]
            }
        }
        _ = messages_service.send_interactive("+1234567890", interactive_dict)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["interactive"]["type"] == "list"
        assert payload["interactive"]["action"]["button"] == "Menu"
        assert len(payload["interactive"]["action"]["sections"]) == 1

    def test_send_interactive_with_model(self, messages_service, mock_http_client):
        """Test sending interactive message using InteractiveMessage model."""
        interactive_model = InteractiveMessage.model_validate({
            "type": "button",
            "body": {"text": "Model-based interactive"},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "confirm", "title": "Confirm"}}
                ]
            }
        })
        _ = messages_service.send_interactive("+1234567890", interactive_model)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["interactive"]["body"]["text"] == "Model-based interactive"

    def test_send_interactive_invalid_parameter(self, messages_service):
        """Test sending interactive message with invalid parameter type."""
        with pytest.raises(ValueError) as exc_info:
            messages_service.send_interactive("+1234567890", "invalid")
        assert "Invalid interactive parameter type" in str(exc_info.value)

    # ========================================================================
    # MESSAGE MANAGEMENT TESTS
    # ========================================================================

    def test_mark_as_read_basic(self, messages_service, mock_http_client):
        """Test marking message as read without typing indicator."""
        _ = messages_service.mark_as_read("wamid.test123")

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["messaging_product"] == "whatsapp"
        assert payload["status"] == "read"
        assert payload["message_id"] == "wamid.test123"
        assert "typing_indicator" not in payload

    def test_mark_as_read_with_typing_indicator(self, messages_service, mock_http_client):
        """Test marking message as read with typing indicator."""
        _ = messages_service.mark_as_read("wamid.test456", typing_indicator=True)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["message_id"] == "wamid.test456"
        assert payload["typing_indicator"] == {"type": "text"}

    def test_send_typing_indicator(self, messages_service, mock_http_client):
        """Test sending typing indicator (convenience method)."""
        _ = messages_service.send_typing_indicator("wamid.typing789")

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["message_id"] == "wamid.typing789"
        assert payload["typing_indicator"] == {"type": "text"}
        assert payload["status"] == "read"

    # ========================================================================
    # PHONE NUMBER FORMATTING TESTS - Enhanced
    # ========================================================================

    def test_format_phone_number_various_formats(self, messages_service):
        """Test phone number formatting with various input formats."""
        # Test various international formats
        assert messages_service._format_phone_number("+1-555-123-4567") == "15551234567"
        assert messages_service._format_phone_number("(555) 123-4567") == "5551234567"
        assert messages_service._format_phone_number("+44 20 7946 0958") == "442079460958"
        assert messages_service._format_phone_number("+33 1 42 34 56 78") == "33142345678"

        # Test with spaces and special characters
        assert messages_service._format_phone_number("+1 234 567 890") == "1234567890"
        assert messages_service._format_phone_number("234.567.890") == "234567890"
        assert messages_service._format_phone_number("234-567-890") == "234567890"

    def test_format_phone_number_edge_cases(self, messages_service):
        """Test phone number formatting edge cases."""
        # Test minimum length (7 digits)
        assert messages_service._format_phone_number("1234567") == "1234567"

        # Test maximum length (15 digits)
        assert messages_service._format_phone_number("+123456789012345") == "123456789012345"

        # Test with leading zeros after country code removal
        assert messages_service._format_phone_number("+1001234567") == "1001234567"

    def test_format_phone_number_too_short(self, messages_service):
        """Test phone number validation - too short."""
        with pytest.raises(ValueError) as exc_info:
            messages_service._format_phone_number("123456")
        assert "Invalid phone number length: 123456" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            messages_service._format_phone_number("+1-23")  # Only 3 digits
        assert "Invalid phone number length: 123" in str(exc_info.value)

    def test_format_phone_number_too_long(self, messages_service):
        """Test phone number validation - too long."""
        long_number = "1234567890123456"  # 16 digits
        with pytest.raises(ValueError) as exc_info:
            messages_service._format_phone_number(long_number)
        assert f"Invalid phone number length: {long_number}" in str(exc_info.value)

    def test_format_phone_number_empty(self, messages_service):
        """Test phone number validation - empty string."""
        with pytest.raises(ValueError) as exc_info:
            messages_service._format_phone_number("")
        assert "Invalid phone number length:" in str(exc_info.value)

    def test_format_phone_number_only_special_chars(self, messages_service):
        """Test phone number with only special characters."""
        with pytest.raises(ValueError) as exc_info:
            messages_service._format_phone_number("+()-. ")
        assert "Invalid phone number length:" in str(exc_info.value)

    # ========================================================================
    # ERROR HANDLING TESTS
    # ========================================================================

    def test_http_client_error_handling(self, messages_service, mock_http_client):
        """Test HTTP client error handling."""
        # Setup mock to raise exception
        from requests.exceptions import HTTPError
        mock_http_client.post.side_effect = HTTPError("API Error")

        with pytest.raises(HTTPError):
            messages_service.send_text("+1234567890", "Test")

    def test_invalid_media_id_detection(self, messages_service, mock_http_client):
        """Test media ID vs URL detection edge cases."""
        # Test edge case: media ID that starts with "http" but isn't a URL
        _ = messages_service.send_image("+1234567890", "httpnot_a_url")
        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]
        # Since it starts with "http", it's treated as a URL (link)
        assert "link" in payload["image"]
        assert payload["image"]["link"] == "httpnot_a_url"

        # Test actual media ID case
        _ = messages_service.send_image("+1234567890", "media_id_123")
        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]
        # Should be treated as media ID since it doesn't start with "http"
        assert "id" in payload["image"]
        assert payload["image"]["id"] == "media_id_123"

    def test_response_validation(self, messages_service, mock_http_client):
        """Test that responses are properly validated as MessageResponse."""
        # Test with valid response
        response = messages_service.send_text("+1234567890", "Hello")
        assert isinstance(response, MessageResponse)
        assert response.messaging_product == "whatsapp"
        assert len(response.messages) == 1
        assert response.messages[0].id == "wamid.123456"

    def test_payload_structure_validation(self, messages_service, mock_http_client):
        """Test that all payloads have required WhatsApp fields."""
        test_cases = [
            ("send_text", ["+1234567890", "Hello"]),
            ("send_image", ["+1234567890", "https://example.com/img.jpg"]),
            ("send_audio", ["+1234567890", "audio_id_123"]),
            ("send_video", ["+1234567890", "video_id_123"]),
            ("send_document", ["+1234567890", "doc_id_123"]),
            ("send_sticker", ["+1234567890", "sticker_id_123"]),
            ("send_location", ["+1234567890", 40.7128, -74.0060]),
        ]

        for method_name, args in test_cases:
            method = getattr(messages_service, method_name)
            _ = method(*args)

            call_args = mock_http_client.post.call_args
            payload = call_args.kwargs["json"]

            # Verify required WhatsApp fields
            assert payload["messaging_product"] == "whatsapp"
            assert payload["recipient_type"] == "individual"
            assert payload["to"] == "1234567890"  # Formatted number
            assert "type" in payload

    # ========================================================================
    # INTEGRATION-LIKE TESTS
    # ========================================================================

    def test_text_message_with_all_optional_params(self, messages_service, mock_http_client):
        """Test text message with all possible parameters."""
        text_msg = TextMessage(
            body="Check out https://example.com for more info!",
            preview_url=True
        )
        response = messages_service.send_text("+1-234-567-890", text=text_msg)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["to"] == "1234567890"  # Formatted
        assert payload["text"]["body"] == "Check out https://example.com for more info!"
        assert payload["text"]["preview_url"] is True
        assert isinstance(response, MessageResponse)

    def test_media_message_comprehensive(self, messages_service, mock_http_client):
        """Test media message with comprehensive parameters."""
        # Test image with caption
        image_msg = ImageMessage(
            link="https://example.com/product.jpg",
            caption="Our latest product - now 50% off! 🎉"
        )
        response = messages_service.send_image("+44 20 7946 0958", image_msg)

        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]

        assert payload["to"] == "442079460958"  # International number formatted
        assert payload["image"]["link"] == "https://example.com/product.jpg"
        assert "🎉" in payload["image"]["caption"]  # Unicode support
        assert isinstance(response, MessageResponse)

    def test_service_endpoint_configuration(self, messages_service):
        """Test that service uses correct endpoint configuration."""
        # Verify base URL construction
        expected_base = "https://graph.facebook.com/123456789/messages"
        assert messages_service.base_url == expected_base
