"""Product categories sub-resource for the Zid SDK.

Provides methods for managing store categories and product-category
assignments, including CRUD on categories and assigning/removing
products from categories.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.product._category import (
    AssignedCategory,
    Category,
    CategoryDetail,
    ShortCategory,
)
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class ProductCategoriesSubResource(BaseResource):
    """Sub-resource for managing store categories and product-category assignments.

    Store-level category management endpoints (list, get, create, update,
    publish, detach) use ``X-Manager-Token``. Product-level assignment
    endpoints (assign, bulk_assign, remove) use ``Access-Token``.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all store categories
        categories = client.products.categories.list()
        for cat in categories:
            print(cat.name, cat.products_count)

        # Assign a product to a category
        assigned = client.products.categories.assign(
            product_id="prod-uuid",
            category_id=1473477,
        )
        ```
    """

    token_header: str = "Access-Token"

    _MANAGER_CATEGORIES_PATH = "/v1/managers/store/categories"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the categories sub-resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)

    def list(self) -> list[Category]:
        """List all store categories.

        Fetches all categories for the store including names, SEO info,
        product counts, sub-categories, and metafields.

        Returns:
            List of Category instances.

        Example:
            ```python
            categories = client.products.categories.list()
            for cat in categories:
                print(cat.name, cat.products_count)
            ```
        """
        response = self._client.get(
            self._MANAGER_CATEGORIES_PATH,
            token_header="X-Manager-Token",
        )
        items = response.get("categories", [])
        return [Category.model_validate(item) for item in items]

    def get(self, category_id: int) -> CategoryDetail:
        """Retrieve detailed information about a specific category.

        Args:
            category_id: The unique identifier of the category.

        Returns:
            CategoryDetail instance with full category information.

        Raises:
            ZidNotFoundError: If the category does not exist.

        Example:
            ```python
            category = client.products.categories.get(1473477)
            print(category.names.en, category.is_published)
            ```
        """
        path = f"{self._MANAGER_CATEGORIES_PATH}/{category_id}/view"
        response = self._client.get(path, token_header="X-Manager-Token")
        return CategoryDetail.model_validate(response["categories"])

    def create(
        self,
        *,
        name_ar: str,
        name_en: str,
        description_ar: str,
        description_en: str,
        parent_id: int | None = None,
    ) -> CategoryDetail:
        """Create a new store category (subcategory).

        The category name must be unique across all categories.

        Args:
            name_ar: Category name in Arabic.
            name_en: Category name in English.
            description_ar: Category description in Arabic.
            description_en: Category description in English.
            parent_id: ID of the parent category to nest under.

        Returns:
            The newly created CategoryDetail instance.

        Raises:
            ZidValidationError: If the category name is already in use.

        Example:
            ```python
            category = client.products.categories.create(
                name_ar="إلكترونيات",
                name_en="Electronics",
                description_ar="أجهزة إلكترونية",
                description_en="Electronic devices",
            )
            print(category.id)
            ```
        """
        data: dict[str, Any] = {
            "name[ar]": name_ar,
            "name[en]": name_en,
            "description[ar]": description_ar,
            "description[en]": description_en,
        }
        if parent_id is not None:
            data["parent_id"] = str(parent_id)

        path = f"{self._MANAGER_CATEGORIES_PATH}/add"
        response = self._client.post(
            path, data=data, token_header="X-Manager-Token",
        )
        return CategoryDetail.model_validate(response["category"])

    def update(
        self,
        category_id: int,
        *,
        name_ar: str,
        name_en: str,
        description_ar: str,
        description_en: str,
    ) -> CategoryDetail:
        """Update an existing store category.

        Args:
            category_id: The unique identifier of the category.
            name_ar: Updated category name in Arabic.
            name_en: Updated category name in English.
            description_ar: Updated category description in Arabic.
            description_en: Updated category description in English.

        Returns:
            The updated CategoryDetail instance.

        Raises:
            ZidNotFoundError: If the category does not exist.
            ZidValidationError: If the update payload is invalid.

        Example:
            ```python
            category = client.products.categories.update(
                1486524,
                name_ar="Hello World",
                name_en="Hello World",
                description_ar="Hello World",
                description_en="Hello World",
            )
            print(category.name)
            ```
        """
        data: dict[str, Any] = {
            "name[ar]": name_ar,
            "name[en]": name_en,
            "description[ar]": description_ar,
            "description[en]": description_en,
            "_method": "put",
        }

        path = f"{self._MANAGER_CATEGORIES_PATH}/{category_id}/update"
        response = self._client.post(
            path, data=data, token_header="X-Manager-Token",
        )
        return CategoryDetail.model_validate(response["category"])

    def publish(self, category_id: int, *, is_published: bool) -> dict[str, Any]:
        """Publish or unpublish a category.

        Args:
            category_id: The unique identifier of the category.
            is_published: ``True`` to publish, ``False`` to unpublish.

        Returns:
            API response dict with status and message.

        Raises:
            ZidNotFoundError: If the category does not exist.

        Example:
            ```python
            client.products.categories.publish(1486524, is_published=True)
            ```
        """
        path = f"{self._MANAGER_CATEGORIES_PATH}/{category_id}/publishing"
        return self._client.put(
            path,
            json={"is_published": "1" if is_published else "0"},
            token_header="X-Manager-Token",
        )

    def detach_all_products(self, category_id: int) -> CategoryDetail:
        """Detach a category from all products.

        Disassociates the category from every product it is linked to.
        The category itself is not deleted.

        Args:
            category_id: The unique identifier of the category.

        Returns:
            The CategoryDetail after detachment (products_count will be 0).

        Raises:
            ZidNotFoundError: If the category does not exist.

        Example:
            ```python
            category = client.products.categories.detach_all_products(1473477)
            print(category.products_count)  # 0
            ```
        """
        path = f"{self._MANAGER_CATEGORIES_PATH}/{category_id}/products/delete"
        response = self._client.delete(path, token_header="X-Manager-Token")
        return CategoryDetail.model_validate(response["category"])

    def assign(self, product_id: str, *, category_id: int) -> AssignedCategory:
        """Assign a product to a category.

        Args:
            product_id: The unique identifier (UUID) of the product.
            category_id: The ID of the category to assign.

        Returns:
            AssignedCategory instance representing the assignment.

        Raises:
            ZidNotFoundError: If the product or category does not exist.

        Example:
            ```python
            assigned = client.products.categories.assign(
                "a7ad89d0-03e2-430f-b6e4-0624ef05e571",
                category_id=1473477,
            )
            print(assigned.name)
            ```
        """
        path = f"/v1/products/{product_id}/categories/"
        response = self._client.post(
            path, json={"id": category_id}, token_header=self.token_header,
        )
        return AssignedCategory.model_validate(response)

    def bulk_assign(self, product_id: str, *, category_ids: list[int]) -> None:
        """Assign a product to multiple categories at once.

        Args:
            product_id: The unique identifier (UUID) of the product.
            category_ids: List of category IDs to assign.

        Returns:
            None (HTTP 200 on success with empty body).

        Raises:
            ZidNotFoundError: If the product does not exist.
            ZidValidationError: If any category ID is invalid.

        Example:
            ```python
            client.products.categories.bulk_assign(
                "a7ad89d0-03e2-430f-b6e4-0624ef05e571",
                category_ids=[1473476, 1323795],
            )
            ```
        """
        path = f"/v1/products/{product_id}/categories/bulk-add/"
        self._client.patch(
            path, json={"ids": category_ids}, token_header=self.token_header,
        )

    def remove(self, product_id: str, category_id: int) -> None:
        """Remove a product from a category.

        Disassociates the category from the product. The category
        itself is not deleted.

        Args:
            product_id: The unique identifier (UUID) of the product.
            category_id: The ID of the category to remove.

        Returns:
            None (HTTP 204 on success).

        Raises:
            ZidNotFoundError: If the product or category does not exist.

        Example:
            ```python
            client.products.categories.remove(
                "a7ad89d0-03e2-430f-b6e4-0624ef05e571",
                1473477,
            )
            ```
        """
        path = f"/v1/products/{product_id}/categories/{category_id}/"
        self._delete(path)
