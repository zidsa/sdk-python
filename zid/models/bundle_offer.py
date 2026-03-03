"""Bundle offer models for the Zid SDK."""

from __future__ import annotations

from typing import Any, Literal

from zid.models.base import BaseModel

# --- Type Aliases ---

BundleOfferStatus = Literal["active", "disabled", "expired", "unstarted"]


# --- Nested Models ---


class LocalizedText(BaseModel):
    """Reusable helper for localized ``{en, ar}`` text objects."""

    en: str | None = None
    ar: str | None = None


class BundleOfferCondition(BaseModel):
    """A condition that must be met for a bundle offer to apply."""

    field: str | None = None
    operator: str | None = None
    value: int | None = None
    applies_to: str | None = None
    product_ids: list[str] | None = None


class BundleOfferAction(BaseModel):
    """An action applied when bundle offer conditions are satisfied.

    The ``value`` field is expressed in the smallest currency unit
    (e.g., cents or halalas) for fixed-amount discounts.
    """

    type: str | None = None
    field: str | None = None
    value: int | float | None = None
    applies_to: str | None = None
    product_ids: list[str] | None = None
    products_quantity: int | None = None


# --- Main Models ---


class BundleOffer(BaseModel):
    """Bundle offer model.

    Represents a store bundle offer discount rule. Bundle offers are
    special promotions where customers get a discount for buying a
    specific bundle of products.

    The ``id`` is a UUID string, not an integer.
    The ``description`` field can be a localized text object or ``[]``
    from the API — :class:`~zid.models.base.BaseModel` handles the
    empty-list-to-None coercion automatically.
    """

    id: str
    name: LocalizedText | None = None
    description: LocalizedText | None = None
    code: str | None = None
    conditions: list[BundleOfferCondition] | None = None
    actions: list[BundleOfferAction] | None = None
    conditions_criteria: str | None = None
    uses_total: int | None = None
    uses_customer: int | None = None
    enabled: bool | None = None
    auto_adding: bool | None = None
    status_code: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    meta: dict[str, Any] | None = None
    channel: str | None = None
    channel_name: LocalizedText | None = None
