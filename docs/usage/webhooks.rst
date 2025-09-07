Webhook Handling
================

Webhooks allow you to receive real-time notifications about messages and status updates.

Webhook Setup
-------------

Verification
~~~~~~~~~~~~

.. code-block:: python

    from fastapi import FastAPI, Query

    app = FastAPI()

    @app.get("/webhook")
    def verify_webhook(
        hub_mode: str = Query(None, alias="hub.mode"),
        hub_verify_token: str = Query(None, alias="hub.verify_token"),
        hub_challenge: str = Query(None, alias="hub.challenge")
    ):
        result = client.webhooks.handle_verification(
            hub_mode, hub_verify_token, hub_challenge
        )
        if result:
            return result
        return {"error": "Invalid token"}, 403

Event Handling
--------------

Receiving Messages
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @app.post("/webhook")
    async def handle_webhook(
        request: Request,
        x_hub_signature_256: str = Header(None)
    ):
        body = await request.body()

        # Validate and parse
        event = client.webhooks.handle_event(x_hub_signature_256, body)

        # Extract messages
        messages = client.webhooks.extract_messages(event)
        for message in messages:
            if message.type == "text":
                print(f"Text: {message.text.body}")
            elif message.type == "image":
                print(f"Image ID: {message.image.id}")

        return {"status": "ok"}

Status Updates
~~~~~~~~~~~~~~

.. code-block:: python

    # Extract status updates
    statuses = client.webhooks.extract_statuses(event)
    for status in statuses:
        print(f"Message {status.id}: {status.status}")
        if status.status == "delivered":
            print("Message was delivered")
        elif status.status == "read":
            print("Message was read")
