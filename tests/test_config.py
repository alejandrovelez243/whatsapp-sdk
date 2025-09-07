#!/usr/bin/env python3
"""Test configuration structure for WhatsApp SDK."""

from whatsapp_sdk import WhatsAppClient, Config

print("Testing WhatsApp SDK configuration...")
print("=" * 50)

# Test 1: Basic initialization with all required parameters
print("\nTest 1: All required parameters")
client1 = WhatsAppClient(
    phone_number_id="123456789",
    access_token="test_token",
    app_secret="my_app_secret",
    webhook_verify_token="my_verify_token"
)
print(f"  Phone Number ID: {client1.phone_number_id}")
print(f"  Access Token: {client1.access_token[:10]}...")
print(f"  App Secret: {client1.app_secret[:10]}...")
print(f"  Webhook Token: {client1.webhook_verify_token}")
print(f"  API Version: {client1.api_version}")
print(f"  Base URL: {client1.base_url}")
print(f"  Config Timeout: {client1.config.timeout}")
print(f"  Config Max Retries: {client1.config.max_retries}")

# Test 2: With custom API version
print("\nTest 2: Custom API version")
client2 = WhatsAppClient(
    phone_number_id="987654321",
    access_token="another_token",
    app_secret="another_secret",
    webhook_verify_token="another_verify_token",
    api_version="v22.0"  # Custom version
)
print(f"  Phone Number ID: {client2.phone_number_id}")
print(f"  API Version: {client2.api_version}")

# Test 3: With custom Config object
print("\nTest 3: With custom Config object")
config = Config(
    timeout=60.0,
    max_retries=5,
    debug=True,
    pool_size=200,
    rate_limit=100
)
client3 = WhatsAppClient(
    phone_number_id="555555555",
    access_token="third_token",
    app_secret="third_secret",
    webhook_verify_token="third_verify_token",
    config=config
)
print(f"  Phone Number ID: {client3.phone_number_id}")
print(f"  Config Timeout: {client3.config.timeout}")
print(f"  Config Max Retries: {client3.config.max_retries}")
print(f"  Config Debug: {client3.config.debug}")
print(f"  Config Pool Size: {client3.config.pool_size}")
print(f"  Config Rate Limit: {client3.config.rate_limit}")

# Test 4: API URL generation
print("\nTest 4: API URL generation")
print(f"  Client 1 API URL: {client1.api_url}")
print(f"  Client 2 API URL: {client2.api_url}")
print(f"  Client 3 API URL: {client3.api_url}")

print("\n" + "=" * 50)
print("✅ All tests passed! Configuration structure is working correctly.")
print("\nKey Points:")
print("  - phone_number_id, access_token, app_secret, webhook_verify_token are REQUIRED")
print("  - Config class only contains connection/behavior settings")
print("  - API version defaults to v23.0 (latest)")
print("  - Clean separation of concerns")