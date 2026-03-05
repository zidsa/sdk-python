"""Product models for the Zid SDK.

All primary product models are exported here. Nested/helper types
can be imported directly from their respective submodules if needed.
"""

from zid.models.product._base import Product, ProductImage, ProductImageSizes, ProductSettings
from zid.models.product._customization import CustomInputField, CustomOption
from zid.models.product._category import (
    AssignedCategory,
    Category,
    CategoryDetail,
    ShortCategory,
)
from zid.models.product._notification import (
    NotificationSettings,
    NotificationStats,
    ProductNotification,
)
from zid.models.product._stock import ProductStockCreate, ProductStockUpdate
from zid.models.product._voucher import OrderVoucher, Voucher
from zid.models.product._attribute import Attribute, AttributePreset, Badge, Metafield

__all__ = [
    "AssignedCategory",
    "Attribute",
    "AttributePreset",
    "Badge",
    "Category",
    "CategoryDetail",
    "CustomInputField",
    "CustomOption",
    "Metafield",
    "NotificationSettings",
    "NotificationStats",
    "OrderVoucher",
    "Product",
    "ProductImage",
    "ProductImageSizes",
    "ProductNotification",
    "ProductSettings",
    "ProductStockCreate",
    "ProductStockUpdate",
    "ShortCategory",
    "Voucher",
]
