"""Abandoned cart models for the Zid SDK.

This module provides Pydantic models for abandoned cart data.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from zid.models.base import BaseModel


# ============================================================================
# Nested Models
# ============================================================================


class AbandonedCartImageThumbs(BaseModel):
    """Image thumbnail URLs at various sizes."""

    full_size: str | None = Field(default=None, validation_alias="fullSize")
    thumbnail: str | None = None
    small: str | None = None
    medium: str | None = None
    large: str | None = None


class AbandonedCartProductImage(BaseModel):
    """Product image in an abandoned cart."""

    id: str | None = None
    origin: str | None = None
    thumbs: AbandonedCartImageThumbs | None = None


class AbandonedCartProductCustomField(BaseModel):
    """Custom field on a product in an abandoned cart."""

    type: str | None = None
    value: str | None = None
    formatted_value: str | None = None
    name: str | None = None
    label: str | None = None


class AbandonedCartProduct(BaseModel):
    """Product in an abandoned cart (detail view)."""

    id: int | str | None = None
    product_id: str | None = None
    product_url: str | None = None
    sku: str | None = None
    name: str | None = None
    custom_field: list[AbandonedCartProductCustomField] | None = None
    price: float | None = None
    price_string: str | None = None
    additions_price: float | None = None
    additions_price_string: str | None = None
    quantity: int | None = None
    total: float | None = None
    total_string: str | None = None
    images: list[AbandonedCartProductImage] | None = None


class AbandonedCartHistory(BaseModel):
    """History entry for an abandoned cart."""

    uuid: str | None = None
    abandoned_cart_id: str | None = None
    type: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AbandonedCartCity(BaseModel):
    """City information for an abandoned cart."""

    id: int | None = None
    name: str | None = None
    national_id: int | None = None
    priority: int | None = None
    country_id: int | None = None
    country_name: str | None = None
    country_code: str | None = None
    ar_name: str | None = None
    en_name: str | None = None


# ============================================================================
# Cart Phase Literal
# ============================================================================

CartPhase = Literal[
    "new",
    "login",
    "shipping_address",
    "shipping_method",
    "payment_method",
    "verification",
    "completed",
]

CartSource = Literal[
    "catalog",
    "md",
    "mazeed_marketplace",
    "mazeed_channels",
    "mazeed",
    "pos",
    "mobile_app",
    "api",
]


# ============================================================================
# Main Models
# ============================================================================


class AbandonedCart(BaseModel):
    """Abandoned cart from list view (DefaultAbandonedCartSerializer).

    This is the summary model returned when listing abandoned carts.
    """

    id: str | None = None
    store_id: str | None = None
    session_id: str | None = None
    url: str | None = None
    cart_id: str | None = None
    order_id: int | None = None
    phase: str | None = None
    customer_id: int | None = None
    customer_name: str | None = None
    customer_email: str | None = None
    customer_mobile: str | None = None
    city_id: int | None = None
    products_count: int | None = None
    reminders_count: int | None = None
    cart_total: float | None = None
    cart_total_string: str | None = None
    whatsapp_message: str | None = None
    currency_code: str | None = None
    source: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AbandonedCartDetail(BaseModel):
    """Abandoned cart detail view (ViewAbandonedCartSerializer).

    This is the full model returned when getting a single abandoned cart.
    Includes products, history, and store information.
    """

    id: str | None = None
    url: str | None = None
    store_id: str | None = None
    store_name: str | None = None
    store_logo: str | None = None
    store_url: str | None = None
    products_count: int | None = None
    products: list[AbandonedCartProduct] | None = None
    city: AbandonedCartCity | None = None
    order_id: int | None = None
    history: list[AbandonedCartHistory] | None = None
    phase: str | None = None
    customer_id: int | None = None
    customer_name: str | None = None
    customer_email: str | None = None
    customer_mobile: str | None = None
    reminders_count: int | None = None
    cart_total: float | None = None
    cart_total_string: str | None = None
    whatsapp_message: str | None = None
    source: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
