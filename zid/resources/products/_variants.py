"""Product variants sub-resource for the Zid SDK.

Provides methods for creating product variants. Creating variants
on a standalone product converts it into a parent product.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.product._base import Product
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class ProductVariantsSubResource(BaseResource):
    """Sub-resource for creating product variants.

    Access via ``client.products.variants``.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # Create variants for a product
        product = client.products.variants.create(
            "product-uuid",
            variants=[
                {
                    "sku": "WH-BLK",
                    "price": 199,
                    "attributes": [
                        {"slug": "color", "value": {"en": "Black", "ar": "اسود"}}
                    ],
                    "stocks": [
                        {
                            "location": "location-uuid",
                            "available_quantity": 50,
                            "is_infinite": False,
                        }
                    ],
                }
            ],
        )
        print(product.structure)  # "parent"
        ```
    """

    token_header: str = "Access-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the product variants sub-resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)

    def create(
        self,
        product_id: str,
        *,
        variants: list[dict[str, Any]],
    ) -> Product:
        """Create one or more variants for a product.

        If the product is standalone (has no variants), this operation
        converts it into a parent product. Each variant is defined by
        its attributes, pricing, stock, and optional metadata.

        Variants require pre-existing product attributes and their
        preset choices. Create those first via
        ``client.products.attributes``.

        Args:
            product_id: The unique identifier (UUID) of the product.
            variants: List of variant dicts. Each may include:

                - ``id`` (str | None): Existing variant UUID to update.
                  Omit when creating new variants.
                - ``is_deleted`` (bool): Mark variant as deleted.
                  Defaults to ``False``.
                - ``sku`` (str | None): SKU for the variant. Auto-generated
                  if omitted.
                - ``price`` (float | None): Selling price.
                - ``sale_price`` (float | None): Discounted price.
                - ``cost`` (float | None): Internal cost for margin tracking.
                - ``barcode`` (str | None): Barcode value.
                - ``attributes`` (list[dict]): **Required.** Attribute
                  definitions, each with ``slug`` (str) and ``value``
                  (dict with ``ar``/``en`` keys).
                - ``stocks`` (list[dict]): Stock entries, each with
                  ``location`` (str UUID), ``available_quantity`` (int),
                  and ``is_infinite`` (bool).
                - ``weight`` (dict): Weight with ``unit`` (str) and
                  ``value`` (float | None).

        Returns:
            The updated Product instance (now with ``structure="parent"``
            and populated ``variants`` list).

        Raises:
            ZidValidationError: If attribute slugs don't exist, barcodes
                are invalid, or the product has vouchers attached.

        Example:
            ```python
            product = client.products.variants.create(
                "a1477bb2-72ea-4be9-b2cf-093cefc721bb",
                variants=[
                    {
                        "sku": "WH-WHT",
                        "price": 144,
                        "attributes": [
                            {
                                "slug": "اللون",
                                "value": {"ar": "ابيض", "en": "White"},
                            }
                        ],
                        "stocks": [
                            {
                                "location": "e2629f14-12ad-4ee4-8103-9db7290c4ccc",
                                "available_quantity": 44,
                                "is_infinite": False,
                            }
                        ],
                        "weight": {"unit": "kg", "value": None},
                    },
                    {
                        "sku": "WH-BLK",
                        "price": 144,
                        "sale_price": 122,
                        "attributes": [
                            {
                                "slug": "اللون",
                                "value": {"ar": "اسود", "en": "Black"},
                            }
                        ],
                        "stocks": [
                            {
                                "location": "e2629f14-12ad-4ee4-8103-9db7290c4ccc",
                                "available_quantity": 77,
                                "is_infinite": False,
                            }
                        ],
                    },
                ],
            )
            for variant in product.variants:
                print(variant.sku, variant.price)
            ```
        """
        path = f"/v1/products/{product_id}/variants/"
        response = self._create(path, json={"variants": variants})
        return Product.model_validate(response)
