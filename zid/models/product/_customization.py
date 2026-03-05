"""Customization models for the Zid SDK.

Contains models for product custom option fields (checkbox/dropdown)
and custom user input fields (text, number, etc.).
"""

from __future__ import annotations

from zid.models.base import BaseModel


# --- Nested Models ---


class CustomOptionChoice(BaseModel):
    """A single choice within a custom option field.

    Each choice has localized labels and an optional price adjustment.
    """

    id: str | None = None
    ar: str | None = None
    en: str | None = None
    price: float | None = None


class CustomOptionLabel(BaseModel):
    """Localized label for a custom option or input field."""

    ar: str | None = None
    en: str | None = None


# --- Main Models ---


class CustomOption(BaseModel):
    """A custom option field on a product (checkbox or dropdown).

    Custom options let customers choose from predefined choices
    (e.g., gift wrapping, warranty tier). Each choice can carry
    an additional price.

    Returned by ``POST /v1/products/{product_id}/custom_options_fields/``
    and ``PUT /v1/products/{product_id}/custom_options_fields/{id}/``.
    """

    id: str
    type: str
    label: CustomOptionLabel
    hint: CustomOptionLabel | None = None
    min_choices: int
    max_choices: int
    can_choose_multiple_options: bool
    is_published: bool
    is_required: bool
    display_order: int
    choices: list[CustomOptionChoice]
    visibility_condition: dict | None = None


class CustomInputField(BaseModel):
    """A custom user input field on a product.

    Input fields collect free-form data from customers at purchase
    time (e.g., engraving text, gift message, special instructions).

    Returned by ``POST /v1/products/{product_id}/custom_user_input_fields/``.
    """

    id: str | None = None
    type: str | None = None
    hint: CustomOptionLabel | None = None
    label: CustomOptionLabel | None = None
