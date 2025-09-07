Contributing
============

We welcome contributions to the WhatsApp SDK Python! This guide will help you get started.

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature
4. Make your changes
5. Submit a pull request

Development Setup
-----------------

.. code-block:: bash

    # Clone your fork
    git clone https://github.com/YOUR_USERNAME/whatsapp-sdk.git
    cd whatsapp-sdk

    # Create virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install in development mode
    pip install -e ".[dev]"

    # Install pre-commit hooks
    pre-commit install

Code Style
----------

We use the following tools to maintain code quality:

- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Run all checks:

.. code-block:: bash

    # Format code
    black src/ tests/

    # Lint
    ruff check src/ tests/

    # Type check
    mypy src/

Testing
-------

Write tests for all new features:

.. code-block:: bash

    # Run all tests
    pytest

    # Run with coverage
    pytest --cov=whatsapp_sdk

    # Run specific test
    pytest tests/unit/services/test_messages.py

Pull Request Process
--------------------

1. Ensure all tests pass
2. Update documentation if needed
3. Add entry to CHANGELOG.md
4. Submit PR with clear description
5. Wait for review and approval

Guidelines
----------

- Follow existing code patterns
- Write clear commit messages
- Include tests for new features
- Update documentation
- Keep PRs focused and small

Questions?
----------

Open an issue on GitHub if you have questions or need help.
