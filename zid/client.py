"""Zid API client entry point."""

from __future__ import annotations

from typing import Any, Callable

from zid.auth import Auth
from zid.http import HTTPClient, RetryConfig, DEFAULT_BASE_URL, DEFAULT_TIMEOUT
from zid.resources.abandoned_carts import AbandonedCartsResource
from zid.resources.customers import CustomersResource
from zid.resources.delivery_options import DeliveryOptionsResource
from zid.resources.geography import GeographyResource
from zid.resources.locations import LocationsResource
from zid.resources.orders import OrdersResource
from zid.resources.payment_methods import PaymentMethodsResource
from zid.resources.reverse_orders import ReverseOrdersResource
from zid.resources.stores import StoresResource
from zid.resources.bundle_offers import BundleOffersResource
from zid.resources.coupons import CouponsResource
from zid.resources.loyalty import LoyaltyResource
from zid.resources.webhooks import WebhooksResource

__all__ = ["ZidClient", "RetryConfig"]


class ZidClient:
    """Main client for interacting with the Zid API.

    Example:
        ```python
        # Basic usage
        client = ZidClient(
            authorization="partner-token",
            store_token="store-access-token",
        )

        # With auto-refresh enabled
        client = ZidClient(
            authorization="partner-token",
            store_token="store-access-token",
            refresh_token="refresh-token",
            client_id="48",
            client_secret="your-secret",
            redirect_uri="https://yourapp.com/callback",
            on_tokens_refreshed=lambda auth: save_to_db(auth),
        )

        # With custom retry configuration
        client = ZidClient(
            authorization="partner-token",
            store_token="store-access-token",
            retry=RetryConfig(
                max_retries=5,
                base_delay=1.0,
                retry_on_rate_limit=True,
                max_rate_limit_wait=300,
            ),
        )

        # Disable retries
        client = ZidClient(
            authorization="partner-token",
            store_token="store-access-token",
            retry=RetryConfig(max_retries=0),
        )

        # Access resources
        for order in client.orders.list():
            print(order.id)
        ```
    """

    def __init__(
        self,
        authorization: str | None = None,
        *,
        store_token: str | None = None,
        store_id: int | str | None = None,
        refresh_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        redirect_uri: str | None = None,
        on_tokens_refreshed: Callable[[Auth], None] | None = None,
        auth: Auth | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        language: str = "en",
        auto_refresh: bool = True,
        retry: RetryConfig | None = None,
    ) -> None:
        """Initialize the Zid client.

        Args:
            authorization: Partner token from OAuth.
            store_token: Store-level access token.
            store_id: Store identifier.
            refresh_token: OAuth refresh token.
            client_id: OAuth client ID (for auto-refresh).
            client_secret: OAuth client secret (for auto-refresh).
            redirect_uri: OAuth redirect URI (for auto-refresh).
            on_tokens_refreshed: Callback when tokens are refreshed.
                Use to persist new tokens to your database.
            auth: Pre-configured Auth instance (alternative to individual args).
            base_url: API base URL.
            timeout: Request timeout in seconds.
            language: Accept-Language header value.
            auto_refresh: Enable automatic token refresh on 401.
            retry: Retry configuration for transient failures and rate limits.
                Defaults to RetryConfig() (3 retries with exponential backoff).

        Raises:
            ValueError: If neither authorization nor auth is provided.
        """
        if auth is not None:
            self._auth = auth
        elif authorization is not None:
            self._auth = Auth(
                authorization=authorization,
                store_token=store_token,
                store_id=store_id,
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                on_tokens_refreshed=on_tokens_refreshed,
            )
        else:
            raise ValueError("Either 'authorization' or 'auth' must be provided")

        self._http = HTTPClient(
            auth=self._auth,
            language=language,
            base_url=base_url,
            timeout=timeout,
            auto_refresh=auto_refresh,
            retry=retry,
        )

        self._resources: dict[str, Any] = {}

    @property
    def auth(self) -> Auth:
        """Get the authentication configuration."""
        return self._auth

    @property
    def abandoned_carts(self) -> AbandonedCartsResource:
        """Access the Abandoned Carts resource."""
        if "abandoned_carts" not in self._resources:
            self._resources["abandoned_carts"] = AbandonedCartsResource(self._http)
        return self._resources["abandoned_carts"]

    @property
    def customers(self) -> CustomersResource:
        """Access the Customers resource."""
        if "customers" not in self._resources:
            self._resources["customers"] = CustomersResource(self._http)
        return self._resources["customers"]

    @property
    def orders(self) -> OrdersResource:
        """Access the Orders resource."""
        if "orders" not in self._resources:
            self._resources["orders"] = OrdersResource(self._http)
        return self._resources["orders"]

    @property
    def locations(self) -> LocationsResource:
        """Access the Locations resource."""
        if "locations" not in self._resources:
            self._resources["locations"] = LocationsResource(self._http)
        return self._resources["locations"]

    @property
    def reverse_orders(self) -> ReverseOrdersResource:
        """Access the Reverse Orders resource."""
        if "reverse_orders" not in self._resources:
            self._resources["reverse_orders"] = ReverseOrdersResource(self._http)
        return self._resources["reverse_orders"]

    @property
    def delivery_options(self) -> DeliveryOptionsResource:
        """Access the Delivery Options resource."""
        if "delivery_options" not in self._resources:
            self._resources["delivery_options"] = DeliveryOptionsResource(self._http)
        return self._resources["delivery_options"]

    @property
    def geography(self) -> GeographyResource:
        """Access the Geography resource (countries and cities)."""
        if "geography" not in self._resources:
            self._resources["geography"] = GeographyResource(self._http)
        return self._resources["geography"]

    @property
    def stores(self) -> StoresResource:
        """Access the Stores resource."""
        if "stores" not in self._resources:
            self._resources["stores"] = StoresResource(self._http)
        return self._resources["stores"]

    @property
    def payment_methods(self) -> PaymentMethodsResource:
        """Access the Payment Methods resource."""
        if "payment_methods" not in self._resources:
            self._resources["payment_methods"] = PaymentMethodsResource(self._http)
        return self._resources["payment_methods"]

    @property
    def webhooks(self) -> WebhooksResource:
        """Access the Webhooks resource."""
        if "webhooks" not in self._resources:
            self._resources["webhooks"] = WebhooksResource(self._http)
        return self._resources["webhooks"]
    @property
    def coupons(self) -> CouponsResource:
        """Access the Coupons resource."""
        if "coupons" not in self._resources:
            self._resources["coupons"] = CouponsResource(self._http)
        return self._resources["coupons"]

    @property
    def bundle_offers(self) -> BundleOffersResource:
        """Access the Bundle Offers resource."""
        if "bundle_offers" not in self._resources:
            self._resources["bundle_offers"] = BundleOffersResource(self._http)
        return self._resources["bundle_offers"]

    @property
    def loyalty(self) -> LoyaltyResource:
        """Access the Loyalty Program resource."""
        if "loyalty" not in self._resources:
            self._resources["loyalty"] = LoyaltyResource(self._http)
        return self._resources["loyalty"]

    def close(self) -> None:
        """Close the client and release resources."""
        self._http.close()

    def __enter__(self) -> ZidClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
