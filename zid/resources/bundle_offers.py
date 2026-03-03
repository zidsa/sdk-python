"""Bundle offers resource for the Zid SDK.

This module provides the BundleOffersResource class for interacting with
the Zid Bundle Offers API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.bundle_offer import BundleOffer
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class BundleOffersResource(BaseResource):
    """Resource for listing store bundle offers.

    This is a read-only resource — the Zid API only exposes a single
    GET endpoint for bundle offers.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all bundle offers (paginated)
        for offer in client.bundle_offers.list():
            print(offer.id, offer.name)

        # Filter by status
        for offer in client.bundle_offers.list(status="active"):
            print(offer.id)
        ```
    """

    token_header: str = "X-Manager-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the bundle offers resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)
        self._base_path = "/v1/managers/store/discounts/bundle-offers"

    def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        code: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        order_by: str | None = None,
        sort_by: str | None = None,
        search_term: str | None = None,
        status: str | None = None,
        type: str | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[BundleOffer]:
        """List all bundle offers with pagination.

        Args:
            page: Page number for pagination (1-indexed).
            per_page: Number of items per page.
            code: Filter by discount rule code (e.g. ``"bundle_offer"``).
            start_date: Filter by start date (ISO format, e.g. ``"2026-01-01"``).
            end_date: Filter by end date (ISO format).
            order_by: Field to order results by (e.g. ``"start_date"``).
            sort_by: Sort direction (``"asc"`` or ``"desc"``).
            search_term: Search bundle offers by name.
            status: Filter by status (``"active"``, ``"disabled"``,
                ``"expired"``, ``"unstarted"``).
            type: Filter by bundle offer type.
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding BundleOffer instances.

        Example:
            ```python
            # List active bundle offers
            for offer in client.bundle_offers.list(status="active"):
                print(offer.id, offer.name)

            # Search by name
            for offer in client.bundle_offers.list(search_term="summer"):
                print(offer.id)
            ```
        """
        params: dict[str, Any] = {}

        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if code is not None:
            params["code"] = code
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if order_by is not None:
            params["order_by"] = order_by
        if sort_by is not None:
            params["sort_by"] = sort_by
        if search_term is not None:
            params["search_term"] = search_term
        if status is not None:
            params["status"] = status
        if type is not None:
            params["type"] = type

        params.update(kwargs)

        return self._list(
            self._base_path,
            BundleOffer.model_validate,
            params=params if params else None,
            results_key="discount_rules",
        )
