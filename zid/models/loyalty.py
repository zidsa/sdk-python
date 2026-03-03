"""Loyalty program models for the Zid SDK.

This module provides Pydantic models for the Loyalty Program API,
including program configuration, rules, transactions, and customer
loyalty data.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from zid.models.base import BaseModel

# --- Type Aliases ---

RedemptionRuleType = Literal["percentage_discount_settings", "fixed_rate_settings"]


# --- Nested Models ---


class AvailableToLevel(BaseModel):
    """Level targeting within a cashback rule's available_to field."""

    level_id: str | None = Field(default=None, validation_alias="levelId")
    level_name: str | None = Field(default=None, validation_alias="levelName")


class CashbackAvailableTo(BaseModel):
    """Targeting configuration for a cashback rule."""

    tags: list[str] | None = None
    level: AvailableToLevel | None = None


class CashbackRule(BaseModel):
    """Cashback rule within a loyalty program.

    Defines how customers earn points based on spending.
    """

    id: str
    external_id: str | None = None
    store_id: str | None = None
    points_rewarded: int | None = None
    amount_to_spend: int | None = None
    available_to: CashbackAvailableTo | None = None
    is_active: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None


class RedemptionReward(BaseModel):
    """Reward configuration within a redemption rule."""

    discount_value: int | float | None = None


class RedemptionRule(BaseModel):
    """Redemption rule within a loyalty program.

    Defines how customers can redeem points for rewards.
    """

    id: str
    external_id: str | None = None
    store_id: str | None = None
    name: str | None = None
    points_to_redeem: int | None = None
    rule_type: str | None = None
    reward: RedemptionReward | None = None
    conditions: Any | None = None
    is_active: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None


# --- Main Models ---


class LoyaltyProgram(BaseModel):
    """Loyalty program details from the ``/list-data`` endpoint.

    Contains cashback rules, redemption rules, point totals,
    expiration settings, and program status.

    Note:
        The API has typos in some field names. This model uses clean
        Python names with ``validation_alias`` to match the actual API keys:

        - ``total_redeemed_points`` ← API sends ``total_redemed_points``
        - ``expiration_period`` ← API sends ``expiration_peroid``
    """

    cashback_rules: list[CashbackRule] | None = None
    redemption_rules: list[RedemptionRule] | None = None
    total_earned_points: int | None = None
    total_redeemed_points: int | None = Field(
        default=None, validation_alias="total_redemed_points"
    )
    total_pending_points: int | None = None
    total_customers_with_points: int | None = None
    expiration_period: int | None = Field(
        default=None, validation_alias="expiration_peroid"
    )
    is_active: bool | None = None


class LoyaltyInfo(BaseModel):
    """Loyalty program info page content from ``/loyalty-program-info``.

    Contains localized title and content for the loyalty program
    information page.
    """

    title_ar: str | None = None
    title_en: str | None = None
    content_ar: str | None = None
    content_en: str | None = None


class LoyaltyTransaction(BaseModel):
    """Full loyalty transaction from ``DefaultCustomerTransactionsSerializer``.

    Represents a single points transaction in a customer's history,
    including order references and status information.
    """

    date: str
    reason: str | None = None
    points: int
    direction: str
    type: str
    order_number: int | None = None
    order_code: str | None = None
    expiry_date: str | None = None
    point_status: str
    point_status_code: str
    collection_method: str


class LoyaltyTransactionSimple(BaseModel):
    """Simplified loyalty transaction from ``LoyaltyTransactionPresenter``.

    Returned by the adjust-points endpoint. Has fewer fields than
    the full :class:`LoyaltyTransaction` (no ``order_code`` or
    ``point_status_code``).
    """

    date: str
    reason: str | None = None
    points: int
    direction: str
    type: str
    order_number: int | None = None
    expiry_date: str | None = None
    point_status: str
    collection_method: str


class CustomerLoyalty(BaseModel):
    """Customer loyalty points summary from ``/customers/details``.

    Contains point balances and inline transaction history.

    Note:
        The API has typos in some field names. This model uses clean
        Python names with ``validation_alias`` to match the actual API keys:

        - ``available_points`` ← API sends ``available_poitns``
        - ``used_points`` ← API sends ``used_poitns``
    """

    points_balance: int | None = None
    pending_points_balance: int | None = None
    pending_negative_points_balance: int | None = None
    available_points: int | None = Field(
        default=None, validation_alias="available_poitns"
    )
    used_points: int | None = Field(
        default=None, validation_alias="used_poitns"
    )
    total_positive_points: int | None = None
    history: list[LoyaltyTransaction] | None = None
