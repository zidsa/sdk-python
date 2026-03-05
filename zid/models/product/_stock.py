"""Stock input models for the Zid SDK.

Contains input models for creating and updating product stock records
in the multi-inventory system. Response models (``ProductStock``,
``StockLocation``) live in ``_base.py`` and are reused here.
"""

from __future__ import annotations

from zid.models.base import BaseModel


# --- Input Models ---


class ProductStockCreate(BaseModel):
    """Input model for creating a product stock record.

    Used with ``POST /v1/products/{product_id}/stocks/``.
    """

    location: str
    available_quantity: int
    is_infinite: bool


class ProductStockUpdate(BaseModel):
    """Input model for updating a product stock record.

    Used with ``PATCH /v1/products/{product_id}/stocks/{stock_id}/``
    and bulk ``PATCH /v1/products/{product_id}/stocks/``.
    """

    location: str
    available_quantity: int | None = None
    is_infinite: bool
