"""Stores resource for the Zid SDK.

This module provides the StoresResource class for interacting with
the Zid Store Profile API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from zid.models.store import StoreProfile, VATSettings
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class StoresResource(BaseResource):
    """Resource for accessing store profile information.

    Provides access to the authenticated store's profile, including
    manager info, store settings, and subscription details.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # Get store profile
        profile = client.stores.get_profile()
        print(profile.user.name)  # Manager name
        print(profile.user.store.title)  # Store name
        print(profile.user.store.subscription.package_name.en)  # Plan name
        ```
    """

    # Uses default X-Manager-Token header
    token_header: str = "X-Manager-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the stores resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)

    def get_profile(self) -> StoreProfile:
        """Retrieve the current store's profile.

        Returns the profile data of the authenticated Manager, including
        detailed information about the Manager, their role, associated store,
        and the set of permissions they hold.

        Returns:
            StoreProfile instance with manager and store details.

        Raises:
            ZidAuthenticationError: If the token is invalid.
            ZidAuthorizationError: If the user doesn't have permission.

        Example:
            ```python
            profile = client.stores.get_profile()
            
            # Access manager info
            print(f"Manager: {profile.user.name}")
            print(f"Email: {profile.user.email}")
            
            # Access store info
            store = profile.user.store
            print(f"Store: {store.title}")
            print(f"URL: {store.url}")
            print(f"Currency: {store.currency.code}")
            
            # Access subscription info
            sub = store.subscription
            print(f"Plan: {sub.package_name.en}")
            print(f"Expires: {sub.expired_at}")
            print(f"Suspended: {sub.is_suspended}")
            ```
        """
        path = "/v1/managers/account/profile"
        response = self._get(path)
        return StoreProfile.model_validate(response)

    def get_vat_settings(self) -> VATSettings:
        """Retrieve VAT settings for the store.

        Returns the VAT configuration for the store, including whether VAT
        is enabled, tax percentages, and country-specific VAT settings.

        Returns:
            VATSettings instance with tax configuration.

        Raises:
            ZidAuthenticationError: If the token is invalid.
            ZidAuthorizationError: If the user doesn't have permission.

        Example:
            ```python
            vat = client.stores.get_vat_settings()
            
            # Check if VAT is enabled
            if vat.tax_settings:
                print(f"VAT Active: {vat.tax_settings.vat_activate}")
                print(f"Can Use VAT: {vat.tax_settings.can_use_vat}")
                print(f"VAT in Price: {vat.tax_settings.is_vat_included_in_product_price}")
                
                # List country-specific settings
                if vat.tax_settings.countries:
                    for country in vat.tax_settings.countries:
                        name = country.country.name.en if country.country and country.country.name else "Unknown"
                        print(f"  {name}: {country.tax_percentage}% (VAT: {country.vat_number})")
            ```
        """
        path = "/v1/managers/store/third-party/vat"
        response = self._get(path)
        return VATSettings.model_validate(response)
