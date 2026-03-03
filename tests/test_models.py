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
