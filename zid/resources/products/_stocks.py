"""Product stocks sub-resource for the Zid SDK.

Provides methods for managing product stock records across
multiple inventory locations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.product._base import ProductStock
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class ProductStocksSubResource(BaseResource):
    """Sub-resource for managing product stock (multi-inventory).

    Access via ``client.products.stocks``.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all stock records for a product
        stocks = client.products.stocks.list("product-uuid")
        for stock in stocks:
            print(stock.location.name, stock.available_quantity)

        # Create a new stock record
        stock = client.products.stocks.create(
            "product-uuid",
            location="location-uuid",
            available_quantity=10,
            is_infinite=False,
        )
        ```
    """

    token_header: str = "Access-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the product stocks sub-resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)

    def list(self, product_id: str) -> list[ProductStock]:
        """List all stock records for a product.

        Retrieves stock entries across all inventory locations
        for the specified product.

        Args:
            product_id: The unique identifier (UUID) of the product.

        Returns:
            List of ProductStock instances.

        Raises:
            ZidNotFoundError: If the product does not exist.

        Example:
            ```python
            stocks = client.products.stocks.list("product-uuid")
            for stock in stocks:
                print(stock.location.name, stock.available_quantity)
            ```
        """
        path = f"/v1/products/{product_id}/stocks/"
        response = self._get(path)
        items = response.get("results", [])
        return [ProductStock.model_validate(item) for item in items]

    def get(self, product_id: str, stock_id: str) -> ProductStock:
        """Retrieve a specific stock record by ID.

        Args:
            product_id: The unique identifier (UUID) of the product.
            stock_id: The unique identifier (UUID) of the stock record.

        Returns:
            ProductStock instance.

        Raises:
            ZidNotFoundError: If the product or stock record does not exist.

        Example:
            ```python
            stock = client.products.stocks.get("product-uuid", "stock-uuid")
            print(stock.available_quantity, stock.is_infinite)
            ```
        """
        path = f"/v1/products/{product_id}/stocks/{stock_id}/"
        response = self._get(path)
        return ProductStock.model_validate(response)

    def create(
        self,
        product_id: str,
        *,
        location: str,
        available_quantity: int,
        is_infinite: bool,
    ) -> dict[str, Any]:
        """Create a new stock record for a product at a location.

        Args:
            product_id: The unique identifier (UUID) of the product.
            location: The unique identifier (UUID) of the inventory location.
            available_quantity: Initial available quantity at this location.
            is_infinite: Whether the product has unlimited stock at this location.

        Returns:
            Dict with the created stock data (``id``, ``location``,
            ``available_quantity``, ``is_infinite``).

        Raises:
            ZidValidationError: If the location is invalid or stock already exists.

        Example:
            ```python
            stock = client.products.stocks.create(
                "product-uuid",
                location="location-uuid",
                available_quantity=25,
                is_infinite=False,
            )
            print(stock["id"])
            ```
        """
        data: dict[str, Any] = {
            "location": location,
            "available_quantity": available_quantity,
            "is_infinite": is_infinite,
        }
        path = f"/v1/products/{product_id}/stocks/"
        return self._create(path, json=data)

    def update(
        self,
        product_id: str,
        stock_id: str,
        *,
        available_quantity: int | None = None,
        is_infinite: bool | None = None,
    ) -> dict[str, Any]:
        """Update a single stock record.

        For bulk updates across multiple locations, use
        :meth:`bulk_update` instead.

        Args:
            product_id: The unique identifier (UUID) of the product.
            stock_id: The unique identifier (UUID) of the stock record.
            available_quantity: New available quantity. Set to ``None``
                when ``is_infinite`` is ``True``.
            is_infinite: Whether the product has unlimited stock.

        Returns:
            Dict with the updated stock data.

        Raises:
            ZidNotFoundError: If the product or stock record does not exist.

        Example:
            ```python
            stock = client.products.stocks.update(
                "product-uuid",
                "stock-uuid",
                available_quantity=5,
                is_infinite=False,
            )
            ```
        """
        data: dict[str, Any] = {}
        if available_quantity is not None:
            data["available_quantity"] = available_quantity
        if is_infinite is not None:
            data["is_infinite"] = is_infinite

        path = f"/v1/products/{product_id}/stocks/{stock_id}/"
        return self._update(path, json=data, method="PATCH")

    def bulk_update(
        self,
        product_id: str,
        stocks: list[dict[str, Any]],
    ) -> None:
        """Bulk update stock records across multiple locations.

        Recommended when updating multiple stock entries at once.

        Each dict should contain ``location`` (UUID), ``available_quantity``,
        and ``is_infinite``.

        Args:
            product_id: The unique identifier (UUID) of the product.
            stocks: List of stock update dicts. Each must include:
                - ``location`` (str): Location UUID.
                - ``available_quantity`` (int | None): Quantity at location.
                - ``is_infinite`` (bool): Whether stock is unlimited.

        Returns:
            None (HTTP 204 on success).

        Raises:
            ZidValidationError: If any stock entry is invalid.

        Example:
            ```python
            client.products.stocks.bulk_update("product-uuid", [
                {
                    "location": "loc-uuid-1",
                    "available_quantity": 10,
                    "is_infinite": False,
                },
                {
                    "location": "loc-uuid-2",
                    "available_quantity": 20,
                    "is_infinite": False,
                },
            ])
            ```
        """
        path = f"/v1/products/{product_id}/stocks/"
        self._update(path, json=stocks, method="PATCH")
