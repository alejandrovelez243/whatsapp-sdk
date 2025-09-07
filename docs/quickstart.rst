Quick Start
===========

This guide will help you get started with the WhatsApp SDK Python in just a few minutes.

Prerequisites
-------------

Before you begin, you'll need:

1. A WhatsApp Business Account
2. A Meta App with WhatsApp Business API access
3. Your credentials:

   - **Phone Number ID**: Your WhatsApp Business phone number ID
   - **Access Token**: Your Meta app access token
   - **App Secret** (optional): For webhook signature validation
   - **Webhook Verify Token** (optional): For webhook setup

Basic Setup
-----------

Initialize the Client
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from whatsapp_sdk import WhatsAppClient

    client = WhatsAppClient(
        phone_number_id="YOUR_PHONE_NUMBER_ID",
        access_token="YOUR_ACCESS_TOKEN"
    )

Using Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a ``.env`` file:

.. code-block:: bash

    WHATSAPP_PHONE_NUMBER_ID=your_phone_id
    WHATSAPP_ACCESS_TOKEN=your_access_token
    WHATSAPP_APP_SECRET=your_app_secret
    WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_verify_token

Then initialize from environment:

.. code-block:: python

    from whatsapp_sdk import WhatsAppClient

    client = WhatsAppClient.from_env()

Send Your First Message
-----------------------

Text Message
~~~~~~~~~~~~

.. code-block:: python

    response = client.messages.send_text(
        to="+1234567890",
        body="Hello from WhatsApp SDK!"
    )

    print(f"Message sent! ID: {response.messages[0].id}")

Image Message
~~~~~~~~~~~~~

.. code-block:: python

    response = client.messages.send_image(
        to="+1234567890",
        image="https://example.com/image.jpg",
        caption="Check out this image!"
    )

Template Message
~~~~~~~~~~~~~~~~

.. code-block:: python

    response = client.templates.send(
        to="+1234567890",
        template_name="hello_world",
        language_code="en_US"
    )

Handle Webhooks
---------------

Basic Webhook Setup
~~~~~~~~~~~~~~~~~~~

Here's a simple FastAPI webhook handler:

.. code-block:: python

    from fastapi import FastAPI, Request, Header, Query

    app = FastAPI()

    @app.get("/webhook")
    def verify_webhook(
        hub_mode: str = Query(None, alias="hub.mode"),
        hub_verify_token: str = Query(None, alias="hub.verify_token"),
        hub_challenge: str = Query(None, alias="hub.challenge")
    ):
        """Verify webhook during setup."""
        result = client.webhooks.handle_verification(
            hub_mode, hub_verify_token, hub_challenge
        )
        if result:
            return result
        return {"error": "Invalid token"}, 403

    @app.post("/webhook")
    async def handle_webhook(
        request: Request,
        x_hub_signature_256: str = Header(None)
    ):
        """Handle incoming webhook events."""
        body = await request.body()

        # Validate and parse the event
        event = client.webhooks.handle_event(x_hub_signature_256, body)

        # Extract messages
        messages = client.webhooks.extract_messages(event)
        for message in messages:
            if message.type == "text":
                print(f"Received text: {message.text.body}")

                # Echo the message back
                client.messages.send_text(
                    to=message.from_,
                    body=f"You said: {message.text.body}"
                )

        return {"status": "ok"}

Common Patterns
---------------

Using Pydantic Models
~~~~~~~~~~~~~~~~~~~~~

The SDK supports Pydantic models for type safety:

.. code-block:: python

    from whatsapp_sdk.models import TextMessage, Contact, Name, Phone

    # Text message with Pydantic
    text_msg = TextMessage(
        body="Hello with type safety!",
        preview_url=True
    )
    response = client.messages.send_text(to="+1234567890", text=text_msg)

    # Contact with Pydantic
    contact = Contact(
        name=Name(
            formatted_name="John Doe",
            first_name="John",
            last_name="Doe"
        ),
        phones=[Phone(phone="+1234567890", type="MOBILE")]
    )
    response = client.messages.send_contact(
        to="+9876543210",
        contacts=[contact]
    )

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

    from whatsapp_sdk.exceptions import WhatsAppError

    try:
        response = client.messages.send_text(
            to="+invalid_number",
            body="This will fail"
        )
    except WhatsAppError as e:
        print(f"Error: {e.message}")
        print(f"Error code: {e.code}")
        print(f"Error details: {e.details}")

Media Upload
~~~~~~~~~~~~

.. code-block:: python

    # Upload a local file
    upload_response = client.media.upload("/path/to/image.jpg")
    media_id = upload_response.id

    # Send using the media ID
    response = client.messages.send_image(
        to="+1234567890",
        image=media_id,
        caption="Uploaded image"
    )

    # Download media
    content = client.media.download(media_id)
    with open("downloaded.jpg", "wb") as f:
        f.write(content)

Best Practices
--------------

1. **Always Use Environment Variables**: Never hardcode credentials
2. **Handle Errors**: Always wrap API calls in try-except blocks
3. **Validate Phone Numbers**: Ensure phone numbers include country code
4. **Use Pydantic Models**: Get type safety and validation
5. **Implement Retry Logic**: The SDK has built-in retries, but handle failures gracefully
6. **Secure Webhooks**: Always validate webhook signatures in production

Next Steps
----------

- Explore :doc:`usage/messages` for all message types
- Learn about :doc:`usage/templates` for template management
- Set up :doc:`usage/webhooks` for receiving messages
- Check the :doc:`api/client` for complete API reference
