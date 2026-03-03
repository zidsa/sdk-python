"""Webhook models for the Zid SDK."""

from typing import Literal

from zid.models.base import BaseModel


# Webhook event types supported by the API
WebhookEventType = Literal[
    "order.create",
    "order.status.update",
    "category.create",
    "category.update",
    "category.delete",
    "product.create",
    "product.update",
    "product.delete",
]

# Order status values for webhook conditions
WebhookOrderStatus = Literal[
    "new",
    "preparing",
    "ready",
    "inDelivery",
    "delivered",
    "cancelled",
]

# Payment method values for webhook conditions
WebhookPaymentMethod = Literal[
    "Cash On Delivery",
    "Credit Card",
    "Bank Transfer",
]


class WebhookConditions(BaseModel):
    """Conditions for filtering webhook events.

    Only applicable for `order.create` and `order.status.update` events.
    """

    status: WebhookOrderStatus | None = None
    delivery_option_id: int | None = None
    payment_method: WebhookPaymentMethod | None = None


class Webhook(BaseModel):
    """Webhook subscription model.

    Represents a webhook subscription that receives real-time
    notifications when specific events occur.
    """

    id: str
    event: str
    target_url: str
    store_id: str
    # API returns: null, [] (empty list), or dict with conditions
    conditions: dict[str, str | int] | list[str] | None = None
    original_id: str
    subscriber: str
    active: bool
    doc: str | None = None


class WebhookCreate(BaseModel):
    """Input model for creating a webhook subscription.

    Attributes:
        event: The event type to subscribe to (e.g., "order.create").
        target_url: The URL that will receive webhook payloads.
        original_id: Unique identifier for the app (App ID or MD5 hash of App ID).
        conditions: Optional conditions to filter events.
    """

    event: str
    target_url: str
    original_id: str | int
    conditions: WebhookConditions | None = None
