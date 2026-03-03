"""Store profile models for the Zid SDK."""

from typing import Any

from zid.models.base import BaseModel


class StoreCountry(BaseModel):
    """Country information."""

    id: int | None = None
    name: str | None = None
    code: str | None = None
    country_code: str | None = None
    flag: str | None = None


class StoreCity(BaseModel):
    """City information."""

    id: int | None = None
    national_id: int | None = None
    name: str | None = None
    priority: int | None = None
    country_id: int | None = None
    country_name: str | None = None
    country_code: str | None = None
    ar_name: str | None = None
    en_name: str | None = None


class StoreCurrency(BaseModel):
    """Currency information."""

    id: int | None = None
    name: str | None = None
    code: str | None = None
    symbol: str | None = None
    country: StoreCountry | None = None


class StoreLanguage(BaseModel):
    """Language information."""

    id: int | None = None
    name: str | None = None
    code: str | None = None
    direction: str | None = None


class StoreTheme(BaseModel):
    """Theme information."""

    id: int | None = None
    code: str | None = None
    name: str | None = None
    main_image: str | None = None
    description: str | None = None
    images: list[str] | None = None


class StoreIndustry(BaseModel):
    """Industry information."""

    id: int | None = None
    name: str | None = None
    slug: str | None = None
    display_order: int | None = None
    is_theme_default: bool | None = None


class StoreCategory(BaseModel):
    """Store category information."""

    id: int | None = None
    ar_name: str | None = None
    en_name: str | None = None
    slug: str | None = None
    industry_id: int | None = None
    display_order: int | None = None
    name: str | None = None


class StoreLogos(BaseModel):
    """Store logos in different languages."""

    ar: str | None = None
    en: str | None = None


class LocalizedName(BaseModel):
    """Localized name with ar/en variants."""

    ar: str | None = None
    en: str | None = None


class SubscriptionPolicies(BaseModel):
    """Subscription feature policies (what features are enabled)."""

    # Core features
    unlimited_products: bool | None = None
    custom_domain: bool | None = None
    free_custom_domain: bool | None = None
    themes: bool | None = None
    custom_css: bool | None = None
    mobile_apps: bool | None = None
    team_work: bool | None = None
    
    # Payment features
    payment_gateways: bool | None = None
    zidpay: bool | None = None
    tamara: bool | None = None
    tabby: bool | None = None
    moyasar_payment: bool | None = None
    tap_payment: bool | None = None
    hyperpay_payment: bool | None = None
    paytabs_payment: bool | None = None
    payfort_payment: bool | None = None
    mispay: bool | None = None
    bank_transfer_payment_method: bool | None = None
    apple_pay_quick_checkout: bool | None = None
    
    # Shipping features
    integrated_shipping_methods: bool | None = None
    custom_shipping_methods: bool | None = None
    pickup_shipping_methods: bool | None = None
    couriers: bool | None = None
    shipping_smsa: bool | None = None
    shipping_aramex: bool | None = None
    zam_shipping_apps: bool | None = None
    
    # Marketing features
    coupons: bool | None = None
    discounts: bool | None = None
    discount_rules: bool | None = None
    bundle_offer: bool | None = None
    loyalty: bool | None = None
    sms_campaigns: bool | None = None
    abandoned_carts: bool | None = None
    affiliate_marketing: bool | None = None
    
    # Analytics features
    stats_dashboard: bool | None = None
    advanced_analytics: bool | None = None
    live_analytics: bool | None = None
    financial_analytics: bool | None = None
    operational_analytics: bool | None = None
    
    # Inventory features
    inventory_locations: bool | None = None
    fulfillment_services: bool | None = None
    
    # Other features
    vat: bool | None = None
    google_maps: bool | None = None
    subcategories: bool | None = None
    products_filtration: bool | None = None
    b2b: bool | None = None
    partners: bool | None = None
    products_import: bool | None = None
    gift_order_feature: bool | None = None
    metafields: bool | None = None
    extra_pages: bool | None = None
    landing_page: bool | None = None
    menu_editor: bool | None = None
    theme_sdk: bool | None = None
    zid_keys: bool | None = None
    third_party_token: bool | None = None
    consultation: bool | None = None
    cs_emails: bool | None = None
    cs_chat: bool | None = None
    sender_email: bool | None = None
    order_notifications: bool | None = None
    new_order_sms: bool | None = None
    is_different_consignee_allowed: bool | None = None
    custom_copyright: bool | None = None
    mazeed: bool | None = None
    spl_integration: bool | None = None
    store_setup: bool | None = None
    zid_academy: bool | None = None
    
    # Integrations
    zapier_integeration: bool | None = None
    rewaa_integeration: bool | None = None
    qoyod_integeration: bool | None = None
    daftra_integeration: bool | None = None
    customers_bulk_import: bool | None = None
    
    # Fulfillment
    makhzny_activation: bool | None = None
    mkhdoom_activation: bool | None = None
    beez_activation: bool | None = None
    shipox_activation: bool | None = None


class StoreSubscription(BaseModel):
    """Store subscription/plan details."""

    id: str | None = None
    cycle_id: str | None = None
    is_warning: bool | None = None
    is_suspended: bool | None = None
    is_expired: bool | None = None
    is_lifetime: bool | None = None
    expired_at: str | None = None
    subscribed_at: str | None = None
    suspension_start_date: str | None = None
    original_fractional_balance: int | None = None
    message: str | None = None
    package_code: str | None = None
    package_key: str | None = None
    package_variant: str | None = None
    package_name: LocalizedName | None = None
    full_package_name: LocalizedName | None = None
    policies: SubscriptionPolicies | None = None
    # Additional fields from actual API response
    status: str | None = None
    is_trial: bool | None = None
    recurring: bool | None = None
    tier: int | None = None
    is_using_new_package_system: bool | None = None
    is_enterprise: bool | None = None
    has_first_paid_subscription: bool | None = None


class StoreBusinessData(BaseModel):
    """Store business registration data."""

    civil_id: int | None = None
    business_place_status: str | None = None
    has_branches: bool | None = None
    branch_no: int | None = None
    business_type: str | None = None
    business_corporate_name: str | None = None
    employee_no: int | None = None
    email: str | None = None
    commercial_name: str | None = None
    is_maroof_checked: bool | None = None
    is_freelance_checked: bool | None = None
    maroof_number: int | None = None
    civil_id_image: str | None = None
    freelance_certificate: str | None = None
    commercial_register_certificate: str | None = None


class MobileObject(BaseModel):
    """Mobile phone with country code."""

    country_code: str | None = None
    mobile: str | None = None


class SmsCampaignsSenderName(BaseModel):
    """SMS campaigns sender name status."""

    sender_name: str | None = None
    status: str | None = None


class Store(BaseModel):
    """Store information within the profile."""

    id: int | None = None
    uuid: str | None = None
    username: str | None = None
    title: str | None = None
    phone: str | None = None
    mobile_object: MobileObject | None = None
    store_business_data: StoreBusinessData | None = None
    timezone: str | None = None
    commercial_registration_number: str | None = None
    commercial_registration_number_activation: str | None = None
    email: str | None = None
    url: str | None = None
    ssl: str | None = None
    sitemap_url: str | None = None
    currency: StoreCurrency | None = None
    currencies: list[StoreCurrency] | None = None
    language: StoreLanguage | None = None
    languages: list[StoreLanguage] | None = None
    theme: StoreTheme | None = None
    logo: str | None = None
    logos: StoreLogos | None = None
    cover: str | None = None
    icon: str | None = None
    maintenance_mode: bool | None = None
    has_new_products_service: bool | None = None
    
    # Social media
    facebook: str | None = None
    twitter: str | None = None
    instagram: str | None = None
    snapchat: str | None = None
    tiktok: str | None = None
    business_center: str | None = None
    maroof: str | None = None
    website: str | None = None
    
    # SMS/WhatsApp
    sms_campaigns_balance: int | None = None
    sms_campaigns_sender_name: SmsCampaignsSenderName | None = None
    store_whatsapp_balance: float | None = None
    
    # Industry/Category
    industry: StoreIndustry | None = None
    category: StoreCategory | None = None
    category_other: str | None = None
    show_store_selected_category_notification: bool | None = None
    malls: list[str] | None = None
    
    # Customer settings
    is_customers_email_mandatory: bool | None = None
    customers_login_by_sms_status: bool | None = None
    customers_login_by_email_status: bool | None = None
    customers_login_by_whatsapp_status: bool | None = None
    
    # Address settings
    is_gmaps_and_spl_in_address_enabled: bool | None = None
    is_gmaps_in_address_enabled: bool | None = None
    is_gmaps_in_address_mandatory: bool | None = None
    is_spl_in_address_enabled: bool | None = None
    
    # Inventory settings
    is_restock_cancelled_orders_enabled: bool | None = None
    is_low_stock_label_enabled: bool | None = None
    low_stock_quantity_limit: int | None = None
    
    # Feature flags
    is_product_reviews_enabled: bool | None = None
    is_metafields_enabled: bool | None = None
    is_different_consignee_allowed: bool | None = None
    is_2fa_enabled: bool | None = None
    is_export_password_protected: bool | None = None
    
    # SEO
    meta_description: str | None = None
    meta_title: str | None = None
    meta_description_en: str | None = None
    meta_title_en: str | None = None
    
    # Subscription
    subscription: StoreSubscription | None = None
    
    # Additional fields from actual API response
    is_vat_required_in_subscription: bool | None = None
    availability: dict[str, Any] | None = None  # Complex nested object for store hours
    is_selling_blocked: bool | None = None
    created_at: str | None = None
    is_mobile_verified: bool | None = None
    is_user_verified: bool | None = None
    is_readiness_completed: bool | None = None
    allow_email_verification: bool | None = None
    is_user_email_compliance_check_enabled: bool | None = None
    analytics_dashboard_token: str | None = None
    has_vitrin: bool | None = None
    is_orders_assigned_to_closest_inventory_enabled: bool | None = None
    is_zidpay_activated: bool | None = None
    is_zidship_activated: bool | None = None
    is_apple_pay_enabled_in_all_browsers: bool | None = None
    is_buy_as_a_guest_enabled: bool | None = None
    is_buy_as_b2b_enabled: bool | None = None
    is_guest_bank_transfer_supported: bool | None = None
    is_guest_cod_supported: bool | None = None
    is_zid_invoice_generation_enabled: bool | None = None
    has_new_shipping_module: bool | None = None
    has_multi_product_inventory: bool | None = None
    has_pos: bool | None = None
    is_pos_ready: bool | None = None
    has_freemium_pos: bool | None = None
    has_b2b_subscription: bool | None = None
    has_new_themes_only: bool | None = None
    is_single_page_checkout_enabled: bool | None = None
    coupon_limits_use_after_discounts: bool | None = None
    show_pickup_option_stock_availability_for_checkout: bool | None = None
    is_product_question_and_answer_enabled: bool | None = None
    is_merchant_growth_enabled: bool | None = None
    is_international_charge_notice_enabled: bool | None = None
    is_qitaf_enabled: bool | None = None
    has_active_fulfillment_app: bool | None = None
    has_wallet_payments: bool | None = None
    registration_source: str | None = None
    source_app: str | None = None
    is_export_restricted_for_users_outside_store_domain: bool | None = None
    has_installed_marketplace_connect_app: bool | None = None
    is_any_payment_method_activated: bool | None = None
    is_any_shipping_method_activated: bool | None = None
    is_kyc_completed: bool | None = None
    store_has_onboarding: bool | None = None
    has_first_subscription_cashback: bool | None = None


class UserProfileData(BaseModel):
    """User profile data (birth date, location, etc.)."""

    birth_date: str | None = None
    country_id: int | None = None
    city_id: int | None = None
    city: StoreCity | None = None
    country: StoreCountry | None = None
    is_organization_employee: bool | None = None
    working_organization_name: str | None = None
    job_title: str | None = None


class BusinessLocation(BaseModel):
    """Business location address."""

    country: StoreCountry | None = None
    city: StoreCity | None = None
    district: str | None = None
    street: str | None = None
    building_no: str | None = None
    postal_code: str | None = None
    additional_postal_code: str | None = None
    lat: str | None = None
    lng: str | None = None
    show_location: bool | None = None
    national_address_certificate: str | None = None
    is_address_confirmed: bool | None = None


class UserRole(BaseModel):
    """User role information."""

    id: str | None = None
    slug: str | None = None
    name: str | None = None


class UserPermission(BaseModel):
    """User permission information."""

    id: str | None = None
    slug: str | None = None
    name: str | None = None
    description: str | None = None
    order: int | None = None
    relies_on: list[str] | None = None
    package_restrictions: list[dict[str, Any]] | None = None


class StoreManager(BaseModel):
    """Manager/user information within the profile."""

    id: int | None = None
    old_id: int | None = None
    uuid: str | None = None
    name: str | None = None
    username: str | None = None
    email: str | None = None
    email_pending_confirmation: str | None = None
    is_email_verified: bool | None = None
    mobile: str | None = None
    mobile_pending_confirmation: str | None = None
    mobile_object: MobileObject | None = None
    gender: str | None = None
    language_code: str | None = None
    intercom_user_hash: str | None = None
    vloops_ref_code: str | None = None
    user_profile_data: UserProfileData | None = None
    md_session_lifetime: int | None = None
    business_location: BusinessLocation | None = None
    roles: list[UserRole] | None = None
    permissions: list[UserPermission] | None = None
    store: Store | None = None


class StoreProfile(BaseModel):
    """Store profile response model.

    This is the main model returned by the get_profile() endpoint.
    Contains manager info (user) which includes the store details.
    """

    status: str | None = None
    user: StoreManager | None = None


class VATCountryName(BaseModel):
    """Localized country name for VAT settings."""

    ar: str | None = None
    en: str | None = None


class VATCountry(BaseModel):
    """Country information in VAT settings."""

    id: int | None = None
    name: VATCountryName | None = None
    iso_code_2: str | None = None
    iso_code_3: str | None = None


class VATCountrySetting(BaseModel):
    """VAT settings for a specific country."""

    id: str | None = None
    country: VATCountry | None = None
    tax_percentage: float | None = None
    vat_number: str | None = None
    tax_registration_certificate: str | None = None
    settings: list[str] | None = None
    is_certificate_visible: bool | None = None
    is_vat_number_visible: bool | None = None


class TaxSettings(BaseModel):
    """Tax settings configuration."""

    can_use_vat: bool | None = None
    vat_activate: bool | None = None
    is_vat_self_paid: bool | None = None
    is_vat_included_in_product_price: bool | None = None
    is_shipping_fee_included_in_vat: bool | None = None
    other_countries_tax_percentage: float | None = None
    countries: list[VATCountrySetting] | None = None


class VATSettings(BaseModel):
    """VAT settings response model.

    This is the main model returned by the get_vat_settings() endpoint.
    Contains the store's VAT configuration and country-specific tax settings.
    """

    status: str | None = None
    tax_settings: TaxSettings | None = None



