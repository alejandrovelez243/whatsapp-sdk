.. WhatsApp SDK Python documentation master file

WhatsApp SDK Python Documentation
==================================

.. image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue
   :target: https://www.python.org/
   :alt: Python Versions

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

.. image:: https://github.com/alejandrovelez243/whatsapp-sdk/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/alejandrovelez243/whatsapp-sdk/actions/workflows/ci.yml
   :alt: Tests

A comprehensive **synchronous** Python SDK for WhatsApp Business Cloud API, following Meta's official documentation.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart
   configuration

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   usage/messages
   usage/templates
   usage/media
   usage/webhooks

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/client
   api/services
   api/models
   api/exceptions

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing
   changelog

Features
--------

- ✅ **100% Synchronous** - Simple, straightforward API without async complexity
- 📘 **Fully Type-Hinted** - Complete type safety with Pydantic models
- 🔄 **Auto-Retry Logic** - Built-in retry mechanism for robust API calls
- 🔐 **Webhook Verification** - Secure webhook signature validation
- 📦 **Media Management** - Upload, download, and manage media files
- 💬 **Template Messages** - Full template message support
- 🔔 **Interactive Messages** - Buttons, lists, and quick replies
- 📍 **Location Messages** - Send and receive location data
- 👥 **Contact Messages** - Share contact cards
- ✨ **Modern Python** - Supports Python 3.8+

Quick Example
-------------

.. code-block:: python

    from whatsapp_sdk import WhatsAppClient

    # Initialize client
    client = WhatsAppClient(
        phone_number_id="YOUR_PHONE_NUMBER_ID",
        access_token="YOUR_ACCESS_TOKEN"
    )

    # Send a text message
    response = client.messages.send_text(
        to="+1234567890",
        body="Hello from WhatsApp SDK!"
    )
    print(f"Message sent! ID: {response.messages[0].id}")

Why This SDK?
------------

This SDK provides a clean, intuitive interface for the WhatsApp Business API with:

- **No Async Complexity**: Simple synchronous calls, no await/async to manage
- **Type Safety**: Full Pydantic model support for all requests and responses
- **Developer Friendly**: Clear error messages and comprehensive documentation
- **Production Ready**: Built-in retry logic, rate limiting, and error handling
- **Well Tested**: Comprehensive test suite with high coverage

Support
-------

- **GitHub Issues**: `Report bugs <https://github.com/alejandrovelez243/whatsapp-sdk/issues>`_
- **GitHub Discussions**: `Ask questions <https://github.com/alejandrovelez243/whatsapp-sdk/discussions>`_
- **Documentation**: You're reading it!

License
-------

MIT License - see the `LICENSE <https://github.com/alejandrovelez243/whatsapp-sdk/blob/main/LICENSE>`_ file for details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
