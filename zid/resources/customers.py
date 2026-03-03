"""Customers resource for the Zid SDK.

This module provides the CustomersResource class for interacting with
the Zid Customers API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.customer import Customer
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class CustomersResource(BaseResource):
    """Resource for managing store customers.

    Provides access to customer data including listing and retrieval.
    Note: The Zid API currently only supports read operations for customers.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all customers (paginated)
        for customer in client.customers.list():
            print(customer.name, customer.email)

        # Get a specific customer
        customer = client.customers.get(12345)
        print(customer.name)

        # Paginate with specific page size
        for customer in client.customers.list(per_page=50):
            print(customer.name)
        ```
    """

    # Uses default X-Manager-Token header
    token_header: str = "X-Manager-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the customers resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)
        self._base_path = "/v1/managers/store/customers"

    def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[Customer]:
        """List all customers with pagination.

        Args:
            page: Page number for pagination (1-indexed).
            per_page: Number of items per page.
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding Customer instances.

        Example:
            ```python
            # Iterate through all customers
            for customer in client.customers.list():
                print(customer.name)

            # Paginate with specific page size
            for customer in client.customers.list(per_page=50):
                print(customer.name)
            ```
        """
        params: dict[str, Any] = {}

        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        params.update(kwargs)

        return self._list(
            self._base_path,
            Customer.model_validate,
            params=params if params else None,
            results_key="customers",
        )

    def get(self, customer_id: int) -> Customer:
        """Retrieve a specific customer by ID.

        Args:
            customer_id: The unique identifier of the customer.

        Returns:
            Customer instance with full details including loyalty points.

        Raises:
            ZidNotFoundError: If the customer does not exist.

        Example:
            ```python
            customer = client.customers.get(12345)
            print(customer.name)
            print(customer.email)
            print(customer.city.name if customer.city else "No city")
            ```
        """
        path = f"{self._base_path}/{customer_id}"
        response = self._get(path)
        return Customer.model_validate(response["customer"])
