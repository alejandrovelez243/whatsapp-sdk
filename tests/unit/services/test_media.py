"""Tests for Media Service."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from whatsapp_sdk.exceptions import WhatsAppMediaError
from whatsapp_sdk.models import MediaUploadResponse
from whatsapp_sdk.services.media import MediaService


class TestMediaService:
    """Test media service functionality."""

    @pytest.fixture()
    def media_service(self, mock_http_client, mock_config):
        """Create media service with mocked dependencies."""
        # Set required attributes on mock HTTP client
        mock_http_client.base_url = "https://graph.facebook.com/v23.0"
        return MediaService(
            http_client=mock_http_client,
            config=mock_config,
            phone_number_id="123456789",
        )

    # ========================================================================
    # UPLOAD FROM FILE TESTS
    # ========================================================================

    def test_upload_success_with_auto_mime_detection(self, media_service, mock_http_client):
        """Test successful file upload with automatic MIME type detection."""
        # Mock file system operations
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat") as mock_stat,
            patch("mimetypes.guess_type", return_value=("image/jpeg", None)),
            patch("builtins.open", mock_open(read_data=b"fake_image_data")),
        ):
            # Setup file size
            mock_stat.return_value.st_size = 1024 * 1024  # 1MB

            # Mock HTTP response
            mock_http_client.upload_multipart.return_value = {"id": "media_123"}

            # Test upload
            response = media_service.upload("/path/to/image.jpg")

            # Verify response
            assert isinstance(response, MediaUploadResponse)
            assert response.id == "media_123"

            # Verify HTTP client call
            mock_http_client.upload_multipart.assert_called_once()
            call_args = mock_http_client.upload_multipart.call_args

            assert call_args[0][0] == "123456789/media"  # endpoint
            assert "file" in call_args[1]["files"]
            assert call_args[1]["data"]["messaging_product"] == "whatsapp"
            assert call_args[1]["data"]["type"] == "image/jpeg"

    def test_upload_success_with_explicit_mime_type(self, media_service, mock_http_client):
        """Test successful file upload with explicit MIME type."""
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat") as mock_stat,
            patch("builtins.open", mock_open(read_data=b"fake_pdf_data")),
        ):
            # Setup file size
            mock_stat.return_value.st_size = 5 * 1024 * 1024  # 5MB

            # Mock HTTP response
            mock_http_client.upload_multipart.return_value = {"id": "media_456"}

            # Test upload with explicit MIME type
            response = media_service.upload("/path/to/document.pdf", mime_type="application/pdf")

            # Verify response
            assert isinstance(response, MediaUploadResponse)
            assert response.id == "media_456"

            # Verify no MIME type detection was attempted
            call_args = mock_http_client.upload_multipart.call_args
            assert call_args[1]["data"]["type"] == "application/pdf"

    def test_upload_file_not_found(self, media_service):
        """Test upload failure when file doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(WhatsAppMediaError) as exc_info:
                media_service.upload("/nonexistent/file.jpg")

            assert "File not found: /nonexistent/file.jpg" in str(exc_info.value)

    def test_upload_mime_type_detection_failure(self, media_service):
        """Test upload failure when MIME type cannot be detected."""
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("mimetypes.guess_type", return_value=(None, None)),
        ):
            with pytest.raises(WhatsAppMediaError) as exc_info:
                media_service.upload("/path/to/unknown_file")

            assert "Could not determine MIME type" in str(exc_info.value)

    def test_upload_file_size_validation_image(self, media_service):
        """Test file size validation for images."""
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat") as mock_stat,
            patch("mimetypes.guess_type", return_value=("image/jpeg", None)),
        ):
            # Setup file size exceeding image limit (5MB)
            mock_stat.return_value.st_size = 6 * 1024 * 1024  # 6MB

            with pytest.raises(WhatsAppMediaError) as exc_info:
                media_service.upload("/path/to/large_image.jpg")

            error_msg = str(exc_info.value)
            assert "File size" in error_msg
            assert "exceeds limit for image" in error_msg

    def test_upload_file_size_validation_video(self, media_service):
        """Test file size validation for videos."""
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat") as mock_stat,
            patch("mimetypes.guess_type", return_value=("video/mp4", None)),
        ):
            # Setup file size exceeding video limit (16MB)
            mock_stat.return_value.st_size = 20 * 1024 * 1024  # 20MB

            with pytest.raises(WhatsAppMediaError) as exc_info:
                media_service.upload("/path/to/large_video.mp4")

            error_msg = str(exc_info.value)
            assert "File size" in error_msg
            assert "exceeds limit for video" in error_msg

    def test_upload_file_size_validation_sticker(self, media_service):
        """Test file size validation for stickers (webp)."""
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat") as mock_stat,
            patch("mimetypes.guess_type", return_value=("image/webp", None)),
        ):
            # Setup file size exceeding sticker limit (512KB)
            mock_stat.return_value.st_size = 600 * 1024  # 600KB

            with pytest.raises(WhatsAppMediaError) as exc_info:
                media_service.upload("/path/to/large_sticker.webp")

            error_msg = str(exc_info.value)
            assert "File size" in error_msg
            assert "exceeds limit for sticker" in error_msg

    # ========================================================================
    # UPLOAD FROM BYTES TESTS
    # ========================================================================

    def test_upload_from_bytes_success(self, media_service, mock_http_client):
        """Test successful upload from bytes."""
        # Mock HTTP response
        mock_http_client.upload_multipart.return_value = {"id": "media_bytes_123"}

        # Test upload from bytes
        file_bytes = b"fake_image_data"
        response = media_service.upload_from_bytes(
            file_bytes=file_bytes,
            mime_type="image/png",
            filename="generated.png"
        )

        # Verify response
        assert isinstance(response, MediaUploadResponse)
        assert response.id == "media_bytes_123"

        # Verify HTTP client call
        mock_http_client.upload_multipart.assert_called_once()
        call_args = mock_http_client.upload_multipart.call_args

        assert call_args[0][0] == "123456789/media"
        files = call_args[1]["files"]
        assert files["file"][0] == "generated.png"  # filename
        assert files["file"][1] == file_bytes  # content
        assert files["file"][2] == "image/png"  # mime type

    def test_upload_from_bytes_without_filename(self, media_service, mock_http_client):
        """Test upload from bytes without explicit filename."""
        mock_http_client.upload_multipart.return_value = {"id": "media_bytes_456"}

        file_bytes = b"fake_audio_data"
        response = media_service.upload_from_bytes(
            file_bytes=file_bytes,
            mime_type="audio/mp3",
            filename="audio.mp3"
        )

        assert isinstance(response, MediaUploadResponse)
        assert response.id == "media_bytes_456"

    def test_upload_from_bytes_size_validation(self, media_service):
        """Test file size validation for bytes upload."""
        # Create bytes exceeding document limit (100MB)
        large_bytes = b"x" * (101 * 1024 * 1024)  # 101MB

        with pytest.raises(WhatsAppMediaError) as exc_info:
            media_service.upload_from_bytes(
                file_bytes=large_bytes,
                mime_type="application/pdf",
                filename="huge_doc.pdf"
            )

        error_msg = str(exc_info.value)
        assert "File size" in error_msg
        assert "exceeds limit for document" in error_msg

    def test_upload_from_bytes_empty_bytes(self, media_service, mock_http_client):
        """Test upload from empty bytes."""
        # Mock HTTP response for empty bytes (should succeed at API level)
        mock_http_client.upload_multipart.return_value = {"id": "empty_bytes_media"}

        # Empty bytes should be allowed (0 bytes is within all size limits)
        response = media_service.upload_from_bytes(
            file_bytes=b"",
            mime_type="image/jpeg",
            filename="empty.jpg"
        )

        # Should succeed - empty files are technically valid
        assert isinstance(response, MediaUploadResponse)
        assert response.id == "empty_bytes_media"

    # ========================================================================
    # GET URL TESTS
    # ========================================================================

    def test_get_url_success(self, media_service, mock_http_client):
        """Test successful media URL retrieval."""
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/download_url",
            "mime_type": "image/jpeg",
            "sha256": "abc123",
            "file_size": 1024,
            "id": "media_789"
        }

        url = media_service.get_url("media_789")

        assert url == "https://example.com/media/download_url"

        # Verify HTTP client call
        mock_http_client.get.assert_called_once_with("media_789")

    def test_get_url_invalid_media_id(self, media_service, mock_http_client):
        """Test URL retrieval with invalid media ID."""
        from whatsapp_sdk.exceptions import WhatsAppAPIError

        mock_http_client.get.side_effect = WhatsAppAPIError("Media not found")

        with pytest.raises(WhatsAppAPIError, match="Media not found"):
            media_service.get_url("invalid_media_id")

    # ========================================================================
    # DOWNLOAD TO MEMORY TESTS
    # ========================================================================

    def test_download_success(self, media_service, mock_http_client):
        """Test successful media download to memory."""
        # Mock URL retrieval
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/download_url",
            "mime_type": "image/jpeg",
            "sha256": "abc123",
            "file_size": 1024,
            "id": "media_download_123"
        }

        # Mock binary download
        expected_content = b"fake_downloaded_data"
        mock_http_client.download_binary.return_value = expected_content

        # Test download
        content = media_service.download("media_download_123")

        # Verify response
        assert content == expected_content

        # Verify HTTP calls
        mock_http_client.get.assert_called_once_with("media_download_123")
        mock_http_client.download_binary.assert_called_once_with("https://example.com/media/download_url")

    def test_download_invalid_media_id(self, media_service, mock_http_client):
        """Test download with invalid media ID."""
        from whatsapp_sdk.exceptions import WhatsAppAPIError

        mock_http_client.get.side_effect = WhatsAppAPIError("Media not found")

        with pytest.raises(WhatsAppAPIError):
            media_service.download("invalid_media_id")

    def test_download_binary_failure(self, media_service, mock_http_client):
        """Test download failure during binary download."""
        # Mock successful URL retrieval
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/download_url",
            "mime_type": "image/jpeg",
            "sha256": "abc123",
            "file_size": 1024,
            "id": "media_fail_123"
        }

        # Mock binary download failure
        mock_http_client.download_binary.side_effect = Exception("Network error")

        with pytest.raises(WhatsAppMediaError, match="Download failed"):
            media_service.download("media_fail_123")

    # ========================================================================
    # DOWNLOAD TO FILE TESTS
    # ========================================================================

    def test_download_to_file_success(self, media_service, mock_http_client):
        """Test successful media download to file."""
        # Mock URL retrieval and binary download
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/download_url",
            "mime_type": "image/jpeg",
            "sha256": "abc123",
            "file_size": 1024,
            "id": "media_file_123"
        }

        expected_content = b"fake_downloaded_file_data"
        mock_http_client.download_binary.return_value = expected_content

        # Mock file operations
        with (
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", mock_open()) as mock_file,
        ):
            # Test download to file
            file_path = "/path/to/save/image.jpg"
            saved_path = media_service.download_to_file("media_file_123", file_path)

            # Verify response
            assert saved_path == file_path

            # Verify file operations
            mock_file.assert_called_once()
            # Verify file was opened in write-binary mode
            args, kwargs = mock_file.call_args
            assert args[0] == Path(file_path)
            assert args[1] == "wb"

            # Verify content was written
            written_data = b"".join(
                call[0][0] for call in mock_file.return_value.write.call_args_list
            )
            assert written_data == expected_content

    def test_download_to_file_creates_directory(self, media_service, mock_http_client):
        """Test that download_to_file creates parent directories."""
        # Mock successful download
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/download_url",
            "mime_type": "image/jpeg",
            "sha256": "abc123",
            "file_size": 1024,
            "id": "media_mkdir_123"
        }
        mock_http_client.download_binary.return_value = b"test_data"

        with (
            patch("pathlib.Path.mkdir") as mock_mkdir,
            patch("builtins.open", mock_open()),
        ):
            file_path = "/new/nested/directory/image.jpg"
            media_service.download_to_file("media_mkdir_123", file_path)

            # Verify directory creation was called
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_download_to_file_permission_error(self, media_service, mock_http_client):
        """Test download to file with permission error."""
        # Mock successful URL retrieval and binary download
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/download_url",
            "mime_type": "image/jpeg",
            "sha256": "abc123",
            "file_size": 1024,
            "id": "media_perm_123"
        }
        mock_http_client.download_binary.return_value = b"test_data"

        # Mock file permission error
        with (
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", side_effect=PermissionError("Access denied")),
            pytest.raises(PermissionError, match="Access denied"),
        ):
            media_service.download_to_file("media_perm_123", "/protected/file.jpg")

    # ========================================================================
    # DELETE TESTS
    # ========================================================================

    def test_delete_success(self, media_service, mock_http_client):
        """Test successful media deletion."""
        mock_http_client.delete.return_value = {"success": True}

        result = media_service.delete("media_delete_123")

        assert result is True

        # Verify HTTP client call
        mock_http_client.delete.assert_called_once_with("media_delete_123")

    def test_delete_failure(self, media_service, mock_http_client):
        """Test media deletion failure."""
        mock_http_client.delete.return_value = {"success": False}

        result = media_service.delete("media_delete_fail")

        assert result is False

    def test_delete_invalid_media_id(self, media_service, mock_http_client):
        """Test deletion with invalid media ID."""
        from whatsapp_sdk.exceptions import WhatsAppAPIError

        mock_http_client.delete.side_effect = WhatsAppAPIError("Media not found")

        with pytest.raises(WhatsAppAPIError, match="Media not found"):
            media_service.delete("invalid_media_id")

    def test_delete_already_deleted_media(self, media_service, mock_http_client):
        """Test deletion of already deleted media."""
        # WhatsApp API might return success=false for already deleted media
        mock_http_client.delete.return_value = {"success": False}

        result = media_service.delete("already_deleted_media")

        assert result is False

    # ========================================================================
    # FILE SIZE VALIDATION TESTS
    # ========================================================================

    def test_validate_file_size_all_media_types(self, media_service):
        """Test file size validation for all media types."""
        # Test image limits
        media_service._validate_file_size("image/jpeg", 5 * 1024 * 1024)  # 5MB - OK
        with pytest.raises(WhatsAppMediaError):
            media_service._validate_file_size("image/jpeg", 6 * 1024 * 1024)  # 6MB - Fail

        # Test video limits
        media_service._validate_file_size("video/mp4", 16 * 1024 * 1024)  # 16MB - OK
        with pytest.raises(WhatsAppMediaError):
            media_service._validate_file_size("video/mp4", 17 * 1024 * 1024)  # 17MB - Fail

        # Test audio limits
        media_service._validate_file_size("audio/mp3", 16 * 1024 * 1024)  # 16MB - OK
        with pytest.raises(WhatsAppMediaError):
            media_service._validate_file_size("audio/mp3", 17 * 1024 * 1024)  # 17MB - Fail

        # Test document limits
        media_service._validate_file_size("application/pdf", 100 * 1024 * 1024)  # 100MB - OK
        with pytest.raises(WhatsAppMediaError):
            media_service._validate_file_size("application/pdf", 101 * 1024 * 1024)  # 101MB - Fail

        # Test sticker limits (webp)
        media_service._validate_file_size("image/webp", 512 * 1024)  # 512KB - OK
        with pytest.raises(WhatsAppMediaError):
            media_service._validate_file_size("image/webp", 513 * 1024)  # 513KB - Fail

    def test_validate_file_size_unknown_mime_type(self, media_service):
        """Test file size validation for unknown MIME types (treated as document)."""
        # Unknown MIME type should be treated as document (100MB limit)
        media_service._validate_file_size("application/unknown", 100 * 1024 * 1024)  # OK
        with pytest.raises(WhatsAppMediaError):
            media_service._validate_file_size("application/unknown", 101 * 1024 * 1024)  # Fail

    def test_validate_file_size_edge_cases(self, media_service):
        """Test file size validation edge cases."""
        # Test exact limits
        media_service._validate_file_size("image/jpeg", 5 * 1024 * 1024)  # Exactly 5MB
        media_service._validate_file_size("video/mp4", 16 * 1024 * 1024)  # Exactly 16MB
        media_service._validate_file_size("audio/mp3", 16 * 1024 * 1024)  # Exactly 16MB
        media_service._validate_file_size("application/pdf", 100 * 1024 * 1024)  # Exactly 100MB
        media_service._validate_file_size("image/webp", 512 * 1024)  # Exactly 512KB

        # Test zero size
        media_service._validate_file_size("image/jpeg", 0)  # Should be OK
        media_service._validate_file_size("application/pdf", 0)  # Should be OK

    # ========================================================================
    # INTEGRATION-LIKE TESTS
    # ========================================================================

    def test_complete_upload_download_cycle(self, media_service, mock_http_client):
        """Test complete upload and download cycle."""
        # Mock upload response
        mock_http_client.upload_multipart.return_value = {"id": "cycle_media_123"}

        # Mock URL and download responses
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/download_url",
            "mime_type": "image/jpeg",
            "sha256": "abc123",
            "file_size": 1024,
            "id": "cycle_media_123"
        }

        expected_content = b"original_file_content"
        mock_http_client.download_binary.return_value = expected_content

        # Test upload
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat") as mock_stat,
            patch("mimetypes.guess_type", return_value=("image/jpeg", None)),
            patch("builtins.open", mock_open(read_data=expected_content)),
        ):
            mock_stat.return_value.st_size = len(expected_content)

            # Upload file
            upload_response = media_service.upload("/path/to/image.jpg")
            media_id = upload_response.id

            # Download the same file
            downloaded_content = media_service.download(media_id)

            # Verify content matches
            assert downloaded_content == expected_content
            assert media_id == "cycle_media_123"

    def test_service_configuration(self, media_service):
        """Test service configuration and base URL construction."""
        # Verify service configuration
        assert media_service.phone_number_id == "123456789"
        assert media_service.base_url.endswith("123456789/media")

    def test_error_propagation_from_http_client(self, media_service, mock_http_client):
        """Test that HTTP client errors are properly propagated."""
        from whatsapp_sdk.exceptions import WhatsAppAPIError, WhatsAppRateLimitError

        # Test rate limit error propagation
        mock_http_client.upload_multipart.side_effect = WhatsAppRateLimitError("Rate limit exceeded")

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat") as mock_stat,
            patch("mimetypes.guess_type", return_value=("image/jpeg", None)),
            patch("builtins.open", mock_open(read_data=b"test")),
        ):
            mock_stat.return_value.st_size = 1024

            with pytest.raises(WhatsAppRateLimitError, match="Rate limit exceeded"):
                media_service.upload("/path/to/image.jpg")

        # Test API error propagation
        mock_http_client.get.side_effect = WhatsAppAPIError("API Error")

        with pytest.raises(WhatsAppAPIError, match="API Error"):
            media_service.get_url("some_media_id")

    # ========================================================================
    # MIME TYPE DETECTION TESTS
    # ========================================================================

    def test_mime_type_detection_various_extensions(self, media_service, mock_http_client):
        """Test MIME type detection for various file extensions."""
        test_cases = [
            ("/path/file.jpg", "image/jpeg"),
            ("/path/file.png", "image/png"),
            ("/path/file.webp", "image/webp"),
            ("/path/file.mp4", "video/mp4"),
            ("/path/file.mp3", "audio/mpeg"),
            ("/path/file.pdf", "application/pdf"),
            ("/path/file.doc", "application/msword"),
        ]

        mock_http_client.upload_multipart.return_value = {"id": "mime_test"}

        for file_path, expected_mime_type in test_cases:
            with (
                patch("pathlib.Path.exists", return_value=True),
                patch("pathlib.Path.stat") as mock_stat,
                patch("mimetypes.guess_type", return_value=(expected_mime_type, None)),
                patch("builtins.open", mock_open(read_data=b"test_data")),
            ):
                mock_stat.return_value.st_size = 1024

                media_service.upload(file_path)

                # Verify correct MIME type was used
                call_args = mock_http_client.upload_multipart.call_args
                assert call_args[1]["data"]["type"] == expected_mime_type

    def test_binary_data_handling(self, media_service, mock_http_client):
        """Test handling of various binary data types."""
        mock_http_client.upload_multipart.return_value = {"id": "binary_test"}

        # Test different binary data patterns
        test_data = [
            b"\x89PNG\r\n\x1a\n",  # PNG header
            b"\xff\xd8\xff\xe0",  # JPEG header
            b"RIFF",  # RIFF header (WAV/WebP)
            b"\x00" * 1000,  # Null bytes
            b"\xff" * 1000,  # All 0xFF bytes
            bytes(range(256)),  # All possible byte values
        ]

        for i, binary_data in enumerate(test_data):
            response = media_service.upload_from_bytes(
                file_bytes=binary_data,
                mime_type="application/octet-stream",
                filename=f"binary_test_{i}.bin"
            )

            assert isinstance(response, MediaUploadResponse)
            assert response.id == "binary_test"

    def test_large_file_handling_simulation(self, media_service, mock_http_client):
        """Test handling of files at size limits."""
        mock_http_client.upload_multipart.return_value = {"id": "large_file_test"}

        # Test files at exact size limits
        size_test_cases = [
            ("image/jpeg", 5 * 1024 * 1024 - 1),  # Just under image limit
            ("video/mp4", 16 * 1024 * 1024 - 1),  # Just under video limit
            ("audio/mp3", 16 * 1024 * 1024 - 1),  # Just under audio limit
            ("application/pdf", 100 * 1024 * 1024 - 1),  # Just under document limit
            ("image/webp", 512 * 1024 - 1),  # Just under sticker limit
        ]

        for mime_type, file_size in size_test_cases:
            with (
                patch("pathlib.Path.exists", return_value=True),
                patch("pathlib.Path.stat") as mock_stat,
                patch("mimetypes.guess_type", return_value=(mime_type, None)),
                patch("builtins.open", mock_open(read_data=b"x" * file_size)),
            ):
                mock_stat.return_value.st_size = file_size

                # Should succeed - just under limit
                response = media_service.upload(f"/path/to/large_file.{mime_type.split('/')[-1]}")
                assert isinstance(response, MediaUploadResponse)
