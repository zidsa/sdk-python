"""Category models for the Zid SDK.

Contains models for store categories used in product-category assignment
and store category management endpoints.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from zid.models.base import BaseModel
from zid.models.product._base import LocalizedField


# --- Nested Models ---


class CategoryMetafield(BaseModel):
    """Metafield attached to a category."""

    id: str
    name: LocalizedField | None = None
    slug: str
    data_type: str
    display_order: int
    structure_definition: str | None = None
    value: Any = None


class CategoryMeta(BaseModel):
    """Hierarchy metadata for a short category (parent/child relationships)."""

    childs: list[Any] = Field(default_factory=list)
    parents: list[Any] = Field(default_factory=list)


# --- Main Models ---


class ShortCategory(BaseModel):
    """Minimal category representation with only basic fields.

    Returned in the ``minimal_categories`` array from
    ``GET /v1/managers/store/categories``.
    """

    id: int
    name: str | None = None
    is_published: bool | None = None


class Category(BaseModel):
    """Store category from the manager category list.

    Returned in the ``categories`` array from
    ``GET /v1/managers/store/categories``. Contains SEO info,
    product counts, sub-categories, and metafields.
    """

    id: int
    uuid: str | None = None
    name: str | None = None
    slug: str | None = None
    seo_category_title: str | None = Field(
        default=None, validation_alias="SEO_category_title",
    )
    seo_category_description: str | None = Field(
        default=None, validation_alias="SEO_category_description",
    )
    names: LocalizedField | None = None
    description: LocalizedField | None = None
    url: str | None = None
    image: str | None = None
    image_full_size: str | None = None
    img_alt_text: str | None = None
    products_count: int | None = None
    sub_categories: list[Category] | None = Field(default_factory=list)
    parent_id: int | None = None
    flat_name: str | None = None
    is_published: bool | None = None
    metafields: list[CategoryMetafield] = Field(default_factory=list)


class CategoryDetail(BaseModel):
    """Detailed category from the view/create/update endpoints.

    Returned by ``GET /v1/managers/store/categories/{id}/view``,
    ``POST /v1/managers/store/categories/add``, and
    ``POST /v1/managers/store/categories/{id}/update``.

    Extends the list representation with i18n SEO fields, cover image,
    and full-size image URL.
    """

    id: int
    name: str | None = None
    uuid: str | None = None
    slug: str | None = None
    seo_category_title: str | None = Field(
        default=None, validation_alias="SEO_category_title",
    )
    seo_category_description: str | None = Field(
        default=None, validation_alias="SEO_category_description",
    )
    i18n_seo_category_title: LocalizedField | None = Field(
        default=None, validation_alias="i18n_SEO_category_title",
    )
    i18n_seo_category_description: LocalizedField | None = Field(
        default=None, validation_alias="i18n_SEO_category_description",
    )
    names: LocalizedField | None = None
    description: LocalizedField | None = None
    url: str | None = None
    image: str | None = None
    image_full_size: str | None = None
    img_alt_text: str | None = None
    i18n_img_alt_text: LocalizedField | None = None
    cover_image: str | None = None
    image_full: str | None = None
    products_count: int | None = None
    sub_categories: list[CategoryDetail] | None = Field(default_factory=list)
    parent_id: int | None = None
    flat_name: str | None = None
    is_published: bool | None = None
    metafields: list[CategoryMetafield] = Field(default_factory=list)


class AssignedCategory(BaseModel):
    """Category returned after assigning a product to a category.

    Returned by ``POST /v1/products/{product_id}/categories/``.
    """

    id: str
    name: LocalizedField | str | None = None
    slug: str | None = None
    description: LocalizedField | str | None = None
    cover_image: str | None = None
    image: str | None = None
    display_order: int | None = None
    meta: CategoryMeta | None = None
