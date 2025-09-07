"""
Configuration management for WhatsApp SDK.
"""

import os
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Config(BaseModel):
    """Configuration for WhatsApp Client connection and behavior."""

    timeout: float = Field(default=30.0, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of retries")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")
    debug: bool = Field(default=False, description="Enable debug logging")
    pool_size: int = Field(default=100, description="Connection pool size")
    rate_limit: int = Field(default=80, description="Calls per second limit")

    @field_validator("timeout")
    @classmethod
    def validate_timeout(cls, v: float) -> float:
        """Validate timeout value."""
        if v <= 0:
            raise ValueError("Timeout must be positive")
        if v > 300:
            raise ValueError("Timeout cannot exceed 300 seconds")
        return v

    @field_validator("max_retries")
    @classmethod
    def validate_max_retries(cls, v: int) -> int:
        """Validate max retries."""
        if v < 0:
            raise ValueError("Max retries cannot be negative")
        if v > 10:
            raise ValueError("Max retries cannot exceed 10")
        return v

    @field_validator("rate_limit")
    @classmethod
    def validate_rate_limit(cls, v: int) -> int:
        """Validate rate limit."""
        if v <= 0:
            raise ValueError("Rate limit must be positive")
        if v > 1000:
            raise ValueError("Rate limit cannot exceed 1000 calls per second")
        return v

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        return cls(
            timeout=float(os.getenv("WHATSAPP_TIMEOUT", "30.0")),
            max_retries=int(os.getenv("WHATSAPP_MAX_RETRIES", "3")),
            verify_ssl=os.getenv("WHATSAPP_VERIFY_SSL", "true").lower() == "true",
            debug=os.getenv("WHATSAPP_DEBUG", "false").lower() == "true",
            pool_size=int(os.getenv("WHATSAPP_POOL_SIZE", "100")),
            rate_limit=int(os.getenv("WHATSAPP_RATE_LIMIT", "80")),
        )

    class Config:
        """Pydantic config."""

        str_strip_whitespace = True
        validate_assignment = True
