Media Management
================

The SDK provides comprehensive media management capabilities for uploading, downloading, and managing media files on WhatsApp Business API.

File Size Limits
----------------

WhatsApp imposes specific file size limits for different media types:

- **Images**: Maximum 5MB
- **Videos**: Maximum 16MB
- **Audio**: Maximum 16MB
- **Documents**: Maximum 100MB
- **Stickers**: Maximum 500KB

Supported formats vary by media type. Always check WhatsApp's official documentation for current format support.

Uploading Media
---------------

From File
~~~~~~~~~

Upload a media file from your local filesystem:

.. code-block:: python

    # Upload image file
    response = client.media.upload("/path/to/image.jpg")
    media_id = response.id
    print(f"Media uploaded with ID: {media_id}")

    # Upload with explicit MIME type
    response = client.media.upload(
        "/path/to/document.pdf",
        mime_type="application/pdf"
    )

From Bytes
~~~~~~~~~~

Upload media directly from memory (useful for dynamic content):

.. code-block:: python

    with open("image.jpg", "rb") as f:
        file_bytes = f.read()

    response = client.media.upload_from_bytes(
        file_bytes=file_bytes,
        mime_type="image/jpeg",
        filename="photo.jpg"
    )
    print(f"Upload successful: {response.id}")

Error Handling for Uploads
~~~~~~~~~~~~~~~~~~~~~~~~~~

Handle common upload errors gracefully:

.. code-block:: python

    from whatsapp_sdk.exceptions import WhatsAppMediaError

    try:
        response = client.media.upload("/path/to/large_file.mp4")
        print(f"Upload successful: {response.id}")
    except WhatsAppMediaError as e:
        if "file too large" in str(e).lower():
            print("File exceeds size limit")
        elif "unsupported format" in str(e).lower():
            print("File format not supported")
        else:
            print(f"Upload failed: {e}")
    except FileNotFoundError:
        print("File not found - check the file path")

Downloading Media
-----------------

Get Media URL
~~~~~~~~~~~~~

Retrieve the download URL for a media file:

.. code-block:: python

    try:
        url_response = client.media.get_url("media_id_123")
        download_url = url_response.url
        print(f"Download URL: {download_url}")
        print(f"MIME type: {url_response.mime_type}")
        print(f"File size: {url_response.file_size} bytes")
    except WhatsAppMediaError as e:
        print(f"Failed to get URL: {e}")

Download Content
~~~~~~~~~~~~~~~~

Download media content directly to memory:

.. code-block:: python

    try:
        content = client.media.download("media_id_123")

        # Save to file
        with open("downloaded.jpg", "wb") as f:
            f.write(content)

        print(f"Downloaded {len(content)} bytes")
    except WhatsAppMediaError as e:
        print(f"Download failed: {e}")

Download to File
~~~~~~~~~~~~~~~~

Download media directly to a file (more memory efficient for large files):

.. code-block:: python

    try:
        saved_path = client.media.download_to_file(
            "media_id_123",
            "/path/to/save/image.jpg"
        )
        print(f"File saved to: {saved_path}")
    except WhatsAppMediaError as e:
        print(f"Download failed: {e}")
    except PermissionError:
        print("Permission denied - check file path permissions")

Download with Validation
~~~~~~~~~~~~~~~~~~~~~~~~

Download with additional validation and error handling:

.. code-block:: python

    import os
    from pathlib import Path

    def safe_download(media_id: str, save_path: str, max_size_mb: int = 50):
        """Safely download media with size and path validation."""
        try:
            # Get media info first
            url_response = client.media.get_url(media_id)

            # Check file size
            file_size_mb = url_response.file_size / (1024 * 1024)
            if file_size_mb > max_size_mb:
                raise ValueError(f"File too large: {file_size_mb:.1f}MB > {max_size_mb}MB")

            # Ensure directory exists
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)

            # Download file
            final_path = client.media.download_to_file(media_id, save_path)
            return final_path

        except Exception as e:
            print(f"Safe download failed: {e}")
            return None

    # Usage
    result = safe_download("media_id_123", "/downloads/image.jpg", max_size_mb=10)
    if result:
        print(f"Successfully downloaded to: {result}")

Deleting Media
--------------

Remove media files from WhatsApp servers:

.. code-block:: python

    try:
        success = client.media.delete("media_id_123")
        if success:
            print("Media deleted successfully")
        else:
            print("Delete operation failed")
    except WhatsAppMediaError as e:
        print(f"Delete failed: {e}")

Bulk Operations
~~~~~~~~~~~~~~~

Handle multiple media files efficiently:

.. code-block:: python

    def cleanup_old_media(media_ids: list[str]) -> dict[str, bool]:
        """Delete multiple media files and return results."""
        results = {}

        for media_id in media_ids:
            try:
                success = client.media.delete(media_id)
                results[media_id] = success
                print(f"Deleted {media_id}: {success}")
            except WhatsAppMediaError as e:
                results[media_id] = False
                print(f"Failed to delete {media_id}: {e}")

        return results

    # Usage
    old_media = ["media_1", "media_2", "media_3"]
    results = cleanup_old_media(old_media)
    successful = sum(results.values())
    print(f"Successfully deleted {successful}/{len(old_media)} files")

Best Practices
--------------

1. **Validate Before Upload**: Check file size and format before uploading
2. **Handle Errors Gracefully**: Always wrap media operations in try-catch blocks
3. **Clean Up**: Delete unused media to save storage space
4. **Monitor Quotas**: Keep track of your media storage usage
5. **Use Appropriate Methods**: Use ``download_to_file()`` for large files to save memory
6. **Security**: Validate file types and sanitize file names when handling user uploads

Common Error Scenarios
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from whatsapp_sdk.exceptions import WhatsAppMediaError, WhatsAppError

    def handle_media_operation():
        try:
            # Your media operation
            response = client.media.upload("/path/to/file.jpg")

        except FileNotFoundError:
            # File doesn't exist
            print("File not found")

        except PermissionError:
            # No permission to read file
            print("Permission denied")

        except WhatsAppMediaError as e:
            # WhatsApp-specific media errors
            if "file too large" in str(e).lower():
                print("File exceeds WhatsApp size limits")
            elif "unsupported" in str(e).lower():
                print("File format not supported by WhatsApp")
            else:
                print(f"Media error: {e}")

        except WhatsAppError as e:
            # General API errors
            print(f"API error: {e}")

        except Exception as e:
            # Unexpected errors
            print(f"Unexpected error: {e}")
