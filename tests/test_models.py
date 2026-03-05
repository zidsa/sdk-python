"""Unit tests for Pydantic models.

Tests model parsing, serialization, and edge cases.
"""

import pytest

from zid.models.customer import Customer, CustomerCity
from zid.models.order import (
    Order,
    OrderSimple,
    OrderTiny,
    OrderCurrency,
    OrderCurrencyInfo,
    OrderStatus,
    OrderCustomer,
)


class TestCustomerModel:
    """Tests for Customer model."""
    
    def test_parse_from_fixture(self, customer_list_response):
        """Parse customer from real API fixture."""
        if not customer_list_response.get("customers"):
            pytest.skip("No customers in fixture")
        
        data = customer_list_response["customers"][0]
        customer = Customer.model_validate(data)
        assert customer.id is not None
        assert customer.name is not None
    
    def test_parse_full(self, customer_detail_response):
        """Parse customer from real API response."""
        data = customer_detail_response.get("customer", customer_detail_response)
        customer = Customer.model_validate(data)
        assert customer.id is not None
        assert customer.name is not None
    
    def test_dict_access(self, customer_list_response):
        """Model supports dict-style access."""
        if not customer_list_response.get("customers"):
            pytest.skip("No customers in fixture")
        
        data = customer_list_response["customers"][0]
        customer = Customer.model_validate(data)
        assert customer["id"] == customer.id
        assert customer["name"] == customer.name
    
    def test_dict_access_missing_key(self, customer_list_response):
        """Dict access raises KeyError for missing keys."""
        if not customer_list_response.get("customers"):
            pytest.skip("No customers in fixture")
        
        data = customer_list_response["customers"][0]
        customer = Customer.model_validate(data)
        with pytest.raises(KeyError):
            _ = customer["nonexistent_field_xyz"]


class TestOrderModels:
    """Tests for Order models."""
    
    def test_parse_order_simple(self, orders_list_response):
        """Parse OrderSimple from list response."""
        if not orders_list_response.get("orders"):
            pytest.skip("No orders in fixture")
        
        data = orders_list_response["orders"][0]
        order = OrderSimple.model_validate(data)
        assert order.id is not None
        assert order.code is not None
    
    def test_parse_order_full(self, orders_list_default_response):
        """Parse full Order from default payload response."""
        if not orders_list_default_response.get("orders"):
            pytest.skip("No orders in fixture")
        
        data = orders_list_default_response["orders"][0]
        order = Order.model_validate(data)
        assert order.id is not None
    
    def test_parse_order_detail(self, order_detail_response):
        """Parse Order from detail endpoint."""
        data = order_detail_response.get("order", order_detail_response)
        order = Order.model_validate(data)
        assert order.id is not None
    
    def test_currency_wrapper_structure(self):
        """Currency field is a wrapper with nested objects."""
        data = {
            "id": 1,
            "invoice_number": 123,
            "currency": {
                "order_currency": {
                    "id": 4,
                    "code": "SAR",
                    "exchange_rate": 1,
                },
                "order_store_currency": {
                    "id": 4,
                    "code": "SAR",
                    "exchange_rate": None,
                }
            }
        }
        order = Order.model_validate(data)
        assert order.currency is not None
        assert order.currency.order_currency is not None
        assert order.currency.order_currency.code == "SAR"
    
    def test_order_status_nested(self):
        """Order status is a nested object."""
        data = {
            "id": 1,
            "invoice_number": 123,
            "order_status": {
                "name": "New",
                "code": "new",
            }
        }
        order = OrderSimple.model_validate(data)
        assert order.order_status is not None
        assert order.order_status.code == "new"
    
    def test_order_tiny_minimal(self):
        """OrderTiny has minimal fields."""
        data = {
            "id": 1,
            "invoice_number": 123,
        }
        order = OrderTiny.model_validate(data)
        assert order.id == 1


class TestModelSerialization:
    """Tests for model serialization round-trips."""
    
    def test_customer_roundtrip(self, customer_list_response):
        """Customer can be serialized and re-parsed."""
        if not customer_list_response.get("customers"):
            pytest.skip("No customers in fixture")
        
        data = customer_list_response["customers"][0]
        original = Customer.model_validate(data)
        
        # Serialize to dict
        serialized = original.model_dump()
        
        # Re-parse
        restored = Customer.model_validate(serialized)
        
        assert restored.id == original.id
        assert restored.name == original.name
    
    def test_order_roundtrip(self, orders_list_response):
        """Order can be serialized and re-parsed."""
        if not orders_list_response.get("orders"):
            pytest.skip("No orders in fixture")
        
        data = orders_list_response["orders"][0]
        original = OrderSimple.model_validate(data)
        
        serialized = original.model_dump()
        restored = OrderSimple.model_validate(serialized)
        
        assert restored.id == original.id
        assert restored.code == original.code


from zid.models.coupon import Coupon, CouponDetail
from zid.models.bundle_offer import BundleOffer, LocalizedText, BundleOfferCondition
from zid.models.loyalty import (
    CashbackRule,
    CustomerLoyalty,
    LoyaltyInfo,
    LoyaltyProgram,
    LoyaltyTransaction,
    LoyaltyTransactionSimple,
    RedemptionRule,
)


class TestCouponModel:
    """Tests for Coupon and CouponDetail models."""

    def test_parse_from_fixture(self, coupons_list_response):
        """Parse coupon from real API fixture."""
        data = coupons_list_response["coupons"][0]
        coupon = Coupon.model_validate(data)
        assert coupon.id == 5851950
        assert coupon.coupon_id == 5851950
        assert coupon.code == "49QA62"
        assert coupon.discount_type == "p"
        assert coupon.discount == 111
        assert coupon.is_active is True
        assert coupon.status_code == "coupon_active"

    def test_parse_detail(self, coupon_detail_response):
        """Parse CouponDetail from view endpoint fixture."""
        data = coupon_detail_response["coupon"]
        detail = CouponDetail.model_validate(data)
        assert detail.id == 5776883
        assert detail.code == "P2ZAHN"
        assert detail.total_sales == 0
        assert detail.total_customers == 0
        assert detail.note is None
        assert detail.orders == []
        assert detail.apply_to_data == []

    def test_coupon_roundtrip(self, coupons_list_response):
        """Coupon can be serialized and re-parsed."""
        data = coupons_list_response["coupons"][0]
        original = Coupon.model_validate(data)
        serialized = original.model_dump()
        restored = Coupon.model_validate(serialized)
        assert restored.id == original.id
        assert restored.code == original.code


class TestBundleOfferModel:
    """Tests for BundleOffer model."""

    def test_parse_from_fixture(self, bundle_offers_list_response):
        """Parse bundle offer from fixture."""
        data = bundle_offers_list_response["discount_rules"][0]
        offer = BundleOffer.model_validate(data)
        assert offer.id == "02ed8742-354d-4b44-8f3f-39766081c12e"
        assert offer.code == "bundle_offer"
        assert offer.enabled is True
        assert offer.status_code == "active"
        assert isinstance(offer.name, LocalizedText)
        assert offer.name.en == "Buy 2 Get 1 Free"

    def test_conditions_and_actions(self, bundle_offers_list_response):
        """Bundle offer conditions and actions are parsed."""
        data = bundle_offers_list_response["discount_rules"][0]
        offer = BundleOffer.model_validate(data)
        assert len(offer.conditions) == 1
        assert offer.conditions[0].field == "products_quantity"
        assert offer.conditions[0].operator == ">="
        assert len(offer.actions) == 1
        assert offer.actions[0].type == "free"

    def test_empty_list_coercion_for_description(self, bundle_offers_list_response):
        """Empty list description is coerced to None by BaseModel."""
        data = bundle_offers_list_response["discount_rules"][1]
        offer = BundleOffer.model_validate(data)
        # BaseModel's _coerce_empty_lists_to_none converts [] to None
        assert offer.description is None

    def test_localized_description(self, bundle_offers_list_response):
        """Localized description object is parsed correctly."""
        data = bundle_offers_list_response["discount_rules"][0]
        offer = BundleOffer.model_validate(data)
        assert isinstance(offer.description, LocalizedText)
        assert offer.description.en == "Summer bundle deal"

    def test_bundle_offer_roundtrip(self, bundle_offers_list_response):
        """BundleOffer can be serialized and re-parsed."""
        data = bundle_offers_list_response["discount_rules"][0]
        original = BundleOffer.model_validate(data)
        serialized = original.model_dump()
        restored = BundleOffer.model_validate(serialized)
        assert restored.id == original.id
        assert restored.code == original.code


class TestLoyaltyModels:
    """Tests for Loyalty models."""

    def test_parse_program(self, loyalty_program_response):
        """Parse LoyaltyProgram from fixture."""
        program = LoyaltyProgram.model_validate(loyalty_program_response)
        assert program.total_earned_points == 1271060
        assert program.total_redeemed_points == 2004  # API typo: total_redemed_points
        assert program.total_pending_points == 51419
        assert program.total_customers_with_points == 48
        assert program.expiration_period == 5  # API typo: expiration_peroid
        assert program.is_active is True

    def test_cashback_rules(self, loyalty_program_response):
        """Cashback rules are parsed correctly."""
        program = LoyaltyProgram.model_validate(loyalty_program_response)
        assert len(program.cashback_rules) == 2
        rule = program.cashback_rules[0]
        assert rule.id == "b1e3ca5d-2a89-4993-89bf-0f31a4b70b00"
        assert rule.points_rewarded == 1
        assert rule.available_to is None

    def test_cashback_rule_with_available_to(self, loyalty_program_response):
        """Cashback rule with available_to object is parsed."""
        program = LoyaltyProgram.model_validate(loyalty_program_response)
        rule = program.cashback_rules[1]
        assert rule.available_to is not None
        assert rule.available_to.tags == []
        assert rule.available_to.level is not None
        assert rule.available_to.level.level_id is None

    def test_redemption_rules(self, loyalty_program_response):
        """Redemption rules are parsed correctly."""
        program = LoyaltyProgram.model_validate(loyalty_program_response)
        assert len(program.redemption_rules) == 1
        rule = program.redemption_rules[0]
        assert rule.id == "175ebe13-9070-4e7d-819e-2f8ba5797b1d"
        assert rule.points_to_redeem == 3
        assert rule.rule_type == "fixed_rate_settings"
        assert rule.reward.discount_value == 1

    def test_customer_loyalty_with_typo_fields(self, loyalty_customer_response):
        """CustomerLoyalty handles API typo fields correctly."""
        data = loyalty_customer_response["loyalty_points_info"]
        loyalty = CustomerLoyalty.model_validate(data)
        assert loyalty.points_balance == 0
        assert loyalty.pending_points_balance == 10
        assert loyalty.available_points == 0  # API sends available_poitns
        assert loyalty.used_points == 6826  # API sends used_poitns
        assert loyalty.total_positive_points == 6836

    def test_customer_loyalty_history(self, loyalty_customer_response):
        """CustomerLoyalty history transactions are parsed."""
        data = loyalty_customer_response["loyalty_points_info"]
        loyalty = CustomerLoyalty.model_validate(data)
        assert len(loyalty.history) == 2
        tx = loyalty.history[0]
        assert isinstance(tx, LoyaltyTransaction)
        assert tx.direction == "-"
        assert tx.type == "expiry"
        assert tx.point_status_code == "expired"

    def test_loyalty_info(self):
        """LoyaltyInfo parses localized content."""
        data = {
            "title_ar": "نقاط الولاء",
            "title_en": None,
            "content_ar": "<p>محتوى</p>",
            "content_en": None,
        }
        info = LoyaltyInfo.model_validate(data)
        assert info.title_ar == "نقاط الولاء"
        assert info.title_en is None

    def test_loyalty_transaction_simple(self):
        """LoyaltyTransactionSimple from adjust-points response."""
        data = {
            "date": "2026-03-02T13:26:14.000000Z",
            "reason": "gift",
            "points": 5,
            "direction": "+",
            "type": "ManualAccumulation",
            "order_number": None,
            "expiry_date": None,
            "point_status": "Active",
            "collection_method": "Manually added points",
        }
        tx = LoyaltyTransactionSimple.model_validate(data)
        assert tx.points == 5
        assert tx.direction == "+"
        assert tx.type == "ManualAccumulation"
        assert tx.point_status == "Active"

    def test_program_roundtrip(self, loyalty_program_response):
        """LoyaltyProgram can be serialized and re-parsed."""
        original = LoyaltyProgram.model_validate(loyalty_program_response)
        serialized = original.model_dump()
        restored = LoyaltyProgram.model_validate(serialized)
        assert restored.total_earned_points == original.total_earned_points
        assert restored.expiration_period == original.expiration_period


from zid.models.product import Product, ProductSettings
from zid.models.product._base import (
    LocalizedField,
    ProductAttribute,
    ProductBadge,
    ProductCategory,
    ProductImage,
    ProductMetafield,
    ProductRating,
    ProductStock,
    ProductVariant,
)


class TestProductModel:
    """Tests for Product model."""

    def test_parse_from_list_fixture(self, products_list_response):
        """Parse product from list response fixture."""
        data = products_list_response["results"][0]
        product = Product.model_validate(data)
        assert product.id == "a1477bb2-72ea-4be9-b2cf-093cefc721bb"
        assert product.product_class == "voucher"
        assert product.sku == "Z.1770805225810645"
        assert product.price == 100
        assert product.is_published is True
        assert product.structure == "standalone"

    def test_parse_product_with_attributes(self, products_list_response):
        """Parse product that has attributes."""
        data = products_list_response["results"][1]
        product = Product.model_validate(data)
        assert len(product.attributes) == 1
        attr = product.attributes[0]
        assert isinstance(attr, ProductAttribute)
        assert attr.id == "1ac221ff-f1d4-4abc-9995-45609e0faa7d"
        assert attr.use_as_filter is True

    def test_parse_categories(self, products_list_response):
        """Parse product categories as nested models."""
        data = products_list_response["results"][0]
        product = Product.model_validate(data)
        assert len(product.categories) == 1
        cat = product.categories[0]
        assert isinstance(cat, ProductCategory)
        assert cat.id == "1473476"
        assert isinstance(cat.name, LocalizedField)
        assert cat.name.en == "Electronics"

    def test_parse_stocks(self, products_list_response):
        """Parse product stocks as nested models."""
        data = products_list_response["results"][0]
        product = Product.model_validate(data)
        assert len(product.stocks) == 1
        stock = product.stocks[0]
        assert isinstance(stock, ProductStock)
        assert stock.available_quantity == 4
        assert stock.is_infinite is False
        assert stock.location.type == "PHYSICAL"

    def test_parse_rating(self, products_list_response):
        """Parse product rating with star breakdowns."""
        data = products_list_response["results"][1]
        product = Product.model_validate(data)
        assert product.rating is not None
        assert isinstance(product.rating, ProductRating)
        assert product.rating.average == 4
        assert product.rating.total_count == 10
        assert product.rating.ratings_5 is not None
        assert product.rating.ratings_5.count == 4

    def test_parse_badge(self, products_list_response):
        """Parse product badge."""
        data = products_list_response["results"][1]
        product = Product.model_validate(data)
        assert product.badge is not None
        assert isinstance(product.badge, ProductBadge)
        assert product.badge.body.en == "Selling fast"
        assert product.badge.icon.code == "selling_fast"

    def test_parse_detail_with_variants(self, product_detail_response):
        """Parse product detail with variants."""
        product = Product.model_validate(product_detail_response)
        assert product.id == "2829a483-4336-43ab-a855-84532c9419c2"
        assert product.structure == "parent"
        assert product.has_options is True
        assert product.variants is not None
        assert len(product.variants) == 1
        variant = product.variants[0]
        assert isinstance(variant, ProductVariant)
        assert variant.parent_id == "2829a483-4336-43ab-a855-84532c9419c2"
        assert variant.structure == "child"

    def test_parse_detail_options(self, product_detail_response):
        """Parse product options from detail response."""
        product = Product.model_validate(product_detail_response)
        assert product.options is not None
        assert len(product.options) == 1
        assert product.options[0].name == "درجة اللون"
        assert product.options[0].choices == ["12", "55", "15"]

    def test_parse_detail_description(self, product_detail_response):
        """Parse product description from detail response."""
        product = Product.model_validate(product_detail_response)
        assert product.description is not None
        assert product.description.en == "Product description"

    def test_parse_metafields(self, product_detail_response):
        """Parse product metafields."""
        product = Product.model_validate(product_detail_response)
        assert len(product.metafields) == 1
        mf = product.metafields[0]
        assert isinstance(mf, ProductMetafield)
        assert mf.data_type == "number"
        assert mf.name.en == "Calories"

    def test_parse_images(self, product_detail_response):
        """Parse product images with size variants."""
        product = Product.model_validate(product_detail_response)
        assert len(product.images) == 1

    def test_product_roundtrip(self, products_list_response):
        """Product can be serialized and re-parsed."""
        data = products_list_response["results"][0]
        original = Product.model_validate(data)
        serialized = original.model_dump()
        restored = Product.model_validate(serialized)
        assert restored.id == original.id
        assert restored.sku == original.sku
        assert restored.price == original.price

    def test_product_detail_roundtrip(self, product_detail_response):
        """Product detail can be serialized and re-parsed."""
        original = Product.model_validate(product_detail_response)
        serialized = original.model_dump()
        restored = Product.model_validate(serialized)
        assert restored.id == original.id
        assert restored.structure == original.structure
        assert len(restored.variants or []) == len(original.variants or [])

    def test_parse_settings(self, product_settings_response):
        """Parse ProductSettings from fixture."""
        data = product_settings_response["settings"]
        settings = ProductSettings.model_validate(data)
        assert settings.extended_search_support is False
        assert settings.related_products_count == 8
        assert settings.default_products_ordering == "-is_infinite,-quantity"
        assert settings.is_wishlist_enabled is True

    def test_null_badge(self, products_list_response):
        """Product with null badge parses correctly."""
        data = products_list_response["results"][0]
        product = Product.model_validate(data)
        assert product.badge is None


from zid.models.product._voucher import OrderVoucher, Voucher


class TestVoucherModel:
    """Tests for Voucher and OrderVoucher models."""

    def test_parse_from_list_fixture(self, product_vouchers_list_response):
        """Parse voucher from list response fixture."""
        data = product_vouchers_list_response["results"][0]
        voucher = Voucher.model_validate(data)
        assert voucher.id == "0b470326-d2b1-4d96-8ee1-ea03a50dfd83"
        assert voucher.product_id == "a1477bb2-72ea-4be9-b2cf-093cefc721bb"
        assert voucher.status == "AVAILABLE"
        assert voucher.key == "FX00001"
        assert voucher.pin_code == "12345"
        assert voucher.serial_number == "Z.12345"
        assert voucher.order is None
        assert voucher.expires_at == "2026-10-10T03:00:00Z"
        assert voucher.expires_at_formatted == "Oct 10, 2026"

    def test_parse_sold_voucher(self, product_vouchers_list_response):
        """Parse a sold voucher with an associated order."""
        data = product_vouchers_list_response["results"][1]
        voucher = Voucher.model_validate(data)
        assert voucher.id == "3663992f-989e-4056-9a71-02a9109ec7fa"
        assert voucher.status == "SOLD"
        assert voucher.order == 64855100
        assert voucher.key == "key-1"
        assert voucher.expires_at_formatted is None

    def test_parse_order_voucher(self, order_vouchers_response):
        """Parse OrderVoucher from order vouchers fixture."""
        data = order_vouchers_response["results"][0]
        voucher = OrderVoucher.model_validate(data)
        assert voucher.id == "0b470326-d2b1-4d96-8ee1-ea03a50dfd83"
        assert voucher.status == "RESERVED"
        assert voucher.order == 64855100
        assert voucher.key == "FX00001"

    def test_voucher_roundtrip(self, product_vouchers_list_response):
        """Voucher can be serialized and re-parsed."""
        data = product_vouchers_list_response["results"][0]
        original = Voucher.model_validate(data)
        serialized = original.model_dump()
        restored = Voucher.model_validate(serialized)
        assert restored.id == original.id
        assert restored.key == original.key
        assert restored.status == original.status
        assert restored.pin_code == original.pin_code

    def test_order_voucher_roundtrip(self, order_vouchers_response):
        """OrderVoucher can be serialized and re-parsed."""
        data = order_vouchers_response["results"][0]
        original = OrderVoucher.model_validate(data)
        serialized = original.model_dump()
        restored = OrderVoucher.model_validate(serialized)
        assert restored.id == original.id
        assert restored.order == original.order
        assert restored.status == original.status


from zid.models.product._category import (
    AssignedCategory,
    Category,
    CategoryDetail,
    CategoryMetafield,
    ShortCategory,
)


class TestCategoryModel:
    """Tests for Category, CategoryDetail, ShortCategory, and AssignedCategory models."""

    def test_parse_category_from_list_fixture(self, product_categories_list_response):
        """Parse Category from list response fixture."""
        data = product_categories_list_response["categories"][0]
        cat = Category.model_validate(data)
        assert cat.id == 1473477
        assert cat.uuid == "8cc71774-bf3e-4383-9778-64d50d965dc7"
        assert cat.name == "test sub"
        assert cat.slug == "تصنيف-فرعي"
        assert cat.seo_category_title == "test sub"
        assert cat.seo_category_description == "Sub category 1"
        assert cat.names.en == "test sub"
        assert cat.names.ar == "تصنيف فرعي"
        assert cat.products_count == 1
        assert cat.is_published is False
        assert cat.parent_id is None
        assert cat.flat_name == "test sub"

    def test_parse_category_with_sub_categories(self, product_categories_list_response):
        """Parse Category that has sub_categories."""
        data = product_categories_list_response["categories"][1]
        cat = Category.model_validate(data)
        assert cat.id == 1259096
        assert cat.image is not None
        assert cat.image_full_size is not None
        assert len(cat.sub_categories) == 1
        sub = cat.sub_categories[0]
        assert isinstance(sub, Category)
        assert sub.id == 1399659
        assert sub.parent_id == 1259096
        assert sub.is_published is True

    def test_parse_category_metafields(self, product_categories_list_response):
        """Parse metafields on a Category."""
        data = product_categories_list_response["categories"][0]
        cat = Category.model_validate(data)
        assert len(cat.metafields) == 1
        mf = cat.metafields[0]
        assert isinstance(mf, CategoryMetafield)
        assert mf.id == "2cf0cf26-d468-452a-9492-2fe5970c3cd8"
        assert mf.slug == "Color-1"
        assert mf.data_type == "text"
        assert mf.display_order == 3
        assert mf.name.en == "Color"

    def test_parse_category_detail(self, product_category_detail_response):
        """Parse CategoryDetail from view endpoint fixture."""
        data = product_category_detail_response["categories"]
        detail = CategoryDetail.model_validate(data)
        assert detail.id == 1473477
        assert detail.uuid == "8cc71774-bf3e-4383-9778-64d50d965dc7"
        assert detail.seo_category_title == "test sub"
        assert detail.i18n_seo_category_title.ar == "تصنيف فرعي"
        assert detail.i18n_seo_category_title.en == "test sub"
        assert detail.i18n_seo_category_description.ar == "تصنيف فرعي1"
        assert detail.i18n_seo_category_description.en == "Sub category 1"
        assert detail.names.en == "test sub"
        assert detail.description.en == "Sub category 1"
        assert detail.cover_image is None
        assert detail.image_full is None
        assert detail.is_published is False
        assert len(detail.metafields) == 2

    def test_parse_short_category(self, product_categories_list_response):
        """Parse ShortCategory from minimal_categories array."""
        data = product_categories_list_response["minimal_categories"][0]
        short = ShortCategory.model_validate(data)
        assert short.id == 1473477
        assert short.name == "test sub"
        assert short.is_published is False

    def test_parse_assigned_category(self):
        """Parse AssignedCategory from assign endpoint response."""
        data = {
            "id": "1473477",
            "name": "test sub",
            "slug": "تصنيف-فرعي",
            "description": "Sub category 1",
            "cover_image": None,
            "image": None,
            "display_order": 0,
            "meta": {
                "childs": [],
                "parents": [],
            },
        }
        assigned = AssignedCategory.model_validate(data)
        assert assigned.id == "1473477"
        assert assigned.name == "test sub"
        assert assigned.display_order == 0
        assert assigned.meta.childs == []
        assert assigned.meta.parents == []

    def test_category_roundtrip(self, product_categories_list_response):
        """Category can be serialized and re-parsed."""
        data = product_categories_list_response["categories"][0]
        original = Category.model_validate(data)
        serialized = original.model_dump()
        restored = Category.model_validate(serialized)
        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.slug == original.slug
        assert restored.is_published == original.is_published

    def test_category_detail_roundtrip(self, product_category_detail_response):
        """CategoryDetail can be serialized and re-parsed."""
        data = product_category_detail_response["categories"]
        original = CategoryDetail.model_validate(data)
        serialized = original.model_dump()
        restored = CategoryDetail.model_validate(serialized)
        assert restored.id == original.id
        assert restored.uuid == original.uuid
        assert restored.is_published == original.is_published
        assert len(restored.metafields) == len(original.metafields)


from zid.models.product._notification import (
    NotificationCustomer,
    NotificationSettings,
    NotificationStats,
    ProductNotification,
)


class TestProductNotificationModel:
    """Tests for ProductNotification, NotificationStats, and NotificationSettings models."""

    def test_parse_from_list_fixture(self, product_notifications_list_response):
        """Parse ProductNotification from list response fixture."""
        data = product_notifications_list_response["results"][0]
        notification = ProductNotification.model_validate(data)
        assert notification.id == "0d8f7dc9-423d-4e54-ab47-6c170f4c0d84"
        assert notification.product_id == "a7ad89d0-03e2-430f-b6e4-0624ef05e571"
        assert notification.language == "ar"
        assert notification.is_notified is False
        assert notification.code == "5XRDXCSL"
        assert notification.is_purchased is False
        assert notification.purchased_total == 0

    def test_parse_notification_customer(self, product_notifications_list_response):
        """Parse nested customer within a notification."""
        data = product_notifications_list_response["results"][0]
        notification = ProductNotification.model_validate(data)
        assert isinstance(notification.customer, NotificationCustomer)
        assert notification.customer.id == 1
        assert notification.customer.name == "مازن الضراب"
        assert notification.customer.email == "test@test.com"
        assert notification.customer.phone_number == "+966501234567"

    def test_parse_notification_product_name(self, product_notifications_list_response):
        """Parse localized product name within a notification."""
        data = product_notifications_list_response["results"][0]
        notification = ProductNotification.model_validate(data)
        assert notification.product_name is not None
        assert notification.product_name.ar == "لوحة"
        assert notification.product_name.en == "voucher-no1 & small size"

    def test_parse_notified_notification(self, product_notifications_list_response):
        """Parse a notification that has been sent and purchased."""
        data = product_notifications_list_response["results"][1]
        notification = ProductNotification.model_validate(data)
        assert notification.is_notified is True
        assert notification.is_purchased is True
        assert notification.purchased_total == 257
        assert notification.language == "en"

    def test_parse_notification_image(self, product_notifications_list_response):
        """Parse notification image sizes."""
        data = product_notifications_list_response["results"][0]
        notification = ProductNotification.model_validate(data)
        assert notification.image is not None
        assert notification.image.full_size == "https://media.zid.store/full.png"
        assert notification.image.thumbnail == "https://media.zid.store/thumb.png"

    def test_parse_notification_stats(self):
        """Parse NotificationStats from API response."""
        data = {
            "total_count": 10,
            "notified_count": 5,
            "purchased_count": 2,
            "purchased_total": 514.50,
        }
        stats = NotificationStats.model_validate(data)
        assert stats.total_count == 10
        assert stats.notified_count == 5
        assert stats.purchased_count == 2
        assert stats.purchased_total == 514.50

    def test_parse_notification_settings(self):
        """Parse NotificationSettings from API response."""
        data = {
            "delay_unit": "hour",
            "delay_value": 15,
            "email_text": {
                "ar": "سيتم إرسال إشعار عند توفر المنتج",
                "en": "You will be notified when the product is available",
            },
            "email_title": {
                "ar": "المنتج متوفر الآن",
                "en": "Product is now available",
            },
            "coupon_code": None,
        }
        settings = NotificationSettings.model_validate(data)
        assert settings.delay_unit == "hour"
        assert settings.delay_value == 15
        assert settings.email_text.en == "You will be notified when the product is available"
        assert settings.email_title.ar == "المنتج متوفر الآن"
        assert settings.coupon_code is None

    def test_notification_roundtrip(self, product_notifications_list_response):
        """ProductNotification can be serialized and re-parsed."""
        data = product_notifications_list_response["results"][0]
        original = ProductNotification.model_validate(data)
        serialized = original.model_dump()
        restored = ProductNotification.model_validate(serialized)
        assert restored.id == original.id
        assert restored.product_id == original.product_id
        assert restored.code == original.code
        assert restored.is_notified == original.is_notified


from zid.models.product._attribute import Attribute, AttributePreset, Badge, Metafield


class TestAttributeModel:
    """Tests for Attribute, AttributePreset, Metafield, and Badge models."""

    def test_parse_attribute_from_list_fixture(self, attributes_list_response):
        """Test parsing attributes from the list fixture."""
        results = attributes_list_response["results"]
        attr = Attribute.model_validate(results[0])
        assert attr.id == "06c7eaed-54e3-4fe3-8c3d-23f0d24d3b9e"
        assert attr.name == "Color"
        assert attr.slug == "color-7"
        assert attr.is_extra is False
        assert attr.is_enabled is True
        assert attr.preset_count == 0
        assert attr.presets == []

    def test_parse_attribute_with_presets(self, attributes_list_response):
        """Test parsing an attribute that has presets."""
        results = attributes_list_response["results"]
        attr = Attribute.model_validate(results[1])
        assert attr.id == "cfb5bd3f-bbc5-4439-a171-b2d70e1c0293"
        assert attr.name == "Size"
        assert len(attr.presets) == 2
        assert attr.preset_count == 2
        assert attr.display_order == 3

        preset = attr.presets[0]
        assert isinstance(preset, AttributePreset)
        assert preset.id == "1f4956ea-e19c-4de9-8c75-7e12b5e4aee8"
        assert preset.value == "Small"
        assert preset.type == "default"
        assert preset.attribute_id == "cfb5bd3f-bbc5-4439-a171-b2d70e1c0293"

    def test_parse_extra_attribute(self, attributes_list_response):
        """Test parsing an extra (non-core) attribute."""
        results = attributes_list_response["results"]
        attr = Attribute.model_validate(results[2])
        assert attr.is_extra is True
        assert attr.is_enabled is False

    def test_parse_preset_detail(self, attribute_presets_list_response):
        """Test parsing preset from the presets list fixture."""
        results = attribute_presets_list_response["results"]
        preset = AttributePreset.model_validate(results[2])
        assert preset.value == "Large"
        assert preset.display_order == 3
        assert preset.attribute_image_id is None

    def test_parse_metafield(self, metafields_list_response):
        """Test parsing metafield from the list fixture."""
        results = metafields_list_response["results"]
        mf = Metafield.model_validate(results[0])
        assert mf.id == "81ad822e-a9b2-4d4c-8a07-7f8110915e2f"
        assert mf.name.en == "Color"
        assert mf.name.ar == "اللون"
        assert mf.slug == "color"
        assert mf.value.en == "Black"

    def test_parse_badge_with_icon(self, badges_list_response):
        """Test parsing a badge that has an icon."""
        items = badges_list_response["data"]
        badge = Badge.model_validate(items[0])
        assert badge.is_example is True
        assert badge.body.en == "{discount_percent} Discount"
        assert badge.icon is not None
        assert badge.icon.code == "discount_percent"

    def test_parse_badge_without_icon(self, badges_list_response):
        """Test parsing a badge without an icon."""
        items = badges_list_response["data"]
        badge = Badge.model_validate(items[1])
        assert badge.is_example is False
        assert badge.icon is None
        assert badge.body.en == "10% discount"

    def test_attribute_roundtrip(self, attributes_list_response):
        """Test serialization roundtrip for Attribute."""
        results = attributes_list_response["results"]
        attr = Attribute.model_validate(results[1])
        data = attr.model_dump(by_alias=True)
        attr2 = Attribute.model_validate(data)
        assert attr2.id == attr.id
        assert attr2.name == attr.name
        assert len(attr2.presets) == len(attr.presets)
