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
