"""Zid SDK resource classes.

This module exports all resource classes for interacting with the Zid API.
Resources are accessed through the ZidClient instance.

Available Resources:
    - CustomersResource: Manage store customers
    - OrdersResource: Manage orders with different payload types
    - LocationsResource: Multi-inventory location management
    - AbandonedCartsResource: Track abandoned shopping carts
    - ReverseOrdersResource: Handle returns and refunds
    - DeliveryOptionsResource: Shipping/delivery configuration
    - PaymentMethodsResource: Payment method configuration
    - ProductsResource: Product management (CRUD, settings, sub-resources)
    - StoresResource: Store profile and settings
    - GeographyResource: Countries and cities data
    - WebhooksResource: Webhook subscriptions

Example:
    ```python
    from zid import ZidClient

    client = ZidClient(authorization="token", store_token="store-token")

    # Access resources through the client
    for order in client.orders.list():
        print(order.id)
    ```
"""

from zid.resources.abandoned_carts import AbandonedCartsResource
from zid.resources.bundle_offers import BundleOffersResource
from zid.resources.coupons import CouponsResource
from zid.resources.customers import CustomersResource
from zid.resources.delivery_options import DeliveryOptionsResource
from zid.resources.geography import GeographyResource
from zid.resources.locations import LocationsResource
from zid.resources.loyalty import LoyaltyResource
from zid.resources.orders import OrdersResource
from zid.resources.payment_methods import PaymentMethodsResource
from zid.resources.products import ProductsResource
from zid.resources.reverse_orders import ReverseOrdersResource
from zid.resources.stores import StoresResource
from zid.resources.webhooks import WebhooksResource

__all__ = [
    "AbandonedCartsResource",
    "BundleOffersResource",
    "CouponsResource",
    "CustomersResource",
    "DeliveryOptionsResource",
    "GeographyResource",
    "LocationsResource",
    "LoyaltyResource",
    "OrdersResource",
    "PaymentMethodsResource",
    "ProductsResource",
    "ReverseOrdersResource",
    "StoresResource",
    "WebhooksResource",
]
