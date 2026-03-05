"""Attributes sub-resource for the Zid SDK.

Provides methods for managing product attributes, attribute presets,
product-level metafields, and product badges.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.product._attribute import Attribute, AttributePreset, Badge, Metafield
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class ProductAttributesSubResource(BaseResource):
    """Sub-resource for managing product attributes, presets, metafields, and badges.

    Accessed via ``client.products.attributes``.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all store attributes
        for attr in client.products.attributes.list():
            print(attr.name, attr.preset_count)

        # Get a specific attribute with its presets
        attr = client.products.attributes.get("cfb5bd3f-bbc5-4439-a171-b2d70e1c0293")
        for preset in attr.presets:
            print(preset.value)
        ```
    """

    token_header: str = "Access-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the attributes sub-resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)

    def list(
        self,
        *,
        page: int | None = None,
        page_size: int | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[Attribute]:
        """List all product attributes for the store.

        Args:
            page: Page number (1-indexed).
            page_size: Number of items per page.
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding Attribute instances.

        Example:
            ```python
            for attr in client.products.attributes.list():
                print(attr.name, attr.is_enabled)
            ```
        """
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        params.update(kwargs)

        return self._list(
            "/v1/attributes/",
            Attribute.model_validate,
            params=params if params else None,
            results_key="results",
        )
    def create(
        self,
        *,
        name: str | dict[str, str],
        slug: str | None = None,
        is_extra: bool | None = None,
        is_enabled: bool | None = None,
        display_order: int | None = None,
    ) -> Attribute:
        """Create a new product attribute.

        Args:
            name: Attribute display name. Can be a plain string or a
                localized dict (e.g., ``{"ar": "الوزن", "en": "Weight"}``).
            slug: URL-friendly identifier. Auto-generated from name
                if omitted.
            is_extra: Whether this is an extra attribute.
            is_enabled: Whether the attribute is active. Defaults to
                ``True`` on the API side.
            display_order: Display ordering position.

        Returns:
            The newly created Attribute instance.

        Raises:
            ZidValidationError: If the payload is invalid.

        Example:
            ```python
            attr = client.products.attributes.create(
                name="Weight",
                slug="weight",
                is_enabled=True,
            )
            print(attr.id, attr.slug)
            ```
        """
        data: dict[str, Any] = {"name": name}
        if slug is not None:
            data["slug"] = slug
        if is_extra is not None:
            data["is_extra"] = is_extra
        if is_enabled is not None:
            data["is_enabled"] = is_enabled
        if display_order is not None:
            data["display_order"] = display_order
        response = self._create("/v1/attributes/", json=data)
        return Attribute.model_validate(response)

    def get(self, attribute_id: str) -> Attribute:
        """Retrieve a specific attribute by ID.

        Args:
            attribute_id: The unique identifier (UUID) of the attribute.

        Returns:
            Attribute instance with its presets.

        Raises:
            ZidNotFoundError: If the attribute does not exist.

        Example:
            ```python
            attr = client.products.attributes.get("cfb5bd3f-...")
            print(attr.name, len(attr.presets))
            ```
        """
        path = f"/v1/attributes/{attribute_id}/"
        response = self._client.get(path, token_header="X-Manager-Token")
        return Attribute.model_validate(response)

    def update(
        self,
        attribute_id: str,
        *,
        name: str | None = None,
        slug: str | None = None,
        is_extra: bool | None = None,
        is_enabled: bool | None = None,
        display_order: int | None = None,
    ) -> Attribute:
        """Update an existing attribute.

        Args:
            attribute_id: The unique identifier (UUID) of the attribute.
            name: Updated display name.
            slug: Updated URL-friendly slug.
            is_extra: Whether the attribute is an extra attribute.
            is_enabled: Whether the attribute is active.
            display_order: Display ordering position.

        Returns:
            The updated Attribute instance.

        Raises:
            ZidNotFoundError: If the attribute does not exist.

        Example:
            ```python
            attr = client.products.attributes.update(
                "cfb5bd3f-...",
                name="Weight 2",
                is_enabled=False,
            )
            ```
        """
        path = f"/v1/attributes/{attribute_id}/"
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if slug is not None:
            data["slug"] = slug
        if is_extra is not None:
            data["is_extra"] = is_extra
        if is_enabled is not None:
            data["is_enabled"] = is_enabled
        if display_order is not None:
            data["display_order"] = display_order
        response = self._update(path, json=data, method="PATCH")
        return Attribute.model_validate(response)

    def delete(self, attribute_id: str) -> None:
        """Delete an attribute.

        Args:
            attribute_id: The unique identifier (UUID) of the attribute.

        Raises:
            ZidNotFoundError: If the attribute does not exist.

        Example:
            ```python
            client.products.attributes.delete("cfb5bd3f-...")
            ```
        """
        path = f"/v1/attributes/{attribute_id}/"
        self._delete(path)


    def list_presets(
        self,
        attribute_id: str,
        *,
        page: int | None = None,
        page_size: int | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[AttributePreset]:
        """List all presets for a specific attribute.

        Args:
            attribute_id: The unique identifier (UUID) of the attribute.
            page: Page number (1-indexed).
            page_size: Number of items per page.
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding AttributePreset instances.

        Example:
            ```python
            for preset in client.products.attributes.list_presets("cfb5bd3f-..."):
                print(preset.value, preset.type)
            ```
        """
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        params.update(kwargs)

        return self._list(
            f"/v1/attributes/{attribute_id}/presets/",
            AttributePreset.model_validate,
            params=params if params else None,
            results_key="results",
        )

    def update_preset(
        self,
        attribute_id: str,
        preset_id: str,
        *,
        value: dict[str, str],
    ) -> AttributePreset:
        """Update an existing attribute preset.

        Args:
            attribute_id: The unique identifier (UUID) of the attribute.
            preset_id: The unique identifier (UUID) of the preset.
            value: Localized preset value
                (e.g., ``{"ar": "أحمر", "en": "Red"}``).

        Returns:
            The updated AttributePreset instance.

        Raises:
            ZidNotFoundError: If the attribute or preset does not exist.

        Example:
            ```python
            preset = client.products.attributes.update_preset(
                "cfb5bd3f-...",
                "4469e2f3-...",
                value={"ar": "الحجم", "en": "Size"},
            )
            print(preset.value)
            ```
        """
        path = f"/v1/attributes/{attribute_id}/presets/{preset_id}/"
        data: dict[str, Any] = {"value": value}
        response = self._client.patch(
            path, json=data, token_header="X-Manager-Token",
        )
        return AttributePreset.model_validate(response)

    def create_preset(
        self,
        attribute_id: str,
        *,
        value: dict[str, str],
    ) -> AttributePreset:
        """Create a new attribute preset.

        Args:
            attribute_id: The unique identifier (UUID) of the attribute.
            value: Localized preset value
                (e.g., ``{"ar": "اللون", "en": "color"}``).

        Returns:
            The newly created AttributePreset instance.

        Example:
            ```python
            preset = client.products.attributes.create_preset(
                "cfb5bd3f-...",
                value={"ar": "اللون", "en": "color"},
            )
            print(preset.id)
            ```
        """
        path = f"/v1/attributes/{attribute_id}/presets/"
        data: dict[str, Any] = {"value": value}
        response = self._create(path, json=data)
        return AttributePreset.model_validate(response)

    def delete_preset(self, attribute_id: str, preset_id: str) -> None:
        """Delete an attribute preset.

        Args:
            attribute_id: The unique identifier (UUID) of the attribute.
            preset_id: The unique identifier (UUID) of the preset.

        Raises:
            ZidNotFoundError: If the attribute or preset does not exist.

        Example:
            ```python
            client.products.attributes.delete_preset("cfb5bd3f-...", "4469e2f3-...")
            ```
        """
        path = f"/v1/attributes/{attribute_id}/presets/{preset_id}/"
        self._delete(path)


    def list_metafields(
        self,
        *,
        page: int | None = None,
        page_size: int | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[Metafield]:
        """List product-level attribute assignments (metafields).

        Args:
            page: Page number (1-indexed).
            page_size: Number of items per page.
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding Metafield instances.

        Example:
            ```python
            for mf in client.products.attributes.list_metafields():
                print(mf.name, mf.value)
            ```
        """
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        params.update(kwargs)

        return self._list(
            "/v1/Metafields/",
            Metafield.model_validate,
            params=params if params else None,
            results_key="results",
        )

    def create_metafield(
        self,
        *,
        name: dict[str, str],
    ) -> Metafield:
        """Create a new product-level attribute (metafield).

        Args:
            name: Localized attribute name
                (e.g., ``{"ar": "اللون", "en": "Color"}``).

        Returns:
            The newly created Metafield instance.

        Raises:
            ZidValidationError: If the payload is invalid.

        Example:
            ```python
            mf = client.products.attributes.create_metafield(
                name={"ar": "اللون", "en": "Color"},
            )
            print(mf.id)
            ```
        """
        data: dict[str, Any] = {"name": name}
        response = self._create("/v1/Metafields", json=data)
        return Metafield.model_validate(response)

    def list_badges(self, **kwargs: Any) -> list[Badge]:
        """List all predefined product badges for the store.

        Args:
            **kwargs: Additional query parameters.

        Returns:
            List of Badge instances.

        Example:
            ```python
            badges = client.products.attributes.list_badges()
            for badge in badges:
                print(badge.body)
            ```
        """
        response = self._get("/v1/badges/", params=kwargs if kwargs else None)
        items = response.get("data", [])
        return [Badge.model_validate(item) for item in items]
