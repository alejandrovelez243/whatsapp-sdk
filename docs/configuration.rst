Configuration
=============

The WhatsApp SDK can be configured in multiple ways to suit your needs.

Configuration Options
---------------------

The SDK accepts the following configuration parameters:

Required Parameters
~~~~~~~~~~~~~~~~~~~

- **phone_number_id** (str): Your WhatsApp Business phone number ID
- **access_token** (str): Your Meta app access token

Optional Parameters
~~~~~~~~~~~~~~~~~~~

- **app_secret** (str): Your Meta app secret for webhook signature validation
- **webhook_verify_token** (str): Token for webhook verification during setup
- **api_version** (str): WhatsApp API version (default: "v23.0")
- **base_url** (str): API base URL (default: "https://graph.facebook.com")
- **timeout** (int): Request timeout in seconds (default: 30)
- **max_retries** (int): Maximum retry attempts for failed requests (default: 3)
- **rate_limit** (int): Maximum requests per second (default: 80)

Configuration Methods
---------------------

Direct Configuration
~~~~~~~~~~~~~~~~~~~~

Pass configuration directly when creating the client:

.. code-block:: python

    from whatsapp_sdk import WhatsAppClient

    client = WhatsAppClient(
        phone_number_id="123456789",
        access_token="your_access_token",
        app_secret="your_app_secret",
        webhook_verify_token="your_verify_token",
        api_version="v23.0",
        timeout=30,
        max_retries=3,
        rate_limit=80
    )

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Set environment variables and create client from them:

.. code-block:: bash

    # .env file or shell exports
    export WHATSAPP_PHONE_NUMBER_ID="123456789"
    export WHATSAPP_ACCESS_TOKEN="your_access_token"
    export WHATSAPP_APP_SECRET="your_app_secret"
    export WHATSAPP_WEBHOOK_VERIFY_TOKEN="your_verify_token"
    export WHATSAPP_API_VERSION="v23.0"
    export WHATSAPP_BASE_URL="https://graph.facebook.com"
    export WHATSAPP_TIMEOUT="30"
    export WHATSAPP_MAX_RETRIES="3"
    export WHATSAPP_RATE_LIMIT="80"

.. code-block:: python

    from whatsapp_sdk import WhatsAppClient

    # Automatically reads from environment
    client = WhatsAppClient.from_env()

Using .env Files
~~~~~~~~~~~~~~~~

Create a ``.env`` file in your project root:

.. code-block:: ini

    # .env
    WHATSAPP_PHONE_NUMBER_ID=123456789
    WHATSAPP_ACCESS_TOKEN=your_access_token
    WHATSAPP_APP_SECRET=your_app_secret
    WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_verify_token

Then load it:

.. code-block:: python

    from dotenv import load_dotenv
    from whatsapp_sdk import WhatsAppClient

    # Load .env file
    load_dotenv()

    # Create client from environment
    client = WhatsAppClient.from_env()

Configuration Object
~~~~~~~~~~~~~~~~~~~~

Use the WhatsAppConfig class for more control:

.. code-block:: python

    from whatsapp_sdk import WhatsAppClient
    from whatsapp_sdk.config import WhatsAppConfig

    config = WhatsAppConfig(
        phone_number_id="123456789",
        access_token="your_access_token",
        app_secret="your_app_secret",
        webhook_verify_token="your_verify_token",
        api_version="v23.0",
        timeout=30,
        max_retries=3,
        rate_limit=80
    )

    client = WhatsAppClient.from_config(config)

Advanced Configuration
----------------------

Custom HTTP Client
~~~~~~~~~~~~~~~~~~

You can customize the HTTP client behavior:

.. code-block:: python

    from whatsapp_sdk import WhatsAppClient

    client = WhatsAppClient(
        phone_number_id="123456789",
        access_token="your_access_token",
        # HTTP client settings
        timeout=60,  # Longer timeout for slow connections
        max_retries=5,  # More retries for unreliable networks
        rate_limit=50  # Lower rate limit to avoid hitting API limits
    )

Multiple Clients
~~~~~~~~~~~~~~~~

You can create multiple clients for different phone numbers:

.. code-block:: python

    # Client for sales department
    sales_client = WhatsAppClient(
        phone_number_id="sales_phone_id",
        access_token="sales_token"
    )

    # Client for support department
    support_client = WhatsAppClient(
        phone_number_id="support_phone_id",
        access_token="support_token"
    )

Security Best Practices
------------------------

1. **Never Hardcode Credentials**

   Always use environment variables or secure vaults:

   .. code-block:: python

       # ❌ Bad
       client = WhatsAppClient(
           phone_number_id="123456789",
           access_token="EAABz1234567890abcdef"
       )

       # ✅ Good
       import os
       client = WhatsAppClient(
           phone_number_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
           access_token=os.getenv("WHATSAPP_ACCESS_TOKEN")
       )

2. **Use App Secret for Webhooks**

   Always validate webhook signatures in production:

   .. code-block:: python

       client = WhatsAppClient(
           phone_number_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
           access_token=os.getenv("WHATSAPP_ACCESS_TOKEN"),
           app_secret=os.getenv("WHATSAPP_APP_SECRET")  # Required for webhook validation
       )

3. **Secure Token Storage**

   - Use environment variables
   - Use secret management services (AWS Secrets Manager, Azure Key Vault, etc.)
   - Never commit credentials to version control
   - Rotate tokens regularly

4. **Validate Configuration**

   The SDK validates configuration on initialization:

   .. code-block:: python

       try:
           client = WhatsAppClient.from_env()
       except ValueError as e:
           print(f"Configuration error: {e}")
           # Handle missing or invalid configuration

Testing Configuration
---------------------

For testing, you can use mock configuration:

.. code-block:: python

    # tests/conftest.py
    import pytest
    from whatsapp_sdk import WhatsAppClient
    from whatsapp_sdk.config import WhatsAppConfig

    @pytest.fixture
    def test_client():
        config = WhatsAppConfig(
            phone_number_id="test_phone_id",
            access_token="test_token",
            base_url="http://localhost:8000"  # Mock server
        )
        return WhatsAppClient.from_config(config)

Configuration Reference
-----------------------

.. autoclass:: whatsapp_sdk.config.WhatsAppConfig
   :members:
   :undoc-members:
   :show-inheritance:
