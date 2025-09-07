"""
HTTP client for WhatsApp API requests.
"""

import asyncio
import time
from typing import Any, Dict, Optional

import httpx

from whatsapp_sdk.exceptions import APIError, AuthenticationError, NetworkError, RateLimitError


class HTTPClient:
    """Low-level HTTP client with retry logic and rate limiting."""

    def __init__(
        self,
        base_url: str,
        access_token: str,
        api_version: str = "v23.0",
        timeout: float = 30.0,
        max_retries: int = 3,
        verify_ssl: bool = True,
        pool_size: int = 100,
        rate_limit: int = 80,
    ) -> None:
        self.base_url = base_url
        self.api_version = api_version
        self.access_token = access_token
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit = rate_limit

        # Create HTTP client with connection pooling
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(timeout),
            follow_redirects=True,
            verify=verify_ssl,
            limits=httpx.Limits(
                max_keepalive_connections=pool_size,
                max_connections=pool_size * 2,
            ),
        )

        # Rate limiting
        self._rate_limiter = RateLimiter(rate_limit)

    async def request(
        self,
        method: str,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make an API request with retry logic."""
        # Apply rate limiting
        await self._rate_limiter.acquire()

        # Prepare request headers
        request_headers = {}
        if headers:
            request_headers.update(headers)

        # Retry logic
        last_exception: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                response = await self.client.request(
                    method=method,
                    url=endpoint,
                    json=json,
                    files=files,
                    params=params,
                    headers=request_headers,
                )

                # Check for rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    raise RateLimitError(retry_after=retry_after)

                # Check for authentication errors
                if response.status_code in (401, 403):
                    error_data = response.json()
                    raise AuthenticationError(
                        message=error_data.get("error", {}).get(
                            "message", "Authentication failed"
                        ),
                        code=str(response.status_code),
                    )

                # Check for other errors
                response.raise_for_status()

                # Parse JSON response
                return response.json()

            except httpx.HTTPStatusError as e:
                # API error
                if e.response.status_code >= 400:
                    try:
                        error_data = e.response.json()
                        raise APIError.from_response(error_data) from e
                    except Exception:
                        raise APIError(
                            message=str(e),
                            status_code=e.response.status_code,
                        ) from e

                # Server error - retry
                if e.response.status_code >= 500:
                    last_exception = e
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(2**attempt)
                        continue
                    raise NetworkError(f"Server error after {self.max_retries} retries: {e}") from e

            except httpx.RequestError as e:
                # Network error - retry
                last_exception = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                raise NetworkError(f"Network error after {self.max_retries} retries: {e}") from e

            except RateLimitError:
                # Don't retry rate limit errors
                raise

            except Exception as e:
                # Unexpected error
                raise NetworkError(f"Unexpected error: {e}") from e

        # All retries exhausted
        if last_exception:
            raise NetworkError(
                f"Request failed after {self.max_retries} retries: {last_exception}"
            )

        raise NetworkError("Request failed for unknown reason")

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a GET request."""
        return await self.request("GET", endpoint, params=params, headers=headers)

    async def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a POST request."""
        return await self.request("POST", endpoint, json=json, files=files, headers=headers)

    async def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a PUT request."""
        return await self.request("PUT", endpoint, json=json, headers=headers)

    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a DELETE request."""
        return await self.request("DELETE", endpoint, headers=headers)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()

    async def __aenter__(self) -> "HTTPClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()


class RateLimiter:
    """Rate limiter for API requests."""

    def __init__(self, calls_per_second: int = 80) -> None:
        self.calls_per_second = calls_per_second
        self.semaphore = asyncio.Semaphore(calls_per_second)
        self.reset_time = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire a rate limit permit."""
        async with self.lock:
            current = time.time()
            if current - self.reset_time >= 1:
                # Reset the semaphore every second
                self.reset_time = current
                self.semaphore = asyncio.Semaphore(self.calls_per_second)

        async with self.semaphore:
            # Hold the permit for a fraction of a second
            await asyncio.sleep(1.0 / self.calls_per_second)
