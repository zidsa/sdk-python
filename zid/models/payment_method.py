"""Payment method models for the Zid SDK."""

from typing import Any

from pydantic import field_validator

from zid.models.base import BaseModel


class PaymentMethodName(BaseModel):
    """Localized payment method name."""

    ar: str | None = None
    en: str | None = None


class PaymentMethod(BaseModel):
    """Payment method configuration for a store.

    Represents a payment method available in the store, such as
    cash on delivery, credit card, bank transfer, etc.

    Note: The `name` field can be either a string or a localized object
    with `ar` and `en` keys. This model normalizes it to always be
    a PaymentMethodName object for consistency.
    """

    id: int
    code: str
    name: str | PaymentMethodName
    enabled: bool
    fees: float | None = None
    fees_string: str | None = None
    type: str | None = None
    icons: list[str] | None = None
    icon: str | None = None  # Some methods have singular icon instead of icons

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, v: Any) -> str | PaymentMethodName:
        """Handle name being either a string or localized object."""
        if isinstance(v, dict):
            return PaymentMethodName.model_validate(v)
        return v

    @property
    def display_name(self) -> str:
        """Get the display name, preferring English if localized."""
        if isinstance(self.name, PaymentMethodName):
            return self.name.en or self.name.ar or ""
        return self.name
