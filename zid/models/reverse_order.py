"""Reverse order models for the Zid SDK.

This module provides Pydantic models for reverse orders (returns/refunds).
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from zid.models.base import BaseModel


# =============================================================================
# Nested Models
# =============================================================================


class ReverseOrderReason(BaseModel):
    """Reason for a reverse order."""

    id: str | None = None
    name: str | None = None


class ReverseOrderCountry(BaseModel):
    """Country information in reverse order context."""

    id: int | None = None
    name: str | None = None
    ar_name: str | None = None
    country_code: str | None = None
    iso_code_2: str | None = None
    iso_code_3: str | None = None
    currency_code: str | None = None
    is_supported_by_zid: int | None = None


class ReverseOrderCity(BaseModel):
    """City information for reverse order consignee."""

    id: int | None = None
    name: str | None = None
    ar_name: str | None = None
    en_name: str | None = None
    country_id: int | None = None
    zone_id: int | None = None
    code: str | None = None
    status: int | None = None
    priority: int | None = None
    national_address_city_id: int | None = None
    governorate_ar_name: str | None = None
    governorate_en_name: str | None = None
    region_id: int | None = None
    region_ar_name: str | None = None
    region_en_name: str | None = None
    country: ReverseOrderCountry | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None


class ReverseOrderInventoryName(BaseModel):
    """Localized name for inventory location."""

    ar: str | None = None
    en: str | None = None


class ReverseOrderInventoryCoordinates(BaseModel):
    """Geographic coordinates for inventory location."""

    type: str | None = None
    coordinates: list[float] | None = None


class ReverseOrderInventory(BaseModel):
    """Inventory location details in reverse order."""

    id: str | None = None
    name: ReverseOrderInventoryName | dict[str, str] | None = None
    type: str | None = None
    coordinates: ReverseOrderInventoryCoordinates | None = None
    is_default: int | None = None
    is_private: int | None = None
    is_enabled: int | None = None
    fulfillment_priority: int | None = None
    city_id: int | None = None
    store_id: str | None = None
    full_address: str | None = None
    channels: list[str] | None = None
    district: str | None = None
    street: str | None = None
    short_address: str | None = None
    meta: Any | None = None
    deleted: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class ReverseOrderWaybill(BaseModel):
    """Waybill information for reverse order shipping."""

    id: str | None = None
    cost: float | None = None
    label: str | None = None
    status: str | None = None
    courier: str | None = None
    tracking_url: str | None = None
    service_level: str | None = None
    tracking_number: str | None = None


class ReverseOrderProductPurchaseRestrictions(BaseModel):
    """Purchase restrictions for a product."""

    max_quantity_per_cart: int | None = None
    min_quantity_per_cart: int | None = None
    sale_price_period_end: float | None = None
    availability_period_end: float | None = None
    sale_price_period_start: float | None = None
    availability_period_start: float | None = None


class ReverseOrderProductInfo(BaseModel):
    """Product information in reverse order context."""

    id: str | None = None
    structure: str | None = None
    store_id: int | None = None
    name: str | None = None
    quantity: int | None = None
    is_infinite: bool | None = None
    slug: str | None = None
    sku: str | None = None
    price: str | None = None
    sale_price: float | None = None
    parent_id: str | None = None
    is_published: int | None = None
    is_draft: int | None = None
    upc: str | None = None
    rating: float | None = None
    revision: int | None = None
    product_class_id: str | None = None
    display_order: int | None = None
    has_been_modified: int | None = None
    cost: str | None = None
    weight: float | None = None
    popularity_points: int | None = None
    requires_shipping: int | None = None
    weight_display_unit: str | None = None
    is_taxable: bool | None = None
    purchase_restrictions: ReverseOrderProductPurchaseRestrictions | None = None
    meta: Any | None = None
    short_description: str | None = None
    badge: str | None = None
    related_products_settings: str | None = None
    related_products_title: str | None = None
    barcode: str | None = None
    product_class: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted: str | None = None


class ReverseOrderOrderProduct(BaseModel):
    """Original order product information."""

    id: int | None = None
    order_id: int | None = None
    product_id: int | None = None
    product_uuid: str | None = None
    sku: str | None = None
    name: str | None = None
    model: str | None = None
    quantity: int | None = None
    requires_shipping: int | None = None
    weight: float | None = None
    cost: float | None = None
    price: str | None = None
    additions_price: str | None = None
    total: str | None = None
    net_price: str | None = None
    net_sale_price: str | None = None
    net_additions_price: str | None = None
    gross_sale_price: str | None = None
    gross_additions_price: str | None = None
    gross_price: str | None = None
    tax_percentage: str | None = None
    tax_amount: str | None = None
    is_taxable: bool | None = None
    is_discounted: bool | None = None
    meta: Any | None = None
    reward: int | None = None
    custom_fields: Any | None = None
    reseller_meta: Any | None = None
    external_product_id: str | None = None
    is_external_product: bool | None = None
    net_unit_price: str | None = None
    gross_unit_price: str | None = None
    undiscounted_net_unit_price: str | None = None
    undiscounted_gross_unit_price: str | None = None
    undiscounted_net_total: str | None = None
    undiscounted_gross_total: str | None = None
    unit_discount_amount: str | None = None
    unit_discount_percentage: str | None = None
    subtotal_discounts: list[Any] | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None


class ReverseOrderProduct(BaseModel):
    """Product in a reverse order."""

    id: str | None = None
    order_reverse_id: str | None = None
    order_product_id: int | None = None
    product_uuid: str | None = None
    quantity: int | None = None
    reversed_quantity: int | None = None
    received_quantity: int | None = None
    not_received_quantity: int | None = None
    damaged_quantity: int | None = None
    product: ReverseOrderProductInfo | None = None
    product_class: str | None = None
    order_product: ReverseOrderOrderProduct | None = None
    created_at: str | None = None
    updated_at: str | None = None


class RefundPaymentMethod(BaseModel):
    """Available refund payment method."""

    name: str | None = None
    code: str | None = None


class ReverseOrderRefund(BaseModel):
    """Refund information for a reverse order."""

    id: str | None = None
    amount: float | None = None
    payment_method: str | None = None
    notes: str | None = None
    bank_transfer_receipt: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

class BankReceiptUploadRefund(BaseModel):
    """Refund information returned after uploading bank receipt."""

    id: str | None = None
    payment_method: str | None = None
    amount: float | None = None
    bank_transfer_receipt: str | None = None
    status: str | None = None


class BankReceiptUploadReverseOrder(BaseModel):
    """Reverse order information returned after uploading bank receipt."""

    id: str | None = None
    refund: BankReceiptUploadRefund | None = None


class BankReceiptUploadResponse(BaseModel):
    """Response from uploading a bank transfer receipt."""

    order_reverse: BankReceiptUploadReverseOrder | None = None


# =============================================================================
# Main Models
# =============================================================================


class ReverseOrder(BaseModel):
    """Reverse order (return/refund) model.

    Represents a request to reverse an order, including partial returns.
    """

    id: str | None = None
    store_id: str | None = None
    order_id: int | None = None
    is_partial: bool | int | None = None
    consignee_name: str | None = None
    consignee_mobile: str | None = None
    consignee_city: ReverseOrderCity | None = None
    consignee_address_1: str | None = None
    consignee_address_2: str | None = None
    inventory_address_id: int | None = None
    inventory_location_id: str | None = None
    inventory: ReverseOrderInventory | None = None
    reason: list[ReverseOrderReason | str] | None = None
    shipping_method: str | None = None
    waybill: ReverseOrderWaybill | list[str] | None = None
    products: list[ReverseOrderProduct] | None = None
    reverse_total: float | None = None
    refund_total: float | None = None
    refund: ReverseOrderRefund | None = None
    available_refund_payment_methods: list[RefundPaymentMethod] | None = None
    shipment_status: str | None = None


class ReverseOrderInvoiceItem(BaseModel):
    """Invoice line item for reverse order totals calculation."""

    code: str | None = None
    value: float | None = None
    value_string: str | None = None
    title: str | None = None


class ReverseOrderTotals(BaseModel):
    """Calculated totals for a reverse order."""

    invoice: list[ReverseOrderInvoiceItem] | None = None


# =============================================================================
# Input Models
# =============================================================================


class ReverseOrderReasonInput(BaseModel):
    """Input model for creating a reverse order reason."""

    id: str
    name: str


class ReverseOrderProductInput(BaseModel):
    """Input model for specifying products in a reverse order."""

    order_product_id: int
    quantity: int


class ReverseOrderCreate(BaseModel):
    """Input model for creating a reverse order.

    Example:
        ```python
        create_data = ReverseOrderCreate(
            order_id=12345,
            consignee_name="John Doe",
            consignee_mobile="+966500000001",
            consignee_city_id=1,
            consignee_address_1="123 Main St",
            consignee_address_2="Apt 4",
            inventory_location_id="location-uuid",
            reason=[{"id": "reason-uuid", "name": "Damaged"}],
            is_partial=False,
        )
        ```
    """

    order_id: int
    consignee_name: str
    consignee_mobile: str
    consignee_city_id: int
    consignee_address_1: str
    consignee_address_2: str | None = None
    inventory_location_id: str | None = None
    reason: list[ReverseOrderReasonInput | dict[str, str]] | None = None
    is_partial: bool | None = None
    refund_payment_method: str | None = None
    products: list[ReverseOrderProductInput | dict[str, Any]] | None = None
    packages_count: int | None = None
    shipping_method: str | None = None


class WaybillCreate(BaseModel):
    """Input model for creating a reverse order waybill."""

    order_id: int
    is_standalone_zidship_waybill: bool = False


class RefundCreate(BaseModel):
    """Input model for creating a refund.

    Example:
        ```python
        refund_data = RefundCreate(
            order_reverse_id="reverse-order-uuid",
            amount=199.56,
            payment_method="zid_bank_transfer",
            notes="Refund processed",
        )
        ```
    """

    order_reverse_id: str
    amount: float
    payment_method: str
    notes: str | None = None
    bank_transfer_receipt: str | None = None


class CalculateTotalsInput(BaseModel):
    """Input model for calculating reverse order totals."""

    order_id: int
    is_partial: bool | int = 0
    products: list[ReverseOrderProductInput | dict[str, Any]] | None = None


class ReverseOrderProductUpdate(BaseModel):
    """Input model for updating a product's quantities in a reverse order.

    Used with the update_products() method to specify received, not received,
    and damaged quantities for each product.

    Note:
        The sum of received_quantity + not_received_quantity + damaged_quantity
        must be less than or equal to the reversed_quantity for the product.
        At least one quantity must be greater than 0.

    Example:
        ```python
        product_update = ReverseOrderProductUpdate(
            id="550e8400-e29b-41d4-a716-446655440001",
            received_quantity=1,
            not_received_quantity=0,
            damaged_quantity=0,
        )
        ```
    """

    id: str
    received_quantity: int
    not_received_quantity: int
    damaged_quantity: int



