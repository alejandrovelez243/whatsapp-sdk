Sending Messages
================

This guide covers all message types supported by the WhatsApp SDK.

Text Messages
-------------

Simple Text
~~~~~~~~~~~

.. code-block:: python

    response = client.messages.send_text(
        to="+1234567890",
        body="Hello World!"
    )

With URL Preview
~~~~~~~~~~~~~~~~

.. code-block:: python

    response = client.messages.send_text(
        to="+1234567890",
        body="Check out https://example.com",
        preview_url=True
    )

Media Messages
--------------

Images
~~~~~~

.. code-block:: python

    # Using URL
    response = client.messages.send_image(
        to="+1234567890",
        image="https://example.com/image.jpg",
        caption="Beautiful sunset"
    )

    # Using media ID
    response = client.messages.send_image(
        to="+1234567890",
        image="media_id_123",
        caption="Uploaded image"
    )

Documents
~~~~~~~~~

.. code-block:: python

    response = client.messages.send_document(
        to="+1234567890",
        document="https://example.com/document.pdf",
        caption="Important document",
        filename="contract.pdf"
    )

Videos
~~~~~~

.. code-block:: python

    response = client.messages.send_video(
        to="+1234567890",
        video="https://example.com/video.mp4",
        caption="Check this out!"
    )

Audio
~~~~~

.. code-block:: python

    response = client.messages.send_audio(
        to="+1234567890",
        audio="https://example.com/audio.mp3"
    )

Location Messages
-----------------

.. code-block:: python

    response = client.messages.send_location(
        to="+1234567890",
        latitude=37.4847,
        longitude=-122.1477,
        name="Meta Headquarters",
        address="1 Hacker Way, Menlo Park, CA"
    )

Contact Messages
----------------

.. code-block:: python

    from whatsapp_sdk.models import Contact, Name, Phone

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

Typing Indicators
-----------------

Typing indicators provide visual feedback to users showing that you are actively typing a response. The typing indicator appears for up to 25 seconds or until you send a message, whichever comes first.

Mark as Read with Typing Indicator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Mark message as read only
    response = client.messages.mark_as_read("wamid.xxx")

    # Mark as read and show typing indicator
    response = client.messages.mark_as_read(
        "wamid.xxx",
        typing_indicator=True
    )

Send Typing Indicator Only
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Show typing indicator while processing
    response = client.messages.send_typing_indicator("wamid.xxx")

    # Process your response (user sees typing indicator)
    import time
    time.sleep(2)  # Simulate processing time

    # Send actual response (typing indicator disappears)
    response = client.messages.send_text(
        to="+1234567890",
        body="Response ready!"
    )

Best Practices for Typing Indicators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**When to Use:**

- Before sending a lengthy response that requires processing time
- During conversational flows to maintain user engagement
- When fetching data from external APIs or databases

**Implementation Tips:**

.. code-block:: python

    def handle_complex_query(message_id: str, user_phone: str, query: str):
        # Show typing indicator immediately
        client.messages.send_typing_indicator(message_id)

        # Process complex query
        result = process_complex_query(query)

        # Send response (typing indicator automatically disappears)
        client.messages.send_text(
            to=user_phone,
            body=f"Here's your answer: {result}"
        )

**Important Notes:**

- Typing indicators last up to 25 seconds maximum
- Sending any message will immediately clear the typing indicator
- Use sparingly to avoid creating a poor user experience
- Don't use for very quick responses (under 1-2 seconds)
