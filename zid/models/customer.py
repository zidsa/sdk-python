"""Customer models for the Zid SDK."""

from datetime import datetime
from typing import Any

from pydantic import Field

from zid.models.base import BaseModel


class CustomerCity(BaseModel):
    """City information for a customer."""

    id: int
    national_id: int | None = None
    name: str
    priority: int
    country_id: int
    country_name: str
    country_code: str
    ar_name: str
    en_name: str


class CustomerPoints(BaseModel):
    """Loyalty points information for a customer (detailed view)."""

    id: str
    external_id: str
    store_id: str
    customer_id: int
    loyalty_provider: str
    points: int
    pending_points: int
    total_positive_points: int
    total_negative_points: int
    pending_negative_points: int
    status: int
    created_at: str
    updated_at: str
    deleted_at: str | None = None


class Customer(BaseModel):
    """Customer model representing a store customer.

    This model is used for both list and detail responses.
    Note: The `points` field can be an integer (list view) or
    a CustomerPoints object (detail view).
    """

    id: int
    name: str
    email: str | None = None
    mobile: str
    gender: str | None = None
    birth_date: str | None = None
    verified: bool
    is_active: bool
    is_cod_enabled: bool
    type: str
    business_name: str | None = None
    tax_number: str | None = None
    commercial_registration: str | None = None
    source: str | None = None
    points: int | CustomerPoints | None = None
    order_total_payments: str
    last_order_date: str | None = None
    created_at: str
    updated_at: str
    city: CustomerCity | None = None
    nickname: str
    pivot_email: str | None = Field(default=None, alias="pivotEmail")
    pivot_mobile: str = Field(alias="pivotMobile")
    order_counts: int
    # Fields only present in detail view
    total_payments: float | None = None
    orders_cost_average: float | None = None
    orders: list[dict[str, Any]] | None = None
    # Tags - present in both list and detail views
    tags: list[dict[str, Any]] | None = None


class CustomerList(BaseModel):
    """Response wrapper for customer list endpoint with pagination metadata."""

    status: str
    customers: list[Customer]
    grand_total: int
    total_customers_count: int
    active_customers_count: int
    inactive_customers_count: int


class CustomerCreate(BaseModel):
    """Input model for creating a customer.

    Note: The Zid API does not currently support customer creation
    via the public API. This model is provided for future compatibility.
    """

    name: str
    email: str | None = None
    mobile: str
    gender: str | None = None
    birth_date: str | None = None
    type: str = "individual"
    business_name: str | None = None
    tax_number: str | None = None
    commercial_registration: str | None = None


class CustomerUpdate(BaseModel):
    """Input model for updating a customer.

    Note: The Zid API does not currently support customer updates
    via the public API. This model is provided for future compatibility.
    """

    name: str | None = None
    email: str | None = None
    mobile: str | None = None
    gender: str | None = None
    birth_date: str | None = None
    type: str | None = None
    business_name: str | None = None
    tax_number: str | None = None
    commercial_registration: str | None = None
    is_active: bool | None = None
    is_cod_enabled: bool | None = None
