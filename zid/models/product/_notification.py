"""Product notification models for the Zid SDK.

Models for availability notifications — customers subscribing to be
notified when out-of-stock products become available again.
"""

from __future__ import annotations

from zid.models.base import BaseModel
from zid.models.product._base import LocalizedField


# --- Nested Models ---


class NotificationCustomer(BaseModel):
    """Customer information within a notification."""

    id: int | None = None
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None


class NotificationImage(BaseModel):
    """Product image sizes within a notification."""

    full_size: str | None = None
    thumbnail: str | None = None
    large: str | None = None
    medium: str | None = None
    small: str | None = None


# --- Main Models ---


class ProductNotification(BaseModel):
    """Availability notification for a product.

    Represents a customer's subscription to be notified when a
    specific product becomes available again.
    """

    id: str
    product_id: str
    product_name: LocalizedField | None = None
    customer: NotificationCustomer | None = None
    language: str | None = None
    is_notified: bool | None = None
    image: NotificationImage | None = None
    created_at: str | None = None
    updated_at: str | None = None
    code: str | None = None
    is_purchased: bool | None = None
    purchased_total: int | float | None = None


class NotificationStats(BaseModel):
    """Statistics for product availability notifications."""

    total_count: int
    notified_count: int
    purchased_count: int
    purchased_total: int | float


class NotificationSettings(BaseModel):
    """Configuration for availability notification emails."""

    delay_unit: str | None = None
    delay_value: int | None = None
    email_text: LocalizedField | None = None
    email_title: LocalizedField | None = None
    coupon_code: str | None = None
