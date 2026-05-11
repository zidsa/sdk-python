"""Core product models for the Zid SDK.

Contains all models needed for the core product endpoints including
nested models for localized names, categories, attributes, images,
weight, SEO, ratings, purchase restrictions, metafields, badges,
stocks, variants, and product settings.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from zid.models.base import BaseModel


# --- Nested Models ---


class LocalizedField(BaseModel):
    """Localized text with Arabic and English values."""

    ar: str | None = None
    en: str | None = None


class ProductCategoryMeta(BaseModel):
    """Metadata for a product category (parent/child relationships)."""

    childs: list[int] = Field(default_factory=list)
    parents: list[int] = Field(default_factory=list)


class ProductCategory(BaseModel):
    """Category assigned to a product."""

    id: str
    name: LocalizedField | None = None
    slug: str
    description: LocalizedField | None = None
    cover_image: str | None = None
    image: str | None = None
    display_order: int | None = None
    meta: ProductCategoryMeta | None = None


class ProductAttribute(BaseModel):
    """Attribute attached to a product (e.g., color, size)."""

    id: str
    slug: str
    name: str
    value: LocalizedField | None = None
    type: str
    type_value: LocalizedField | None = None
    product_id: str
    attribute_image_id: str | None = None
    display_order: int | None = None
    attribute_id: str
    attribute_display_order: int | None = None
    use_as_filter: bool


class ProductImageSizes(BaseModel):
    """Different size URLs for a product image."""

    thumbnail: str
    full_size: str
    medium: str
    small: str
    large: str


class ProductImage(BaseModel):
    """A product image with multiple size variants."""

    id: str
    image: ProductImageSizes
    alt_text: str | None = None
    display_order: int | None = None


class ProductWeight(BaseModel):
    """Product weight with value and unit."""

    value: float | None = None
    unit: str


class ProductSeo(BaseModel):
    """SEO metadata for a product."""

    title: LocalizedField | None = None
    description: LocalizedField | None = None


class RatingBreakdown(BaseModel):
    """Rating count and percentage for a single star level."""

    percentage: float
    count: int


class ProductRating(BaseModel):
    """Product rating statistics across all star levels."""

    average: int | float
    total_count: int
    ratings_1: RatingBreakdown | None = Field(default=None, validation_alias="1_ratings")
    ratings_2: RatingBreakdown | None = Field(default=None, validation_alias="2_ratings")
    ratings_3: RatingBreakdown | None = Field(default=None, validation_alias="3_ratings")
    ratings_4: RatingBreakdown | None = Field(default=None, validation_alias="4_ratings")
    ratings_5: RatingBreakdown | None = Field(default=None, validation_alias="5_ratings")


class PurchaseRestrictions(BaseModel):
    """Restrictions on product purchasing (quantity limits, availability windows)."""

    min_quantity_per_cart: int | None = None
    max_quantity_per_cart: int | None = None
    availability_period_start: str | int | None = None
    availability_period_end: str | int | None = None
    sale_price_period_start: str | int | None = None
    sale_price_period_end: str | int | None = None


class ProductMetafield(BaseModel):
    """Custom metafield attached to a product."""

    id: str
    name: LocalizedField | None = None
    slug: str
    data_type: str
    display_order: int
    value: Any = None


class ProductBadgeIcon(BaseModel):
    """Icon associated with a product badge."""

    code: str


class ProductBadge(BaseModel):
    """Badge displayed on a product (e.g., 'New', 'Sale')."""

    body: LocalizedField | None = None
    icon: ProductBadgeIcon | None = None
    is_example: bool | None = None


class StockLocation(BaseModel):
    """Location information for a stock entry.

    The API sometimes returns ``name`` as a localized object
    (``{"ar": "...", "en": "..."}``) and sometimes as a plain string.
    Both forms are accepted.
    """

    id: str
    name: LocalizedField | str | None = None
    type: str
    full_address: str


class ProductStock(BaseModel):
    """Stock entry for a product at a specific location."""

    id: str
    location: StockLocation
    available_quantity: int | None = None
    is_infinite: bool


class ProductMeta(BaseModel):
    """Product metadata (location, parent/child relationships)."""

    location_id: str | None = None
    childs: list[str] | None = None
    parents: list[str] | None = None


class ProductOption(BaseModel):
    """A selectable option on a product (e.g., size, color)."""

    id: str
    name: str
    slug: str
    choices: list[str] = Field(default_factory=list)


class ProductVariant(BaseModel):
    """A product variant with its own pricing, stock, and attributes.

    Variants share most fields with the parent product but can override
    pricing, SKU, stock, and other properties.
    """

    id: str
    product_class: str | None = None
    sku: str | None = None
    barcode: str | None = None
    parent_id: str | None = None
    name: LocalizedField | None = None
    slug: str | None = None
    price: float | None = None
    short_description: LocalizedField | str | None = None
    sale_price: float | None = None
    formatted_price: str | None = None
    formatted_sale_price: str | None = None
    currency: str | None = None
    currency_symbol: str | None = None
    attributes: list[ProductAttribute] = Field(default_factory=list)
    categories: list[ProductCategory] = Field(default_factory=list)
    display_order: int | None = None
    has_options: bool | None = None
    has_fields: bool | None = None
    images: list[Any] = Field(default_factory=list)
    videos: list[Any] = Field(default_factory=list)
    is_draft: bool | None = None
    quantity: int | None = None
    is_infinite: bool | None = None
    html_url: str | None = None
    weight: ProductWeight | None = None
    keywords: list[str] = Field(default_factory=list)
    requires_shipping: bool | None = None
    is_taxable: bool | None = None
    structure: str | None = None
    seo: str | None = None
    rating: ProductRating | None = None
    store_id: int | None = None
    purchase_restrictions: PurchaseRestrictions | None = None
    metafields: list[ProductMetafield] | None = Field(default=None)
    meta: list[str] | None = None
    related_products_settings: str | None = None
    related_products_title: LocalizedField | None = None
    badge: ProductBadge | None = None
    cost: float | None = None
    is_published: bool | None = None
    waiting_customers_count: int | None = None
    group_products: list[Any] | None = None
    stocks: list[ProductStock] = Field(default_factory=list)
    sold_products_count: int | None = None
    created_at: str | None = None
    updated_at: str | None = None


# --- Main Models ---


class Product(BaseModel):
    """A Zid store product.

    Represents a detailed product object including pricing, media,
    inventory, SEO, ratings, metafields, and grouped products.

    Returned by ``GET /v1/products/`` and ``GET /v1/products/{product_id}/``.
    """

    id: str
    product_class: str | None = None
    sku: str | None = None
    barcode: str | None = None
    parent_id: str | None = None
    name: LocalizedField | None = None
    slug: str | None = None
    price: float | None = None
    short_description: LocalizedField | str | None = None
    sale_price: float | None = None
    formatted_price: str | None = None
    formatted_sale_price: str | None = None
    currency: str | None = None
    currency_symbol: str | None = None
    attributes: list[ProductAttribute] = Field(default_factory=list)
    categories: list[ProductCategory] = Field(default_factory=list)
    display_order: int | None = None
    has_options: bool | None = None
    has_fields: bool | None = None
    images: list[Any] = Field(default_factory=list)
    videos: list[Any] = Field(default_factory=list)
    is_draft: bool | None = None
    quantity: int | None = None
    is_infinite: bool | None = None
    html_url: str | None = None
    weight: ProductWeight | None = None
    keywords: list[str] = Field(default_factory=list)
    requires_shipping: bool | None = None
    is_taxable: bool | None = None
    structure: str | None = None
    seo: ProductSeo | None = None
    rating: ProductRating | None = None
    store_id: int | None = None
    purchase_restrictions: PurchaseRestrictions | None = None
    metafields: list[ProductMetafield] | None = Field(default=None)
    meta: ProductMeta | None = None
    related_products_settings: str | None = None
    related_products_title: LocalizedField | None = None
    badge: ProductBadge | None = None
    variants: list[ProductVariant] | None = None
    cost: float | None = None
    is_published: bool | None = None
    waiting_customers_count: int | None = None
    description: LocalizedField | None = None
    custom_user_input_fields: list[Any] | None = None
    custom_option_fields: list[Any] | None = None
    options: list[ProductOption] | None = None
    related_products: list[str] | None = None
    next_product: str | None = None
    previous_product: str | None = None
    group_products: list[Any] | None = None
    stocks: list[ProductStock] = Field(default_factory=list)
    vouchers_count: int | None = None
    sold_products_count: int | None = None
    created_at: str | None = None
    updated_at: str | None = None


class ProductSettings(BaseModel):
    """Store-level product configuration settings.

    Returned by ``GET /v1/products/settings``.
    """

    extended_search_support: bool
    related_products_status: bool
    related_products_count: int
    sold_products_count_status: bool
    min_sold_products_count: int
    default_products_ordering: str
    has_products_filtration: bool
    is_wishlist_enabled: bool
