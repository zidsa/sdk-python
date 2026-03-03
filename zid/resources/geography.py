"""Geography resource for the Zid SDK.

This module provides the GeographyResource class for retrieving
country and city data from the Zid API.

The resource provides three main methods:
    - list_operating_countries(): Countries where the store operates
    - list_all_countries(): All available countries in the system
    - list_cities(country_id): Cities for a specific country
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from zid.models.geography import CityDetail, Country
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class GeographyResource(BaseResource):
    """Resource for retrieving countries and cities.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List countries where the store operates
        countries = client.geography.list_operating_countries()
        for country in countries:
            print(f"{country.name} ({country.code})")
        ```
    """

    token_header: str = "X-Manager-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the geography resource."""
        super().__init__(client)

    def list_operating_countries(self) -> list[Country]:
        """List countries where the store operates.

        Returns:
            List of Country instances.

        Example:
            ```python
            countries = client.geography.list_operating_countries()
            for country in countries:
                print(f"{country.name} ({country.code})")
            ```
        """
        response = self._get("/v1/managers/countries")
        countries_data = response.get("countries", [])
        return [Country.model_validate(item) for item in countries_data]

    def list_all_countries(self) -> list[Country]:
        """List all available countries.

        This endpoint returns all countries' names, codes, and IDs,
        and is not specific to any particular store's operations.

        Returns:
            List of Country instances.

        Example:
            ```python
            countries = client.geography.list_all_countries()
            for country in countries:
                print(f"{country.name} ({country.code}) - {country.flag}")
            ```
        """
        response = self._get("/v1/settings/countries")
        countries_data = response.get("countries", [])
        return [Country.model_validate(item) for item in countries_data]

    def list_cities(self, country_id: int) -> list[CityDetail]:
        """List cities for a specific country.

        Args:
            country_id: The ID of the country to get cities for.

        Returns:
            List of CityDetail instances.

        Example:
            ```python
            # Get cities for Saudi Arabia (country_id=184)
            cities = client.geography.list_cities(184)
            for city in cities:
                print(f"{city.name} ({city.ar_name})")
            ```
        """
        response = self._get(f"/v1/managers/cities/by-country-id/{country_id}")
        cities_data = response.get("cities", [])
        return [CityDetail.model_validate(item) for item in cities_data]
