"""Internal HTTP client wrapper for Zid API.

This module provides an HTTP abstraction layer using httpx that handles
authentication, headers, error mapping, automatic token refresh, and
retry logic with exponential backoff.
"""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

import httpx

from zid.exceptions import (
    TokenRefreshError,
    ZidAPIError,
    ZidAuthenticationError,
    ZidAuthorizationError,
    ZidConnectionError,
    ZidNotFoundError,
    ZidRateLimitError,
    ZidServerError,
    ZidValidationError,
)

if TYPE_CHECKING:
    from zid.auth import Auth

logger = logging.getLogger("zid")

DEFAULT_BASE_URL = "https://api.zid.sa"
DEFAULT_TIMEOUT = 30.0

__all__ = ["HTTPClient", "RetryConfig", "DEFAULT_BASE_URL", "DEFAULT_TIMEOUT"]


@dataclass(frozen=True)
class RetryConfig:
    """Configuration for retry behavior.

    Attributes:
        max_retries: Maximum number of retry attempts (0 = no retries).
        base_delay: Initial delay in seconds before first retry.
        max_delay: Maximum delay in seconds between retries.
        exponential_base: Base for exponential backoff calculation.
        jitter: Whether to add random jitter to delays.
        retry_on_status: HTTP status codes that trigger a retry.
        retry_on_rate_limit: Whether to auto-wait and retry on 429.
        max_rate_limit_wait: Maximum seconds to wait for rate limit (0 = no limit).
    """

    max_retries: int = 3
    base_delay: float = 0.5
    max_delay: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True
    retry_on_status: frozenset[int] = field(
        default_factory=lambda: frozenset({500, 502, 503, 504})
    )
    retry_on_rate_limit: bool = True
    max_rate_limit_wait: float = 120.0

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for a given retry attempt using exponential backoff.

        Args:
            attempt: The retry attempt number (0-indexed).

        Returns:
            Delay in seconds, capped at max_delay.
        """
        delay = self.base_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)

        if self.jitter:
            # Add jitter: random value between 0 and delay
            delay = delay * (0.5 + random.random() * 0.5)

        return delay


class HTTPClient:
    """Internal HTTP client for Zid API requests.

    Handles authentication headers, error mapping, automatic token refresh,
    and retry logic with exponential backoff.

    Example:
        ```python
        # Default retry behavior (3 retries with exponential backoff)
        client = HTTPClient(auth=auth)

        # Custom retry configuration
        client = HTTPClient(
            auth=auth,
            retry=RetryConfig(
                max_retries=5,
                base_delay=1.0,
                retry_on_rate_limit=True,
            ),
        )

        # Disable retries
        client = HTTPClient(auth=auth, retry=RetryConfig(max_retries=0))
        ```
    """

    def __init__(
        self,
        *,
        auth: Auth,
        language: str = "en",
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        auto_refresh: bool = True,
        retry: RetryConfig | None = None,
        log_requests: bool = False,
        request_hook: Callable[[httpx.Request], None] | None = None,
        response_hook: Callable[[httpx.Response], None] | None = None,
    ) -> None:
        """Initialize the HTTP client.

        Args:
            auth: Authentication credentials (mutable, updated on refresh).
            language: Accept-Language header value.
            base_url: API base URL.
            timeout: Request timeout in seconds.
            auto_refresh: Automatically refresh tokens on 401.
            retry: Retry configuration. Defaults to RetryConfig() if None.
            log_requests: Enable request/response logging.
            request_hook: Callback invoked before each request.
            response_hook: Callback invoked after each response.
        """
        self._auth = auth
        self._language = language
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._auto_refresh = auto_refresh
        self._retry = retry if retry is not None else RetryConfig()
        self._log_requests = log_requests
        self._request_hook = request_hook
        self._response_hook = response_hook

        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=self._timeout,
        )

    def _build_headers(self, token_header: str = "X-Manager-Token") -> dict[str, str]:
        """Build request headers with current auth credentials."""
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self._auth.authorization}",
            "Accept-Language": self._language,
        }

        if self._auth.store_token:
            headers[token_header] = self._auth.store_token

        if self._auth.store_id is not None:
            headers["Store-Id"] = str(self._auth.store_id)

        if self._auth.role:
            headers["Role"] = self._auth.role

        return headers

    def _log_request(self, request: httpx.Request) -> None:
        if self._log_requests:
            logger.debug("Request: %s %s", request.method, request.url)

    def _log_response(self, response: httpx.Response) -> None:
        if self._log_requests:
            logger.debug("Response: %s %s", response.status_code, response.url)

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Map HTTP errors to SDK exceptions."""
        if response.is_success:
            return

        status_code = response.status_code
        request_id = response.headers.get("X-Request-Id")

        try:
            body = response.json()
        except Exception:
            body = {"message": response.text or "Unknown error"}

        message = self._extract_error_message(body)
        error_code = body.get("error_code") or body.get("code")

        if status_code == 401:
            raise ZidAuthenticationError(
                message=message,
                request_id=request_id,
                body=body,
                error_code=error_code,
            )

        if status_code == 403:
            raise ZidAuthorizationError(
                message=message,
                request_id=request_id,
                body=body,
                error_code=error_code,
            )

        if status_code == 404:
            raise ZidNotFoundError(
                message=message,
                request_id=request_id,
                body=body,
                error_code=error_code,
            )

        if status_code in (400, 422):
            errors = self._extract_validation_errors(body)
            detail = body.get("detail") if isinstance(body.get("detail"), list) else None
            raise ZidValidationError(
                message=message,
                status_code=status_code,
                request_id=request_id,
                body=body,
                errors=errors,
                detail=detail,
            )

        if status_code == 429:
            retry_after = None
            if "Retry-After" in response.headers:
                try:
                    retry_after = int(response.headers["Retry-After"])
                except ValueError:
                    pass
            raise ZidRateLimitError(
                message=message,
                request_id=request_id,
                body=body,
                retry_after=retry_after,
            )

        if status_code >= 500:
            raise ZidServerError(
                message=message,
                status_code=status_code,
                request_id=request_id,
                body=body,
                error_code=error_code,
            )

        raise ZidAPIError(
            message=message,
            status_code=status_code,
            request_id=request_id,
            body=body,
            error_code=error_code,
        )

    def _extract_error_message(self, body: dict[str, Any]) -> str:
        if "message" in body:
            msg = body["message"]
            return msg if isinstance(msg, str) else str(msg)
        if "error" in body:
            err = body["error"]
            return err if isinstance(err, str) else str(err)
        if "detail" in body:
            detail = body["detail"]
            if isinstance(detail, str):
                return detail
            if isinstance(detail, list) and detail:
                return str(detail[0].get("msg", "Validation error"))
        return "API error"

    def _extract_validation_errors(self, body: dict[str, Any]) -> dict[str, list[str]]:
        errors: dict[str, list[str]] = {}
        for key, value in body.items():
            if key in ("message", "error", "error_code", "code", "detail", "status"):
                continue
            if isinstance(value, list) and all(isinstance(v, str) for v in value):
                errors[key] = value
        return errors

    def _execute(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token_header: str = "X-Manager-Token",
    ) -> httpx.Response:
        """Execute a single HTTP request."""
        request_headers = self._build_headers(token_header=token_header)
        if headers:
            request_headers.update(headers)

        request = self._client.build_request(
            method=method,
            url=path,
            params=params,
            json=json,
            data=data,
            headers=request_headers,
        )

        self._log_request(request)
        if self._request_hook:
            self._request_hook(request)

        response = self._client.send(request)

        self._log_response(response)
        if self._response_hook:
            self._response_hook(response)

        return response

    def _should_retry(self, response: httpx.Response) -> bool:
        """Determine if a response should trigger a retry."""
        return response.status_code in self._retry.retry_on_status

    def _handle_rate_limit(self, response: httpx.Response) -> float | None:
        """Handle rate limit response and return wait time if should retry.

        Returns:
            Wait time in seconds, or None if should not retry.
        """
        if response.status_code != 429:
            return None

        if not self._retry.retry_on_rate_limit:
            return None

        # Parse Retry-After header
        retry_after = 60.0  # Default wait time
        if "Retry-After" in response.headers:
            try:
                retry_after = float(response.headers["Retry-After"])
            except ValueError:
                pass

        # Check if wait time exceeds maximum
        if self._retry.max_rate_limit_wait > 0 and retry_after > self._retry.max_rate_limit_wait:
            logger.warning(
                "Rate limit retry-after (%ss) exceeds max wait (%ss), not retrying",
                retry_after,
                self._retry.max_rate_limit_wait,
            )
            return None

        return retry_after

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token_header: str = "X-Manager-Token",
    ) -> Any:
        """Make an HTTP request with automatic retry and token refresh.

        Implements:
        - Exponential backoff with jitter for transient errors (5xx)
        - Automatic wait and retry on rate limits (429)
        - Token refresh on authentication errors (401)

        Args:
            method: HTTP method.
            path: API endpoint path.
            params: Query parameters.
            json: JSON request body.
            data: Form-encoded request body.
            headers: Additional headers.
            token_header: Header name for store token.

        Returns:
            Parsed JSON response.

        Raises:
            ZidAPIError: On API errors after all retries exhausted.
            ZidConnectionError: On network failures after all retries exhausted.
        """
        last_exception: Exception | None = None
        attempt = 0
        max_attempts = self._retry.max_retries + 1  # +1 for initial attempt

        while attempt < max_attempts:
            try:
                response = self._execute(
                    method, path,
                    params=params, json=json, data=data,
                    headers=headers, token_header=token_header,
                )

                # Handle 401 with auto-refresh (not a retry, just token refresh)
                if response.status_code == 401 and self._auto_refresh and self._auth.can_refresh:
                    logger.info("Got 401, attempting token refresh")
                    try:
                        self._auth.refresh()
                        response = self._execute(
                            method, path,
                            params=params, json=json, data=data,
                            headers=headers, token_header=token_header,
                        )
                    except TokenRefreshError:
                        logger.warning("Token refresh failed, raising original 401")

                # Handle rate limiting
                rate_limit_wait = self._handle_rate_limit(response)
                if rate_limit_wait is not None:
                    logger.info(
                        "Rate limited, waiting %.1fs before retry (attempt %d/%d)",
                        rate_limit_wait,
                        attempt + 1,
                        max_attempts,
                    )
                    time.sleep(rate_limit_wait)
                    attempt += 1
                    continue

                # Handle retryable server errors
                if self._should_retry(response) and attempt < max_attempts - 1:
                    delay = self._retry.calculate_delay(attempt)
                    logger.info(
                        "Server error %d, retrying in %.2fs (attempt %d/%d)",
                        response.status_code,
                        delay,
                        attempt + 1,
                        max_attempts,
                    )
                    time.sleep(delay)
                    attempt += 1
                    continue

                # Success or non-retryable error
                self._raise_for_status(response)

                if response.status_code == 204:
                    return None

                return response.json()

            except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError) as e:
                last_exception = e

                if attempt < max_attempts - 1:
                    delay = self._retry.calculate_delay(attempt)
                    logger.info(
                        "Connection error: %s, retrying in %.2fs (attempt %d/%d)",
                        type(e).__name__,
                        delay,
                        attempt + 1,
                        max_attempts,
                    )
                    time.sleep(delay)
                    attempt += 1
                    continue

                # All retries exhausted
                if isinstance(e, httpx.ConnectError):
                    raise ZidConnectionError(
                        message="Failed to connect to Zid API",
                        original_error=e,
                    ) from e
                elif isinstance(e, httpx.TimeoutException):
                    raise ZidConnectionError(
                        message="Request to Zid API timed out",
                        original_error=e,
                    ) from e
                else:
                    raise ZidConnectionError(
                        message="Network error occurred",
                        original_error=e,
                    ) from e

        # Should not reach here, but handle edge case
        if last_exception:
            raise ZidConnectionError(
                message="Request failed after all retries",
                original_error=last_exception,
            ) from last_exception

        raise ZidAPIError(
            message="Request failed after all retries",
            status_code=0,
        )

    def get(self, path: str, **kwargs: Any) -> Any:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Any:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Any:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Any:
        return self.request("DELETE", path, **kwargs)
    def upload(
        self,
        path: str,
        *,
        files: dict[str, tuple[str, bytes, str]],
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token_header: str = "X-Manager-Token",
    ) -> Any:
        """Upload files using multipart form data.

        Args:
            path: API endpoint path.
            files: Dictionary of files to upload. Each value is a tuple of
                (filename, file_content, content_type).
            data: Additional form data fields.
            headers: Additional headers.
            token_header: Header name for store token.

        Returns:
            Parsed JSON response.

        Example:
            ```python
            response = client.upload(
                "/v1/upload",
                files={"receipt": ("receipt.png", image_bytes, "image/png")},
                data={"refund_id": "uuid-here"},
            )
            ```
        """
        request_headers = self._build_headers(token_header=token_header)
        if headers:
            request_headers.update(headers)

        # Build multipart files dict for httpx
        httpx_files = {
            name: (filename, content, content_type)
            for name, (filename, content, content_type) in files.items()
        }

        request = self._client.build_request(
            method="POST",
            url=path,
            files=httpx_files,
            data=data,
            headers=request_headers,
        )

        self._log_request(request)
        if self._request_hook:
            self._request_hook(request)

        response = self._client.send(request)

        self._log_response(response)
        if self._response_hook:
            self._response_hook(response)

        self._raise_for_status(response)

        if response.status_code == 204:
            return None

        return response.json()



    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> HTTPClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
