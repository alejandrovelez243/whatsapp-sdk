Media Management
================

The SDK provides comprehensive media management capabilities.

Uploading Media
---------------

From File
~~~~~~~~~

.. code-block:: python

    response = client.media.upload("/path/to/image.jpg")
    media_id = response.id
    print(f"Media uploaded with ID: {media_id}")

From Bytes
~~~~~~~~~~

.. code-block:: python

    with open("image.jpg", "rb") as f:
        file_bytes = f.read()

    response = client.media.upload_from_bytes(
        file_bytes=file_bytes,
        mime_type="image/jpeg",
        filename="photo.jpg"
    )

Downloading Media
-----------------

Get Media URL
~~~~~~~~~~~~~

.. code-block:: python

    url = client.media.get_url("media_id_123")
    print(f"Download URL: {url}")

Download Content
~~~~~~~~~~~~~~~~

.. code-block:: python

    content = client.media.download("media_id_123")
    with open("downloaded.jpg", "wb") as f:
        f.write(content)

Download to File
~~~~~~~~~~~~~~~~

.. code-block:: python

    saved_path = client.media.download_to_file(
        "media_id_123",
        "/path/to/save/image.jpg"
    )

Deleting Media
--------------

.. code-block:: python

    success = client.media.delete("media_id_123")
    if success:
        print("Media deleted successfully")
