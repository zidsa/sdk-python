"""Base resource class for Zid API resources.

This module provides the abstract base class that all resource classes inherit from.
"""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from zid.pagination import PaginatedIterator

if TYPE_CHECKING:
    from zid.http import HTTPClient

ModelT = TypeVar("ModelT")

__all__ = ["BaseResource"]


class BaseResource(ABC):
    """Abstract base class for all Zid API resources.

    Provides common functionality for CRUD operations, path building,
    and pagination integration.

    Attributes:
        token_header: Header name for the store token. Override to "Access-Token"
            for product-related endpoints. Default is "X-Manager-Token".
    """

    token_header: str = "X-Manager-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the resource.

        Args:
            client: HTTP client for making API requests.
        """
        self._client = client

    def _build_path(self, *parts: str | int) -> str:
        """Build an API path from parts.

        Args:
            *parts: Path segments to join.

        Returns:
            Joined path string with leading slash.
        """
        segments = [str(p) for p in parts if p is not None]
        return "/" + "/".join(segments)

    def _list(
        self,
        path: str,
        model_factory: Callable[[dict[str, Any]], ModelT],
        *,
        params: dict[str, Any] | None = None,
        results_key: str = "results",
    ) -> PaginatedIterator[ModelT]:
        """Create a paginated iterator for list operations.

        Args:
            path: API endpoint path.
            model_factory: Callable to convert raw dict to model instance.
            params: Query parameters.
            results_key: Key in response containing the items array.

        Returns:
            Paginated iterator yielding model instances.
        """
        return PaginatedIterator(
            client=self._client,
            path=path,
            params=params,
            model_factory=model_factory,
            results_key=results_key,
            token_header=self.token_header,
        )

    def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a GET request.

        Args:
            path: API endpoint path.
            params: Query parameters.

        Returns:
            Response data as dict.
        """
        return self._client.get(
            path,
            params=params,
            token_header=self.token_header,
        )

    def _create(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a POST request for creation.

        Args:
            path: API endpoint path.
            json: JSON request body.
            data: Form-encoded request body.
            params: Query parameters.

        Returns:
            Response data as dict.
        """
        return self._client.post(
            path,
            json=json,
            data=data,
            params=params,
            token_header=self.token_header,
        )

    def _update(
        self,
        path: str,
        *,
        json: dict[str, Any] | list[Any] | None = None,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        method: str = "PUT",
    ) -> dict[str, Any]:
        """Make a PUT or PATCH request for updates.

        Args:
            path: API endpoint path.
            json: JSON request body (dict or list).
            data: Form-encoded request body.
            params: Query parameters.
            method: HTTP method ("PUT" or "PATCH").

        Returns:
            Response data as dict.
        """
        if method == "PATCH":
            return self._client.patch(
                path,
                json=json,
                data=data,
                params=params,
                token_header=self.token_header,
            )
        return self._client.put(
            path,
            json=json,
            data=data,
            params=params,
            token_header=self.token_header,
        )

    def _delete(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make a DELETE request.

        Args:
            path: API endpoint path.
            params: Query parameters.

        Returns:
            Response data (may be None for 204 responses).
        """
        return self._client.delete(
            path,
            params=params,
            token_header=self.token_header,
        )
