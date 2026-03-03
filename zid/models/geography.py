"""Geography models for the Zid SDK.

Shared models for Countries and Cities resources.
"""

from zid.models.base import BaseModel


class Country(BaseModel):
    """Country model.

    Used by both operating countries and all countries endpoints.
    """

    id: int
    name: str
    code: str | None = None
    country_code: str | None = None
    flag: str | None = None


class City(BaseModel):
    """Simple city model with just id and name."""

    id: int
    name: str


class CityDetail(BaseModel):
    """Detailed city model with country information.

    Used by the cities-by-country endpoint.
    """

    id: int
    name: str
    national_id: int | None = None
    priority: int | None = None
    country_id: int | None = None
    country_name: str | None = None
    country_code: str | None = None
    ar_name: str | None = None
    en_name: str | None = None
