"""Product images sub-resource for the Zid SDK.

Provides methods for listing, uploading, reordering, and deleting
product images.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.product._base import ProductImage
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class ProductImagesSubResource(BaseResource):
    """Sub-resource for managing product images.

    Access via ``client.products.images``.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all images for a product
        for image in client.products.images.list("product-uuid"):
            print(image.id, image.alt_text)

        # Upload an image
        with open("photo.jpg", "rb") as f:
            image = client.products.images.upload(
                "product-uuid",
                image=("photo.jpg", f.read(), "image/jpeg"),
                alt_text="Front view",
            )

        # Reorder an image
        image = client.products.images.update_order(
            "product-uuid",
            "image-uuid",
            display_order=3,
        )

        # Delete an image
        client.products.images.delete("product-uuid", "image-uuid")
        ```
    """

    token_header: str = "Access-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the product images sub-resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)

    def list(
        self,
        product_id: str,
        *,
        page: int | None = None,
        page_size: int = 15,
        **kwargs: Any,
    ) -> PaginatedIterator[ProductImage]:
        """List all images for a product.

        Args:
            product_id: The unique identifier (UUID) of the product.
            page: Page number (1-indexed).
            page_size: Number of items per page (max 100, default 15).
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding ProductImage instances.

        Raises:
            ZidNotFoundError: If the product does not exist.

        Example:
            ```python
            for image in client.products.images.list("product-uuid"):
                print(image.id, image.image.full_size)
            ```
        """
        params: dict[str, Any] = {"page_size": page_size}
        if page is not None:
            params["page"] = page
        params.update(kwargs)

        path = f"/v1/products/{product_id}/images/"
        return self._list(
            path,
            ProductImage.model_validate,
            params=params if params else None,
            results_key="results",
        )

    def update_order(
        self,
        product_id: str,
        image_id: str,
        *,
        display_order: int,
    ) -> ProductImage:
        """Update the display order of a product image.

        Args:
            product_id: The unique identifier (UUID) of the product.
            image_id: The unique identifier (UUID) of the image.
            display_order: New display position. Lower values appear first.

        Returns:
            Updated ProductImage instance.

        Raises:
            ZidNotFoundError: If the product or image does not exist.

        Example:
            ```python
            image = client.products.images.update_order(
                "product-uuid",
                "image-uuid",
                display_order=1,
            )
            print(image.display_order)
            ```
        """
        path = f"/v1/products/{product_id}/images/{image_id}/"
        response = self._update(
            path,
            json={"display_order": display_order},
            method="PATCH",
        )
        return ProductImage.model_validate(response)

    def upload(
        self,
        product_id: str,
        *,
        image: tuple[str, bytes, str],
        alt_text: str,
    ) -> ProductImage:
        """Upload a new image to a product.

        Args:
            product_id: The unique identifier (UUID) of the product.
            image: Tuple of ``(filename, content, content_type)``.
                Example: ``("photo.jpg", file_bytes, "image/jpeg")``.
            alt_text: Descriptive text for the image, used for
                accessibility and SEO.

        Returns:
            The newly created ProductImage instance.

        Raises:
            ZidValidationError: If the image or alt_text is invalid.

        Example:
            ```python
            with open("photo.jpg", "rb") as f:
                image = client.products.images.upload(
                    "product-uuid",
                    image=("photo.jpg", f.read(), "image/jpeg"),
                    alt_text="Front view of product",
                )
            print(image.id, image.display_order)
            ```
        """
        path = f"/v1/products/{product_id}/images/"
        response = self._client.upload(
            path,
            files={"image": image},
            data={"alt_text": alt_text},
            token_header=self.token_header,
        )
        return ProductImage.model_validate(response)

    def delete(self, product_id: str, image_id: str) -> None:
        """Delete a product image.

        Args:
            product_id: The unique identifier (UUID) of the product.
            image_id: The unique identifier (UUID) of the image.

        Returns:
            None (HTTP 204 on success).

        Raises:
            ZidNotFoundError: If the product or image does not exist.

        Example:
            ```python
            client.products.images.delete("product-uuid", "image-uuid")
            ```
        """
        path = f"/v1/products/{product_id}/images/{image_id}/"
        self._delete(path)
