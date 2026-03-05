"""Orders resource for the Zid SDK.

This module provides the OrdersResource class for interacting with
the Zid Orders API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, overload

if TYPE_CHECKING:
    from zid.http import HTTPClient

from zid.models.order import (
    CreditNote,
    CustomOrderStatus,
    Order,
    OrderCreateAddress,
    OrderCreateAddressMeta,
    OrderCreateConsignee,
    OrderCreateCustomer,
    OrderCreatePaymentMethod,
    OrderCreateProduct,
    OrderCreateShippingMethod,
    OrderPos,
    OrderPrint,
    OrderPrintSummary,
    OrderSimple,
    OrderTiny,
    PayloadType,
)
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource


class OrdersResource(BaseResource):
    """Resource for managing store orders.

    Provides access to order data including listing, retrieval, and status updates.
    Supports different payload types for optimized responses.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List orders with default (simple) payload
        for order in client.orders.list():
            print(order.id, order.order_status.code)

        # List orders with full details including products
        for order in client.orders.list(payload_type="default"):
            print(order.id, order.products)

        # Get a specific order
        order = client.orders.get(12345)
        print(order.customer.name)

        # Update order status
        order = client.orders.update_status(12345, order_status="preparing")
        ```
    """

    # Uses default X-Manager-Token header
    token_header: str = "X-Manager-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the orders resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)
        self._base_path = "/v1/managers/store/orders"

    # --- List method overloads for type safety ---

    @overload
    def list(
        self,
        *,
        payload_type: Literal["default"],
        page: int | None = ...,
        per_page: int | None = ...,
        order_status: str | None = ...,
        payment_status: str | None = ...,
        payment_method: str | None = ...,
        customer_id: int | None = ...,
        date_from: str | None = ...,
        date_to: str | None = ...,
        sort_by: str | None = ...,
        search_term: str | None = ...,
        source: str | None = ...,
        **kwargs: Any,
    ) -> PaginatedIterator[Order]: ...

    @overload
    def list(
        self,
        *,
        payload_type: Literal["tiny"],
        page: int | None = ...,
        per_page: int | None = ...,
        order_status: str | None = ...,
        payment_status: str | None = ...,
        payment_method: str | None = ...,
        customer_id: int | None = ...,
        date_from: str | None = ...,
        date_to: str | None = ...,
        sort_by: str | None = ...,
        search_term: str | None = ...,
        source: str | None = ...,
        **kwargs: Any,
    ) -> PaginatedIterator[OrderTiny]: ...

    @overload
    def list(
        self,
        *,
        payload_type: Literal["pos"],
        page: int | None = ...,
        per_page: int | None = ...,
        order_status: str | None = ...,
        payment_status: str | None = ...,
        payment_method: str | None = ...,
        customer_id: int | None = ...,
        date_from: str | None = ...,
        date_to: str | None = ...,
        sort_by: str | None = ...,
        search_term: str | None = ...,
        source: str | None = ...,
        **kwargs: Any,
    ) -> PaginatedIterator[OrderPos]: ...

    @overload
    def list(
        self,
        *,
        payload_type: Literal["print"],
        page: int | None = ...,
        per_page: int | None = ...,
        order_status: str | None = ...,
        payment_status: str | None = ...,
        payment_method: str | None = ...,
        customer_id: int | None = ...,
        date_from: str | None = ...,
        date_to: str | None = ...,
        sort_by: str | None = ...,
        search_term: str | None = ...,
        source: str | None = ...,
        **kwargs: Any,
    ) -> PaginatedIterator[OrderPrint]: ...

    @overload
    def list(
        self,
        *,
        payload_type: Literal["print_summary"],
        page: int | None = ...,
        per_page: int | None = ...,
        order_status: str | None = ...,
        payment_status: str | None = ...,
        payment_method: str | None = ...,
        customer_id: int | None = ...,
        date_from: str | None = ...,
        date_to: str | None = ...,
        sort_by: str | None = ...,
        search_term: str | None = ...,
        source: str | None = ...,
        **kwargs: Any,
    ) -> PaginatedIterator[OrderPrintSummary]: ...

    @overload
    def list(
        self,
        *,
        payload_type: Literal["simple"] | None = ...,
        page: int | None = ...,
        per_page: int | None = ...,
        order_status: str | None = ...,
        payment_status: str | None = ...,
        payment_method: str | None = ...,
        customer_id: int | None = ...,
        date_from: str | None = ...,
        date_to: str | None = ...,
        sort_by: str | None = ...,
        search_term: str | None = ...,
        source: str | None = ...,
        **kwargs: Any,
    ) -> PaginatedIterator[OrderSimple]: ...

    def list(
        self,
        *,
        payload_type: PayloadType | None = None,
        page: int | None = None,
        per_page: int | None = None,
        order_status: str | None = None,
        payment_status: str | None = None,
        payment_method: str | None = None,
        customer_id: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        sort_by: str | None = None,
        search_term: str | None = None,
        source: str | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[Any]:
        """List orders with pagination.

        Args:
            payload_type: Response detail level. Options:
                - "default": Full response with products (slowest)
                - "simple": Lightweight without products (default)
                - "tiny": Minimal, essential IDs only
                - "pos": Optimized for POS systems
                - "print": For printed invoices
                - "print_summary": Summary for receipts
            page: Page number (1-indexed).
            per_page: Items per page (max 100).
            order_status: Filter by status (new, preparing, ready, indelivery, delivered, canceled).
            payment_status: Filter by payment status (pending, paid, refunded, voided).
            payment_method: Filter by payment method code.
            customer_id: Filter by customer ID.
            date_from: Filter orders from date (ISO format).
            date_to: Filter orders to date (ISO format).
            sort_by: Sort direction (asc, desc).
            search_term: Search by customer phone, email, order code, or name.
            source: Filter by order source.
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding order instances of the appropriate type.

        Example:
            ```python
            # List with simple payload (default)
            for order in client.orders.list():
                print(order.id, order.order_status.code)

            # List with full details
            for order in client.orders.list(payload_type="default"):
                print(order.products)

            # Filter by status
            for order in client.orders.list(order_status="new"):
                print(order.id)
            ```
        """
        params: dict[str, Any] = {}

        if payload_type is not None:
            params["payload_type"] = payload_type
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if order_status is not None:
            params["order_status"] = order_status
        if payment_status is not None:
            params["payment_status"] = payment_status
        if payment_method is not None:
            params["payment_method"] = payment_method
        if customer_id is not None:
            params["customer_id"] = customer_id
        if date_from is not None:
            params["date_from"] = date_from
        if date_to is not None:
            params["date_to"] = date_to
        if sort_by is not None:
            params["sort_by"] = sort_by
        if search_term is not None:
            params["search_term"] = search_term
        if source is not None:
            params["source"] = source

        params.update(kwargs)

        # Select model based on payload_type
        model_class = self._get_model_for_payload_type(payload_type)

        return self._list(
            self._base_path,
            model_class.model_validate,
            params=params if params else None,
            results_key="orders",
        )

    def _get_model_for_payload_type(
        self, payload_type: PayloadType | None
    ) -> type[Order | OrderSimple | OrderTiny | OrderPos | OrderPrint | OrderPrintSummary]:
        """Get the appropriate model class for a payload type."""
        if payload_type == "default":
            return Order
        elif payload_type == "tiny":
            return OrderTiny
        elif payload_type == "pos":
            return OrderPos
        elif payload_type == "print":
            return OrderPrint
        elif payload_type == "print_summary":
            return OrderPrintSummary
        else:
            # Default is "simple"
            return OrderSimple


    def get(self, order_id: int) -> Order:
        """Retrieve a specific order by ID.

        Args:
            order_id: The unique identifier of the order.

        Returns:
            Order instance with full details including products.

        Raises:
            ZidNotFoundError: If the order does not exist.

        Example:
            ```python
            order = client.orders.get(12345)
            print(order.customer.name)
            print(order.products)
            ```
        """
        path = f"{self._base_path}/{order_id}/view"
        response = self._get(path)
        return Order.model_validate(response["order"])

    def update_status(
        self,
        order_id: int,
        *,
        order_status: str,
        inventory_address_id: str | None = None,
        tracking_number: str | None = None,
        tracking_url: str | None = None,
        waybill_url: str | None = None,
    ) -> Order:
        """Update the status of an order.

        Args:
            order_id: The unique identifier of the order.
            order_status: New status (new, preparing, ready, indelivery, delivered, cancelled).
            inventory_address_id: Pickup location ID (required when setting to "ready").
            tracking_number: Shipping company tracking ID.
            tracking_url: Shipping company tracking URL.
            waybill_url: Direct link for shipping waybill.

        Returns:
            Updated Order instance.

        Raises:
            ZidValidationError: If the status transition is invalid.

        Example:
            ```python
            # Move order to preparing
            order = client.orders.update_status(12345, order_status="preparing")

            # Move to ready with inventory address
            order = client.orders.update_status(
                12345,
                order_status="ready",
                inventory_address_id="abc-123"
            )
            ```
        """
        path = f"{self._base_path}/{order_id}/change-order-status"

        data: dict[str, Any] = {"order_status": order_status}
        if inventory_address_id is not None:
            data["inventory_address_id"] = inventory_address_id
        if tracking_number is not None:
            data["tracking_number"] = tracking_number
        if tracking_url is not None:
            data["tracking_url"] = tracking_url
        if waybill_url is not None:
            data["waybill_url"] = waybill_url

        response = self._create(path, json=data)
        return Order.model_validate(response["order"])

    def list_credit_notes(self, order_id: int) -> list[CreditNote]:
        """List credit notes for an order.

        Credit notes are issued for orders that have been cancelled or modified.

        Args:
            order_id: The unique identifier of the order.

        Returns:
            List of CreditNote instances.

        Example:
            ```python
            credit_notes = client.orders.list_credit_notes(12345)
            for note in credit_notes:
                print(note.invoice_number, note.order_total_string)
            ```
        """
        path = f"{self._base_path}/{order_id}/credit-notes"
        response = self._get(path)

        # Response structure: {"code": "...", "payload": {"credit_notes": [...]}}
        payload = response.get("payload", {})
        credit_notes_data = payload.get("credit_notes", [])

        return [CreditNote.model_validate(cn) for cn in credit_notes_data]

    def add_comment(self, order_id: int, comment: str) -> Order:
        """Add a comment to an order.

        Comments are visible to merchants in the order activity dashboard.
        Partners can add up to 20 comments per order, each limited to 100 characters.
        Comments are non-editable once added.

        Args:
            order_id: The unique identifier of the order.
            comment: The comment text to add (max 100 characters).

        Returns:
            Updated Order instance with the new comment in histories.

        Raises:
            ZidValidationError: If the comment exceeds 100 characters or limit reached.

        Example:
            ```python
            order = client.orders.add_comment(
                12345,
                "Customer asked to delay shipment by one day"
            )
            # Check the latest history entry
            if order.histories:
                print(order.histories[-1].description)
            ```
        """
        path = f"{self._base_path}/{order_id}/add-order-comment"
        data = {"comment": comment}
        response = self._create(path, json=data)
        return Order.model_validate(response["order"])

    def create(
        self,
        *,
        currency_code: str,
        customer: OrderCreateCustomer | dict[str, Any],
        consignee: OrderCreateConsignee | dict[str, Any],
        products: list[OrderCreateProduct | dict[str, Any]],
        shipping_method: OrderCreateShippingMethod | dict[str, Any],
        payment_method: OrderCreatePaymentMethod | dict[str, Any],
        is_gift: bool = False,
        is_gifted_consignee_notifiable: bool = True,
        created_by: str = "api",
        coupon_code: str | None = None,
        customer_comment: str | None = None,
    ) -> Order:
        """Create a new draft order.

        Creates an order on behalf of a merchant with the specified products,
        customer, shipping, and payment details.

        Args:
            currency_code: Currency code for the order (e.g., "SAR").
            customer: Customer information (name, mobile, email).
            consignee: Recipient/shipping address information.
            products: List of products with SKU and quantity.
            shipping_method: Shipping method type and ID.
            payment_method: Payment method ID.
            is_gift: Whether this is a gift order.
            is_gifted_consignee_notifiable: Whether to notify gift recipient.
            created_by: Source of order creation (default: "api").
            coupon_code: Optional coupon code to apply.
            customer_comment: Optional customer note.

        Returns:
            Created Order instance.

        Raises:
            ZidValidationError: If required fields are missing or invalid.

        Example:
            ```python
            order = client.orders.create(
                currency_code="SAR",
                customer={
                    "full_name": "John Doe",
                    "mobile_country_code": "966",
                    "mobile_number": "500000005",
                    "email": "john@example.com",
                },
                consignee={
                    "contact": {
                        "full_name": "John Doe",
                        "mobile_country_code": "966",
                        "mobile_number": "500000005",
                    },
                    "address": {
                        "line_1": "King Fahd Road",
                        "line_2": "Building 12",
                        "city_name": "Riyadh",
                        "country_code": "SA",
                    },
                },
                products=[{"sku": "PROD-SKU-123", "quantity": 1}],
                shipping_method={"type": "delivery", "id": 432480},
                payment_method={"id": 555224},
            )
            print(order.id, order.code)
            ```
        """
        # Convert models to dicts if needed
        def to_dict(obj: Any) -> dict[str, Any]:
            if hasattr(obj, "model_dump"):
                return obj.model_dump(exclude_none=True, by_alias=True)
            return obj

        data: dict[str, Any] = {
            "currency_code": currency_code,
            "created_by": created_by,
            "customer": to_dict(customer),
            "consignee": to_dict(consignee),
            "products": [to_dict(p) for p in products],
            "shipping_method": to_dict(shipping_method),
            "payment_method": to_dict(payment_method),
            "is_gift": is_gift,
            "is_gifted_consignee_notifiable": is_gifted_consignee_notifiable,
        }

        if coupon_code is not None:
            data["coupon_code"] = coupon_code
        if customer_comment is not None:
            data["customer_comment"] = customer_comment

        # Note: This endpoint uses /drafts, not /orders
        response = self._create("/v1/managers/store/drafts", json=data)
        return Order.model_validate(response["order"])

    def list_custom_statuses(self) -> list[CustomOrderStatus]:
        """List custom order statuses for the store.

        Returns main order statuses with their custom sub-statuses defined by the store.
        Custom statuses allow merchants to create sub-statuses under predefined
        parent statuses (New, Preparing, Ready, In Delivery, Delivered, Cancelled, Reversed).

        Returns:
            List of CustomOrderStatus instances, each containing the parent status
            and its custom sub-statuses.

        Example:
            ```python
            statuses = client.orders.list_custom_statuses()
            for status in statuses:
                print(f"{status.status} ({status.code})")
                if status.sub_statuses:
                    for sub in status.sub_statuses:
                        print(f"  - {sub.name} ({sub.color})")
            ```
        """
        path = f"{self._base_path}/custom-statuses"
        response = self._get(path)

        # Response structure: {"code": "...", "payload": [...]}
        payload = response.get("payload", [])
        return [CustomOrderStatus.model_validate(s) for s in payload]


