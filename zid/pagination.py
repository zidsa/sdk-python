"""Pagination abstractions for Zid API responses.

This module provides iterators that transparently handle pagination,
yielding items across pages with lazy loading.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, Iterator, TypeVar

if TYPE_CHECKING:
    from zid.http import HTTPClient

ModelT = TypeVar("ModelT")

__all__ = ["PaginatedIterator"]


class PaginatedIterator(Generic[ModelT]):
    """Iterator that transparently handles pagination across API responses.

    Supports both cursor-based pagination (next/previous URLs) and
    offset/limit pagination (page/page_size). Items are lazily loaded
    as iteration progresses.

    Type Parameters:
        ModelT: The type of items yielded by the iterator.
    """

    def __init__(
        self,
        client: HTTPClient,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        model_factory: Callable[[dict[str, Any]], ModelT],
        results_key: str = "results",
        token_header: str = "X-Manager-Token",
    ) -> None:
        """Initialize the paginated iterator.

        Args:
            client: HTTP client for making requests.
            path: API endpoint path.
            params: Initial query parameters.
            model_factory: Callable to convert raw dict to model instance.
            results_key: Key in response containing the items array.
            token_header: Header name for store token.
        """
        self._client = client
        self._path = path
        self._params = params or {}
        self._model_factory = model_factory
        self._results_key = results_key
        self._token_header = token_header

        self._items: list[ModelT] = []
        self._index = 0
        self._total_count: int | None = None
        self._next_url: str | None = None
        self._next_page: int | None = None
        self._last_page: int | None = None
        self._current_page: int = 0
        self._exhausted = False
        self._first_fetch_done = False

    def _fetch_page(self) -> None:
        """Fetch the next page of results."""
        if self._exhausted:
            return

        if not self._first_fetch_done:
            response = self._client.get(
                self._path,
                params=self._params,
                token_header=self._token_header,
            )
            self._first_fetch_done = True
        elif self._next_url:
            response = self._client.get(
                self._next_url,
                token_header=self._token_header,
            )
        elif self._next_page is not None and self._last_page is not None:
            if self._current_page >= self._last_page:
                self._exhausted = True
                return
            params = {**self._params, "page": self._next_page}
            response = self._client.get(
                self._path,
                params=params,
                token_header=self._token_header,
            )
        else:
            self._exhausted = True
            return

        self._parse_response(response)

    def _parse_response(self, response: dict[str, Any]) -> None:
        """Parse pagination response and extract items."""
        items_data = response.get(self._results_key, [])
        self._items.extend(self._model_factory(item) for item in items_data)

        if "count" in response:
            self._total_count = response["count"]

        if "next" in response:
            self._next_url = response.get("next")
            if self._next_url is None:
                self._exhausted = True
        elif "pagination" in response:
            pagination = response["pagination"]
            self._current_page = pagination.get("page", 1)
            self._next_page = pagination.get("next_page")
            self._last_page = pagination.get("last_page")
            self._total_count = pagination.get("count")
            if self._next_page is None or self._current_page >= self._last_page:
                self._exhausted = True
        elif "next_page" in response:
            self._current_page = response.get("page", 1)
            self._next_page = response.get("next_page")
            self._last_page = response.get("last_page")
            self._total_count = response.get("count")
            if self._next_page is None or self._current_page >= self._last_page:
                self._exhausted = True
        else:
            self._exhausted = True

    @property
    def total_count(self) -> int | None:
        """Total number of items across all pages.

        Returns None if the API doesn't provide a count, or if no
        request has been made yet. Access this property to trigger
        the first fetch if needed.
        """
        if not self._first_fetch_done:
            self._fetch_page()
        return self._total_count

    def __iter__(self) -> Iterator[ModelT]:
        """Return the iterator."""
        return self

    def __next__(self) -> ModelT:
        """Return the next item, fetching more pages as needed."""
        while self._index >= len(self._items):
            if self._exhausted:
                raise StopIteration
            self._fetch_page()
            if self._index >= len(self._items) and self._exhausted:
                raise StopIteration

        item = self._items[self._index]
        self._index += 1
        return item

    def __len__(self) -> int:
        """Return total count if available, otherwise count fetched items.

        Note: This may trigger a fetch if no request has been made yet.
        """
        if self._total_count is not None:
            return self._total_count
        if not self._first_fetch_done:
            self._fetch_page()
        if self._total_count is not None:
            return self._total_count
        return len(self._items)
