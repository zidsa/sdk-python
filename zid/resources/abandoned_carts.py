"""Abandoned carts resource for the Zid SDK.

This module provides the AbandonedCartsResource class for interacting with
the Zid Abandoned Carts API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from zid.models.abandoned_cart import AbandonedCart, AbandonedCartDetail
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class AbandonedCartsResource(BaseResource):
    """Resource for managing abandoned carts.

    Provides access to abandoned cart data including listing and retrieval.
    Abandoned carts are shopping carts where customers added products but
    did not complete checkout within 10 minutes of inactivity.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all abandoned carts (paginated)
        for cart in client.abandoned_carts.list():
            print(cart.customer_name, cart.cart_total_string)

        # Get a specific abandoned cart with full details
        cart = client.abandoned_carts.get("cart-uuid")
        print(cart.products)

        # Filter by phase
        for cart in client.abandoned_carts.list(phase="payment_method"):
            print(cart.customer_name, cart.phase)
        ```
    """

    # Uses default X-Manager-Token header
    token_header: str = "X-Manager-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the abandoned carts resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)
        self._base_path = "/v1/managers/store/abandoned-carts"

    def list(
        self,
        *,
        page: int | None = None,
        page_size: int | None = None,
        phase: Literal[
            "new",
            "login",
            "shipping_address",
            "shipping_method",
            "payment_method",
            "verification",
            "completed",
        ] | None = None,
        search_term: str | None = None,
        customer_id: str | int | None = None,
        products_count: int | None = None,
        has_reminders: bool | None = None,
        country_id: int | None = None,
        city_id: int | None = None,
        currency_code: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        cart_total: float | None = None,
        filter_order_by: str | None = None,
        filter_sort_by: Literal["ASC", "DESC"] | None = None,
        customer_type: Literal["individual", "business"] | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[AbandonedCart]:
        """List all abandoned carts with pagination.

        Args:
            page: Page number for pagination (1-indexed).
            page_size: Number of items per page (max 100).
            phase: Filter by checkout phase where cart was abandoned.
            search_term: Search term to filter carts.
            customer_id: Filter by customer ID.
            products_count: Filter by number of products in cart.
            has_reminders: Filter by whether reminders have been sent.
            country_id: Filter by country ID.
            city_id: Filter by city ID.
            currency_code: Filter by currency code (e.g., "SAR", "EGP").
            date_from: Filter by start date (format: "YYYY-MM-DD").
            date_to: Filter by end date (format: "YYYY-MM-DD").
            cart_total: Filter by cart total value.
            filter_order_by: Field to order by (e.g., "created_at").
            filter_sort_by: Sort direction ("ASC" or "DESC").
            customer_type: Filter by customer type ("individual" or "business").
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding AbandonedCart instances.

        Example:
            ```python
            # Iterate through all abandoned carts
            for cart in client.abandoned_carts.list():
                print(cart.customer_name, cart.cart_total_string)

            # Filter by phase
            for cart in client.abandoned_carts.list(phase="payment_method"):
                print(cart.customer_name)

            # Filter by date range
            for cart in client.abandoned_carts.list(
                date_from="2025-01-01",
                date_to="2025-01-31",
            ):
                print(cart.created_at)
            ```
        """
        params: dict[str, Any] = {}

        # page and page_size are required by the API
        params["page"] = page if page is not None else 1
        params["page_size"] = page_size if page_size is not None else 15
        if phase is not None:
            params["phase"] = phase
        if search_term is not None:
            params["search_term"] = search_term
        if customer_id is not None:
            params["customer_id"] = str(customer_id)
        if products_count is not None:
            params["products_count"] = products_count
        if has_reminders is not None:
            params["has_reminders"] = "1" if has_reminders else "0"
        if country_id is not None:
            params["country_id"] = country_id
        if city_id is not None:
            params["city_id"] = city_id
        if currency_code is not None:
            params["currency_code"] = currency_code
        if date_from is not None:
            params["date_from"] = date_from
        if date_to is not None:
            params["date_to"] = date_to
        if cart_total is not None:
            params["cart_total"] = cart_total
        if filter_order_by is not None:
            params["filter_order_by"] = filter_order_by
        if filter_sort_by is not None:
            params["filter_sort_by"] = filter_sort_by.lower()
        if customer_type is not None:
            params["customer_type"] = customer_type

        params.update(kwargs)

        return self._list(
            self._base_path,
            AbandonedCart.model_validate,
            params=params if params else None,
            results_key="abandoned-carts",
        )

    def get(self, cart_id: str) -> AbandonedCartDetail:
        """Retrieve a specific abandoned cart by ID.

        Args:
            cart_id: The unique identifier (UUID) of the abandoned cart.

        Returns:
            AbandonedCartDetail instance with full details including products and history.

        Raises:
            ZidNotFoundError: If the cart does not exist.

        Example:
            ```python
            cart = client.abandoned_carts.get("b978fcc2-ccd0-45f6-81a7-7ab1f3b8f85d")
            print(cart.customer_name)
            print(cart.store_name)
            for product in cart.products or []:
                print(f"  - {product.name}: {product.total_string}")
            ```
        """
        path = f"{self._base_path}/{cart_id}"
        response = self._get(path)
        return AbandonedCartDetail.model_validate(response["abandoned_cart"])
