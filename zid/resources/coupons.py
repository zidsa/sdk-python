"""Coupons resource for the Zid SDK.

This module provides the CouponsResource class for interacting with
the Zid Coupons API — list, view, create, update, and delete coupons.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.coupon import Coupon, CouponDetail, CouponStatus, DiscountType
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class CouponsResource(BaseResource):
    """Resource for managing store coupons.

    Provides full CRUD access to coupons including listing, viewing details,
    creating, updating, and deleting coupons.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all coupons (paginated)
        for coupon in client.coupons.list():
            print(coupon.code, coupon.discount)

        # Get a specific coupon with detail
        detail = client.coupons.get(12345)
        print(detail.total_sales, detail.total_customers)

        # Create a new coupon
        coupon = client.coupons.create(
            name="Summer Sale",
            code="SUMMER2026",
            discount_type="p",
            discount="20",
            free_shipping="1",
            free_cod="0",
            total="100",
            date_start="2026-07-01",
            date_end="2026-07-31",
            uses_total=100,
            uses_customer=3,
            apply_to="all",
            status="1",
            applying_method="CODE",
            conditions="",
            max_total="0",
            max_weight=0,
        )
        ```
    """

    token_header: str = "X-Manager-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the coupons resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)
        self._base_path = "/v1/managers/store/coupons"

    def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        search_term: str | None = None,
        total_usage_value: int | None = None,
        total_usage_compare: str | None = None,
        discount_status: CouponStatus | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        date_attribute: str | None = None,
        order_by: str | None = None,
        sort_type: str | None = None,
        discount_type: DiscountType | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[Coupon]:
        """List all coupons with pagination.

        Args:
            page: Page number for pagination (1-indexed).
            per_page: Number of items per page.
            search_term: Term to search for specific coupons.
            total_usage_value: Filter by total usage count.
            total_usage_compare: Comparison operator for total usage (">", "<", "=").
            discount_status: Filter by coupon status.
            date_from: Start date for date range filter (YYYY-MM-DD).
            date_to: End date for date range filter (YYYY-MM-DD).
            date_attribute: Date attribute to filter on ("date_start" or "date_end").
            order_by: Field to order results by.
            sort_type: Sort direction ("asc" or "desc").
            discount_type: Filter by discount type ("f" or "p").
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding Coupon instances.

        Example:
            ```python
            # List active coupons
            for coupon in client.coupons.list(discount_status="coupon_active"):
                print(coupon.code)

            # Search coupons
            for coupon in client.coupons.list(search_term="SUMMER"):
                print(coupon.name)
            ```
        """
        params: dict[str, Any] = {}

        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if search_term is not None:
            params["search_term"] = search_term
        if total_usage_value is not None:
            params["total_usage_value"] = total_usage_value
        if total_usage_compare is not None:
            params["total_usage_compare"] = total_usage_compare
        if discount_status is not None:
            params["discount_status"] = discount_status
        if date_from is not None:
            params["date_from"] = date_from
        if date_to is not None:
            params["date_to"] = date_to
        if date_attribute is not None:
            params["date_attribute"] = date_attribute
        if order_by is not None:
            params["order_by"] = order_by
        if sort_type is not None:
            params["sort_type"] = sort_type
        if discount_type is not None:
            params["discount_type"] = discount_type

        params.update(kwargs)

        return self._list(
            self._base_path,
            Coupon.model_validate,
            params=params if params else None,
            results_key="coupons",
        )

    def get(self, coupon_id: int) -> CouponDetail:
        """Retrieve a specific coupon by ID with full details.

        Args:
            coupon_id: The unique identifier of the coupon.

        Returns:
            CouponDetail instance with orders, sales, and customer data.

        Raises:
            ZidNotFoundError: If the coupon does not exist.

        Example:
            ```python
            coupon = client.coupons.get(12345)
            print(coupon.code, coupon.total_sales)
            ```
        """
        path = f"{self._base_path}/{coupon_id}/view"
        response = self._get(path)
        return CouponDetail.model_validate(response["coupon"])

    def create(
        self,
        *,
        name: str,
        code: str,
        discount_type: DiscountType,
        discount: str,
        free_shipping: str,
        free_cod: str,
        total: str,
        date_start: str,
        date_end: str,
        uses_total: int,
        uses_customer: int,
        apply_to: str,
        status: str,
        applying_method: str,
        conditions: str,
        max_total: str,
        max_weight: int | float,
        apply_to_array: list[str] | None = None,
        is_mazeed_active: int | bool | None = None,
        is_pos_active: int | bool | None = None,
        is_mobile_app_active: int | bool | None = None,
        maximum_discount_value: float | None = None,
    ) -> CouponDetail:
        """Create a new coupon.

        Args:
            name: Coupon name for merchant reference.
            code: Unique coupon code.
            discount_type: Discount type ("f" for fixed, "p" for percentage).
            discount: Discount value as string.
            free_shipping: "1" to enable free shipping, "0" to disable.
            free_cod: "1" to enable free COD, "0" to disable.
            total: Minimum cart total required (as string).
            date_start: Start date (YYYY-MM-DD).
            date_end: End date (YYYY-MM-DD).
            uses_total: Maximum total uses.
            uses_customer: Maximum uses per customer.
            apply_to: Where coupon applies ("all", "products", "categories", etc.).
            status: "1" to activate, "0" to deactivate.
            applying_method: Application method ("CODE" or "AUTOMATIC").
            conditions: Coupon conditions as string.
            max_total: Maximum cart total for coupon to apply (as string).
            max_weight: Maximum cart weight in kg for free shipping coupons.
                The API stores this value in grams (input is multiplied
                by 1000 server-side).
            apply_to_array: Product UIDs or category IDs the coupon applies to.
            is_mazeed_active: 1/True to activate in Mazeed, 0/False to deactivate.
            is_pos_active: 1/True to activate in POS, 0/False to deactivate.
            is_mobile_app_active: 1/True to activate in mobile app, 0/False to deactivate.
            maximum_discount_value: Maximum discount value cap.
                Only effective for percentage coupons (``discount_type="p"``).

        Returns:
            CouponDetail instance of the created coupon.

        Raises:
            ZidValidationError: If required fields are missing or invalid.

        Example:
            ```python
            coupon = client.coupons.create(
                name="Summer Sale",
                code="SUMMER2026",
                discount_type="p",
                discount="20",
                free_shipping="1",
                free_cod="0",
                total="100",
                date_start="2026-07-01",
                date_end="2026-07-31",
                uses_total=100,
                uses_customer=3,
                apply_to="all",
                status="1",
                applying_method="CODE",
                conditions="",
                max_total="0",
                max_weight=0,
            )
            print(coupon.id, coupon.code)
            ```
        """
        data: dict[str, Any] = {
            "name": name,
            "code": code,
            "discount_type": discount_type,
            "discount": discount,
            "free_shipping": free_shipping,
            "free_cod": free_cod,
            "total": total,
            "date_start": date_start,
            "date_end": date_end,
            "uses_total": uses_total,
            "uses_customer": uses_customer,
            "apply_to": apply_to,
            "status": status,
            "applying_method": applying_method,
            "conditions": conditions,
            "max_total": max_total,
            "max_weight": max_weight,
        }

        if apply_to_array is not None:
            data["apply_to_array"] = apply_to_array
        if is_mazeed_active is not None:
            data["is_mazeed_active"] = self._bool_to_form(is_mazeed_active)
        if is_pos_active is not None:
            data["is_pos_active"] = self._bool_to_form(is_pos_active)
        if is_mobile_app_active is not None:
            data["is_mobile_app_active"] = self._bool_to_form(is_mobile_app_active)
        if maximum_discount_value is not None:
            data["maximum_discount_value"] = maximum_discount_value

        response = self._create(f"{self._base_path}/add", data=data)
        return CouponDetail.model_validate(response["coupon"])

    @staticmethod
    def _bool_to_form(value: bool | int | str) -> str:
        """Convert a boolean/int/str to a form-data-safe ``"1"``/``"0"`` string.

        The Zid API expects ``"1"`` or ``"0"`` for boolean fields when sent
        as ``multipart/form-data``.  Python ``True``/``False`` would be
        serialised as ``"True"``/``"False"`` which the API rejects.
        """
        if isinstance(value, bool):
            return "1" if value else "0"
        if isinstance(value, int):
            return "1" if value else "0"
        # Already a string — pass through ("1", "0", "true", "false", …)
        return str(value)

    def update(
        self,
        coupon_id: int,
        *,
        name: str,
        code: str,
        discount_type: DiscountType,
        discount: str,
        free_shipping: str | None = None,
        free_cod: str | None = None,
        total: str | None = None,
        max_total: str | None = None,
        max_weight: int | float | None = None,
        date_start: str | None = None,
        date_end: str | None = None,
        uses_total: str | None = None,
        uses_customer: str | None = None,
        status: str | None = None,
        apply_to: str | None = None,
        applying_method: str | None = None,
        apply_to_array: list[str] | None = None,
        maximum_discount_value: float | None = None,
        is_mazeed_active: bool | int | str | None = None,
        is_pos_active: bool | int | str | None = None,
        is_shown_in_pos: bool | int | str | None = None,
        is_mobile_app_active: bool | int | str | None = None,
        conditions: list[str] | None = None,
        conditions_criteria: str | None = None,
    ) -> CouponDetail:
        """Update an existing coupon.

        The update endpoint uses POST (not PUT). Only ``name``, ``code``,
        ``discount_type``, and ``discount`` are required; all other fields
        are optional.

        Args:
            coupon_id: The unique identifier of the coupon to update.
            name: Coupon name.
            code: Unique coupon code.
            discount_type: Discount type ("f", "p", or "n").
            discount: Discount value as string.
            free_shipping: "1" to enable free shipping, "0" to disable.
            free_cod: Free COD flag.
            total: Minimum order total.
            max_total: Maximum cart total.
            max_weight: Maximum cart weight in kg.  The API stores this
                value in grams (input is multiplied by 1000 server-side).
            date_start: Start date (YYYY-MM-DD).
            date_end: End date (YYYY-MM-DD).
            uses_total: Maximum total uses.
            uses_customer: Maximum uses per customer.
            status: "1" for active, "0" for inactive.
            apply_to: Where coupon applies.
            applying_method: "CODE" or "AUTOMATIC".
            apply_to_array: Product/category IDs the coupon applies to.
            maximum_discount_value: Maximum discount value cap.
                Only effective for percentage coupons (``discount_type="p"``).
            is_mazeed_active: Active in Mazeed (bool, int ``1``/``0``, or str).
            is_pos_active: Active in POS (bool, int ``1``/``0``, or str).
            is_shown_in_pos: Visible in POS (bool, int ``1``/``0``, or str).
            is_mobile_app_active: Active in mobile app (bool, int ``1``/``0``, or str).
            conditions: Coupon conditions.
            conditions_criteria: Conditions criteria ("all" or "any").

        Returns:
            CouponDetail instance of the updated coupon.

        Raises:
            ZidValidationError: If fields are invalid.

        Example:
            ```python
            coupon = client.coupons.update(
                12345,
                name="Updated Sale",
                code="SUMMER2026",
                discount_type="f",
                discount="155",
            )
            print(coupon.discount)
            ```
        """
        data: dict[str, Any] = {
            "name": name,
            "code": code,
            "discount_type": discount_type,
            "discount": discount,
        }

        if free_shipping is not None:
            data["free_shipping"] = free_shipping
        if free_cod is not None:
            data["free_cod"] = free_cod
        if total is not None:
            data["total"] = total
        if max_total is not None:
            data["max_total"] = max_total
        if max_weight is not None:
            data["max_weight"] = max_weight
        if date_start is not None:
            data["date_start"] = date_start
        if date_end is not None:
            data["date_end"] = date_end
        if uses_total is not None:
            data["uses_total"] = uses_total
        if uses_customer is not None:
            data["uses_customer"] = uses_customer
        if status is not None:
            data["status"] = status
        if apply_to is not None:
            data["apply_to"] = apply_to
        if applying_method is not None:
            data["applying_method"] = applying_method
        if apply_to_array is not None:
            data["apply_to_array"] = apply_to_array
        if maximum_discount_value is not None:
            data["maximum_discount_value"] = maximum_discount_value
        if is_mazeed_active is not None:
            data["is_mazeed_active"] = self._bool_to_form(is_mazeed_active)
        if is_pos_active is not None:
            data["is_pos_active"] = self._bool_to_form(is_pos_active)
        if is_shown_in_pos is not None:
            data["is_shown_in_pos"] = self._bool_to_form(is_shown_in_pos)
        if is_mobile_app_active is not None:
            data["is_mobile_app_active"] = self._bool_to_form(is_mobile_app_active)
        if conditions is not None:
            data["conditions"] = conditions
        if conditions_criteria is not None:
            data["conditions_criteria"] = conditions_criteria

        # Update endpoint uses POST, not PUT
        path = f"{self._base_path}/{coupon_id}/update"
        response = self._create(path, data=data)
        return CouponDetail.model_validate(response["coupon"])

    def delete(self, coupon_id: int) -> bool:
        """Delete a coupon.

        Args:
            coupon_id: The unique identifier of the coupon to delete.

        Returns:
            True if the coupon was deleted successfully.

        Raises:
            ZidNotFoundError: If the coupon does not exist.

        Example:
            ```python
            client.coupons.delete(12345)
            ```
        """
        path = f"{self._base_path}/{coupon_id}"
        self._delete(path)
        return True
