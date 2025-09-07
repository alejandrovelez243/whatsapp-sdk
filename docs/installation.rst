Installation
============

Requirements
------------

- Python 3.8 or higher
- pip or uv package manager

Install from PyPI
-----------------

The easiest way to install the WhatsApp SDK is from PyPI:

.. code-block:: bash

    pip install whatsapp-sdk

Or using uv:

.. code-block:: bash

    uv add whatsapp-sdk

Install from Source
-------------------

To install the latest development version from GitHub:

.. code-block:: bash

    pip install git+https://github.com/alejandrovelez243/whatsapp-sdk.git

Or clone and install locally:

.. code-block:: bash

    git clone https://github.com/alejandrovelez243/whatsapp-sdk.git
    cd whatsapp-sdk
    pip install -e .

Development Installation
------------------------

For development with all testing and linting tools:

.. code-block:: bash

    git clone https://github.com/alejandrovelez243/whatsapp-sdk.git
    cd whatsapp-sdk

    # Using uv (recommended)
    uv sync --extra dev

    # Or using pip
    pip install -e ".[dev]"

Dependencies
------------

The SDK has minimal dependencies:

- **httpx**: Modern HTTP client with connection pooling
- **pydantic>=2.0**: Data validation and type safety
- **python-dotenv**: Environment variable management (optional)

All dependencies are automatically installed when you install the SDK.

Verify Installation
-------------------

To verify the installation:

.. code-block:: python

    import whatsapp_sdk
    print(whatsapp_sdk.__version__)

Or from the command line:

.. code-block:: bash

    python -c "import whatsapp_sdk; print(whatsapp_sdk.__version__)"

Next Steps
----------

Once installed, proceed to :doc:`quickstart` to learn how to use the SDK.
