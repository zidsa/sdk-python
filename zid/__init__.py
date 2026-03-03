"""Zid Python SDK - A Python client for the Zid e-commerce platform API.

Example:
    ```python
    from zid import ZidClient, Order, Customer

    client = ZidClient(
        authorization="partner-token",
        store_token="store-access-token",
    )

    # List orders
    for order in client.orders.list():
        print(order.id, order.order_status.code)

    # Get a customer
    customer = client.customers.get(123)
    print(customer.name)
    ```
"""

from zid.auth import Auth
from zid.client import ZidClient, RetryConfig
from zid.exceptions import (
    AuthError,
    TokenRefreshError,
    ZidAPIError,
    ZidAuthenticationError,
    ZidAuthorizationError,
    ZidConnectionError,
    ZidError,
    ZidNotFoundError,
    ZidRateLimitError,
    ZidServerError,
    ZidValidationError,
)
from zid.pagination import PaginatedIterator

# Models - primary types for convenience
from zid.models import (
    AbandonedCart,
    AbandonedCartDetail,
    BundleOffer,
    City,
    Country,
    Coupon,
    CouponDetail,
    CreditNote,
    Customer,
    CustomerCreate,
    CustomerLoyalty,
    CustomerUpdate,
    DeliveryOption,
    LocalizedText,
    Location,
    LocationCreate,
    LocationUpdate,
    LoyaltyInfo,
    LoyaltyProgram,
    LoyaltyTransaction,
    LoyaltyTransactionSimple,
    Order,
    OrderSimple,
    OrderTiny,
    PaymentMethod,
    ReverseOrder,
    ReverseOrderCreate,
    Store,
    StoreProfile,
    VATSettings,
    Webhook,
    WebhookCreate,
)

__all__ = [
    # Client
    "ZidClient",
    "Auth",
    "RetryConfig",
    # Pagination
    "PaginatedIterator",
    # Exceptions
    "AuthError",
    "TokenRefreshError",
    "ZidAPIError",
    "ZidAuthenticationError",
    "ZidAuthorizationError",
    "ZidConnectionError",
    "ZidError",
    "ZidNotFoundError",
    "ZidRateLimitError",
    "ZidServerError",
    "ZidValidationError",
    # Models
    "AbandonedCart",
    "AbandonedCartDetail",
    "BundleOffer",
    "City",
    "Country",
    "Coupon",
    "CouponDetail",
    "CreditNote",
    "Customer",
    "CustomerCreate",
    "CustomerLoyalty",
    "CustomerUpdate",
    "DeliveryOption",
    "LocalizedText",
    "Location",
    "LocationCreate",
    "LocationUpdate",
    "LoyaltyInfo",
    "LoyaltyProgram",
    "LoyaltyTransaction",
    "LoyaltyTransactionSimple",
    "Order",
    "OrderSimple",
    "OrderTiny",
    "PaymentMethod",
    "ReverseOrder",
    "ReverseOrderCreate",
    "Store",
    "StoreProfile",
    "VATSettings",
    "Webhook",
    "WebhookCreate",
]
