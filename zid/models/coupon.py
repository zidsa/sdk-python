"""Coupon models for the Zid SDK."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from zid.models.base import BaseModel

# --- Type Aliases ---

CouponStatus = Literal[
    "coupon_active",
    "coupon_inactive",
    "coupon_expired",
    "coupon_used",
    "coupon_unstarted",
]

DiscountType = Literal["f", "p", "n"]


# --- Main Models ---


class Coupon(BaseModel):
    """Coupon model representing a store discount coupon.

    Used for list results from the coupons endpoint.
    Fields match the ``DefaultCouponSerializer`` schema from the Zid API,
    plus additional fields returned in actual responses.
    """

    coupon_id: int = Field(validation_alias="coupon_id")
    id: int
    store_id: int | None = None
    store_name: str | None = None
    store_logo: str | None = None
    code: str
    name: str
    uses_total: int | None = None
    created_at: str | None = None
    total_usage: int | None = None
    discount_type: str | None = None
    applying_method: str | None = None
    conditions: list[dict[str, Any]] | None = None
    conditions_criteria: str | None = None
    discount: int | float | None = None
    logged: bool | None = None
    free_shipping: bool | None = None
    free_cod: bool | None = None
    apply_to: str | None = None
    total: int | float | None = None
    max_total: int | float | None = None
    max_weight: int | float | None = None
    date_start: str | None = None
    date_end: str | None = None
    uses_customer: int | None = None
    coupon_status: bool | None = None
    status_code: str | None = None
    maximum_discount_value: float | None = None
    is_mazeed_active: bool | None = None
    is_pos_active: bool | None = None
    is_shown_in_pos: bool | None = None
    is_mobile_app_active: bool | None = None
    is_manageable: bool | None = None
    is_active: bool | None = None
    enabled: bool | None = None


class CouponDetail(Coupon):
    """Extended coupon model with detail-only fields.

    Returned by the view endpoint (``/coupons/{id}/view``).
    Inherits all fields from :class:`Coupon` and adds order/sales data.
    """

    orders: list[dict[str, Any]] | None = None
    total_sales: int | float | None = None
    total_customers: int | None = None
    note: str | None = None
    apply_to_data: list[str | dict[str, Any]] | None = None
