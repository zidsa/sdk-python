"""Loyalty program resource for the Zid SDK.

This module provides the LoyaltyResource class for interacting with
the Zid Loyalty Program API, including program configuration, rules
management, and customer points operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from zid.models.loyalty import (
    CashbackRule,
    CustomerLoyalty,
    LoyaltyInfo,
    LoyaltyProgram,
    LoyaltyTransaction,
    LoyaltyTransactionSimple,
    RedemptionRule,
    RedemptionRuleType,
)
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class LoyaltyResource(BaseResource):
    """Resource for managing the store's loyalty program.

    Provides access to loyalty program configuration, cashback and redemption
    rules, customer points, and transaction history.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # Check if loyalty program is active
        is_active = client.loyalty.get_status()

        # Get full program details
        program = client.loyalty.get_program()
        print(program.total_earned_points)

        # Get customer loyalty summary
        summary = client.loyalty.get_customer_summary(customer_id=37)
        print(summary.points_balance)
        ```
    """

    token_header: str = "X-Manager-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the loyalty resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)
        # No single _base_path — endpoints are split across multiple paths.

    # --- Read Methods ---

    def get_status(self) -> bool:
        """Get the loyalty program activation status.

        Returns:
            True if the loyalty program is active, False otherwise.

        Example:
            ```python
            if client.loyalty.get_status():
                print("Loyalty program is active")
            ```
        """
        response = self._get("/v1/managers/loyalty-program/loyalty-status")
        return bool(response.get("loyalty_status", False))

    def get_program(self) -> LoyaltyProgram:
        """Retrieve full loyalty program details.

        Returns the program configuration including cashback rules,
        redemption rules, point totals, expiration settings, and status.

        Returns:
            LoyaltyProgram instance with all program data.

        Example:
            ```python
            program = client.loyalty.get_program()
            print(program.total_earned_points)
            print(program.expiration_period)
            for rule in program.cashback_rules or []:
                print(rule.points_rewarded, rule.amount_to_spend)
            ```
        """
        response = self._get("/v1/managers/loyalty-program/list-data")
        return LoyaltyProgram.model_validate(response)

    def get_info(self) -> LoyaltyInfo:
        """Retrieve loyalty program info page content.

        Returns localized title and content for the loyalty program
        information page.

        Returns:
            LoyaltyInfo instance with localized content.

        Example:
            ```python
            info = client.loyalty.get_info()
            print(info.title_en)
            print(info.content_ar)
            ```
        """
        response = self._get("/v1/managers/store/loyalty-program-info")
        payload = response.get("payload", {})
        return LoyaltyInfo.model_validate(payload)

    def get_customer_summary(self, *, customer_id: int | str) -> CustomerLoyalty:
        """Retrieve a customer's loyalty points summary.

        Args:
            customer_id: The customer ID to look up.

        Returns:
            CustomerLoyalty instance with balances and transaction history.

        Raises:
            ZidAPIError: If the customer is not found in the loyalty program.

        Example:
            ```python
            summary = client.loyalty.get_customer_summary(customer_id=37)
            print(summary.points_balance)
            print(summary.available_points)
            ```
        """
        response = self._get(
            "/v1/managers/loyalty-program/customers/details",
            params={"customerId": str(customer_id)},
        )
        return CustomerLoyalty.model_validate(response["loyalty_points_info"])

    def get_customer_history(
        self, *, customer_id: int | str
    ) -> list[LoyaltyTransaction]:
        """Retrieve a customer's points transaction history.

        Args:
            customer_id: The customer ID to look up.

        Returns:
            List of LoyaltyTransaction instances.

        Example:
            ```python
            history = client.loyalty.get_customer_history(customer_id=37)
            for tx in history:
                print(tx.date, tx.direction, tx.points)
            ```
        """
        path = f"/v1/managers/loyalty-program/points-history/{customer_id}"
        response = self._get(path)
        items = response.get("history", [])
        return [LoyaltyTransaction.model_validate(item) for item in items]

    # --- Write Methods ---

    def activate(self, *, active: bool) -> dict[str, Any]:
        """Activate or deactivate the loyalty program.

        Args:
            active: True to activate, False to deactivate.

        Returns:
            Raw response dict containing ``loyalty_program`` status info.

        Example:
            ```python
            # Activate the program
            result = client.loyalty.activate(active=True)

            # Deactivate the program
            result = client.loyalty.activate(active=False)
            ```
        """
        data: dict[str, Any] = {"activate": 1 if active else 0}
        return self._create(
            "/v1/managers/loyalty-program/activation",
            data=data,
        )

    def set_points_expiration(self, *, days: int) -> dict[str, Any]:
        """Set the points expiration period.

        Args:
            days: Number of days until points expire.

        Returns:
            Raw response dict containing ``points_expiry_period``.

        Example:
            ```python
            result = client.loyalty.set_points_expiration(days=30)
            print(result["points_expiry_period"])
            ```
        """
        data: dict[str, Any] = {"days": str(days)}
        return self._create(
            "/v1/managers/loyalty-program/points-expiration",
            data=data,
        )

    def update_cashback_rule(
        self,
        *,
        rule_id: str,
        money: int | float,
        points: int,
    ) -> dict[str, Any]:
        """Update a cashback rule's configuration.

        Args:
            rule_id: UUID of the cashback rule to update.
            money: Amount to spend to earn points.
            points: Number of points rewarded.

        Returns:
            Raw response dict containing updated ``data`` with
            ``points_collection_methods_list``.

        Example:
            ```python
            result = client.loyalty.update_cashback_rule(
                rule_id="efc450a4-3f09-4544-bcdd-80ddcbde23c8",
                money=100,
                points=1,
            )
            ```
        """
        data: dict[str, Any] = {
            "ruleId": rule_id,
            "config[money]": money,
            "config[points]": points,
        }
        return self._create(
            "/v1/managers/loyalty-program/points-collection/update",
            data=data,
        )

    def create_redemption_rule(
        self,
        *,
        rule_type: RedemptionRuleType,
        discount: int | float,
        points: int,
    ) -> RedemptionRule:
        """Create a new points redemption rule.

        Args:
            rule_type: Type of redemption rule
                (``"fixed_rate_settings"`` or ``"percentage_discount_settings"``).
            discount: Discount value for the reward.
            points: Number of points required to redeem.

        Returns:
            Created RedemptionRule instance.

        Example:
            ```python
            rule = client.loyalty.create_redemption_rule(
                rule_type="fixed_rate_settings",
                discount=10,
                points=100,
            )
            print(rule.id)
            ```
        """
        data: dict[str, Any] = {
            "config[type]": rule_type,
            "config[discount]": discount,
            "config[points]": points,
        }
        response = self._create(
            "/v1/managers/loyalty-program/points-redemption",
            data=data,
        )
        redemption = response.get("points_redemption", {})
        return RedemptionRule.model_validate(redemption["redemptionRule"])

    def update_redemption_rule(
        self,
        *,
        rule_id: str,
        rule_type: RedemptionRuleType,
        discount: int | float,
        points: int,
    ) -> dict[str, Any]:
        """Update an existing points redemption rule.

        Args:
            rule_id: UUID of the redemption rule to update.
            rule_type: Type of redemption rule
                (``"fixed_rate_settings"`` or ``"percentage_discount_settings"``).
            discount: New discount value.
            points: New points required to redeem.

        Returns:
            Raw response dict containing ``points_redemption`` status.

        Example:
            ```python
            result = client.loyalty.update_redemption_rule(
                rule_id="4890974d-d474-4d08-99a4-a42b856ea71a",
                rule_type="percentage_discount_settings",
                discount=5,
                points=5,
            )
            ```
        """
        data: dict[str, Any] = {
            "ruleId": rule_id,
            "config[type]": rule_type,
            "config[discount]": discount,
            "config[points]": points,
        }
        return self._create(
            "/v1/managers/loyalty-program/points-redemption/update",
            data=data,
        )

    def delete_redemption_rule(self, *, rule_id: str) -> dict[str, Any]:
        """Delete a points redemption rule.

        Args:
            rule_id: UUID of the redemption rule to delete.

        Returns:
            Raw response dict containing ``points_redemption`` status.

        Raises:
            ZidNotFoundError: If the redemption rule does not exist.

        Example:
            ```python
            result = client.loyalty.delete_redemption_rule(
                rule_id="4890974d-d474-4d08-99a4-a42b856ea71a"
            )
            ```
        """
        data: dict[str, Any] = {"ruleId": rule_id}
        return self._create(
            "/v1/managers/loyalty-program/points-redemption/delete",
            data=data,
        )

    def adjust_customer_points(
        self,
        *,
        customer_id: int,
        direction: Literal["+", "-"],
        points: int,
        reason: str | None = None,
    ) -> LoyaltyTransactionSimple:
        """Manually adjust a customer's loyalty points balance.

        Args:
            customer_id: The customer ID.
            direction: ``"+"`` to add points, ``"-"`` to deduct.
            points: Number of points to adjust.
            reason: Optional reason for the adjustment.

        Returns:
            LoyaltyTransactionSimple instance for the adjustment.

        Example:
            ```python
            tx = client.loyalty.adjust_customer_points(
                customer_id=37,
                direction="+",
                points=100,
                reason="gift",
            )
            print(tx.points, tx.direction)
            ```
        """
        data: dict[str, Any] = {
            "customerId": customer_id,
            "direction": direction,
            "points": points,
        }
        if reason is not None:
            data["reason"] = reason
        response = self._create(
            "/v1/managers/loyalty-program/customers/adjust-customer-points",
            data=data,
        )
        return LoyaltyTransactionSimple.model_validate(response["data"])
