Template Messages
=================

Template messages are pre-approved message formats that can be sent to users outside the 24-hour messaging window.

Sending Templates
-----------------

Simple Template
~~~~~~~~~~~~~~~

.. code-block:: python

    response = client.templates.send(
        to="+1234567890",
        template_name="hello_world",
        language_code="en_US"
    )

Template with Parameters
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from whatsapp_sdk.models import TemplateComponent, TemplateParameter

    components = [
        TemplateComponent(
            type="body",
            parameters=[
                TemplateParameter(type="text", text="John"),
                TemplateParameter(type="text", text="ABC123")
            ]
        )
    ]

    response = client.templates.send(
        to="+1234567890",
        template_name="order_confirmation",
        language_code="en_US",
        components=components
    )

Managing Templates
------------------

List Templates
~~~~~~~~~~~~~~

.. code-block:: python

    templates = client.templates.list()
    for template in templates.data:
        print(f"Name: {template.name}")
        print(f"Status: {template.status}")

Create Template
~~~~~~~~~~~~~~~

.. code-block:: python

    response = client.templates.create(
        name="welcome_message",
        category="MARKETING",
        language="en_US",
        components=[
            {
                "type": "HEADER",
                "format": "TEXT",
                "text": "Welcome to {{1}}!"
            },
            {
                "type": "BODY",
                "text": "Hi {{1}}, thanks for joining!"
            }
        ]
    )
