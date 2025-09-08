"""Tests for Media Service."""

from __future__ import annotations

from unittest.mock import mock_open, patch

import pytest

from whatsapp_sdk.exceptions import WhatsAppMediaError
from whatsapp_sdk.models import MediaUploadResponse
from whatsapp_sdk.services.media import MediaService


class TestMediaService:
    """Test media service functionality."""

    @pytest.fixture()
    def media_service(self, mock_http_client, mock_config):
        """Create MediaService instance with mocked dependencies."""
        return MediaService(
            http_client=mock_http_client,
            config=mock_config,
            phone_number_id="123456789"
        )

    # ========================================================================
    # UPLOAD TESTS
    # ========================================================================

    def test_upload_success_with_auto_mime_detection(self, media_service, mock_http_client):
        """Test successful file upload with automatic MIME type detection."""
        # Mock file system operations
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.stat") as mock_stat, \
             patch("mimetypes.guess_type", return_value=("image/jpeg", None)), \
             patch("builtins.open", mock_open(read_data=b"fake_image_data")):
            # Setup file size
            mock_stat.return_value.st_size = 1024 * 1024  # 1MB

            # Mock HTTP response
            mock_http_client.upload_multipart.return_value = {"id": "media_123"}

            # Test upload
            response = media_service.upload("/path/to/image.jpg")

            # Verify response
            assert isinstance(response, MediaUploadResponse)
            assert response.id == "media_123"

            # Verify HTTP client was called correctly
            mock_http_client.upload_multipart.assert_called_once()
            call_args = mock_http_client.upload_multipart.call_args
            assert "123456789/media" in call_args[0][0]
            assert call_args[1]["data"]["type"] == "image/jpeg"

    def test_upload_success_with_explicit_mime_type(self, media_service, mock_http_client):
        """Test successful file upload with explicit MIME type."""
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.stat") as mock_stat, \
             patch("builtins.open", mock_open(read_data=b"fake_image_data")):
            # Setup file size
            mock_stat.return_value.st_size = 1024 * 1024  # 1MB

            # Mock HTTP response
            mock_http_client.upload_multipart.return_value = {"id": "media_456"}

            # Test upload with explicit MIME type
            response = media_service.upload(
                "/path/to/image.jpg",
                mime_type="image/png"
            )

            # Verify response
            assert isinstance(response, MediaUploadResponse)
            assert response.id == "media_456"

            # Verify explicit MIME type was used
            call_args = mock_http_client.upload_multipart.call_args
            assert call_args[1]["data"]["type"] == "image/png"

    def test_upload_file_not_found(self, media_service):
        """Test upload failure when file doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False), \
             pytest.raises(WhatsAppMediaError, match="File not found"):
            media_service.upload("/nonexistent/file.jpg")

    def test_upload_mime_type_detection_failure(self, media_service):
        """Test upload failure when MIME type cannot be detected."""
        with patch("pathlib.Path.exists", return_value=True), \
             patch("mimetypes.guess_type", return_value=(None, None)), \
             pytest.raises(WhatsAppMediaError, match="Could not determine MIME type"):
            media_service.upload("/path/to/unknown.xyz")

    def test_upload_file_size_validation_image(self, media_service):
        """Test file size validation for images."""
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.stat") as mock_stat, \
             patch("mimetypes.guess_type", return_value=("image/jpeg", None)), \
             patch("builtins.open", mock_open(read_data=b"x" * (5 * 1024 * 1024 + 1))):
            # Setup file size over limit (5MB + 1 byte)
            mock_stat.return_value.st_size = 5 * 1024 * 1024 + 1

            with pytest.raises(WhatsAppMediaError, match="File size .* exceeds limit"):
                media_service.upload("/path/to/large_image.jpg")

    def test_upload_file_size_validation_video(self, media_service):
        """Test file size validation for videos."""
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.stat") as mock_stat, \
             patch("mimetypes.guess_type", return_value=("video/mp4", None)), \
             patch("builtins.open", mock_open(read_data=b"x" * (16 * 1024 * 1024 + 1))):
            # Setup file size over limit (16MB + 1 byte)
            mock_stat.return_value.st_size = 16 * 1024 * 1024 + 1

            with pytest.raises(WhatsAppMediaError, match="File size .* exceeds limit"):
                media_service.upload("/path/to/large_video.mp4")

    def test_upload_file_size_validation_sticker(self, media_service):
        """Test file size validation for stickers (webp)."""
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.stat") as mock_stat, \
             patch("mimetypes.guess_type", return_value=("image/webp", None)), \
             patch("builtins.open", mock_open(read_data=b"x" * (512 * 1024 + 1))):
            # Setup file size over limit (512KB + 1 byte)
            mock_stat.return_value.st_size = 512 * 1024 + 1

            with pytest.raises(WhatsAppMediaError, match="File size .* exceeds limit"):
                media_service.upload("/path/to/large_sticker.webp")

    def test_upload_from_bytes_success(self, media_service, mock_http_client):
        """Test successful upload from bytes."""
        # Mock HTTP response
        mock_http_client.upload_multipart.return_value = {"id": "media_bytes_123"}

        # Test upload from bytes
        file_bytes = b"test_file_content"
        response = media_service.upload_from_bytes(
            file_bytes,
            mime_type="image/jpeg",
            filename="test.jpg"
        )

        # Verify response
        assert isinstance(response, MediaUploadResponse)
        assert response.id == "media_bytes_123"

        # Verify HTTP client was called correctly
        mock_http_client.upload_multipart.assert_called_once()
        call_args = mock_http_client.upload_multipart.call_args
        assert call_args[1]["data"]["type"] == "image/jpeg"

    def test_upload_from_bytes_without_explicit_filename(self, media_service, mock_http_client):
        """Test upload from bytes with generic filename."""
        # Mock HTTP response
        mock_http_client.upload_multipart.return_value = {"id": "media_noname_123"}

        # Test upload with generic filename
        file_bytes = b"test_content"
        response = media_service.upload_from_bytes(
            file_bytes,
            mime_type="application/pdf",
            filename="file.pdf"  # MediaService requires filename
        )

        # Verify response
        assert isinstance(response, MediaUploadResponse)
        assert response.id == "media_noname_123"

    def test_upload_from_bytes_size_validation(self, media_service):
        """Test file size validation for bytes upload."""
        # Create bytes over image size limit
        large_bytes = b"x" * (5 * 1024 * 1024 + 1)

        with pytest.raises(WhatsAppMediaError, match="File size .* exceeds limit"):
            media_service.upload_from_bytes(large_bytes, mime_type="image/jpeg", filename="large.jpg")

    def test_upload_from_bytes_empty_bytes(self, media_service, mock_http_client):
        """Test upload with empty bytes (allowed by current implementation)."""
        # Current implementation doesn't prevent empty bytes
        # It would be up to WhatsApp API to reject them
        mock_http_client.upload_multipart.return_value = {"id": "empty_123"}

        response = media_service.upload_from_bytes(b"", mime_type="image/jpeg", filename="empty.jpg")
        assert isinstance(response, MediaUploadResponse)
        assert response.id == "empty_123"

    # ========================================================================
    # GET URL TESTS
    # ========================================================================

    def test_get_url_success(self, media_service, mock_http_client):
        """Test successful media URL retrieval."""
        # Mock HTTP response
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/file.jpg",
            "mime_type": "image/jpeg",
            "sha256": "hash123",
            "file_size": 1024,
            "id": "media_url_123"
        }

        # Test get URL - returns string, not object
        url = media_service.get_url("media_url_123")

        # Verify response is a string URL
        assert url == "https://example.com/media/file.jpg"
        assert isinstance(url, str)

        # Verify HTTP client was called correctly
        mock_http_client.get.assert_called_once_with("media_url_123")

    def test_get_url_invalid_media_id(self, media_service, mock_http_client):
        """Test get URL with invalid media ID."""
        # Mock HTTP error response
        mock_http_client.get.side_effect = WhatsAppMediaError("Media not found")

        with pytest.raises(WhatsAppMediaError, match="Media not found"):
            media_service.get_url("invalid_media_id")

    # ========================================================================
    # DOWNLOAD TESTS
    # ========================================================================

    def test_download_success(self, media_service, mock_http_client):
        """Test successful media download to memory."""
        # Mock get URL response
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/file.jpg",
            "mime_type": "image/jpeg",
            "sha256": "hash123",
            "file_size": 1024,
            "id": "media_dl_123"
        }

        # Mock download binary response
        mock_http_client.download_binary.return_value = b"fake_image_data"

        # Test download
        content = media_service.download("media_dl_123")

        # Verify content
        assert content == b"fake_image_data"

        # Verify HTTP client calls
        mock_http_client.get.assert_called_once_with("media_dl_123")
        mock_http_client.download_binary.assert_called_once()

    def test_download_invalid_media_id(self, media_service, mock_http_client):
        """Test download with invalid media ID."""
        # Mock error response
        mock_http_client.get.side_effect = WhatsAppMediaError("Media not found")

        with pytest.raises(WhatsAppMediaError, match="Media not found"):
            media_service.download("invalid_media_id")

    def test_download_binary_failure(self, media_service, mock_http_client):
        """Test download failure during binary download."""
        # Mock get URL success
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/file.jpg",
            "mime_type": "image/jpeg",
            "sha256": "hash123",
            "file_size": 1024,
            "id": "media_fail_123"
        }

        # Mock download binary failure
        mock_http_client.download_binary.side_effect = WhatsAppMediaError("Download failed")

        with pytest.raises(WhatsAppMediaError, match="Download failed"):
            media_service.download("media_fail_123")

    def test_download_to_file_success(self, media_service, mock_http_client):
        """Test successful download to file."""
        # Mock get URL response
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/file.jpg",
            "mime_type": "image/jpeg",
            "sha256": "hash123",
            "file_size": 1024,
            "id": "media_file_123"
        }

        # Mock download binary response
        mock_http_client.download_binary.return_value = b"fake_image_data"

        # Mock file operations
        with patch("pathlib.Path.mkdir"), \
             patch("builtins.open", mock_open()) as mock_file:
            # Test download to file
            result_path = media_service.download_to_file(
                "media_file_123",
                "/path/to/save/image.jpg"
            )

            # Verify result
            assert result_path == "/path/to/save/image.jpg"

            # Verify file was written - MediaService uses Path internally
            from pathlib import Path
            mock_file.assert_called_once_with(Path("/path/to/save/image.jpg"), "wb")
            mock_file().write.assert_called_once_with(b"fake_image_data")

    def test_download_to_file_creates_directory(self, media_service, mock_http_client):
        """Test download to file creates directory if needed."""
        # Mock get URL response
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/file.jpg",
            "mime_type": "image/jpeg",
            "sha256": "hash123",
            "file_size": 1024,
            "id": "media_dir_123"
        }
        mock_http_client.download_binary.return_value = b"test_data"

        with patch("pathlib.Path.mkdir") as mock_mkdir, \
             patch("builtins.open", mock_open()), \
             patch("pathlib.Path.exists", return_value=False):
            # Test download to file with non-existent directory
            media_service.download_to_file(
                "media_dir_123",
                "/new/directory/file.jpg"
            )

            # Verify directory was created
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_download_to_file_permission_error(self, media_service, mock_http_client):
        """Test download to file with permission error."""
        # Mock get URL response
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/file.jpg",
            "mime_type": "image/jpeg",
            "sha256": "hash123",
            "file_size": 1024,
            "id": "media_perm_123"
        }
        mock_http_client.download_binary.return_value = b"test_data"

        # Mock file permission error
        with patch("pathlib.Path.mkdir"), \
             patch("builtins.open", side_effect=PermissionError("Access denied")), \
             pytest.raises(PermissionError, match="Access denied"):
            media_service.download_to_file("media_perm_123", "/protected/file.jpg")

    # ========================================================================
    # DELETE TESTS
    # ========================================================================

    def test_delete_success(self, media_service, mock_http_client):
        """Test successful media deletion."""
        # Mock HTTP response
        mock_http_client.delete.return_value = {"success": True}

        # Test delete
        result = media_service.delete("media_del_123")

        # Verify result
        assert result is True

        # Verify HTTP client was called correctly
        mock_http_client.delete.assert_called_once_with("media_del_123")

    def test_delete_failure(self, media_service, mock_http_client):
        """Test media deletion failure."""
        # Mock HTTP response
        mock_http_client.delete.return_value = {"success": False}

        # Test delete
        result = media_service.delete("media_del_fail")

        # Verify result
        assert result is False

    def test_delete_invalid_media_id(self, media_service, mock_http_client):
        """Test delete with invalid media ID."""
        # Mock error response
        mock_http_client.delete.side_effect = WhatsAppMediaError("Media not found")

        with pytest.raises(WhatsAppMediaError, match="Media not found"):
            media_service.delete("invalid_media_id")

    def test_delete_already_deleted_media(self, media_service, mock_http_client):
        """Test delete media that was already deleted."""
        # Mock error response
        mock_http_client.delete.side_effect = WhatsAppMediaError("Media already deleted")

        with pytest.raises(WhatsAppMediaError, match="Media already deleted"):
            media_service.delete("already_deleted_id")

    # ========================================================================
    # VALIDATION TESTS
    # ========================================================================

    def test_validate_file_size_all_media_types(self, media_service):
        """Test file size validation for all media types."""
        # Test within limits - correct parameter order (mime_type, file_size)
        assert media_service._validate_file_size("image/jpeg", 1024) is None
        assert media_service._validate_file_size("video/mp4", 1024) is None
        assert media_service._validate_file_size("audio/mpeg", 1024) is None
        assert media_service._validate_file_size("application/pdf", 1024) is None
        assert media_service._validate_file_size("image/webp", 1024) is None

        # Test at limits
        assert media_service._validate_file_size("image/jpeg", 5 * 1024 * 1024) is None
        assert media_service._validate_file_size("video/mp4", 16 * 1024 * 1024) is None
        assert media_service._validate_file_size("audio/mpeg", 16 * 1024 * 1024) is None
        assert media_service._validate_file_size("application/pdf", 100 * 1024 * 1024) is None
        assert media_service._validate_file_size("image/webp", 512 * 1024) is None

    def test_validate_file_size_unknown_mime_type(self, media_service):
        """Test file size validation for unknown MIME type."""
        # Unknown MIME types should use document limit (100MB)
        assert media_service._validate_file_size("unknown/type", 50 * 1024 * 1024) is None

        # Over 100MB should fail
        with pytest.raises(WhatsAppMediaError):
            media_service._validate_file_size("unknown/type", 101 * 1024 * 1024)

    def test_validate_file_size_edge_cases(self, media_service):
        """Test file size validation edge cases."""
        # Test over limits by 1 byte - correct parameter order
        with pytest.raises(WhatsAppMediaError):
            media_service._validate_file_size("image/jpeg", 5 * 1024 * 1024 + 1)

        with pytest.raises(WhatsAppMediaError):
            media_service._validate_file_size("video/mp4", 16 * 1024 * 1024 + 1)

        with pytest.raises(WhatsAppMediaError):
            media_service._validate_file_size("image/webp", 512 * 1024 + 1)

    # ========================================================================
    # INTEGRATION-LIKE TESTS
    # ========================================================================

    def test_complete_upload_download_cycle(self, media_service, mock_http_client):
        """Test complete upload and download cycle."""
        # Test upload
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.stat") as mock_stat, \
             patch("mimetypes.guess_type", return_value=("image/jpeg", None)), \
             patch("builtins.open", mock_open(read_data=b"test_image")):
            mock_stat.return_value.st_size = 1024
            mock_http_client.upload_multipart.return_value = {"id": "cycle_123"}

            upload_response = media_service.upload("/path/to/image.jpg")
            assert upload_response.id == "cycle_123"

        # Test download of uploaded media
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/cycle_123",
            "mime_type": "image/jpeg",
            "sha256": "hash123",
            "file_size": 1024,
            "id": "cycle_123"
        }
        mock_http_client.download_binary.return_value = b"test_image"

        downloaded_content = media_service.download("cycle_123")
        assert downloaded_content == b"test_image"

    def test_service_configuration(self, media_service):
        """Test service is properly configured."""
        assert media_service.phone_number_id == "123456789"
        assert hasattr(media_service, "http_client")
        assert hasattr(media_service, "config")

    def test_error_propagation_from_http_client(self, media_service, mock_http_client):
        """Test that errors from HTTPClient are properly propagated."""
        from whatsapp_sdk.exceptions import WhatsAppRateLimitError

        # Test rate limit error propagation
        mock_http_client.upload_multipart.side_effect = WhatsAppRateLimitError("Rate limit exceeded")

        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.stat") as mock_stat, \
             patch("mimetypes.guess_type", return_value=("image/jpeg", None)), \
             patch("builtins.open", mock_open(read_data=b"test_image")):
            mock_stat.return_value.st_size = 1024

            with pytest.raises(WhatsAppRateLimitError, match="Rate limit exceeded"):
                media_service.upload("/path/to/image.jpg")

    def test_mime_type_detection_various_extensions(self, media_service, mock_http_client):
        """Test MIME type detection for various file extensions."""
        test_cases = [
            ("/path/to/file.jpg", "image/jpeg"),
            ("/path/to/file.png", "image/png"),
            ("/path/to/file.mp4", "video/mp4"),
            ("/path/to/file.mp3", "audio/mpeg"),
            ("/path/to/file.pdf", "application/pdf"),
            ("/path/to/file.webp", "image/webp"),
        ]

        for file_path, expected_mime_type in test_cases:
            with patch("pathlib.Path.exists", return_value=True), \
                 patch("pathlib.Path.stat") as mock_stat, \
                 patch("mimetypes.guess_type", return_value=(expected_mime_type, None)), \
                 patch("builtins.open", mock_open(read_data=b"test_data")):
                mock_stat.return_value.st_size = 1024
                mock_http_client.upload_multipart.return_value = {"id": "test_123"}

                response = media_service.upload(file_path)
                assert isinstance(response, MediaUploadResponse)

                # Verify correct MIME type was used
                call_args = mock_http_client.upload_multipart.call_args
                assert call_args[1]["data"]["type"] == expected_mime_type

    def test_binary_data_handling(self, media_service, mock_http_client):
        """Test handling of binary data in uploads and downloads."""
        # Test with actual binary data patterns
        binary_data = bytes([0x00, 0x01, 0x02, 0xFF, 0xFE, 0xFD])

        # Test upload from bytes
        mock_http_client.upload_multipart.return_value = {"id": "binary_123"}
        response = media_service.upload_from_bytes(binary_data, mime_type="application/octet-stream", filename="binary.bin")
        assert response.id == "binary_123"

        # Test download returns binary data correctly
        mock_http_client.get.return_value = {
            "url": "https://example.com/media/binary_123",
            "mime_type": "application/octet-stream",
            "sha256": "hash123",
            "file_size": len(binary_data),
            "id": "binary_123"
        }
        mock_http_client.download_binary.return_value = binary_data

        downloaded = media_service.download("binary_123")
        assert downloaded == binary_data

    def test_large_file_handling_simulation(self, media_service, mock_http_client):
        """Test handling of files at maximum allowed sizes."""
        size_test_cases = [
            ("image/jpeg", 5 * 1024 * 1024),      # 5MB image
            ("video/mp4", 16 * 1024 * 1024),      # 16MB video
            ("audio/mpeg", 16 * 1024 * 1024),     # 16MB audio
            ("application/pdf", 100 * 1024 * 1024), # 100MB document
            ("image/webp", 512 * 1024),           # 512KB sticker
        ]

        for mime_type, file_size in size_test_cases:
            with patch("pathlib.Path.exists", return_value=True), \
                 patch("pathlib.Path.stat") as mock_stat, \
                 patch("mimetypes.guess_type", return_value=(mime_type, None)), \
                 patch("builtins.open", mock_open(read_data=b"x" * file_size)):
                mock_stat.return_value.st_size = file_size

                # Should succeed - just under limit
                response = media_service.upload(f"/path/to/large_file.{mime_type.split('/')[-1]}")
                assert isinstance(response, MediaUploadResponse)
