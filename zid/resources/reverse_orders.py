"""Reverse orders resource for the Zid SDK.

This module provides the ReverseOrdersResource class for managing
returns and refunds through the Zid API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.reverse_order import (
    ReverseOrder,
    ReverseOrderReason,
    ReverseOrderTotals,
    ReverseOrderProductUpdate,
)
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class ReverseOrdersResource(BaseResource):
    """Resource for managing reverse orders (returns/refunds).

    Provides methods for creating reverse orders, managing reasons,
    creating waybills, calculating refund totals, and processing refunds.

    Note:
        This resource uses the Access-Token header instead of X-Manager-Token.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List reverse order reasons
        reasons = client.reverse_orders.list_reasons()
        for reason in reasons:
            print(reason.id, reason.name)

        # Calculate refund totals before creating reverse order
        totals = client.reverse_orders.calculate_totals(
            order_id=12345,
            is_partial=False,
        )
        for item in totals.invoice:
            print(item.title, item.value_string)

        # Create a reverse order
        reverse_order = client.reverse_orders.create(
            order_id=12345,
            consignee_name="John Doe",
            consignee_mobile="+966500000001",
            consignee_city_id=1,
            consignee_address_1="123 Main St",
            consignee_address_2="Apt 4",
            inventory_location_id="location-uuid",
            reason=[{"id": "reason-uuid", "name": "Damaged"}],
        )

        # Create a refund
        reverse_order = client.reverse_orders.refund(
            order_reverse_id=reverse_order.id,
            amount=199.56,
            payment_method="zid_bank_transfer",
        )
        ```
    """

    # Reverse orders endpoints use Access-Token header
    token_header: str = "Access-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the reverse orders resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)
        self._base_path = "/v1/managers/store/reverse-orders"

    def create(
        self,
        *,
        order_id: int,
        consignee_name: str,
        consignee_mobile: str,
        consignee_city_id: int,
        consignee_address_1: str,
        consignee_address_2: str | None = None,
        inventory_location_id: str | None = None,
        reason: list[dict[str, str]] | None = None,
        is_partial: bool | None = None,
        refund_payment_method: str | None = None,
        products: list[dict[str, Any]] | None = None,
        packages_count: int | None = None,
        shipping_method: str | None = None,
    ) -> ReverseOrder:
        """Create a reverse order (return request).

        Args:
            order_id: The ID of the order to reverse.
            consignee_name: Name of the consignee.
            consignee_mobile: Mobile number of the consignee.
            consignee_city_id: City ID of the consignee.
            consignee_address_1: Primary address line.
            consignee_address_2: Secondary address line.
            inventory_location_id: Inventory location ID for multi-inventory stores.
            reason: List of reasons for the reverse order.
                Each reason should be a dict with "id" and "name" keys.
            is_partial: Whether this is a partial return.
            refund_payment_method: Payment method for refund
                (e.g., "zid_bank_transfer", "credit_card", "cash").
            products: List of products to return for partial returns.
                Each product should have "order_product_id" and "quantity".
            packages_count: Number of packages.
            shipping_method: Shipping method for return.

        Returns:
            Created ReverseOrder instance.

        Raises:
            ZidValidationError: If required fields are missing or invalid.

        Example:
            ```python
            reverse_order = client.reverse_orders.create(
                order_id=12345,
                consignee_name="John Doe",
                consignee_mobile="+966500000001",
                consignee_city_id=1,
                consignee_address_1="123 Main St",
                consignee_address_2="Apt 4",
                inventory_location_id="location-uuid",
                reason=[{"id": "reason-uuid", "name": "Damaged"}],
            )
            print(reverse_order.id, reverse_order.reverse_total)
            ```
        """
        data: dict[str, Any] = {
            "order_id": order_id,
            "consignee_name": consignee_name,
            "consignee_mobile": consignee_mobile,
            "consignee_city_id": consignee_city_id,
            "consignee_address_1": consignee_address_1,
        }

        if consignee_address_2 is not None:
            data["consignee_address_2"] = consignee_address_2
        if inventory_location_id is not None:
            data["inventory_location_id"] = inventory_location_id
        if reason is not None:
            data["reason"] = reason
        if is_partial is not None:
            data["is_partial"] = is_partial
        if refund_payment_method is not None:
            data["refund_payment_method"] = refund_payment_method
        if products is not None:
            data["products"] = products
        if packages_count is not None:
            data["packages_count"] = packages_count
        if shipping_method is not None:
            data["shipping_method"] = shipping_method

        response = self._create(self._base_path, json=data)
        return ReverseOrder.model_validate(response["order_reverse"])

    def create_waybill(
        self,
        *,
        order_id: int,
        is_standalone_zidship_waybill: bool = False,
    ) -> ReverseOrder:
        """Create a waybill for a reverse order.

        Args:
            order_id: The ID of the order.
            is_standalone_zidship_waybill: Whether this is a standalone ZidShip waybill.

        Returns:
            ReverseOrder with waybill information.

        Example:
            ```python
            reverse_order = client.reverse_orders.create_waybill(
                order_id=12345,
                is_standalone_zidship_waybill=False,
            )
            print(reverse_order.waybill)
            ```
        """
        path = f"{self._base_path}/waybill"
        data = {
            "order_id": order_id,
            "is_standalone_zidship_waybill": is_standalone_zidship_waybill,
        }

        response = self._create(path, data=data)
        return ReverseOrder.model_validate(response)

    def add_reason(self, *, name: str) -> ReverseOrderReason:
        """Add a new reverse order reason.

        Args:
            name: The name/description of the reason.

        Returns:
            Created ReverseOrderReason instance.

        Example:
            ```python
            reason = client.reverse_orders.add_reason(name="Customer not responding")
            print(reason.id, reason.name)
            ```
        """
        path = f"{self._base_path}/reasons"
        response = self._create(path, data={"name": name})
        return ReverseOrderReason.model_validate(response["order_reverse_reason"])

    def list_reasons(self, *, name: str | None = None) -> list[ReverseOrderReason]:
        """List reverse order reasons.

        Args:
            name: Filter reasons by name (optional).

        Returns:
            List of ReverseOrderReason instances.

        Example:
            ```python
            reasons = client.reverse_orders.list_reasons()
            for reason in reasons:
                print(reason.id, reason.name)

            # Filter by name
            damaged_reasons = client.reverse_orders.list_reasons(name="damaged")
            ```
        """
        path = f"{self._base_path}/reasons"
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name

        response = self._get(path, params=params if params else None)
        reasons_data = response.get("order_reverse_reasons", [])
        return [ReverseOrderReason.model_validate(r) for r in reasons_data]

    def calculate_totals(
        self,
        *,
        order_id: int,
        is_partial: bool | int = False,
        products: list[dict[str, Any]] | None = None,
    ) -> ReverseOrderTotals:
        """Calculate refund totals for a reverse order.

        Use this before creating a reverse order to preview refund amounts.

        Args:
            order_id: The ID of the order.
            is_partial: Whether this is a partial return (0 or 1, or bool).
            products: List of products for partial returns.
                Each product should have "order_product_id" and "quantity".

        Returns:
            ReverseOrderTotals with invoice breakdown.

        Example:
            ```python
            # Full return
            totals = client.reverse_orders.calculate_totals(order_id=12345)
            for item in totals.invoice:
                print(f"{item.title}: {item.value_string}")

            # Partial return
            totals = client.reverse_orders.calculate_totals(
                order_id=12345,
                is_partial=True,
                products=[
                    {"order_product_id": 111, "quantity": 1},
                ],
            )
            ```
        """
        # This endpoint uses a different path and X-Manager-Token header
        path = "/v1/managers/reverse-credit-note/totals"
        data: dict[str, Any] = {
            "order_id": order_id,
            "is_partial": 1 if is_partial else 0,
        }

        if products is not None:
            # API expects form-encoded array format
            for i, product in enumerate(products):
                data[f"products[{i}][order_product_id]"] = product["order_product_id"]
                data[f"products[{i}][quantity]"] = product["quantity"]

        # Use X-Manager-Token for this endpoint
        response = self._client.post(
            path,
            data=data,
            token_header="X-Manager-Token",
        )
        return ReverseOrderTotals.model_validate(response)

    def refund(
        self,
        *,
        order_reverse_id: str,
        amount: float,
        payment_method: str,
        notes: str | None = None,
        bank_transfer_receipt: str | None = None,
    ) -> ReverseOrder:
        """Create a refund for a reverse order.

        Args:
            order_reverse_id: The ID of the reverse order.
            amount: Refund amount (should not exceed refund_total).
            payment_method: Payment method for refund. Options:
                - "credit_card"
                - "zid_bank_transfer"
                - "bank_transfer"
                - "cash"
                - "zid_cod"
            notes: Optional notes for the refund.
            bank_transfer_receipt: Bank transfer receipt (for bank_transfer method).

        Returns:
            Updated ReverseOrder with refund information.

        Note:
            If payment_method is "zid_bank_transfer", you may need to upload
            a bank receipt separately.

        Example:
            ```python
            reverse_order = client.reverse_orders.refund(
                order_reverse_id="reverse-uuid",
                amount=199.56,
                payment_method="zid_bank_transfer",
                notes="Refund processed via bank transfer",
            )
            print(reverse_order.refund)
            ```
        """
        path = f"{self._base_path}/refund"
        data: dict[str, Any] = {
            "order_reverse_id": order_reverse_id,
            "amount": amount,
            "payment_method": payment_method,
        }

        if notes is not None:
            data["notes"] = notes
        if bank_transfer_receipt is not None:
            data["bank_transfer_receipt"] = bank_transfer_receipt

        response = self._create(path, data=data)
        return ReverseOrder.model_validate(response["order_reverse"])
    def upload_bank_receipt(
        self,
        *,
        refund_id: str,
        file: bytes,
        filename: str = "receipt.png",
        content_type: str = "image/png",
    ) -> "BankReceiptUploadResponse":
        """Upload a bank transfer receipt for a refund.

        This endpoint is used after a refund has been created using the
        zid_bank_transfer payment method. It associates the uploaded receipt
        file with the refund and updates the related reverse order.

        Args:
            refund_id: The UUID of the refund to attach the receipt to.
            file: The receipt file content as bytes.
            filename: The filename for the upload (default: "receipt.png").
            content_type: The MIME type of the file. Allowed formats:
                image/jpeg, image/jpg, image/png, image/gif, image/bmp, image/webp.
                Maximum file size is 5 MB.

        Returns:
            BankReceiptUploadResponse with updated reverse order and refund info.

        Note:
            This endpoint is mandatory when the refund payment method is
            `zid_bank_transfer`. Only image files are supported.

        Example:
            ```python
            # Read receipt image
            with open("receipt.png", "rb") as f:
                receipt_bytes = f.read()

            # Upload the receipt
            result = client.reverse_orders.upload_bank_receipt(
                refund_id="f3a9b2d4-92f7-4d1b-a123-abc123456789",
                file=receipt_bytes,
                filename="bank_receipt.png",
                content_type="image/png",
            )
            print(result.order_reverse.refund.bank_transfer_receipt)
            ```
        """
        from zid.models.reverse_order import BankReceiptUploadResponse

        path = f"{self._base_path}/refund/upload-bank-receipt"

        response = self._client.upload(
            path,
            files={"bank_transfer_receipt": (filename, file, content_type)},
            data={"refund_id": refund_id},
            token_header=self.token_header,
        )

        return BankReceiptUploadResponse.model_validate(response.get("data", response))

    def update_products(
        self,
        *,
        order_reverse_id: str,
        products: list[ReverseOrderProductUpdate | dict[str, Any]],
    ) -> ReverseOrder:
        """Update received status and condition quantities for products in a reverse order.

        This endpoint is used after a reverse order has been created and the returned
        products are physically processed. It allows specifying how many items were:
        - Received in good condition
        - Not received
        - Received but damaged

        These values are critical for final refund reconciliation, inventory adjustments,
        and return auditing.

        Args:
            order_reverse_id: The UUID of the reverse order being updated.
            products: List of products with their quantity updates. Each product must have:
                - id: The UUID of the product record in order_reverse_products
                - received_quantity: Number of items received in good condition
                - not_received_quantity: Number of items expected but not received
                - damaged_quantity: Number of items received but damaged

        Returns:
            Updated ReverseOrder with the new product quantities.

        Note:
            - Each product must belong to the specified reverse order
            - For each product: received_quantity + not_received_quantity + damaged_quantity
              must be <= reversed_quantity
            - At least one quantity must be greater than 0
            - Updates are atomic - if one product fails validation, the entire request fails

        Example:
            ```python
            reverse_order = client.reverse_orders.update_products(
                order_reverse_id="64d0f002-0185-4fd1-94d2-e3a86be622c9",
                products=[
                    {
                        "id": "af9e0150-1c56-4a1b-87e9-846d6a0acf19",
                        "received_quantity": 1,
                        "not_received_quantity": 0,
                        "damaged_quantity": 0,
                    },
                ],
            )
            for product in reverse_order.products:
                print(f"Product {product.id}: received={product.received_quantity}")
            ```
        """
        path = f"{self._base_path}/products"

        # Convert ReverseOrderProductUpdate models to dicts if needed
        products_data = []
        for product in products:
            if isinstance(product, ReverseOrderProductUpdate):
                products_data.append(product.model_dump())
            else:
                products_data.append(product)

        data = {
            "order_reverse_id": order_reverse_id,
            "products": products_data,
        }

        response = self._update(path, json=data)
        return ReverseOrder.model_validate(response["order_reverse"])


