"""Products resource for the Zid SDK.

Provides core CRUD operations for products including listing, retrieval,
creation, updating, deletion, and bulk updates.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any

from zid.models.product._base import Product, ProductSettings
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource
from zid.resources.products._categories import ProductCategoriesSubResource
from zid.resources.products._images import ProductImagesSubResource
from zid.resources.products._stocks import ProductStocksSubResource
from zid.resources.products._variants import ProductVariantsSubResource
from zid.resources.products._customizations import ProductCustomizationsSubResource
from zid.resources.products._notifications import ProductNotificationsSubResource
from zid.resources.products._vouchers import ProductVouchersSubResource
from zid.resources.products._attributes import ProductAttributesSubResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class ProductsResource(BaseResource):
    """Resource for managing store products.

    Provides core CRUD operations on products and access to product
    sub-resources (vouchers, categories, images, stocks, etc.).

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List products
        for product in client.products.list():
            print(product.name)

        # Get a single product
        product = client.products.get("product-uuid")
        print(product.price)

        # Create a product
        product = client.products.create(
            name="Wireless Headphones",
            price=257,
            sku="WH-1000XM5",
        )
        ```
    """

    token_header: str = "Access-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the products resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)
        self._base_path = "/v1/products"

        # Sub-resources
        self.vouchers = ProductVouchersSubResource(client)
        self.categories = ProductCategoriesSubResource(client)
        self.images = ProductImagesSubResource(client)
        self.stocks = ProductStocksSubResource(client)
        self.variants = ProductVariantsSubResource(client)
        self.customizations = ProductCustomizationsSubResource(client)
        self.notifications = ProductNotificationsSubResource(client)
        self.attributes = ProductAttributesSubResource(client)

    def list(
        self,
        *,
        page: int | None = None,
        page_size: int | None = None,
        product_class: str | None = None,
        is_published: bool | None = None,
        search: str | None = None,
        ordering: str | None = None,
        extended: bool | None = None,
        structure: str | None = None,
        barcode: str | None = None,
        in_stock: bool | None = None,
        quantity: int | None = None,
        sale_price__isnull: bool | None = None,
        search_price_type: str | None = None,
        search_price_value: str | None = None,
        search_quantity_type: str | None = None,
        search_quantity_value: int | None = None,
        locations: str | None = None,
        id__in: list[str] | None = None,
        is_infinite: bool | None = None,
        deleted: bool | None = None,
        is_purchasable: bool | None = None,
        category_id: int | None = None,
        currency: str | None = None,
        fields: str | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[Product]:
        """List all products with pagination and filtering.

        Args:
            page: Page number (1-indexed).
            page_size: Number of items per page (default 10).
            product_class: Filter by product class
                (``"voucher"``, ``"grouped_product"``, ``"downloadable"``,
                ``"dynamic_bundle"``).
            is_published: Filter by published status.
            search: Search products by name.
            ordering: Sort field (``"created_at"`` or ``"updated_at"``).
            extended: When ``True``, includes extended data such as variants.
            structure: Filter by structure type
                (``"standalone"``, ``"parent"``, ``"child"``).
            barcode: Filter by barcode.
            in_stock: Filter by stock availability.
            quantity: Filter by quantity.
            sale_price__isnull: Filter by whether sale price is null.
            search_price_type: Price comparison operator (``"gt"``, ``"lt"``, ``"eq"``).
            search_price_value: Price value for comparison.
            search_quantity_type: Quantity comparison operator (``"gt"``, ``"lt"``, ``"eq"``).
            search_quantity_value: Quantity value for comparison.
            locations: Comma-separated location identifiers.
            id__in: List of product IDs to include.
            is_infinite: Filter products with infinite stock.
            deleted: Include or exclude deleted products.
            is_purchasable: Filter by purchasability.
                .. deprecated:: Use other filters instead.
            category_id: Filter by category ID.
                .. deprecated:: Use category filtering via other means.
            currency: Filter by currency code (e.g. ``"USD"``).
                .. deprecated::
            fields: Comma-separated list of fields to include in response.
                .. deprecated::
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding Product instances.

        Example:
            ```python
            # List all published products
            for product in client.products.list(is_published=True):
                print(product.name)

            # Search with extended data (includes variants)
            for product in client.products.list(search="headphones", extended=True):
                print(product.id, product.variants)
            ```
        """
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if product_class is not None:
            params["product_class"] = product_class
        if is_published is not None:
            params["is_published"] = is_published
        if search is not None:
            params["search"] = search
        if ordering is not None:
            params["ordering"] = ordering
        if extended is not None:
            params["extended"] = extended
        if structure is not None:
            params["structure"] = structure
        if barcode is not None:
            params["barcode"] = barcode
        if in_stock is not None:
            params["in_stock"] = in_stock
        if quantity is not None:
            params["quantity"] = quantity
        if sale_price__isnull is not None:
            params["sale_price__isnull"] = sale_price__isnull
        if search_price_type is not None:
            params["search_price_type"] = search_price_type
        if search_price_value is not None:
            params["search_price_value"] = search_price_value
        if search_quantity_type is not None:
            params["search_quantity_type"] = search_quantity_type
        if search_quantity_value is not None:
            params["search_quantity_value"] = search_quantity_value
        if locations is not None:
            params["locations"] = locations
        if id__in is not None:
            params["id__in"] = ",".join(id__in)
        if is_infinite is not None:
            params["is_infinite"] = is_infinite
        if deleted is not None:
            params["deleted"] = deleted
        if is_purchasable is not None:
            warnings.warn("is_purchasable is deprecated", DeprecationWarning, stacklevel=2)
            params["is_purchasable"] = is_purchasable
        if category_id is not None:
            warnings.warn("category_id is deprecated", DeprecationWarning, stacklevel=2)
            params["category_id"] = category_id
        if currency is not None:
            warnings.warn("currency is deprecated", DeprecationWarning, stacklevel=2)
            params["currency"] = currency
        if fields is not None:
            warnings.warn("fields is deprecated", DeprecationWarning, stacklevel=2)
            params["fields"] = fields
        params.update(kwargs)

        return self._list(
            f"{self._base_path}/",
            Product.model_validate,
            params=params if params else None,
            results_key="results",
        )

    def get(self, product_id: str) -> Product:
        """Retrieve a single product by ID.

        Args:
            product_id: The unique identifier (UUID) of the product.

        Returns:
            Product instance with full details.

        Raises:
            ZidNotFoundError: If the product does not exist.

        Example:
            ```python
            product = client.products.get("a1477bb2-72ea-4be9-b2cf-093cefc721bb")
            print(product.name, product.price)
            ```
        """
        path = f"{self._base_path}/{product_id}/"
        response = self._get(path)
        return Product.model_validate(response)

    def create(
        self,
        *,
        name: str,
        price: float,
        sku: str,
        sale_price: float | None = None,
        is_draft: bool | None = None,
        is_infinite: bool | None = None,
        quantity: int | None = None,
        requires_shipping: bool | None = None,
        is_taxable: bool | None = None,
    ) -> Product:
        """Create a new product.

        Args:
            name: Product name displayed to customers.
            price: Base product price before discounts or tax.
            sku: Stock Keeping Unit (must be unique per store).
            sale_price: Discounted price (must be less than ``price``).
            is_draft: If ``True``, save as draft without publishing.
            is_infinite: Whether the product has unlimited stock.
            quantity: Available stock quantity (required if ``is_infinite`` is ``False``).
            requires_shipping: Whether the product requires shipping.
            is_taxable: Whether tax is applied to the product.

        Returns:
            The newly created Product instance.

        Raises:
            ZidValidationError: If required fields are missing or invalid
                (e.g., duplicate SKU).

        Example:
            ```python
            product = client.products.create(
                name="Wireless Headphones",
                price=257,
                sku="WH-1000XM5",
                sale_price=199,
                quantity=50,
                requires_shipping=True,
            )
            print(product.id)
            ```
        """
        data: dict[str, Any] = {
            "name": name,
            "price": price,
            "sku": sku,
        }
        if sale_price is not None:
            data["sale_price"] = sale_price
        if is_draft is not None:
            data["is_draft"] = is_draft
        if is_infinite is not None:
            data["is_infinite"] = is_infinite
        if quantity is not None:
            data["quantity"] = quantity
        if requires_shipping is not None:
            data["requires_shipping"] = requires_shipping
        if is_taxable is not None:
            data["is_taxable"] = is_taxable

        response = self._client.post(
            f"{self._base_path}/", json=data, token_header="X-Manager-Token",
        )
        return Product.model_validate(response)

    def update(
        self,
        product_id: str,
        *,
        name: dict[str, str] | None = None,
        price: float | None = None,
        sale_price: float | None = None,
        sku: str | None = None,
        is_draft: bool | None = None,
        is_infinite: bool | None = None,
        quantity: int | None = None,
        requires_shipping: bool | None = None,
        is_taxable: bool | None = None,
    ) -> Product:
        """Update an existing product.

        Args:
            product_id: The unique identifier (UUID) of the product.
            name: Localized product name (e.g., ``{"ar": "منتج", "en": "Product"}``).
            price: Base selling price.
            sale_price: Discounted price (must be less than ``price``).
            sku: Stock Keeping Unit.
            is_draft: Whether the product is a draft.
            is_infinite: Whether the product has unlimited stock.
            quantity: Available stock quantity.
            requires_shipping: Whether the product requires shipping.
            is_taxable: Whether tax is applied.

        Returns:
            The updated Product instance.

        Raises:
            ZidNotFoundError: If the product does not exist.
            ZidValidationError: If the update payload is invalid.

        Example:
            ```python
            product = client.products.update(
                "a497974d-1755-423a-b06c-e0578ba8c318",
                name={"ar": "منتج", "en": "Product"},
                price=299,
            )
            print(product.price)
            ```
        """
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if price is not None:
            data["price"] = price
        if sale_price is not None:
            data["sale_price"] = sale_price
        if sku is not None:
            data["sku"] = sku
        if is_draft is not None:
            data["is_draft"] = is_draft
        if is_infinite is not None:
            data["is_infinite"] = is_infinite
        if quantity is not None:
            data["quantity"] = quantity
        if requires_shipping is not None:
            data["requires_shipping"] = requires_shipping
        if is_taxable is not None:
            data["is_taxable"] = is_taxable

        path = f"{self._base_path}/{product_id}/"
        response = self._update(path, json=data, method="PATCH")
        return Product.model_validate(response)

    def delete(self, product_id: str) -> None:
        """Delete a product by ID.

        Args:
            product_id: The unique identifier (UUID) of the product.

        Returns:
            None (HTTP 204 on success).

        Raises:
            ZidNotFoundError: If the product does not exist.

        Example:
            ```python
            client.products.delete("51fcad4c-9f9d-4ac5-be7c-38c7a6684ec3")
            ```
        """
        path = f"{self._base_path}/{product_id}/"
        self._delete(path)

    def bulk_update(self, products: list[dict[str, Any]]) -> list[Product]:
        """Bulk update multiple products at once.

        Each dict in the list should contain at least an ``id`` or ``sku``
        to identify the product, plus the fields to update.

        Args:
            products: List of product update dicts. Each dict may include
                ``id``, ``sku``, ``name``, ``price``, ``sale_price``, ``cost``,
                ``is_draft``, ``quantity``, ``is_infinite``, ``weight``,
                ``keywords``, ``requires_shipping``, ``is_published``, etc.

        Returns:
            List of updated Product instances.

        Raises:
            ZidValidationError: If any product update is invalid (e.g., sale
                price exceeds price). Max 50 products per request.

        Example:
            ```python
            updated = client.products.bulk_update([
                {
                    "id": "a497974d-1755-423a-b06c-e0578ba8c318",
                    "price": 299,
                    "is_published": True,
                },
                {
                    "sku": "WH-1000XX3",
                    "quantity": 100,
                },
            ])
            for product in updated:
                print(product.id, product.price)
            ```
        """
        response = self._update(
            f"{self._base_path}/",
            json=products,
            method="PATCH",
        )
        if isinstance(response, list):
            return [Product.model_validate(item) for item in response]
        return [Product.model_validate(item) for item in response.get("results", response)]

    def get_settings(self) -> ProductSettings:
        """Retrieve store-level product configuration settings.

        Returns:
            ProductSettings instance with store configuration.

        Example:
            ```python
            settings = client.products.get_settings()
            print(settings.default_products_ordering)
            print(settings.is_wishlist_enabled)
            ```
        """
        response = self._client.get(
            f"{self._base_path}/settings/", token_header="X-Manager-Token",
        )
        return ProductSettings.model_validate(response["settings"])
    def set_manual_order(
        self,
        *,
        products: list[str],
        category: int | None = None,
    ) -> None:
        """Set a custom display order for products.

        Accepts an ordered list of product UUIDs that defines the manual
        sort order. Optionally scope the ordering to a specific category.

        Args:
            products: Ordered list of product IDs (UUIDs) defining the
                desired display sequence.
            category: Category ID to scope the ordering to. When provided,
                the manual order applies only within that category.

        Returns:
            None on success.

        Raises:
            ZidValidationError: If the products list is empty or contains
                invalid IDs.

        Example:
            ```python
            client.products.set_manual_order(
                products=[
                    "d22fb4a6-cbcf-464c-8877-6cbf3df52056",
                    "d22fb4a6-cbcf-46g5-8877-6c367f52053",
                ],
                category=42,
            )
            ```
        """
        data: dict[str, Any] = {"products": products}
        if category is not None:
            data["category"] = category
        self._create(f"{self._base_path}/ordering/", json=data)

    def reset_manual_order(self) -> None:
        """Reset any manual product ordering for the store.

        Removes all custom sorting previously set via
        :meth:`set_manual_order`, reverting products to the default
        ordering.

        Returns:
            None (HTTP 204 on success).

        Example:
            ```python
            client.products.reset_manual_order()
            ```
        """
        self._delete(f"{self._base_path}/ordering/")

    def export_all(self) -> None:
        """Email all products to the store owner as a CSV export.

        Triggers an asynchronous export. For merchants on the current
        dashboard the file is sent via email; on the new dashboard it
        can be downloaded from *Settings → Export Requests*.

        Returns:
            None (HTTP 204 on success).

        Example:
            ```python
            client.products.export_all()
            ```
        """
        self._create(f"{self._base_path}/export/")

    def import_file(
        self,
        *,
        file: tuple[str, bytes, str],
        response_type: str = "json",
        delete_old_products: bool | None = None,
    ) -> None:
        """Import products from a CSV or XLSX file.

        Args:
            file: Tuple of ``(filename, content, content_type)``.
                Accepted formats: ``.csv``, ``.xlsx``.
            response_type: Response format (``"json"`` or ``"xml"``).
                Defaults to ``"json"``.
            delete_old_products: When ``True``, all existing products are
                deleted before importing. Defaults to ``False`` on the API
                side when omitted.

        Returns:
            None on success.

        Raises:
            ZidValidationError: If the file format is invalid or required
                columns are missing.

        Example:
            ```python
            with open("products.csv", "rb") as f:
                client.products.import_file(
                    file=("products.csv", f.read(), "text/csv"),
                )
            ```
        """
        data: dict[str, Any] = {"response_type": response_type}
        if delete_old_products is not None:
            data["delete_old_products"] = delete_old_products
        self._client.upload(
            f"{self._base_path}/import/",
            files={"file": file},
            data=data,
            token_header=self.token_header,
        )

