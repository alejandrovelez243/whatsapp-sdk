Exceptions API Reference
========================

.. automodule:: whatsapp_sdk.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Exception Hierarchy
-------------------

.. code-block:: text

    WhatsAppError
    ├── WhatsAppAPIError
    ├── WhatsAppAuthError
    ├── WhatsAppRateLimitError
    ├── WhatsAppValidationError
    ├── WhatsAppWebhookError
    └── WhatsAppMediaError

Usage Examples
--------------

.. code-block:: python

    from whatsapp_sdk.exceptions import WhatsAppError, WhatsAppAPIError

    try:
        response = client.messages.send_text(
            to="+invalid",
            body="Hello"
        )
    except WhatsAppValidationError as e:
        print(f"Validation error: {e.message}")
    except WhatsAppAPIError as e:
        print(f"API error: {e.code} - {e.message}")
    except WhatsAppError as e:
        print(f"General error: {e}")
