"""Voucher models for the Zid SDK.

Contains models for digital product voucher management including
voucher details and order-associated vouchers.
"""

from __future__ import annotations

from typing import Literal

from zid.models.base import BaseModel


# --- Type Aliases ---

VoucherStatus = Literal["AVAILABLE", "SOLD", "RESERVED", "RETURNED"]


# --- Main Models ---


class Voucher(BaseModel):
    """A digital product voucher.

    Represents a voucher code attached to a digital product. Each voucher
    has a unique key that is delivered to the customer upon purchase.

    Returned by ``GET /v1/products/{product_id}/vouchers/`` and
    ``POST /v1/products/{product_id}/vouchers/``.
    """

    id: str
    product_id: str | None = None
    status: str
    order: int | None = None
    serial_number: str | None = None
    key: str
    pin_code: str | None = None
    expires_at: str | None = None
    updated_at: str | None = None
    created_at: str | None = None
    expires_at_formatted: str | None = None


class OrderVoucher(BaseModel):
    """A voucher associated with a specific order.

    Returned by ``GET /v1/order-vouchers/{order_id}/``.
    """

    id: str
    product_id: str
    status: str
    order: int | None = None
    serial_number: str | None = None
    key: str
    pin_code: str | None = None
    expires_at: str | None = None
    updated_at: str
    created_at: str
    expires_at_formatted: str | None = None
