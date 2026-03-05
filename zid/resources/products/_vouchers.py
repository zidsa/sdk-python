"""Vouchers sub-resource for the Zid SDK.

Provides methods for managing digital product vouchers including
listing, creating, updating, deleting, importing, and exporting.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.product._voucher import OrderVoucher, Voucher
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class ProductVouchersSubResource(BaseResource):
    """Sub-resource for managing digital product vouchers.

    Vouchers are unique codes attached to digital products. Each voucher
    has a key that is delivered to the customer upon purchase.

    Access via ``client.products.vouchers``.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List vouchers for a product
        for voucher in client.products.vouchers.list("product-uuid"):
            print(voucher.key, voucher.status)

        # Create a voucher
        voucher = client.products.vouchers.create(
            "product-uuid",
            key="ABC123",
            status="AVAILABLE",
        )
        ```
    """

    token_header: str = "Access-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the vouchers sub-resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)

    def list(
        self,
        product_id: str,
        *,
        page: int | None = None,
        page_size: int | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[Voucher]:
        """List all vouchers for a product.

        Args:
            product_id: UUID of the product.
            page: Page number (1-indexed).
            page_size: Number of items per page.
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding Voucher instances.

        Raises:
            ZidValidationError: If the product is not a voucher-type product.

        Example:
            ```python
            for voucher in client.products.vouchers.list("product-uuid"):
                print(voucher.key, voucher.status)
            ```
        """
        path = f"/v1/products/{product_id}/vouchers/"
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        params.update(kwargs)

        return self._list(
            path,
            Voucher.model_validate,
            params=params if params else None,
            results_key="results",
        )

    def create(
        self,
        product_id: str,
        *,
        key: str,
        status: str,
        serial_number: str | None = None,
        pin_code: str | None = None,
        order: str | None = None,
        expires_at: str | None = None,
    ) -> Voucher:
        """Create a new voucher for a product.

        Args:
            product_id: UUID of the product.
            key: Unique voucher code delivered to the customer.
            status: Voucher status (``AVAILABLE``, ``SOLD``, ``RESERVED``,
                or ``RETURNED``).
            serial_number: Optional identification code (like an SKU).
            pin_code: Optional secondary secret code for extra security.
            order: Optional order ID to associate with the voucher.
            expires_at: Optional expiration date (ISO 8601 format).

        Returns:
            The created Voucher instance.

        Raises:
            ZidValidationError: If the key already exists for this product.

        Example:
            ```python
            voucher = client.products.vouchers.create(
                "product-uuid",
                key="GIFT-CODE-001",
                status="AVAILABLE",
                pin_code="1234",
                expires_at="2026-12-31T00:00:00Z",
            )
            ```
        """
        path = f"/v1/products/{product_id}/vouchers/"
        data: dict[str, Any] = {"key": key, "status": status}
        if serial_number is not None:
            data["serial_number"] = serial_number
        if pin_code is not None:
            data["pin_code"] = pin_code
        if order is not None:
            data["order"] = order
        if expires_at is not None:
            data["expires_at"] = expires_at

        response = self._create(path, json=data)
        return Voucher.model_validate(response)

    def update(
        self,
        product_id: str,
        voucher_id: str,
        *,
        key: str,
        status: str | None = None,
        serial_number: str | None = None,
        pin_code: str | None = None,
        expires_at: str | None = None,
    ) -> Voucher:
        """Update an existing voucher.

        Args:
            product_id: UUID of the product.
            voucher_id: UUID of the voucher to update.
            key: Updated voucher code (required).
            status: Updated voucher status.
            serial_number: Updated serial number.
            pin_code: Updated pin code.
            expires_at: Updated expiration date (ISO 8601 format).

        Returns:
            Updated Voucher instance.

        Raises:
            ZidNotFoundError: If the voucher does not exist.

        Example:
            ```python
            voucher = client.products.vouchers.update(
                "product-uuid",
                "voucher-uuid",
                key="UPDATED-KEY",
                status="SOLD",
            )
            ```
        """
        path = f"/v1/products/{product_id}/vouchers/{voucher_id}/"
        data: dict[str, Any] = {"key": key}
        if status is not None:
            data["status"] = status
        if serial_number is not None:
            data["serial_number"] = serial_number
        if pin_code is not None:
            data["pin_code"] = pin_code
        if expires_at is not None:
            data["expires_at"] = expires_at

        response = self._update(path, json=data, method="PATCH")
        return Voucher.model_validate(response)

    def delete(self, product_id: str, voucher_id: str) -> None:
        """Delete a voucher.

        Args:
            product_id: UUID of the product.
            voucher_id: UUID of the voucher to delete.

        Returns:
            None.

        Raises:
            ZidNotFoundError: If the voucher does not exist.

        Example:
            ```python
            client.products.vouchers.delete("product-uuid", "voucher-uuid")
            ```
        """
        path = f"/v1/products/{product_id}/vouchers/{voucher_id}/"
        self._delete(path)

    def import_file(
        self,
        product_id: str,
        *,
        file: tuple[str, bytes, str],
    ) -> None:
        """Import vouchers from a CSV or Excel file.

        The file must contain the required columns: ``key``, ``pin_code``,
        ``status``. Optional columns: ``expires_at``, ``serial_number``,
        ``created_at``, ``updated_at``.

        Args:
            product_id: UUID of the product.
            file: Tuple of ``(filename, content, content_type)``.
                Accepted extensions: ``.csv``, ``.xls``, ``.xlsx``.

        Returns:
            None (201 response on success).

        Raises:
            ZidValidationError: If the file extension is not supported.

        Example:
            ```python
            with open("vouchers.csv", "rb") as f:
                client.products.vouchers.import_file(
                    "product-uuid",
                    file=("vouchers.csv", f.read(), "text/csv"),
                )
            ```
        """
        path = f"/v1/products/{product_id}/vouchers/import/"
        self._client.upload(
            path,
            files={"file": file},
            token_header=self.token_header,
        )

    def export(
        self,
        product_id: str,
        *,
        email: str | None = None,
    ) -> dict[str, Any]:
        """Export vouchers to an Excel file.

        The exported file is sent to the specified email address, or the
        store owner's email if not provided.

        Args:
            product_id: UUID of the product.
            email: Email address to send the export to.

        Returns:
            Response dict (empty on success).

        Example:
            ```python
            client.products.vouchers.export(
                "product-uuid",
                email="merchant@example.com",
            )
            ```
        """
        path = f"/v1/products/{product_id}/vouchers/export/"
        data: dict[str, Any] = {}
        if email is not None:
            data["email"] = email

        return self._create(path, json=data)

    def get_order_vouchers(
        self,
        order_id: str,
        *,
        page: int | None = None,
        page_size: int | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[OrderVoucher]:
        """Get vouchers associated with a specific order.

        Args:
            order_id: The order ID.
            page: Page number (1-indexed).
            page_size: Number of items per page.
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding OrderVoucher instances.

        Example:
            ```python
            for voucher in client.products.vouchers.get_order_vouchers("64855100"):
                print(voucher.key, voucher.status)
            ```
        """
        path = f"/v1/order-vouchers/{order_id}/"
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        params.update(kwargs)

        return self._list(
            path,
            OrderVoucher.model_validate,
            params=params if params else None,
            results_key="results",
        )
