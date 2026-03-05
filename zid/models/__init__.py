"""Zid SDK data models.

Primary models are exported here for convenience. Nested/helper types
can be accessed through their parent models or imported directly from
their respective modules.

Example:
    ```python
    from zid import Order, Customer  # Main types from root
    from zid.models import Order     # Also works

    # Nested types via parent or direct import
    order.customer  # Returns OrderCustomer
    from zid.models.order import OrderCustomer  # Direct import if needed
    ```
"""

# Base
from zid.models.base import BaseModel

# Primary models - what users interact with most
from zid.models.abandoned_cart import AbandonedCart, AbandonedCartDetail
from zid.models.bundle_offer import BundleOffer, LocalizedText
from zid.models.coupon import Coupon, CouponDetail
from zid.models.customer import Customer, CustomerCreate, CustomerUpdate
from zid.models.delivery_option import DeliveryOption
from zid.models.geography import Country, City
from zid.models.location import Location, LocationCreate, LocationUpdate
from zid.models.loyalty import (
    CustomerLoyalty,
    LoyaltyInfo,
    LoyaltyProgram,
    LoyaltyTransaction,
    LoyaltyTransactionSimple,
)
from zid.models.order import Order, OrderSimple, OrderTiny, CreditNote
from zid.models.product import (
    AssignedCategory,
    Attribute,
    AttributePreset,
    Badge,
    Category,
    CategoryDetail,
    CustomInputField,
    CustomOption,
    Metafield,
    NotificationSettings,
    NotificationStats,
    OrderVoucher,
    Product,
    ProductImage,
    ProductImageSizes,
    ProductNotification,
    ProductSettings,
    ProductStockCreate,
    ProductStockUpdate,
    ShortCategory,
    Voucher,
)
from zid.models.payment_method import PaymentMethod
from zid.models.reverse_order import ReverseOrder, ReverseOrderCreate
from zid.models.store import Store, StoreProfile, VATSettings
from zid.models.webhook import Webhook, WebhookCreate

__all__ = [
    # Base
    "BaseModel",
    # Primary models
    "AbandonedCart",
    "AbandonedCartDetail",
    "AssignedCategory",
    "Attribute",
    "AttributePreset",
    "Badge",
    "BundleOffer",
    "Category",
    "CategoryDetail",
    "City",
    "Country",
    "Coupon",
    "CouponDetail",
    "CreditNote",
    "Customer",
    "CustomerCreate",
    "CustomerLoyalty",
    "CustomerUpdate",
    "CustomInputField",
    "CustomOption",
    "DeliveryOption",
    "LocalizedText",
    "Location",
    "LocationCreate",
    "LocationUpdate",
    "LoyaltyInfo",
    "LoyaltyProgram",
    "LoyaltyTransaction",
    "LoyaltyTransactionSimple",
    "Metafield",
    "NotificationSettings",
    "NotificationStats",
    "Order",
    "OrderSimple",
    "OrderTiny",
    "OrderVoucher",
    "PaymentMethod",
    "Product",
    "ProductImage",
    "ProductImageSizes",
    "ProductNotification",
    "ProductSettings",
    "ProductStockCreate",
    "ProductStockUpdate",
    "ReverseOrder",
    "ReverseOrderCreate",
    "ShortCategory",
    "Store",
    "StoreProfile",
    "VATSettings",
    "Voucher",
    "Webhook",
    "WebhookCreate",
]
