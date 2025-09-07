"""
Main WhatsApp client for interacting with the WhatsApp Business API.
"""

import hashlib
import hmac
import logging
from typing import Any, Dict, Optional, Union

from whatsapp_sdk.config import Config
from whatsapp_sdk.exceptions import ValidationError, WebhookError
from whatsapp_sdk.http_client import HTTPClient

logger = logging.getLogger(__name__)


class WhatsAppClient:
    """Main client for WhatsApp Business API."""

    def __init__(
        self,
        phone_number_id: str,
        access_token: str,
        app_secret: str,
        webhook_verify_token: str,
        api_version: str = "v23.0",
        base_url: str = "https://graph.facebook.com",
        config: Optional[Config] = None,
    ) -> None:
        """
        Initialize WhatsApp client.

        Args:
            phone_number_id: WhatsApp Business phone number ID (required)
            access_token: Facebook Graph API access token (required)
            app_secret: App secret for webhook signature validation (required)
            webhook_verify_token: Token for webhook verification (required)
            api_version: WhatsApp API version (default: v23.0)
            base_url: Base URL for API (default: https://graph.facebook.com)
            config: Config object with connection settings (timeout, retries, etc.)
        """
        # Store main parameters
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = base_url
        self.app_secret = app_secret
        self.webhook_verify_token = webhook_verify_token
        
        # Use provided config or create default
        self.config = config or Config()

        # Set up logging
        if self.config.debug:
            logging.basicConfig(level=logging.DEBUG)
            logger.setLevel(logging.DEBUG)

        # Initialize HTTP client
        self.http = HTTPClient(
            base_url=self.base_url,
            access_token=self.access_token,
            api_version=self.api_version,
            timeout=self.config.timeout,
            max_retries=self.config.max_retries,
            verify_ssl=self.config.verify_ssl,
            pool_size=self.config.pool_size,
            rate_limit=self.config.rate_limit,
        )

        # Initialize service modules (will be added later)
        # self.messages = MessageService(self)
        # self.templates = TemplateService(self)
        # self.media = MediaService(self)
        # self.webhooks = WebhookService(self)

    @classmethod
    def from_env(cls) -> "WhatsAppClient":
        """Create client from environment variables."""
        import os
        
        phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        app_secret = os.getenv("WHATSAPP_APP_SECRET")
        webhook_verify_token = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN")
        
        if not phone_number_id:
            raise ValueError("WHATSAPP_PHONE_NUMBER_ID environment variable is required")
        if not access_token:
            raise ValueError("WHATSAPP_ACCESS_TOKEN environment variable is required")
        if not app_secret:
            raise ValueError("WHATSAPP_APP_SECRET environment variable is required")
        if not webhook_verify_token:
            raise ValueError("WHATSAPP_WEBHOOK_VERIFY_TOKEN environment variable is required")
        
        return cls(
            phone_number_id=phone_number_id,
            access_token=access_token,
            app_secret=app_secret,
            webhook_verify_token=webhook_verify_token,
            api_version=os.getenv("WHATSAPP_API_VERSION", "v23.0"),
            base_url=os.getenv("WHATSAPP_BASE_URL", "https://graph.facebook.com"),
            config=Config.from_env()
        )

    @property
    def api_url(self) -> str:
        """Get the API URL for this client."""
        return f"{self.api_version}/{self.phone_number_id}"

    def validate_webhook_signature(
        self,
        signature: str,
        payload: bytes,
    ) -> bool:
        """
        Validate webhook signature.

        Args:
            signature: X-Hub-Signature-256 header value
            payload: Raw request body

        Returns:
            True if signature is valid

        Raises:
            WebhookError: If app_secret is not configured
        """
        if not self.app_secret:
            raise WebhookError("app_secret is required for webhook signature validation")

        # Remove 'sha256=' prefix if present
        if signature.startswith("sha256="):
            signature = signature[7:]

        # Calculate expected signature
        expected = hmac.new(
            self.app_secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()

        # Compare signatures
        return hmac.compare_digest(expected, signature)

    def verify_webhook_token(self, token: str) -> bool:
        """
        Verify webhook verification token.

        Args:
            token: Token from webhook verification request

        Returns:
            True if token matches configured token
        """
        if not self.webhook_verify_token:
            logger.warning("webhook_verify_token not configured")
            return False

        return token == self.webhook_verify_token

    async def send_text(
        self,
        to: str,
        body: str,
        preview_url: bool = False,
        messaging_product: str = "whatsapp",
    ) -> Dict[str, Any]:
        """
        Send a text message.

        Args:
            to: Recipient phone number
            body: Message text
            preview_url: Enable URL preview
            messaging_product: Messaging product (always 'whatsapp')

        Returns:
            API response

        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        # Validate phone number
        to = self._validate_phone_number(to)

        # Validate message body
        if not body or not body.strip():
            raise ValidationError("Message body cannot be empty")

        if len(body) > 4096:
            raise ValidationError("Message body cannot exceed 4096 characters")

        # Prepare request payload
        payload = {
            "messaging_product": messaging_product,
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "preview_url": preview_url,
                "body": body,
            },
        }

        # Send request
        endpoint = f"{self.api_url}/messages"
        response = await self.http.post(endpoint, json=payload)

        if self.config.debug:
            logger.debug(f"Sent text message to {to}: {response}")

        return response

    async def send_image(
        self,
        to: str,
        image: Union[str, bytes],
        caption: Optional[str] = None,
        messaging_product: str = "whatsapp",
    ) -> Dict[str, Any]:
        """
        Send an image message.

        Args:
            to: Recipient phone number
            image: Image URL or media ID
            caption: Optional caption
            messaging_product: Messaging product

        Returns:
            API response
        """
        # Validate phone number
        to = self._validate_phone_number(to)

        # Validate caption
        if caption and len(caption) > 1024:
            raise ValidationError("Caption cannot exceed 1024 characters")

        # Prepare image data
        image_data: Dict[str, Any] = {}
        if isinstance(image, str):
            if image.startswith("http"):
                image_data["link"] = image
            else:
                image_data["id"] = image
        else:
            # TODO: Upload image and get media ID
            raise NotImplementedError("Image upload not yet implemented")

        if caption:
            image_data["caption"] = caption

        # Prepare request payload
        payload = {
            "messaging_product": messaging_product,
            "recipient_type": "individual",
            "to": to,
            "type": "image",
            "image": image_data,
        }

        # Send request
        endpoint = f"{self.api_url}/messages"
        response = await self.http.post(endpoint, json=payload)

        if self.config.debug:
            logger.debug(f"Sent image message to {to}: {response}")

        return response

    async def mark_as_read(self, message_id: str) -> Dict[str, Any]:
        """
        Mark a message as read.

        Args:
            message_id: Message ID to mark as read

        Returns:
            API response
        """
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }

        endpoint = f"{self.api_url}/messages"
        response = await self.http.post(endpoint, json=payload)

        if self.config.debug:
            logger.debug(f"Marked message {message_id} as read: {response}")

        return response

    def _validate_phone_number(self, phone: str) -> str:
        """
        Validate and format phone number.

        Args:
            phone: Phone number to validate

        Returns:
            Formatted phone number

        Raises:
            ValidationError: If phone number is invalid
        """
        # Remove all non-digits
        digits = "".join(filter(str.isdigit, phone))

        # Validate length (7-15 digits for international numbers)
        if len(digits) < 7 or len(digits) > 15:
            raise ValidationError(f"Invalid phone number: {phone}")

        return digits

    async def close(self) -> None:
        """Close the client and cleanup resources."""
        await self.http.close()

    async def __aenter__(self) -> "WhatsAppClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()
