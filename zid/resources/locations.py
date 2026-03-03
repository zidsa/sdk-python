"""Locations resource for the Zid SDK (Multi-Inventory).

This module provides the LocationsResource class for interacting with
the Zid Multi-Inventory Locations API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.location import Location, StockUpdateItem
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class LocationsResource(BaseResource):
    """Resource for managing inventory locations.

    Provides access to multi-inventory location management including
    CRUD operations and stock updates.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all locations (paginated)
        for location in client.locations.list():
            print(location.name, location.city.name if location.city else "")

        # Get a specific location
        location = client.locations.get("location-uuid")
        print(location.full_address)

        # Create a new location
        location = client.locations.create(
            name={"ar": "مخزن الرياض", "en": "Riyadh Warehouse"},
            city=1,
            coordinates={"latitude": 24.7136, "longitude": 46.6753},
            full_address="123 Main St, Riyadh",
            is_enabled=True,
        )

        # Update a location
        location = client.locations.update(
            "location-uuid",
            name="Updated Name",
            is_enabled=False,
        )

        # Update stock for products at a location
        client.locations.update_stock(
            "location-uuid",
            [
                {"product_id": "prod-uuid-1", "available_quantity": 100, "is_infinite": False},
                {"product_id": "prod-uuid-2", "available_quantity": 50, "is_infinite": False},
            ],
        )
        ```
    """

    # Locations API uses Access-Token header
    token_header: str = "Access-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the locations resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)
        self._base_path = "/v1/locations"

    def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[Location]:
        """List all inventory locations with pagination.

        Args:
            page: Page number for pagination (1-indexed).
            per_page: Number of items per page.
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding Location instances.

        Example:
            ```python
            # Iterate through all locations
            for location in client.locations.list():
                print(location.name)

            # Paginate with specific page size
            for location in client.locations.list(per_page=10):
                print(location.full_address)
            ```
        """
        params: dict[str, Any] = {}

        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        params.update(kwargs)

        return self._list(
            f"{self._base_path}/",
            Location.model_validate,
            params=params if params else None,
            results_key="results",
        )

    def get(self, location_id: str) -> Location:
        """Retrieve a specific location by ID.

        Args:
            location_id: The unique identifier (UUID) of the location.

        Returns:
            Location instance with full details.

        Raises:
            ZidNotFoundError: If the location does not exist.

        Example:
            ```python
            location = client.locations.get("8ee590fe-d02d-4c50-9184-f628bb8b115a")
            print(location.name)
            print(location.full_address)
            print(location.city.name if location.city else "No city")
            ```
        """
        path = f"{self._base_path}/{location_id}/"
        response = self._get(path)
        return Location.model_validate(response)

    def create(
        self,
        *,
        name: dict[str, str] | str,
        city: int,
        coordinates: dict[str, float | str],
        full_address: str,
        short_address: str | None = None,
        is_default: bool = False,
        is_private: bool = False,
        is_enabled: bool = True,
        channels: list[str] | None = None,
        **kwargs: Any,
    ) -> Location:
        """Create a new inventory location.

        Args:
            name: Location name. Can be a dict with 'ar' and/or 'en' keys,
                or a simple string.
            city: City ID where the location is based.
            coordinates: Dict with 'latitude' and 'longitude' keys.
            full_address: Full physical address of the location.
            short_address: Short address code (required for Saudi Arabia).
            is_default: Whether this is the default location.
            is_private: Whether this location is private.
            is_enabled: Whether this location is enabled.
            channels: List of channels (e.g., ["pos", "catalog"]).
            **kwargs: Additional fields to include in the request.

        Returns:
            The created Location instance.

        Example:
            ```python
            location = client.locations.create(
                name={"ar": "مخزن الرياض", "en": "Riyadh Warehouse"},
                city=1,
                coordinates={"latitude": 24.7136, "longitude": 46.6753},
                full_address="123 Main St, Riyadh, Saudi Arabia",
                is_enabled=True,
                channels=["pos", "catalog"],
            )
            print(f"Created location: {location.id}")
            ```
        """
        payload: dict[str, Any] = {
            "name": name,
            "city": city,
            "coordinates": coordinates,
            "full_address": full_address,
            "is_default": is_default,
            "is_private": is_private,
            "is_enabled": is_enabled,
        }

        if short_address is not None:
            payload["short_address"] = short_address
        if channels is not None:
            payload["channels"] = channels

        payload.update(kwargs)

        response = self._create(f"{self._base_path}/", json=payload)
        return Location.model_validate(response)

    def update(
        self,
        location_id: str,
        *,
        name: str | None = None,
        city: int | None = None,
        coordinates: dict[str, float | str] | None = None,
        full_address: str | None = None,
        short_address: str | None = None,
        is_default: bool | None = None,
        is_private: bool | None = None,
        is_enabled: bool | None = None,
        channels: list[str] | None = None,
        **kwargs: Any,
    ) -> Location:
        """Update an existing inventory location.

        Args:
            location_id: The unique identifier (UUID) of the location.
            name: New name for the location.
            city: New city ID.
            coordinates: New coordinates dict with 'latitude' and 'longitude'.
            full_address: New full address.
            short_address: New short address code.
            is_default: Whether this is the default location.
            is_private: Whether this location is private.
            is_enabled: Whether this location is enabled.
            channels: New list of channels.
            **kwargs: Additional fields to include in the request.

        Returns:
            The updated Location instance.

        Example:
            ```python
            location = client.locations.update(
                "8ee590fe-d02d-4c50-9184-f628bb8b115a",
                name="Updated Warehouse Name",
                is_enabled=False,
            )
            print(f"Updated location: {location.name}")
            ```
        """
        payload: dict[str, Any] = {}

        if name is not None:
            payload["name"] = name
        if city is not None:
            payload["city"] = city
        if coordinates is not None:
            payload["coordinates"] = coordinates
        if full_address is not None:
            payload["full_address"] = full_address
        if short_address is not None:
            payload["short_address"] = short_address
        if is_default is not None:
            payload["is_default"] = is_default
        if is_private is not None:
            payload["is_private"] = is_private
        if is_enabled is not None:
            payload["is_enabled"] = is_enabled
        if channels is not None:
            payload["channels"] = channels

        payload.update(kwargs)

        path = f"{self._base_path}/{location_id}/"
        response = self._update(path, json=payload, method="PATCH")
        return Location.model_validate(response)

    def update_stock(
        self,
        location_id: str,
        items: list[dict[str, Any] | StockUpdateItem],
    ) -> None:
        """Update product stock quantities for a location.

        Args:
            location_id: The unique identifier (UUID) of the location.
            items: List of stock update items. Each item should have:
                - product_id: UUID of the product
                - available_quantity: Number of units available
                - is_infinite: Whether stock is unlimited (default: False)

        Raises:
            ZidValidationError: If the location is not enabled or items are invalid.

        Example:
            ```python
            client.locations.update_stock(
                "8ee590fe-d02d-4c50-9184-f628bb8b115a",
                [
                    {"product_id": "prod-uuid-1", "available_quantity": 100, "is_infinite": False},
                    {"product_id": "prod-uuid-2", "available_quantity": 0, "is_infinite": True},
                ],
            )
            ```
        """
        # Convert StockUpdateItem instances to dicts if needed
        payload = []
        for item in items:
            if isinstance(item, StockUpdateItem):
                payload.append(item.model_dump(by_alias=True))
            else:
                payload.append(item)

        path = f"{self._base_path}/{location_id}/stock-update/"
        self._client.post(path, json=payload, token_header=self.token_header)
