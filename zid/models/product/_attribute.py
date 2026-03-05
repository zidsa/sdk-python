"""Attribute, preset, metafield, and badge models for the Zid SDK."""

from __future__ import annotations

from zid.models.base import BaseModel
from zid.models.product._base import LocalizedField


# --- Nested Models ---


class AttributePreset(BaseModel):
    """A predefined selectable value for a product attribute.

    Presets allow merchants to quickly assign attribute values
    (e.g., "Red", "Blue" for a "Color" attribute).
    """

    id: str
    slug: str
    name: LocalizedField | str
    value: LocalizedField | str
    type: str
    type_value: LocalizedField | str | None = None
    display_order: int | None = None
    attribute_image_id: str | None = None
    attribute_id: str


class BadgeIcon(BaseModel):
    """Icon associated with a badge."""

    code: str


# --- Main Models ---


class Attribute(BaseModel):
    """A store-level product attribute (e.g., Color, Size).

    Attributes define the dimensions along which product variants
    can differ. Each attribute can have multiple presets.
    """

    id: str
    name: LocalizedField | str
    slug: str
    presets: list[AttributePreset] = []
    is_extra: bool
    is_enabled: bool
    display_order: int | None = None
    preset_count: int | None = None


class Metafield(BaseModel):
    """A product-level attribute assignment with localized name and value."""

    id: str
    name: LocalizedField | None = None
    slug: str
    data_type: str | None = None
    display_order: int | None = None
    value: LocalizedField | str | int | bool | list | dict | None = None


class Badge(BaseModel):
    """A predefined product badge (e.g., "10% Discount", "Free Shipping").

    Badges are store-level labels that can be applied to products
    for promotional display.
    """

    body: LocalizedField | None = None
    icon: BadgeIcon | None = None
    is_example: bool
