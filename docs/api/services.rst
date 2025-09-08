Services API Reference
======================

Messages Service
----------------

.. autoclass:: whatsapp_sdk.services.messages.MessagesService
   :members:
   :undoc-members:
   :show-inheritance:

Templates Service
-----------------

.. autoclass:: whatsapp_sdk.services.templates.TemplatesService
   :members:
   :undoc-members:
   :show-inheritance:

Media Service
-------------

.. autoclass:: whatsapp_sdk.services.media.MediaService
   :members:
   :undoc-members:
   :show-inheritance:

Webhooks Service
----------------

.. autoclass:: whatsapp_sdk.services.webhooks.WebhooksService
   :members:
   :undoc-members:
   :show-inheritance:

HTTP Client
-----------

The underlying HTTP client provides additional methods for media operations:

.. autoclass:: whatsapp_sdk.http_client.HTTPClient
   :members: upload_multipart, download_binary
   :undoc-members:
   :show-inheritance:

.. automethod:: whatsapp_sdk.http_client.HTTPClient.upload_multipart

   Make POST request with multipart/form-data for file uploads.

   Used internally by MediaService for uploading files with proper
   multipart encoding support.

.. automethod:: whatsapp_sdk.http_client.HTTPClient.download_binary

   Download binary content from a URL.

   Used internally by MediaService for downloading media files
   as binary content with proper error handling and retry logic.
