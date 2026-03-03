"""Zid SDK exception hierarchy.

This module defines domain-specific exceptions that abstract HTTP errors
into meaningful, actionable exceptions for SDK consumers.
"""

from typing import Any

__all__ = [
    "ZidError",
    "AuthError",
    "TokenRefreshError",
    "ZidAPIError",
    "ZidAuthenticationError",
    "ZidAuthorizationError",
    "ZidNotFoundError",
    "ZidValidationError",
    "ZidRateLimitError",
    "ZidServerError",
    "ZidConnectionError",
]


class ZidError(Exception):
    """Base exception for all Zid SDK errors."""

    def __init__(self, message: str = "An error occurred") -> None:
        self.message = message
        super().__init__(self.message)


class AuthError(ZidError):
    """Raised when authentication configuration is invalid."""

    pass


class TokenRefreshError(ZidError):
    """Raised when token refresh fails."""

    pass


class ZidAPIError(ZidError):
    """Exception for API-level errors.

    Raised when the Zid API returns an error response.

    Attributes:
        status_code: HTTP status code from the response.
        request_id: Unique request identifier for debugging.
        body: Raw response body as dict.
        error_code: Zid-specific error code (e.g., ERROR_SESSION_INVALID).
        error_type: Error type from response (e.g., "error", "validation_errors").
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        request_id: str | None = None,
        body: dict[str, Any] | None = None,
        error_code: str | None = None,
        error_type: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.request_id = request_id
        self.body = body
        self.error_code = error_code
        self.error_type = error_type
        super().__init__(message)

    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        if self.error_code:
            parts.append(f"Code: {self.error_code}")
        if self.request_id:
            parts.append(f"Request ID: {self.request_id}")
        return " | ".join(parts)


class ZidAuthenticationError(ZidAPIError):
    """Exception for 401 Unauthorized errors.

    Raised when authentication credentials are invalid or missing.
    Common error codes: ERROR_SESSION_MISSING, ERROR_SESSION_INVALID.
    """

    def __init__(
        self,
        message: str = "Authentication failed",
        request_id: str | None = None,
        body: dict[str, Any] | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=401,
            request_id=request_id,
            body=body,
            error_code=error_code,
            error_type="error",
        )


class ZidAuthorizationError(ZidAPIError):
    """Exception for 403 Forbidden errors.

    Raised when the authenticated user lacks permission for the requested action.
    This can occur when missing required OAuth scopes or store-level permissions.
    """

    def __init__(
        self,
        message: str = "Permission denied",
        request_id: str | None = None,
        body: dict[str, Any] | None = None,
        error_code: str | None = None,
        required_scope: str | None = None,
    ) -> None:
        self.required_scope = required_scope
        super().__init__(
            message,
            status_code=403,
            request_id=request_id,
            body=body,
            error_code=error_code,
            error_type="error",
        )

    def __str__(self) -> str:
        base = super().__str__()
        if self.required_scope:
            return f"{base} | Required scope: {self.required_scope}"
        return base


class ZidNotFoundError(ZidAPIError):
    """Exception for 404 Not Found errors.

    Raised when the requested resource does not exist.
    """

    def __init__(
        self,
        message: str = "Resource not found",
        request_id: str | None = None,
        body: dict[str, Any] | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=404,
            request_id=request_id,
            body=body,
            error_code=error_code,
            error_type="error",
        )


class ZidValidationError(ZidAPIError):
    """Exception for 400/422 validation errors.

    Raised when request data fails validation. Includes field-level error details.

    Attributes:
        errors: Dict mapping field names to lists of error messages.
        detail: List of validation error details (FastAPI/Pydantic style).
    """

    def __init__(
        self,
        message: str = "Validation failed",
        status_code: int = 422,
        request_id: str | None = None,
        body: dict[str, Any] | None = None,
        errors: dict[str, list[str]] | None = None,
        detail: list[dict[str, Any]] | None = None,
    ) -> None:
        self.errors = errors or {}
        self.detail = detail or []
        super().__init__(
            message,
            status_code=status_code,
            request_id=request_id,
            body=body,
            error_code="ERROR_POPUP_OK" if errors else None,
            error_type="validation_errors",
        )

    def __str__(self) -> str:
        base = super().__str__()
        if self.errors:
            field_errors = "; ".join(
                f"{field}: {', '.join(msgs)}" for field, msgs in self.errors.items()
            )
            return f"{base} | Errors: {field_errors}"
        if self.detail:
            details = "; ".join(
                f"{'.'.join(str(loc) for loc in d.get('loc', []))}: {d.get('msg', '')}"
                for d in self.detail
            )
            return f"{base} | Details: {details}"
        return base


class ZidRateLimitError(ZidAPIError):
    """Exception for 429 Too Many Requests errors.

    Raised when the API rate limit is exceeded. Includes retry-after information.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        request_id: str | None = None,
        body: dict[str, Any] | None = None,
        retry_after: int | None = None,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(
            message,
            status_code=429,
            request_id=request_id,
            body=body,
            error_type="error",
        )

    def __str__(self) -> str:
        base = super().__str__()
        if self.retry_after is not None:
            return f"{base} | Retry after: {self.retry_after}s"
        return base


class ZidServerError(ZidAPIError):
    """Exception for 5xx server errors.

    Raised when the Zid API encounters an internal error.
    """

    def __init__(
        self,
        message: str = "Server error",
        status_code: int = 500,
        request_id: str | None = None,
        body: dict[str, Any] | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=status_code,
            request_id=request_id,
            body=body,
            error_code=error_code,
            error_type="error",
        )


class ZidConnectionError(ZidError):
    """Exception for network failures.

    Raised when unable to connect to the Zid API due to network issues.
    """

    def __init__(
        self,
        message: str = "Connection failed",
        original_error: Exception | None = None,
    ) -> None:
        self.original_error = original_error
        super().__init__(message)

    def __str__(self) -> str:
        if self.original_error:
            return f"{self.message}: {self.original_error}"
        return self.message
