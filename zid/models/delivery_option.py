"""Delivery option models for the Zid SDK."""

from zid.models.base import BaseModel


class DeliveryOptionCity(BaseModel):
    """City information for a delivery option."""

    id: int
    national_id: int | None = None
    name: str
    priority: int
    country_id: int
    country_name: str | None = None
    country_code: str | None = None
    ar_name: str
    en_name: str


class DeliveryOption(BaseModel):
    """Delivery/shipping option model.

    Represents a shipping method configured for the store.
    """

    id: int
    name: str | None = None
    system_option_code: str | None = None
    select_cities: list[DeliveryOptionCity] | None = None
    shipping_method_status: str | None = None

