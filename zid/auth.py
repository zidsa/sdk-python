"""Authentication handler for Zid API.

This module manages OAuth tokens and automatic token refresh.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

import httpx

from zid.exceptions import AuthError, TokenRefreshError

if TYPE_CHECKING:
    pass

logger = logging.getLogger("zid.auth")

OAUTH_BASE_URL = "https://oauth.zid.sa"
TOKEN_ENDPOINT = "/oauth/token"

__all__ = ["Auth", "TokenResponse"]


@dataclass
class TokenResponse:
    """Response from OAuth token endpoint."""

    access_token: str
    authorization: str
    refresh_token: str
    expires_in: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TokenResponse:
        """Parse token response from OAuth server."""
        return cls(
            access_token=data["access_token"],
            authorization=data["Authorization"],
            refresh_token=data["refresh_token"],
            expires_in=data.get("expires_in", 31536000),
        )


@dataclass
class Auth:
    """Authentication credentials for Zid API.

    Supports automatic token refresh when configured with OAuth credentials.

    Args:
        authorization: Partner authorization token (required).
        store_token: Store-level access token.
        store_id: Store identifier.
        role: User role (default: "Manager").
        refresh_token: OAuth refresh token for automatic renewal.
        client_id: OAuth client ID (required for auto-refresh).
        client_secret: OAuth client secret (required for auto-refresh).
        redirect_uri: OAuth redirect URI (required for auto-refresh).
        on_tokens_refreshed: Callback when tokens are refreshed.
            Use this to persist new tokens to your database.
            Signature: (auth: Auth) -> None
    """

    authorization: str
    store_token: str | None = None
    store_id: int | str | None = None
    role: str = "Manager"

    # OAuth refresh credentials
    refresh_token: str | None = None
    client_id: str | None = None
    client_secret: str | None = None
    redirect_uri: str | None = None

    # Callback for token persistence
    on_tokens_refreshed: Callable[[Auth], None] | None = field(
        default=None, repr=False
    )

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """Validate required credentials."""
        if not self.authorization or not self.authorization.strip():
            raise AuthError("authorization token is required")

    @property
    def can_refresh(self) -> bool:
        """Check if automatic token refresh is configured."""
        return all([
            self.refresh_token,
            self.client_id,
            self.client_secret,
            self.redirect_uri,
        ])

    def refresh(self) -> bool:
        """Refresh OAuth tokens.

        Calls the Zid OAuth server to get new tokens and updates this instance.

        Returns:
            True if refresh succeeded.

        Raises:
            TokenRefreshError: If refresh fails or is not configured.
        """
        if not self.can_refresh:
            raise TokenRefreshError("Token refresh not configured. Provide refresh_token, client_id, client_secret, and redirect_uri.")

        try:
            response = httpx.post(
                f"{OAUTH_BASE_URL}{TOKEN_ENDPOINT}",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            tokens = TokenResponse.from_dict(response.json())

        except httpx.HTTPStatusError as e:
            logger.warning("Token refresh failed: %s", e.response.text)
            raise TokenRefreshError(f"OAuth server returned {e.response.status_code}") from e
        except httpx.RequestError as e:
            logger.warning("Token refresh network error: %s", e)
            raise TokenRefreshError("Failed to connect to OAuth server") from e
        except (KeyError, TypeError) as e:
            logger.warning("Invalid token response: %s", e)
            raise TokenRefreshError("Invalid response from OAuth server") from e

        # Update credentials
        self.authorization = tokens.authorization
        self.store_token = tokens.access_token
        self.refresh_token = tokens.refresh_token

        logger.info("Tokens refreshed successfully")

        # Notify callback for persistence
        if self.on_tokens_refreshed:
            self.on_tokens_refreshed(self)

        return True
