"""Unit tests for resource classes.

Tests resource methods with mocked HTTP responses.
"""

import pytest

from zid.resources.customers import CustomersResource
from zid.resources.orders import OrdersResource
from zid.models.customer import Customer
from zid.models.order import Order, OrderSimple


class TestCustomersResource:
    """Tests for CustomersResource."""
    
    def test_list_returns_iterator(self, mock_http, customer_list_response):
        """list() returns a paginated iterator."""
        mock_http.set_response("GET", "/v1/managers/store/customers", customer_list_response)
        
        resource = CustomersResource(mock_http)
        result = resource.list()
        
        # Should be iterable
        customers = list(result)
        assert all(isinstance(c, Customer) for c in customers)
    
    def test_list_with_params(self, mock_http, customer_list_response):
        """list() passes parameters correctly."""
        mock_http.set_response("GET", "/v1/managers/store/customers", customer_list_response)
        
        resource = CustomersResource(mock_http)
        list(resource.list(per_page=50, page=2))
        
        # Check params were passed
        request = mock_http.requests[0]
        assert request["params"]["per_page"] == 50
        assert request["params"]["page"] == 2
    
    def test_get_returns_customer(self, mock_http, customer_detail_response):
        """get() returns a Customer instance."""
        mock_http.set_response(
            "GET",
            "/v1/managers/store/customers/{id}",
            customer_detail_response,
        )
        
        resource = CustomersResource(mock_http)
        customer = resource.get(123)
        
        assert isinstance(customer, Customer)
    
    def test_get_extracts_from_wrapper(self, mock_http, customer_detail_response):
        """get() extracts customer from response wrapper."""
        mock_http.set_response(
            "GET",
            "/v1/managers/store/customers/{id}",
            customer_detail_response,
        )
        
        resource = CustomersResource(mock_http)
        customer = resource.get(123)
        
        assert isinstance(customer, Customer)
        assert customer.id is not None


class TestOrdersResource:
    """Tests for OrdersResource."""
    
    def test_list_default_payload(self, mock_http, orders_list_response):
        """list() with default payload returns OrderSimple."""
        mock_http.set_response("GET", "/v1/managers/store/orders", orders_list_response)
        
        resource = OrdersResource(mock_http)
        orders = list(resource.list())
        
        assert all(isinstance(o, OrderSimple) for o in orders)
    
    def test_list_full_payload(self, mock_http, orders_list_default_response):
        """list(payload_type='default') returns full Order."""
        mock_http.set_response("GET", "/v1/managers/store/orders", orders_list_default_response)
        
        resource = OrdersResource(mock_http)
        orders = list(resource.list(payload_type="default"))
        
        assert all(isinstance(o, Order) for o in orders)
    
    def test_list_with_filters(self, mock_http, orders_list_response):
        """list() passes filter parameters."""
        mock_http.set_response("GET", "/v1/managers/store/orders", orders_list_response)
        
        resource = OrdersResource(mock_http)
        list(resource.list(
            order_status="new",
            payment_status="paid",
            per_page=10,
        ))
        
        request = mock_http.requests[0]
        assert request["params"]["order_status"] == "new"
        assert request["params"]["payment_status"] == "paid"
        assert request["params"]["per_page"] == 10
    
    def test_get_returns_full_order(self, mock_http, order_detail_response):
        """get() returns full Order instance."""
        mock_http.set_response(
            "GET",
            "/v1/managers/store/orders/{id}/view",
            order_detail_response,
        )
        
        resource = OrdersResource(mock_http)
        order = resource.get(123)
        
        assert isinstance(order, Order)
    
    def test_update_status(self, mock_http, order_detail_response):
        """update_status() sends correct request."""
        mock_http.set_response(
            "POST",
            "/v1/managers/store/orders/{id}/change-order-status",
            order_detail_response,
        )
        
        resource = OrdersResource(mock_http)
        order = resource.update_status(123, order_status="preparing")
        
        assert isinstance(order, Order)
        
        # Check request was made with correct data
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"]["order_status"] == "preparing"
    
    def test_update_status_with_tracking(self, mock_http, order_detail_response):
        """update_status() includes optional tracking info."""
        mock_http.set_response(
            "POST",
            "/v1/managers/store/orders/{id}/change-order-status",
            order_detail_response,
        )
        
        resource = OrdersResource(mock_http)
        resource.update_status(
            123,
            order_status="indelivery",
            tracking_number="TRACK123",
            tracking_url="https://track.example.com/TRACK123",
        )
        
        request = mock_http.requests[0]
        assert request["json"]["order_status"] == "indelivery"
        assert request["json"]["tracking_number"] == "TRACK123"
        assert request["json"]["tracking_url"] == "https://track.example.com/TRACK123"
    
    def test_list_credit_notes(self, mock_http):
        """list_credit_notes() returns credit notes."""
        mock_http.set_response(
            "GET",
            "/v1/managers/store/orders/{id}/credit-notes",
            {
                "code": "success",
                "payload": {
                    "credit_notes": [
                        {"id": "cn-1", "order_id": 123, "store_id": 1},
                    ]
                }
            },
        )
        
        resource = OrdersResource(mock_http)
        notes = resource.list_credit_notes(123)
        
        assert len(notes) == 1
        assert notes[0].id == "cn-1"


from zid.resources.coupons import CouponsResource
from zid.resources.bundle_offers import BundleOffersResource
from zid.resources.loyalty import LoyaltyResource
from zid.models.coupon import Coupon, CouponDetail
from zid.models.bundle_offer import BundleOffer
from zid.models.loyalty import (
    CustomerLoyalty,
    LoyaltyInfo,
    LoyaltyProgram,
    LoyaltyTransaction,
    LoyaltyTransactionSimple,
    RedemptionRule,
)


class TestCouponsResource:
    """Tests for CouponsResource."""

    def test_list_returns_iterator(self, mock_http, coupons_list_response):
        """list() returns a paginated iterator of Coupon."""
        mock_http.set_response("GET", "/v1/managers/store/coupons", coupons_list_response)
        resource = CouponsResource(mock_http)
        result = list(resource.list())
        assert len(result) == 1
        assert all(isinstance(c, Coupon) for c in result)

    def test_get_returns_coupon_detail(self, mock_http, coupon_detail_response):
        """get() returns a CouponDetail instance."""
        mock_http.set_response(
            "GET",
            "/v1/managers/store/coupons/{id}/view",
            coupon_detail_response,
        )
        resource = CouponsResource(mock_http)
        detail = resource.get(5776883)
        assert isinstance(detail, CouponDetail)
        assert detail.id == 5776883
        assert detail.total_sales == 0

    def test_create_uses_form_data(self, mock_http, coupon_detail_response):
        """create() sends form-data (data=), not JSON."""
        mock_http.set_response("POST", "/v1/managers/store/coupons/add", coupon_detail_response)
        resource = CouponsResource(mock_http)
        resource.create(
            name="Test",
            code="TEST",
            discount_type="p",
            discount="20",
            free_shipping="1",
            free_cod="0",
            total="100",
            date_start="2026-01-01",
            date_end="2026-12-31",
            uses_total=100,
            uses_customer=3,
            apply_to="all",
            status="1",
            applying_method="CODE",
            conditions="",
            max_total="0",
            max_weight=0,
        )
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["data"]["name"] == "Test"
        assert request["data"]["discount_type"] == "p"
        assert request["json"] is None

    def test_update_uses_post(self, mock_http, coupon_detail_response):
        """update() uses POST (not PUT) with form-data."""
        mock_http.set_response(
            "POST",
            "/v1/managers/store/coupons/{id}/update",
            coupon_detail_response,
        )
        resource = CouponsResource(mock_http)
        result = resource.update(
            5776883,
            name="Updated",
            code="P2ZAHN",
            discount_type="f",
            discount="155",
        )
        assert isinstance(result, CouponDetail)
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["data"]["name"] == "Updated"

    def test_delete(self, mock_http):
        """delete() returns True on success."""
        mock_http.set_response("DELETE", "/v1/managers/store/coupons/{id}", {})
        resource = CouponsResource(mock_http)
        result = resource.delete(12345)
        assert result is True


class TestBundleOffersResource:
    """Tests for BundleOffersResource."""

    def test_list_returns_iterator(self, mock_http, bundle_offers_list_response):
        """list() returns a paginated iterator of BundleOffer."""
        mock_http.set_response(
            "GET",
            "/v1/managers/store/discounts/bundle-offers",
            bundle_offers_list_response,
        )
        resource = BundleOffersResource(mock_http)
        result = list(resource.list())
        assert len(result) == 2
        assert all(isinstance(o, BundleOffer) for o in result)

    def test_list_parses_uuid_ids(self, mock_http, bundle_offers_list_response):
        """Bundle offer IDs are UUID strings."""
        mock_http.set_response(
            "GET",
            "/v1/managers/store/discounts/bundle-offers",
            bundle_offers_list_response,
        )
        resource = BundleOffersResource(mock_http)
        result = list(resource.list())
        assert result[0].id == "02ed8742-354d-4b44-8f3f-39766081c12e"


class TestLoyaltyResource:
    """Tests for LoyaltyResource."""

    def test_get_status(self, mock_http):
        """get_status() returns a boolean."""
        mock_http.set_response(
            "GET",
            "/v1/managers/loyalty-program/loyalty-status",
            {"loyalty_status": True},
        )
        resource = LoyaltyResource(mock_http)
        assert resource.get_status() is True

    def test_get_status_inactive(self, mock_http):
        """get_status() returns False when inactive."""
        mock_http.set_response(
            "GET",
            "/v1/managers/loyalty-program/loyalty-status",
            {"loyalty_status": False},
        )
        resource = LoyaltyResource(mock_http)
        assert resource.get_status() is False

    def test_get_program(self, mock_http, loyalty_program_response):
        """get_program() returns LoyaltyProgram."""
        mock_http.set_response(
            "GET",
            "/v1/managers/loyalty-program/list-data",
            loyalty_program_response,
        )
        resource = LoyaltyResource(mock_http)
        program = resource.get_program()
        assert isinstance(program, LoyaltyProgram)
        assert program.total_earned_points == 1271060
        assert program.is_active is True

    def test_get_info(self, mock_http):
        """get_info() returns LoyaltyInfo from payload."""
        mock_http.set_response(
            "GET",
            "/v1/managers/store/loyalty-program-info",
            {
                "payload": {
                    "title_ar": "نقاط الولاء",
                    "title_en": None,
                    "content_ar": "<p>محتوى</p>",
                    "content_en": None,
                },
            },
        )
        resource = LoyaltyResource(mock_http)
        info = resource.get_info()
        assert isinstance(info, LoyaltyInfo)
        assert info.title_ar == "نقاط الولاء"

    def test_get_customer_summary(self, mock_http, loyalty_customer_response):
        """get_customer_summary() returns CustomerLoyalty."""
        mock_http.set_response(
            "GET",
            "/v1/managers/loyalty-program/customers/details",
            loyalty_customer_response,
        )
        resource = LoyaltyResource(mock_http)
        summary = resource.get_customer_summary(customer_id=37)
        assert isinstance(summary, CustomerLoyalty)
        assert summary.points_balance == 0
        assert summary.available_points == 0

    def test_get_customer_history(self, mock_http):
        """get_customer_history() returns list of LoyaltyTransaction."""
        mock_http.set_response(
            "GET",
            "/v1/managers/loyalty-program/points-history/{id}",
            {
                "history": [
                    {
                        "date": "2026-02-16T19:41:52.000000Z",
                        "reason": "Expired pending transaction",
                        "points": 135,
                        "direction": "-",
                        "type": "expiry",
                        "order_number": None,
                        "order_code": None,
                        "expiry_date": None,
                        "point_status": "Expired",
                        "point_status_code": "expired",
                        "collection_method": "Points expired",
                    }
                ]
            },
        )
        resource = LoyaltyResource(mock_http)
        history = resource.get_customer_history(customer_id=37)
        assert len(history) == 1
        assert isinstance(history[0], LoyaltyTransaction)
        assert history[0].points == 135

    def test_activate(self, mock_http):
        """activate() sends correct form data."""
        mock_http.set_response(
            "POST",
            "/v1/managers/loyalty-program/activation",
            {"loyalty_program": {"is_active": True}},
        )
        resource = LoyaltyResource(mock_http)
        resource.activate(active=True)
        request = mock_http.requests[0]
        assert request["data"]["activate"] == 1

    def test_deactivate(self, mock_http):
        """activate(active=False) sends 0."""
        mock_http.set_response(
            "POST",
            "/v1/managers/loyalty-program/activation",
            {"loyalty_program": {"is_active": False}},
        )
        resource = LoyaltyResource(mock_http)
        resource.activate(active=False)
        request = mock_http.requests[0]
        assert request["data"]["activate"] == 0

    def test_set_points_expiration(self, mock_http):
        """set_points_expiration() sends days as string."""
        mock_http.set_response(
            "POST",
            "/v1/managers/loyalty-program/points-expiration",
            {"points_expiry_period": 30},
        )
        resource = LoyaltyResource(mock_http)
        resource.set_points_expiration(days=30)
        request = mock_http.requests[0]
        assert request["data"]["days"] == "30"

    def test_update_cashback_rule(self, mock_http):
        """update_cashback_rule() sends bracket-notation keys."""
        mock_http.set_response(
            "POST",
            "/v1/managers/loyalty-program/points-collection/update",
            {"data": {"points_collection_methods_list": []}},
        )
        resource = LoyaltyResource(mock_http)
        resource.update_cashback_rule(
            rule_id="efc450a4-3f09-4544-bcdd-80ddcbde23c8",
            money=100,
            points=1,
        )
        request = mock_http.requests[0]
        assert request["data"]["ruleId"] == "efc450a4-3f09-4544-bcdd-80ddcbde23c8"
        assert request["data"]["config[money]"] == 100
        assert request["data"]["config[points]"] == 1

    def test_create_redemption_rule(self, mock_http):
        """create_redemption_rule() returns RedemptionRule."""
        mock_http.set_response(
            "POST",
            "/v1/managers/loyalty-program/points-redemption",
            {
                "points_redemption": {
                    "redemptionRule": {
                        "id": "bf1aeb4a-d85e-443d-80dc-f0ac43757605",
                        "store_id": "3dfc16e6-ad19-4126-9c2a-5e4a7fb73051",
                        "name": "100",
                        "points_to_redeem": 100,
                        "rule_type": "fixed_rate_settings",
                        "reward": {"discount_value": 10},
                        "is_active": True,
                        "created_at": "2024-07-31T11:10:50.000000Z",
                        "updated_at": "2024-07-31T11:10:50.000000Z",
                    }
                }
            },
        )
        resource = LoyaltyResource(mock_http)
        rule = resource.create_redemption_rule(
            rule_type="fixed_rate_settings",
            discount=10,
            points=100,
        )
        assert isinstance(rule, RedemptionRule)
        assert rule.id == "bf1aeb4a-d85e-443d-80dc-f0ac43757605"
        request = mock_http.requests[0]
        assert request["data"]["config[type]"] == "fixed_rate_settings"

    def test_adjust_customer_points(self, mock_http):
        """adjust_customer_points() returns LoyaltyTransactionSimple."""
        mock_http.set_response(
            "POST",
            "/v1/managers/loyalty-program/customers/adjust-customer-points",
            {
                "data": {
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
            },
        )
        resource = LoyaltyResource(mock_http)
        tx = resource.adjust_customer_points(
            customer_id=37,
            direction="+",
            points=5,
            reason="gift",
        )
        assert isinstance(tx, LoyaltyTransactionSimple)
        assert tx.points == 5
        assert tx.direction == "+"
        request = mock_http.requests[0]
        assert request["data"]["customerId"] == 37
        assert request["data"]["direction"] == "+"
