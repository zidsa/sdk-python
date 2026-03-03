"""Order models for the Zid SDK.

This module provides Pydantic models for the Orders API, including
different payload type variants for optimized responses.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from zid.models.base import BaseModel


# --- Shared/Nested Models ---


class OrderStatus(BaseModel):
    """Order status information."""

    name: str
    code: str | int  # API sometimes returns int


class OrderDisplayStatus(BaseModel):
    """Order display status for UI."""

    id: int | None = None
    name: str
    code: str
    color: str | None = None


class OrderCustomer(BaseModel):
    """Customer information within an order."""

    id: int
    name: str
    email: str | None = None
    mobile: str | None = None
    note: str | None = None
    verified: int | None = None
    type: str | None = None
    business_name: str | None = None
    tax_number: str | None = None
    commercial_registration: str | None = None


class OrderShippingAddress(BaseModel):
    """Shipping address for an order."""

    id: int | None = None
    formatted_address: str | None = None
    street: str | None = None
    district: str | None = None
    address: str | None = None
    lat: float | int | None = None
    lng: float | int | None = None
    short_address: str | None = None
    postal_code: str | None = None
    building_number: str | None = None
    additional_number: str | None = None
    city: dict[str, Any] | None = None
    country: dict[str, Any] | None = None
    meta: dict[str, Any] | None = None


class ShippingTracking(BaseModel):
    """Shipping tracking information."""

    number: str | None = None
    status: str | None = None
    url: str | None = None


class ShippingMethodDetail(BaseModel):
    """Detailed shipping method information within order shipping."""

    id: int | None = None
    name: str | None = None
    code: str | None = None
    estimated_delivery_time: str | None = None
    icon: str | None = None
    is_system_option: bool | None = None
    waybill: Waybill | dict[str, Any] | None = None
    had_errors_while_fetching_waybill: bool | None = None
    waybill_tracking_id: str | None = None
    has_waybill_and_packing_list: bool | None = None
    tracking: ShippingTracking | None = None
    courier: str | dict[str, Any] | None = None
    return_shipment: dict[str, Any] | None = None
    packages_count: int | None = None
    # Additional fields from simple shipping method
    type: str | None = None
    logo: str | None = None
    cost: float | str | None = None
    cost_string: str | None = None



class AddressCity(BaseModel):
    """City information within an address."""

    id: int | None = None
    name: str | None = None
    national_id: int | None = None
    priority: int | None = None
    country_id: int | None = None
    country_name: str | None = None
    country_code: str | None = None
    ar_name: str | None = None
    en_name: str | None = None


class AddressCountry(BaseModel):
    """Country information within an address."""

    id: int | None = None
    name: str | None = None
    code: str | None = None


class AddressMeta(BaseModel):
    """Address metadata."""

    postcode: str | None = None
    building_number: str | None = None
    additional_number: str | None = None


class GiftCardDetail(BaseModel):
    """Gift card detail information.

    Note: API typically returns list of strings, but this model supports
    structured data if the API returns objects in the future.
    """

    code: str | None = None
    amount: float | str | None = None
    amount_string: str | None = None


class ProductCustomField(BaseModel):
    """Custom field on an order product."""

    type: str | None = None
    value: str | None = None
    formatted_value: str | None = None
    name: str | None = None
    label: str | None = None


class ProductOption(BaseModel):
    """Product option selection.

    Note: API typically returns list of strings for options,
    but this model supports structured data if available.
    """

    name: str | None = None
    value: str | None = None
    label: str | None = None


class Waybill(BaseModel):
    """Shipping waybill information."""

    id: str | None = None
    tracking_number: str | None = None
    tracking_url: str | None = None
    label_url: str | None = None
    status: str | None = None
    carrier: str | None = None
    carrier_code: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class ChangedByDetails(BaseModel):
    """Details about who changed an order status."""

    id: int | None = None
    name: str | None = None
    email: str | None = None
    type: str | None = None
    role: str | None = None


class InvoiceSettings(BaseModel):
    """Invoice/print settings for an order."""

    is_zid_invoice_generation_enabled: bool | None = None
    is_tax_number_active: bool | None = None
    is_return_policy_active: bool | None = None
    is_products_weight_active: bool | None = None
    is_products_image_active: bool | None = None
    is_barcode_active: bool | None = None
    is_qr_code_active: bool | None = None
    is_expected_time_active: bool | None = None
    is_store_address_active: bool | None = None
    is_vat_settings_active: bool | None = None
    is_sku_active: bool | None = None
    is_thanks_msg_active: bool | None = None
    is_order_status_active: bool | None = None
    is_discount_coupon_active: bool | None = None
    config_logo: str | None = None
    store_business_address: bool | None = None
    store_business_name: bool | None = None
    store_business_type: bool | None = None
    commercial_number: bool | None = None
    is_payment_stamp_active: bool | None = None
    is_order_notifications_enabled: bool | None = None
    is_owner_email_notifications_enabled: bool | None = None
    is_product_description_active: bool | None = None





class ShippingAddress(BaseModel):
    """Shipping address within order shipping object."""

    formatted_address: str | None = None
    street: str | None = None
    district: str | None = None
    lat: float | None = None
    lng: float | None = None
    short_address: str | None = None
    meta: AddressMeta | None = None
    city: AddressCity | None = None
    country: AddressCountry | None = None


class OrderShipping(BaseModel):
    """Complete shipping information for an order.
    
    Contains shipping method details and delivery address.
    """

    method: ShippingMethodDetail | None = None
    address: ShippingAddress | None = None
    # Additional fields that may appear at shipping level
    cost: float | str | None = None
    cost_string: str | None = None


class PaymentMethodDetail(BaseModel):
    """Detailed payment method information within order payment."""

    id: int | None = None
    name: str | None = None
    code: str | None = None
    type: str | None = None
    logo: str | None = None
    transaction_status: str | None = None
    transaction_status_name: str | None = None
    transaction_bank: str | None = None
    transaction_slip: str | None = None
    transaction_sender_name: str | None = None
    updated_at: str | None = None


class PaymentInvoiceItem(BaseModel):
    """Invoice line item within order payment."""

    code: str | None = None
    value: str | float | None = None
    value_string: str | None = None
    title: str | None = None


class OrderPayment(BaseModel):
    """Complete payment information for an order.
    
    Contains payment method details and invoice breakdown.
    """

    method: PaymentMethodDetail | None = None
    invoice: list[PaymentInvoiceItem] | None = None


# Legacy aliases for backward compatibility
class OrderShippingMethod(BaseModel):
    """Shipping method information (simple version)."""

    id: int | None = None
    type: str | None = None
    is_system_option: bool | None = None
    name: str | None = None
    estimated_delivery_time: str | None = None
    code: str | None = None
    logo: str | None = None
    cost: float | str | None = None
    cost_string: str | None = None


class OrderPaymentMethod(BaseModel):
    """Payment method information (simple version)."""

    id: int | None = None
    name: str | None = None
    code: str | None = None
    type: str | None = None
    logo: str | None = None


class OrderTag(BaseModel):
    """Order tag information."""

    id: str
    name: str
    color: str | None = None
    store_id: str | None = None
    user_id: str | None = None
    orders: list[str] | None = None


class OrderReverseLabelRequest(BaseModel):
    """Reverse order label request information.

    This is the detailed structure returned in order list/detail responses
    for reverse_order_label_request and reverse_order_label_requests fields.
    """

    id: str | None = None
    store_id: str | int | None = None
    order_id: int | None = None
    is_partial: int | bool | None = None
    consignee_name: str | None = None
    consignee_mobile: str | None = None
    consignee_city: dict[str, Any] | None = None
    consignee_address_1: str | None = None
    consignee_address_2: str | None = None
    inventory_address_id: int | None = None
    inventory_location_id: str | None = None
    inventory: dict[str, Any] | None = None
    reason: list[str | dict[str, Any]] | None = None
    shipping_method: str | None = None
    waybill: Waybill | dict[str, Any] | None = None
    products: list[dict[str, Any]] | None = None
    # Legacy fields for backward compatibility
    status: str | None = None
    created_at: str | None = None



# Alias for backward compatibility
OrderReverse = OrderReverseLabelRequest


class SplitPayment(BaseModel):
    """Split payment information."""

    id: int | None = None
    amount: float | str | None = None
    payment_method: OrderPaymentMethod | None = None


class OrderInvoiceItem(BaseModel):
    """Invoice line item."""

    label: str | None = None
    value: str | None = None
    type: str | None = None


class OrderCurrencyInfo(BaseModel):
    """Single currency information."""

    id: int | None = None
    code: str | None = None
    name: str | None = None
    symbol: str | None = None
    exchange_rate: float | None = None


class OrderCurrency(BaseModel):
    """Currency wrapper containing order and store currencies.
    
    The API returns:
    - order_currency: The currency used for the order
    - order_store_currency: The store's default currency
    """

    order_currency: OrderCurrencyInfo | None = None
    order_store_currency: OrderCurrencyInfo | None = None


class OrderCoupon(BaseModel):
    """Coupon information applied to order."""

    id: int | None = None
    code: str | None = None
    name: str | None = None
    discount: str | None = None
    discount_string: str | None = None
    discount_type: str | None = None
    discount_value: float | str | None = None


class OrderProductImage(BaseModel):
    """Product image information."""

    id: str | None = None
    origin: str | None = None
    thumbs: dict[str, str] | None = None


class OrderProductVoucher(BaseModel):
    """Voucher information for digital products."""

    id: str | None = None
    product_id: str | None = None
    status: str | None = None
    order: int | None = None
    serial_number: str | None = None
    key: str | None = None
    pin_code: str | None = None
    expires_at: str | None = None
    updated_at: str | None = None
    created_at: str | None = None
    expires_at_formatted: str | None = None


class OrderProductDownloadable(BaseModel):
    """Downloadable file information for digital products."""

    download_url: str | None = None
    download_limit: int | None = None
    download_requests_count: int | None = None
    expiration_period: int | None = None
    is_external: bool | None = None
    display_name: str | None = None


class OrderProductWeight(BaseModel):
    """Product weight with unit."""

    value: float | int | None = None
    unit: str | None = None


class OrderProduct(BaseModel):
    """Product within an order."""

    id: str | None = None
    order_product_id: int | None = None  # Integer ID needed for reverse orders
    product_id: str | None = None
    parent_id: str | None = None
    parent_name: str | None = None
    product_class: str | None = None
    code: str | None = None
    name: str | None = None
    short_description: dict[str, str] | str | None = None
    sku: str | None = None
    quantity: int | None = None
    is_taxable: bool | None = None
    is_discounted: bool | None = None
    is_external_product: bool | None = None
    weight: OrderProductWeight | float | None = None  # API returns object or float
    price: float | str | None = None
    price_string: str | None = None
    sale_price: float | str | None = None
    sale_price_string: str | None = None
    total: float | str | None = None
    total_string: str | None = None
    tax_percentage: float | None = None
    tax_amount: float | str | None = None
    tax_amount_string: str | None = None
    tax_amount_string_per_item: str | None = None
    images: list[OrderProductImage] | None = None
    options: list[ProductOption | str] | None = None
    custom_fields: list[ProductCustomField] | None = None
    barcode: str | None = None
    meta: dict[str, Any] | None = None
    discounts: list[dict[str, Any]] | dict[str, Any] | None = None
    vouchers: list[OrderProductVoucher] | None = None
    downloadables: list[OrderProductDownloadable] | None = None
    downloadables_zipped: list[OrderProductDownloadable] | None = None
    # Net/Gross pricing fields
    net_price_with_additions: float | None = None
    net_price_with_additions_string: str | None = None
    price_with_additions: float | None = None
    price_with_additions_string: str | None = None
    net_price: float | None = None
    net_price_string: str | None = None
    net_sale_price: float | None = None
    net_sale_price_string: str | None = None
    net_additions_price: float | None = None
    net_additions_price_string: str | None = None
    gross_price: float | None = None
    gross_price_string: str | None = None
    gross_sale_price: float | None = None
    gross_sale_price_string: str | None = None
    gross_additions_price: float | None = None
    gross_additions_price_string: str | None = None
    # Before/discount fields
    price_before: float | None = None
    price_before_string: str | None = None
    total_before: float | None = None
    total_before_string: str | None = None
    discount_percentage: float | None = None
    discounted_tax_amount: float | None = None
    discounted_tax_amount_string: str | None = None
    discounted_tax_amount_string_per_item: str | None = None
    additions_price: float | None = None
    additions_price_string: str | None = None
    discounted_total: float | None = None
    discounted_total_string: str | None = None
    inventory_allocations: list[dict[str, Any]] | None = None
    bundle_products: dict[str, list[dict[str, Any]]] | None = None  # For dynamic bundles


class OrderHistory(BaseModel):
    """Order history/audit entry."""

    order_status_id: int | None = None
    order_status_name: str | None = None
    changed_by_id: int | None = None
    changed_by_type: str | None = None
    changed_by_details: ChangedByDetails | dict[str, Any] | None = None
    comment: str | None = None
    created_at: str | None = None
    humanized_created_at: str | None = None


class OrderConsignee(BaseModel):
    """Consignee (recipient) information."""

    name: str | None = None
    email: str | None = None
    mobile: str | None = None


class InventoryAddress(BaseModel):
    """Inventory/fulfillment location address."""

    id: str | None = None
    name: dict[str, str] | str | None = None
    city: dict[str, Any] | None = None
    full_address: str | None = None
    short_address: str | None = None
    street: str | None = None
    district: str | None = None
    postal_code: str | None = None
    coordinates: dict[str, float] | None = None
    cop_enabled: bool | None = None
    is_pickup_option: bool | None = None
    is_zidship_default: bool | None = None
    working_hours: list[dict[str, Any]] | None = None


class MarketplaceCommission(BaseModel):
    """Marketplace commission details."""

    amount: float | str | None = None
    percentage: float | None = None


# --- Payload Type Models ---


class OrderTiny(BaseModel):
    """Minimal order response (payload_type=tiny).

    Contains only essential identifiers and status information.
    """

    id: int
    invoice_number: int
    currency: str | None = None
    customer: OrderCustomer | None = None
    status: str | None = None
    source: str | None = None
    shipping_method: str | None = None
    shipping_address: OrderShippingAddress | None = None
    payment: str | None = None
    payment_status: str | None = None
    transaction_reference: str | None = None
    total: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class OrderSimple(BaseModel):
    """Lightweight order response (payload_type=simple).

    Default response type without products.
    """

    id: int
    invoice_number: int
    code: str | None = None
    store_id: int | None = None
    order_url: str | None = None
    store_name: str | None = None
    shipping_method_code: str | None = None
    store_url: str | None = None
    currency_code: str | None = None
    order_status: OrderStatus | None = None
    display_status: OrderDisplayStatus | None = None
    customer: OrderCustomer | None = None
    has_different_consignee: int | None = None
    is_guest_customer: int | None = None
    is_gift_order: int | None = None
    gift_card_details: list[GiftCardDetail | str] | None = None
    is_quick_checkout_order: bool | None = None
    order_total: str | float | None = None
    order_total_string: str | None = None
    has_different_transaction_currency: bool | None = None
    transaction_reference: str | None = None
    transaction_amount: float | None = None
    transaction_amount_string: str | None = None
    issue_date: str | None = None
    payment_status: str | None = None
    is_potential_fraud: bool | None = None
    source: str | None = None
    source_code: str | None = None
    is_reseller_transaction: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    is_on_demand: bool | None = None
    import_id: str | None = None
    store_logo: str | None = None
    store_uuid: str | None = None
    tags: list[OrderTag] | None = None
    requires_shipping: bool | None = None
    should_merchant_set_shipping_method: bool | None = None
    shipping: OrderShipping | None = None
    payment: OrderPayment | None = None
    cod_confirmed: bool | None = None
    reverse_order_label_request: OrderReverseLabelRequest | None = None
    reverse_order_label_requests: list[OrderReverseLabelRequest] | None = None


class Order(BaseModel):
    """Full order response (payload_type=default).

    Includes products, customer details, totals, and all order information.
    """

    id: int
    invoice_number: int
    code: str | None = None
    store_id: int | None = None
    order_url: str | None = None
    store_name: str | None = None
    shipping_method_code: str | None = None
    store_url: str | None = None
    currency_code: str | None = None
    order_status: OrderStatus | None = None
    display_status: OrderDisplayStatus | None = None
    customer: OrderCustomer | None = None
    has_different_consignee: int | None = None
    is_guest_customer: int | None = None
    is_gift_order: int | None = None
    gift_card_details: list[GiftCardDetail | str] | None = None
    consignee: OrderConsignee | None = None
    is_quick_checkout_order: bool | None = None
    order_total: str | float | None = None
    order_total_string: str | None = None
    has_different_transaction_currency: bool | None = None
    transaction_reference: str | None = None
    transaction_amount: float | None = None
    transaction_amount_string: str | None = None
    issue_date: str | None = None
    payment_status: str | None = None
    is_potential_fraud: bool | None = None
    source: str | None = None
    source_code: str | None = None
    is_reseller_transaction: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    is_on_demand: bool | None = None
    import_id: str | None = None
    store_logo: str | None = None
    store_uuid: str | None = None
    tags: list[OrderTag] | None = None
    requires_shipping: bool | None = None
    should_merchant_set_shipping_method: bool | None = None
    shipping: OrderShipping | None = None
    payment: OrderPayment | None = None
    cod_confirmed: bool | None = None
    reverse_order_label_request: OrderReverseLabelRequest | None = None
    reverse_order_label_requests: list[OrderReverseLabelRequest] | None = None
    customer_note: str | None = None
    gift_message: str | None = None
    payment_link: dict[str, Any] | str | None = None  # API returns object or string
    service_fee_invoice_link: str | None = None
    weight: int | None = None
    weight_cost_details: list[str] | None = None
    currency: OrderCurrency | None = None
    coupon: OrderCoupon | None = None
    products: list[OrderProduct] | None = None
    products_count: int | None = None
    products_sum_total_string: str | None = None
    language: str | None = None
    histories: list[OrderHistory] | None = None
    product_ids: list[str] | None = None
    is_reactivated: bool | None = None
    return_policy: str | None = None
    packages_count: int | None = None
    inventory_address: InventoryAddress | dict[str, Any] | None = None
    expected_shipping_method_type: str | None = None
    reseller_meta: list[str] | None = None
    zidship_ticket_number: str | None = None
    edits_count: int | None = None
    delivered_at: str | None = None
    is_marketplace_order: bool | None = None
    marketplace_commission: MarketplaceCommission | None = None
    pos_invoice_number: str | None = None
    return_invoice_number: str | None = None
    invoice_link: str | None = None
    payment_network: str | None = None
    digital_products_access_token: str | None = None
    # Detail endpoint only fields
    previous_order: int | None = None
    next_order: int | None = None
    invoice_settings: InvoiceSettings | dict[str, Any] | None = None


class OrderPos(BaseModel):
    """POS-optimized order response (payload_type=pos).
    
    Note: API returns same fields as OrderSimple for this payload type.
    """

    id: int
    invoice_number: int
    code: str | None = None
    store_id: int | None = None
    order_url: str | None = None
    store_name: str | None = None
    shipping_method_code: str | None = None
    store_url: str | None = None
    currency_code: str | None = None
    order_status: OrderStatus | None = None
    display_status: OrderDisplayStatus | None = None
    customer: OrderCustomer | None = None
    has_different_consignee: int | None = None
    is_guest_customer: int | None = None
    is_gift_order: int | None = None
    gift_card_details: list[GiftCardDetail | str] | None = None
    is_quick_checkout_order: bool | None = None
    order_total: str | float | None = None
    order_total_string: str | None = None
    has_different_transaction_currency: bool | None = None
    transaction_reference: str | None = None
    transaction_amount: float | None = None
    transaction_amount_string: str | None = None
    issue_date: str | None = None
    payment_status: str | None = None
    is_potential_fraud: bool | None = None
    source: str | None = None
    source_code: str | None = None
    is_reseller_transaction: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    is_on_demand: bool | None = None
    import_id: str | None = None
    store_logo: str | None = None
    store_uuid: str | None = None
    tags: list[OrderTag] | None = None
    requires_shipping: bool | None = None
    should_merchant_set_shipping_method: bool | None = None
    shipping: OrderShipping | None = None
    payment: OrderPayment | None = None
    cod_confirmed: bool | None = None
    reverse_order_label_request: OrderReverseLabelRequest | None = None
    reverse_order_label_requests: list[OrderReverseLabelRequest] | None = None


class OrderVatSettings(BaseModel):
    """Store VAT settings included in print payloads.
    
    Note: API can return either flat structure or nested with status/tax_settings.
    """

    # Flat structure fields (legacy)
    id: str | None = None
    country: dict[str, Any] | None = None
    tax_percentage: float | None = None
    vat_number: str | None = None
    tax_registration_certificate: str | None = None
    settings: list[Any] | None = None
    is_certificate_visible: bool | None = None
    is_vat_number_visible: bool | None = None
    can_use_vat: bool | None = None
    vat_activate: bool | None = None
    is_vat_self_paid: bool | None = None
    is_vat_included_in_product_price: bool | None = None
    is_shipping_fee_included_in_vat: bool | None = None
    other_countries_tax_percentage: float | None = None
    # Nested structure fields (new format)
    status: str | None = None
    tax_settings: dict[str, Any] | None = None
    message: dict[str, Any] | None = None


class OrderZatca(BaseModel):
    """ZATCA (Saudi tax authority) QR code data."""

    qr_code_data: str | None = None


class OrderPrint(BaseModel):
    """Print-optimized order response (payload_type=print)."""

    id: int
    invoice_number: int
    code: str | None = None
    store_id: int | None = None
    order_url: str | None = None
    store_name: str | None = None
    shipping_method_code: str | None = None
    store_url: str | None = None
    currency_code: str | None = None
    order_status: OrderStatus | None = None
    display_status: OrderDisplayStatus | None = None
    customer: OrderCustomer | None = None
    has_different_consignee: int | None = None
    is_guest_customer: int | None = None
    is_gift_order: int | None = None
    gift_card_details: list[GiftCardDetail | str] | None = None
    is_quick_checkout_order: bool | None = None
    order_total: str | float | int | None = None
    order_total_string: str | None = None
    has_different_transaction_currency: bool | None = None
    transaction_reference: str | None = None
    transaction_amount: float | str | None = None
    transaction_amount_string: str | None = None
    issue_date: str | None = None
    payment_status: str | None = None
    is_potential_fraud: bool | None = None
    source: str | None = None
    source_code: str | None = None
    is_reseller_transaction: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    is_on_demand: bool | None = None
    import_id: str | None = None
    store_logo: str | None = None
    store_uuid: str | None = None
    product_ids: list[str] | None = None
    products_count: int | None = None
    is_marketplace_order: bool | None = None
    pos_invoice_number: str | None = None
    shipping: OrderShipping | None = None
    payment: OrderPayment | None = None
    cod_confirmed: bool | None = None
    consignee: OrderConsignee | None = None
    customer_note: str | None = None
    products: list[OrderProduct] | None = None
    products_sum_total_string: str | None = None
    coupon: OrderCoupon | None = None
    return_policy: str | None = None
    invoice_link: str | None = None
    payment_method: PaymentMethodDetail | None = None
    store_address: str | None = None
    store_vat_settings: OrderVatSettings | dict[str, Any] | None = None
    zatca: OrderZatca | None = None
    order_credit_notes: list[dict[str, Any]] | None = None


class OrderPrintSummary(BaseModel):
    """Print summary order response (payload_type=print_summary)."""

    id: int
    invoice_number: int
    code: str | None = None
    store_id: int | None = None
    order_url: str | None = None
    store_name: str | None = None
    shipping_method_code: str | None = None
    store_url: str | None = None
    currency_code: str | None = None
    order_status: OrderStatus | None = None
    display_status: OrderDisplayStatus | None = None
    customer: OrderCustomer | None = None
    has_different_consignee: int | None = None
    is_guest_customer: int | None = None
    is_gift_order: int | None = None
    gift_card_details: list[GiftCardDetail | str] | None = None
    is_quick_checkout_order: bool | None = None
    order_total: str | float | None = None
    order_total_string: str | None = None
    has_different_transaction_currency: bool | None = None
    transaction_reference: str | None = None
    transaction_amount: float | None = None
    transaction_amount_string: str | None = None
    issue_date: str | None = None
    payment_status: str | None = None
    is_potential_fraud: bool | None = None
    source: str | None = None
    source_code: str | None = None
    is_reseller_transaction: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    is_on_demand: bool | None = None
    import_id: str | None = None
    is_marketplace_order: bool | None = None
    shipping: OrderShipping | None = None
    payment: OrderPayment | None = None
    cod_confirmed: bool | None = None
    customer_note: str | None = None
    products: list[OrderProduct] | None = None
    products_sum_total_string: str | None = None
    coupon: OrderCoupon | None = None
    return_policy: str | None = None
    invoice_link: str | None = None
    payment_method: PaymentMethodDetail | None = None
    store_address: str | None = None
    store_vat_settings: OrderVatSettings | dict[str, Any] | None = None


# --- Response Wrappers ---


class OrderStatusCount(BaseModel):
    """Order count per status."""

    ready: int | None = None
    initial: int | None = None
    new: int | None = None
    preparing: int | None = None
    indelivery: int | None = None
    delivered: int | None = None
    reversed: int | None = None
    partially_reversed: int | None = None
    reverse_in_progress: int | None = None
    canceled: int | None = None
    cancelled: int | None = None


class OrderListResponse(BaseModel):
    """Response wrapper for order list endpoint."""

    status: str | None = None
    orders: list[dict[str, Any]]
    grand_total: int | None = None
    total_order_count: int | None = None
    total_order_count_per_status: OrderStatusCount | None = None


# --- Credit Note Models ---


class CreditNoteItem(BaseModel):
    """Item within a credit note."""

    id: str | None = None
    product_id: str | None = None
    code: str | None = None
    name: str | None = None
    sku: str | None = None
    quantity: int | None = None
    price: float | str | None = None
    price_string: str | None = None
    total: float | str | None = None
    total_string: str | None = None
    images: list[OrderProductImage] | None = None


class CreditNote(BaseModel):
    """Credit note for an order."""

    id: str
    order_id: int
    store_id: int
    invoice_type: str | None = None
    translated_invoice_type: str | None = None
    original_invoice_number: int | None = None
    invoice_number: int | None = None
    issue_reason: str | None = None
    invoice_title: str | None = None
    translated_issue_reason: str | None = None
    store_name: str | None = None
    shipping_method_code: str | None = None
    store_url: str | None = None
    order_status: OrderStatus | None = None
    payment_status: str | None = None
    currency_code: str | None = None
    customer: OrderCustomer | None = None
    order_total: str | None = None
    order_total_string: str | None = None
    items: list[CreditNoteItem] | None = None
    shipping: OrderShipping | None = None
    payment: OrderPayment | None = None
    created_at: str | None = None
    updated_at: str | None = None


# Type alias for payload_type parameter
PayloadType = Literal["default", "simple", "tiny", "pos", "print", "print_summary"]


# --- Custom Order Status Models ---


class CustomOrderStatusName(BaseModel):
    """Localized name for custom order status."""

    ar: str | None = None
    en: str | None = None


class CustomOrderSubStatus(BaseModel):
    """Custom sub-status within a parent order status.
    
    Represents a store-defined custom status that can be assigned to orders
    under a specific parent status (e.g., "Awaiting Approval" under "New").
    """

    id: int
    name: str | CustomOrderStatusName | None = None  # API returns string or object
    code: str | None = None
    color: str | None = None
    is_active: bool | None = None
    display_order: int | None = None
    parent_status_id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None


class CustomOrderStatus(BaseModel):
    """Main order status with its custom sub-statuses.
    
    Represents a predefined parent status (e.g., New, Preparing, Delivered)
    along with any custom sub-statuses defined by the store.
    """

    id: int
    status: str  # Localized main status name
    code: str  # Main status code (e.g., "new", "preparing")
    is_customizable: bool  # Whether this status supports custom sub-statuses
    sub_statuses: list[CustomOrderSubStatus] | None = None


# --- Order Creation Input Models ---


class OrderCreateCustomer(BaseModel):
    """Customer information for order creation."""

    full_name: str
    mobile_country_code: str
    mobile_number: str
    email: str | None = None


class OrderCreateAddressMeta(BaseModel):
    """Address metadata for order creation."""

    postcode: str | None = None
    building_number: str | None = None
    additional_number: str | None = None
    city_name: str | None = None


class OrderCreateAddress(BaseModel):
    """Address for order creation."""

    line_1: str
    line_2: str
    city_name: str
    country_code: str
    lat: float | None = None
    lng: float | None = None
    meta: OrderCreateAddressMeta | None = None


class OrderCreateConsignee(BaseModel):
    """Consignee (recipient) for order creation."""

    contact: OrderCreateCustomer
    address: OrderCreateAddress


class OrderCreateProduct(BaseModel):
    """Product item for order creation."""

    sku: str
    quantity: int


class OrderCreateShippingMethod(BaseModel):
    """Shipping method for order creation."""

    type: str
    id: int


class OrderCreatePaymentMethod(BaseModel):
    """Payment method for order creation."""

    id: int
