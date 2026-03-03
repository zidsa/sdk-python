"""Location models for the Zid SDK (Multi-Inventory)."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from zid.models.base import BaseModel


class LocationCountry(BaseModel):
    """Country information for a location."""

    id: int
    name: str
    ar_name: str
    iso_code_2: str | None = None
    iso_code_3: str | None = None
    code: str | None = None


class LocationCity(BaseModel):
    """City information for a location."""

    id: int
    name: str
    ar_name: str
    country: LocationCountry | None = None
    country_code: str | None = None


class LocationCoordinates(BaseModel):
    """Geographic coordinates for a location."""

    latitude: float
    longitude: float


class LocationName(BaseModel):
    """Localized name for a location."""

    ar: str | None = None
    en: str | None = None


class LinkedUser(BaseModel):
    """User linked to a location."""

    user_uuid: str | None = None
    full_name: str | None = None


class Location(BaseModel):
    """Inventory location model.

    Represents a physical or virtual inventory location for a store.
    """

    id: str
    name: LocationName | None = None
    city: LocationCity | None = None
    type: str | None = None
    coordinates: LocationCoordinates | None = None
    full_address: str | None = None
    short_address: str | None = None
    district: str | None = None
    street: str | None = None
    fulfillment_priority: int | None = None
    is_default: bool | None = None
    is_private: bool | None = None
    is_enabled: bool | None = None
    has_stocks: bool | None = None
    channels: list[str] | None = None
    linked_users: list[LinkedUser] | None = None


class LocationListResponse(BaseModel):
    """Response wrapper for location list endpoint with pagination metadata."""

    next: str | None = None
    previous: str | None = None
    count: int | None = None
    active_locations_limit: int | None = None
    active_locations_count: int | None = None
    results: list[Location] | None = None


class LocationCoordinatesInput(BaseModel):
    """Coordinates input for creating/updating a location."""

    latitude: float | str
    longitude: float | str


class LocationNameInput(BaseModel):
    """Localized name input for creating a location."""

    ar: str | None = None
    en: str | None = None


class LocationCreate(BaseModel):
    """Input model for creating a location."""

    name: LocationNameInput | str
    city: int
    coordinates: LocationCoordinatesInput
    full_address: str
    short_address: str | None = None
    is_default: bool = False
    is_private: bool = False
    is_enabled: bool = True
    channels: list[str] | None = None


class LocationUpdate(BaseModel):
    """Input model for updating a location."""

    name: str | None = None
    city: int | None = None
    coordinates: LocationCoordinatesInput | None = None
    full_address: str | None = None
    short_address: str | None = None
    is_default: bool | None = None
    is_private: bool | None = None
    is_enabled: bool | None = None
    channels: list[str] | None = None


class StockUpdateItem(BaseModel):
    """Single item for stock update request."""

    product_id: str
    available_quantity: int
    is_infinite: bool = False
