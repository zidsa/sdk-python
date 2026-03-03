"""Delivery options resource for the Zid SDK.

This module provides the DeliveryOptionsResource class for interacting with
the Zid Delivery Options API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.delivery_option import DeliveryOption
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class DeliveryOptionsResource(BaseResource):
    """Resource for managing store delivery/shipping options.

    Provides access to delivery option data including listing configured
    shipping methods and creating new ones.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all delivery options (paginated)
        for option in client.delivery_options.list():
            print(option.name, option.shipping_method_status)

        # List with simple payload
        for option in client.delivery_options.list(payload_type="simple"):
            print(option.id, option.name)
        ```
    """

    # Uses default X-Manager-Token header
    token_header: str = "X-Manager-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the delivery options resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)
        self._base_path = "/v1/managers/store/delivery-options"

    def list(
        self,
        *,
        payload_type: str = "simple",
        **kwargs: Any,
    ) -> PaginatedIterator[DeliveryOption]:
        """List all delivery options with pagination.

        Args:
            payload_type: Payload format type (e.g., "simple"). Required by API.
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding DeliveryOption instances.

        Example:
            ```python
            # Iterate through all delivery options
            for option in client.delivery_options.list():
                print(option.name)
                if option.select_cities:
                    for city in option.select_cities:
                        print(f"  - {city.name}")
            ```
        """
        params: dict[str, Any] = {"payload_type": payload_type}
        params.update(kwargs)

        return self._list(
            self._base_path,
            DeliveryOption.model_validate,
            params=params,
            results_key="delivery_options",
        )


