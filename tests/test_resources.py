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
            "/v1/managers/loyalty-program/points-history/{id}/",
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


from zid.resources.products import ProductsResource
from zid.models.product import Product, ProductSettings


class TestProductsResource:
    """Tests for ProductsResource."""

    def test_list_returns_iterator(self, mock_http, products_list_response):
        """list() returns a paginated iterator of Product."""
        mock_http.set_response("GET", "/v1/products/", products_list_response)
        resource = ProductsResource(mock_http)
        result = list(resource.list())
        assert len(result) == 2
        assert all(isinstance(p, Product) for p in result)

    def test_list_with_filters(self, mock_http, products_list_response):
        """list() passes filter parameters correctly."""
        mock_http.set_response("GET", "/v1/products/", products_list_response)
        resource = ProductsResource(mock_http)
        list(resource.list(
            page=2,
            page_size=15,
            is_published=True,
            search="headphones",
            structure="standalone",
        ))
        request = mock_http.requests[0]
        assert request["params"]["page"] == 2
        assert request["params"]["page_size"] == 15
        assert request["params"]["is_published"] is True
        assert request["params"]["search"] == "headphones"
        assert request["params"]["structure"] == "standalone"

    def test_list_with_id_in(self, mock_http, products_list_response):
        """list() joins id__in list into comma-separated string."""
        mock_http.set_response("GET", "/v1/products/", products_list_response)
        resource = ProductsResource(mock_http)
        list(resource.list(id__in=["abc-123", "def-456"]))
        request = mock_http.requests[0]
        assert request["params"]["id__in"] == "abc-123,def-456"

    def test_get_returns_product(self, mock_http, product_detail_response):
        """get() returns a Product instance."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/",
            product_detail_response,
        )
        resource = ProductsResource(mock_http)
        product = resource.get("2829a483-4336-43ab-a855-84532c9419c2")
        assert isinstance(product, Product)
        assert product.id == "2829a483-4336-43ab-a855-84532c9419c2"
        assert product.structure == "parent"

    def test_create_sends_json(self, mock_http, product_detail_response):
        """create() sends JSON body with correct fields."""
        mock_http.set_response("POST", "/v1/products/", product_detail_response)
        resource = ProductsResource(mock_http)
        product = resource.create(
            name="Wireless Headphones",
            price=257,
            sku="WH-1000XM5",
            sale_price=199,
            quantity=50,
        )
        assert isinstance(product, Product)
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"]["name"] == "Wireless Headphones"
        assert request["json"]["price"] == 257
        assert request["json"]["sku"] == "WH-1000XM5"
        assert request["json"]["sale_price"] == 199
        assert request["json"]["quantity"] == 50

    def test_create_minimal(self, mock_http, product_detail_response):
        """create() with only required fields."""
        mock_http.set_response("POST", "/v1/products/", product_detail_response)
        resource = ProductsResource(mock_http)
        resource.create(name="Test", price=10, sku="TST-001")
        request = mock_http.requests[0]
        assert request["json"] == {"name": "Test", "price": 10, "sku": "TST-001"}

    def test_update_sends_patch(self, mock_http, product_detail_response):
        """update() sends PATCH request with correct fields."""
        mock_http.set_response(
            "PATCH",
            "/v1/products/{product_id}/",
            product_detail_response,
        )
        resource = ProductsResource(mock_http)
        product = resource.update(
            "2829a483-4336-43ab-a855-84532c9419c2",
            price=299,
            name={"ar": "منتج", "en": "Product"},
        )
        assert isinstance(product, Product)
        request = mock_http.requests[0]
        assert request["method"] == "PATCH"
        assert request["json"]["price"] == 299
        assert request["json"]["name"] == {"ar": "منتج", "en": "Product"}

    def test_delete(self, mock_http):
        """delete() sends DELETE request."""
        mock_http.set_response(
            "DELETE",
            "/v1/products/{product_id}/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.delete("51fcad4c-9f9d-4ac5-be7c-38c7a6684ec3")
        request = mock_http.requests[0]
        assert request["method"] == "DELETE"
        assert "/v1/products/51fcad4c-9f9d-4ac5-be7c-38c7a6684ec3/" in request["path"]

    def test_bulk_update(self, mock_http):
        """bulk_update() sends PATCH to base path with list payload."""
        mock_http.set_response(
            "PATCH",
            "/v1/products/",
            {
                "results": [
                    {
                        "id": "a497974d-1755-423a-b06c-e0578ba8c318",
                        "sku": "WH-1000XX3",
                        "barcode": "",
                        "name": {"en": "Updated"},
                        "slug": "updated",
                        "price": 299,
                        "currency": "SAR",
                        "currency_symbol": " SAR ",
                        "has_options": False,
                        "has_fields": False,
                        "is_draft": False,
                        "is_infinite": False,
                        "html_url": "https://osama.zid.store/products/updated",
                        "requires_shipping": True,
                        "is_taxable": True,
                        "structure": "standalone",
                        "store_id": 3,
                        "is_published": True,
                        "created_at": "2026-02-10T18:33:37Z",
                        "updated_at": "2026-02-10T18:47:39Z",
                    }
                ],
            },
        )
        resource = ProductsResource(mock_http)
        result = resource.bulk_update([
            {"id": "a497974d-1755-423a-b06c-e0578ba8c318", "price": 299},
        ])
        assert len(result) == 1
        assert isinstance(result[0], Product)
        request = mock_http.requests[0]
        assert request["method"] == "PATCH"

    def test_get_settings(self, mock_http, product_settings_response):
        """get_settings() returns ProductSettings."""
        mock_http.set_response(
            "GET",
            "/v1/products/settings/",
            product_settings_response,
        )
        resource = ProductsResource(mock_http)
        settings = resource.get_settings()
        assert isinstance(settings, ProductSettings)
        assert settings.related_products_count == 8
        assert settings.default_products_ordering == "-is_infinite,-quantity"
        assert settings.is_wishlist_enabled is True

    def test_set_manual_order(self, mock_http):
        """set_manual_order() sends POST with product IDs."""
        mock_http.set_response("POST", "/v1/products/ordering/", {})
        resource = ProductsResource(mock_http)
        resource.set_manual_order(
            products=[
                "d22fb4a6-cbcf-464c-8877-6cbf3df52056",
                "d22fb4a6-cbcf-46g5-8877-6c367f52053",
            ],
        )
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"]["products"] == [
            "d22fb4a6-cbcf-464c-8877-6cbf3df52056",
            "d22fb4a6-cbcf-46g5-8877-6c367f52053",
        ]
        assert "category" not in request["json"]

    def test_set_manual_order_with_category(self, mock_http):
        """set_manual_order() includes category when provided."""
        mock_http.set_response("POST", "/v1/products/ordering/", {})
        resource = ProductsResource(mock_http)
        resource.set_manual_order(
            products=["d22fb4a6-cbcf-464c-8877-6cbf3df52056"],
            category=42,
        )
        request = mock_http.requests[0]
        assert request["json"]["category"] == 42

    def test_reset_manual_order(self, mock_http):
        """reset_manual_order() sends DELETE to ordering endpoint."""
        mock_http.set_response("DELETE", "/v1/products/ordering/", {})
        resource = ProductsResource(mock_http)
        resource.reset_manual_order()
        request = mock_http.requests[0]
        assert request["method"] == "DELETE"
        assert request["path"] == "/v1/products/ordering/"

    def test_export_all(self, mock_http):
        """export_all() sends POST to export endpoint."""
        mock_http.set_response("POST", "/v1/products/export/", {})
        resource = ProductsResource(mock_http)
        resource.export_all()
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["path"] == "/v1/products/export/"

    def test_import_file(self, mock_http):
        """import_file() uploads file via multipart form."""
        mock_http.set_response("POST", "/v1/products/import/", {})
        resource = ProductsResource(mock_http)
        resource.import_file(file=("products.csv", b"csv-content", "text/csv"))
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["path"] == "/v1/products/import/"
        assert request["data"]["response_type"] == "json"

    def test_import_file_with_options(self, mock_http):
        """import_file() passes delete_old_products and response_type."""
        mock_http.set_response("POST", "/v1/products/import/", {})
        resource = ProductsResource(mock_http)
        resource.import_file(
            file=("products.xlsx", b"xlsx-content", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            response_type="json",
            delete_old_products=True,
        )
        request = mock_http.requests[0]
        assert request["data"]["delete_old_products"] is True
        assert request["data"]["response_type"] == "json"


from zid.models.product._voucher import OrderVoucher, Voucher


class TestProductVouchersSubResource:
    """Tests for ProductVouchersSubResource via ProductsResource.vouchers."""

    def test_list_returns_iterator(self, mock_http, product_vouchers_list_response):
        """list() returns a paginated iterator of Voucher."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/vouchers/",
            product_vouchers_list_response,
        )
        resource = ProductsResource(mock_http)
        result = list(resource.vouchers.list("a1477bb2-72ea-4be9-b2cf-093cefc721bb"))
        assert len(result) == 2
        assert all(isinstance(v, Voucher) for v in result)
        assert result[0].id == "0b470326-d2b1-4d96-8ee1-ea03a50dfd83"
        assert result[1].status == "SOLD"

    def test_list_with_pagination_params(self, mock_http, product_vouchers_list_response):
        """list() passes pagination parameters correctly."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/vouchers/",
            product_vouchers_list_response,
        )
        resource = ProductsResource(mock_http)
        list(resource.vouchers.list(
            "a1477bb2-72ea-4be9-b2cf-093cefc721bb",
            page=2,
            page_size=10,
        ))
        request = mock_http.requests[0]
        assert request["params"]["page"] == 2
        assert request["params"]["page_size"] == 10

    def test_create_returns_voucher(self, mock_http):
        """create() returns a Voucher instance."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/vouchers/",
            {
                "id": "3663992f-989e-4056-9a71-02a9109ec7fa",
                "product_id": "a1477bb2-72ea-4be9-b2cf-093cefc721bb",
                "status": "AVAILABLE",
                "order": None,
                "serial_number": "serial-number-1",
                "key": "key-1",
                "pin_code": "pin-code-example",
                "expires_at": "2026-10-10T00:00:00Z",
                "updated_at": "2026-02-11T12:39:55.597191Z",
                "created_at": "2026-02-11T12:39:55.597152Z",
            },
        )
        resource = ProductsResource(mock_http)
        voucher = resource.vouchers.create(
            "a1477bb2-72ea-4be9-b2cf-093cefc721bb",
            key="key-1",
            status="AVAILABLE",
            serial_number="serial-number-1",
            pin_code="pin-code-example",
            expires_at="2026-10-10T00:00:00Z",
        )
        assert isinstance(voucher, Voucher)
        assert voucher.id == "3663992f-989e-4056-9a71-02a9109ec7fa"
        assert voucher.key == "key-1"
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"]["key"] == "key-1"
        assert request["json"]["status"] == "AVAILABLE"
        assert request["json"]["serial_number"] == "serial-number-1"
        assert request["json"]["pin_code"] == "pin-code-example"

    def test_create_minimal(self, mock_http):
        """create() with only required fields."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/vouchers/",
            {
                "id": "abc-123",
                "product_id": "prod-uuid",
                "status": "AVAILABLE",
                "order": None,
                "serial_number": None,
                "key": "MY-KEY",
                "pin_code": None,
                "expires_at": None,
                "updated_at": "2026-02-11T12:39:55.597191Z",
                "created_at": "2026-02-11T12:39:55.597152Z",
            },
        )
        resource = ProductsResource(mock_http)
        resource.vouchers.create("prod-uuid", key="MY-KEY", status="AVAILABLE")
        request = mock_http.requests[0]
        assert request["json"] == {"key": "MY-KEY", "status": "AVAILABLE"}

    def test_update_returns_voucher(self, mock_http):
        """update() returns a single Voucher instance."""
        mock_http.set_response(
            "PATCH",
            "/v1/products/{product_id}/vouchers/{voucher_id}/",
            {
                "id": "0d6dc296-f757-4f11-83b2-6d5fddb6ad85",
                "key": "UPDATED-KEY",
                "pin_code": "1234",
                "status": "AVAILABLE",
                "serial_number": "SN123456",
                "expires_at": "2026-12-31",
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z",
            },
        )
        resource = ProductsResource(mock_http)
        result = resource.vouchers.update(
            "a1477bb2-72ea-4be9-b2cf-093cefc721bb",
            "0d6dc296-f757-4f11-83b2-6d5fddb6ad85",
            key="UPDATED-KEY",
            status="AVAILABLE",
        )
        assert isinstance(result, Voucher)
        assert result.key == "UPDATED-KEY"
        request = mock_http.requests[0]
        assert request["method"] == "PATCH"
        assert request["json"]["key"] == "UPDATED-KEY"
        assert request["json"]["status"] == "AVAILABLE"

    def test_delete(self, mock_http):
        """delete() sends DELETE request."""
        mock_http.set_response(
            "DELETE",
            "/v1/products/{product_id}/vouchers/{voucher_id}/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.vouchers.delete(
            "a1477bb2-72ea-4be9-b2cf-093cefc721bb",
            "0b470326-d2b1-4d96-8ee1-ea03a50dfd83",
        )
        request = mock_http.requests[0]
        assert request["method"] == "DELETE"
        assert "vouchers" in request["path"]

    def test_import_file(self, mock_http):
        """import_file() uploads a file via POST."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/vouchers/import/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.vouchers.import_file(
            "a1477bb2-72ea-4be9-b2cf-093cefc721bb",
            file=("vouchers.csv", b"key,pin_code,status\nABC,1234,AVAILABLE", "text/csv"),
        )
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert "import" in request["path"]

    def test_export(self, mock_http):
        """export() sends POST with optional email."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/vouchers/export/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.vouchers.export(
            "a1477bb2-72ea-4be9-b2cf-093cefc721bb",
            email="merchant@example.com",
        )
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"]["email"] == "merchant@example.com"

    def test_export_without_email(self, mock_http):
        """export() works without email parameter."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/vouchers/export/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.vouchers.export("a1477bb2-72ea-4be9-b2cf-093cefc721bb")
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"] == {}

    def test_get_order_vouchers(self, mock_http, order_vouchers_response):
        """get_order_vouchers() returns paginated iterator of OrderVoucher."""
        mock_http.set_response(
            "GET",
            "/v1/order-vouchers/{order_id}/",
            order_vouchers_response,
        )
        resource = ProductsResource(mock_http)
        result = list(resource.vouchers.get_order_vouchers("64855100"))
        assert len(result) == 1
        assert all(isinstance(v, OrderVoucher) for v in result)
        assert result[0].status == "RESERVED"
        assert result[0].order == 64855100

    def test_get_order_vouchers_with_pagination(self, mock_http, order_vouchers_response):
        """get_order_vouchers() passes pagination parameters."""
        mock_http.set_response(
            "GET",
            "/v1/order-vouchers/{order_id}/",
            order_vouchers_response,
        )
        resource = ProductsResource(mock_http)
        list(resource.vouchers.get_order_vouchers("64855100", page=1, page_size=15))
        request = mock_http.requests[0]
        assert request["params"]["page"] == 1
        assert request["params"]["page_size"] == 15


from zid.models.product._category import (
    AssignedCategory,
    Category,
    CategoryDetail,
)


class TestProductCategoriesSubResource:
    """Tests for ProductCategoriesSubResource via ProductsResource.categories."""

    def test_list_returns_categories(self, mock_http, product_categories_list_response):
        """list() returns a list of Category instances."""
        mock_http.set_response(
            "GET",
            "/v1/managers/store/categories",
            product_categories_list_response,
        )
        resource = ProductsResource(mock_http)
        result = resource.categories.list()
        assert len(result) == 2
        assert all(isinstance(c, Category) for c in result)
        assert result[0].id == 1473477
        assert result[0].name == "test sub"
        assert result[1].id == 1259096

    def test_list_with_sub_categories(self, mock_http, product_categories_list_response):
        """list() parses nested sub_categories."""
        mock_http.set_response(
            "GET",
            "/v1/managers/store/categories",
            product_categories_list_response,
        )
        resource = ProductsResource(mock_http)
        result = resource.categories.list()
        cat_with_subs = result[1]
        assert len(cat_with_subs.sub_categories) == 1
        assert cat_with_subs.sub_categories[0].id == 1399659

    def test_get_returns_category_detail(self, mock_http, product_category_detail_response):
        """get() returns a CategoryDetail instance."""
        mock_http.set_response(
            "GET",
            "/v1/managers/store/categories/{category_id}/view",
            product_category_detail_response,
        )
        resource = ProductsResource(mock_http)
        detail = resource.categories.get(1473477)
        assert isinstance(detail, CategoryDetail)
        assert detail.id == 1473477
        assert detail.uuid == "8cc71774-bf3e-4383-9778-64d50d965dc7"
        assert detail.i18n_seo_category_title.en == "test sub"
        assert len(detail.metafields) == 2

    def test_create_sends_form_data(self, mock_http):
        """create() sends multipart form data with X-Manager-Token."""
        mock_http.set_response(
            "POST",
            "/v1/managers/store/categories/add",
            {
                "status": "object",
                "category": {
                    "id": 1482387,
                    "name": "تصنيف فرعي ٢",
                    "uuid": "9c955dba-b87a-49f0-9b0b-fa9aa930c035",
                    "slug": "تصنيف-فرعي-٢",
                    "SEO_category_title": "تصنيف فرعي ٢",
                    "SEO_category_description": "تصنيف فرعي1",
                    "i18n_SEO_category_title": {"ar": "تصنيف فرعي ٢", "en": "sub category 2"},
                    "i18n_SEO_category_description": {"ar": "تصنيف فرعي1", "en": "test sub 2222f2"},
                    "names": {"en": "sub category 2", "ar": "تصنيف فرعي ٢"},
                    "description": {"en": "test sub 2222f2", "ar": "تصنيف فرعي1"},
                    "url": "https://osama.zid.store/categories/1482387/تصنيف-فرعي-٢",
                    "image": None,
                    "image_full_size": None,
                    "img_alt_text": "",
                    "i18n_img_alt_text": {"ar": None},
                    "cover_image": None,
                    "image_full": None,
                    "products_count": 0,
                    "sub_categories": [],
                    "parent_id": 1482385,
                    "flat_name": "test121212125 - تصنيف فرعي ٢",
                    "is_published": True,
                    "metafields": [],
                },
                "message": {"type": "object", "code": None, "name": None, "description": None},
            },
        )
        resource = ProductsResource(mock_http)
        result = resource.categories.create(
            name_ar="تصنيف فرعي ٢",
            name_en="sub category 2",
            description_ar="تصنيف فرعي1",
            description_en="test sub 2222f2",
            parent_id=1482385,
        )
        assert isinstance(result, CategoryDetail)
        assert result.id == 1482387
        assert result.parent_id == 1482385
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["data"]["name[ar]"] == "تصنيف فرعي ٢"
        assert request["data"]["name[en]"] == "sub category 2"
        assert request["data"]["parent_id"] == "1482385"

    def test_create_without_parent(self, mock_http):
        """create() omits parent_id when not provided."""
        mock_http.set_response(
            "POST",
            "/v1/managers/store/categories/add",
            {
                "status": "object",
                "category": {
                    "id": 1500000,
                    "name": "New Cat",
                    "uuid": "abc-uuid",
                    "slug": "new-cat",
                    "SEO_category_title": "New Cat",
                    "SEO_category_description": "Desc",
                    "i18n_SEO_category_title": {"ar": "جديد", "en": "New Cat"},
                    "i18n_SEO_category_description": {"ar": "وصف", "en": "Desc"},
                    "names": {"en": "New Cat", "ar": "جديد"},
                    "description": {"en": "Desc", "ar": "وصف"},
                    "url": "https://example.com/categories/1500000/new-cat",
                    "image": None,
                    "image_full_size": None,
                    "img_alt_text": "",
                    "i18n_img_alt_text": {"ar": None},
                    "cover_image": None,
                    "image_full": None,
                    "products_count": 0,
                    "sub_categories": [],
                    "parent_id": None,
                    "flat_name": "New Cat",
                    "is_published": True,
                    "metafields": [],
                },
                "message": {"type": "object", "code": None, "name": None, "description": None},
            },
        )
        resource = ProductsResource(mock_http)
        resource.categories.create(
            name_ar="جديد",
            name_en="New Cat",
            description_ar="وصف",
            description_en="Desc",
        )
        request = mock_http.requests[0]
        assert "parent_id" not in request["data"]

    def test_update_sends_form_data(self, mock_http):
        """update() sends multipart form data with _method=put."""
        mock_http.set_response(
            "POST",
            "/v1/managers/store/categories/{category_id}/update",
            {
                "status": "object",
                "category": {
                    "id": 1486524,
                    "name": "Hello World",
                    "uuid": "d20ff9ed-90c0-4733-9657-6b4e671d7809",
                    "slug": "hello-world",
                    "SEO_category_title": "Hello World",
                    "SEO_category_description": "Hello World",
                    "i18n_SEO_category_title": {"ar": "Hello World", "en": "Hello World"},
                    "i18n_SEO_category_description": {"ar": "Hello World", "en": "Hello World"},
                    "names": {"en": "Hello World", "ar": "Hello World"},
                    "description": {"en": "Hello World", "ar": "Hello World"},
                    "url": "https://osama.zid.store/categories/1486524/hello-world",
                    "image": None,
                    "image_full_size": None,
                    "img_alt_text": "",
                    "i18n_img_alt_text": {"ar": None},
                    "cover_image": None,
                    "image_full": None,
                    "products_count": 0,
                    "sub_categories": [],
                    "parent_id": None,
                    "flat_name": "Hello World",
                    "is_published": True,
                    "metafields": [],
                },
                "message": {"type": "object", "code": None, "name": None, "description": None},
            },
        )
        resource = ProductsResource(mock_http)
        result = resource.categories.update(
            1486524,
            name_ar="Hello World",
            name_en="Hello World",
            description_ar="Hello World",
            description_en="Hello World",
        )
        assert isinstance(result, CategoryDetail)
        assert result.id == 1486524
        assert result.name == "Hello World"
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["data"]["_method"] == "put"
        assert request["data"]["name[en]"] == "Hello World"

    def test_publish(self, mock_http):
        """publish() sends PUT with is_published flag."""
        mock_http.set_response(
            "PUT",
            "/v1/managers/store/categories/{category_id}/publishing",
            {
                "status": "success",
                "message": {"type": "success", "code": "", "name": "", "description": "ok"},
            },
        )
        resource = ProductsResource(mock_http)
        result = resource.categories.publish(1486524, is_published=True)
        assert result["status"] == "success"
        request = mock_http.requests[0]
        assert request["method"] == "PUT"
        assert request["json"]["is_published"] == "1"

    def test_unpublish(self, mock_http):
        """publish() with is_published=False sends '0'."""
        mock_http.set_response(
            "PUT",
            "/v1/managers/store/categories/{category_id}/publishing",
            {
                "status": "success",
                "message": {"type": "success", "code": "", "name": "", "description": "ok"},
            },
        )
        resource = ProductsResource(mock_http)
        resource.categories.publish(1486524, is_published=False)
        request = mock_http.requests[0]
        assert request["json"]["is_published"] == "0"

    def test_detach_all_products(self, mock_http):
        """detach_all_products() returns CategoryDetail with products_count=0."""
        mock_http.set_response(
            "DELETE",
            "/v1/managers/store/categories/{category_id}/products/delete",
            {
                "status": "object",
                "category": {
                    "id": 1473477,
                    "name": "تصنيف فرعي",
                    "uuid": "8cc71774-bf3e-4383-9778-64d50d965dc7",
                    "slug": "تصنيف-فرعي",
                    "SEO_category_title": "تصنيف فرعي",
                    "SEO_category_description": "تصنيف فرعي1",
                    "i18n_SEO_category_title": {"ar": "تصنيف فرعي", "en": "test sub"},
                    "i18n_SEO_category_description": {"ar": "تصنيف فرعي1", "en": "Sub category 1"},
                    "names": {"en": "test sub", "ar": "تصنيف فرعي"},
                    "description": {"en": "Sub category 1", "ar": "تصنيف فرعي1"},
                    "url": "https://osama.zid.store/categories/1473477/تصنيف-فرعي",
                    "image": None,
                    "image_full_size": None,
                    "img_alt_text": "",
                    "i18n_img_alt_text": {"ar": None},
                    "cover_image": None,
                    "image_full": None,
                    "products_count": 0,
                    "sub_categories": [],
                    "parent_id": None,
                    "flat_name": "تصنيف فرعي",
                    "is_published": False,
                    "metafields": [],
                },
                "message": {"type": "object", "code": None, "name": None, "description": None},
            },
        )
        resource = ProductsResource(mock_http)
        result = resource.categories.detach_all_products(1473477)
        assert isinstance(result, CategoryDetail)
        assert result.products_count == 0
        request = mock_http.requests[0]
        assert request["method"] == "DELETE"

    def test_assign_returns_assigned_category(self, mock_http):
        """assign() returns an AssignedCategory instance."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/categories/",
            {
                "id": "1473477",
                "name": "test sub",
                "slug": "تصنيف-فرعي",
                "description": "Sub category 1",
                "cover_image": None,
                "image": None,
                "display_order": 0,
                "meta": {"childs": [], "parents": []},
            },
            status=201,
        )
        resource = ProductsResource(mock_http)
        result = resource.categories.assign(
            "a7ad89d0-03e2-430f-b6e4-0624ef05e571",
            category_id=1473477,
        )
        assert isinstance(result, AssignedCategory)
        assert result.id == "1473477"
        assert result.name == "test sub"
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"]["id"] == 1473477

    def test_bulk_assign(self, mock_http):
        """bulk_assign() sends PATCH with category IDs."""
        mock_http.set_response(
            "PATCH",
            "/v1/products/{product_id}/categories/bulk-add/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.categories.bulk_assign(
            "a7ad89d0-03e2-430f-b6e4-0624ef05e571",
            category_ids=[1473476, 1323795],
        )
        request = mock_http.requests[0]
        assert request["method"] == "PATCH"
        assert request["json"]["ids"] == [1473476, 1323795]

    def test_remove(self, mock_http):
        """remove() sends DELETE request."""
        mock_http.set_response(
            "DELETE",
            "/v1/products/{product_id}/categories/{category_id}/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.categories.remove(
            "a7ad89d0-03e2-430f-b6e4-0624ef05e571",
            1473477,
        )
        request = mock_http.requests[0]
        assert request["method"] == "DELETE"
        assert "categories/1473477" in request["path"]


from zid.models.product._base import ProductImage, ProductImageSizes


class TestProductImagesSubResource:
    """Tests for ProductImagesSubResource via ProductsResource.images."""

    def test_list_returns_iterator(self, mock_http, product_images_list_response):
        """list() returns a paginated iterator of ProductImage."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/images/",
            product_images_list_response,
        )
        resource = ProductsResource(mock_http)
        result = list(resource.images.list("96d0f5c3-1958-4a31-8b03-7014c2070630"))
        assert len(result) == 2
        assert all(isinstance(img, ProductImage) for img in result)
        assert result[0].id == "0bcc247a-61fa-4a95-bab1-21827a824749"
        assert result[0].alt_text is None
        assert result[0].display_order == 1
        assert result[1].id == "59b5fff2-2281-44a4-8bf1-56d9fd1165bb"
        assert result[1].alt_text == "Black Sneaker"
        assert result[1].display_order == 2

    def test_list_parses_image_sizes(self, mock_http, product_images_list_response):
        """list() correctly parses nested image size URLs."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/images/",
            product_images_list_response,
        )
        resource = ProductsResource(mock_http)
        result = list(resource.images.list("96d0f5c3-1958-4a31-8b03-7014c2070630"))
        sizes = result[0].image
        assert isinstance(sizes, ProductImageSizes)
        assert "full_size" in sizes.full_size or "zid.store" in sizes.full_size
        assert sizes.thumbnail is not None
        assert sizes.large is not None
        assert sizes.medium is not None
        assert sizes.small is not None

    def test_list_with_pagination_params(self, mock_http, product_images_list_response):
        """list() passes pagination parameters correctly."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/images/",
            product_images_list_response,
        )
        resource = ProductsResource(mock_http)
        list(resource.images.list(
            "96d0f5c3-1958-4a31-8b03-7014c2070630",
            page=2,
            page_size=50,
        ))
        request = mock_http.requests[0]
        assert request["params"]["page"] == 2
        assert request["params"]["page_size"] == 50

    def test_list_default_page_size(self, mock_http, product_images_list_response):
        """list() sends page_size=15 by default."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/images/",
            product_images_list_response,
        )
        resource = ProductsResource(mock_http)
        list(resource.images.list("96d0f5c3-1958-4a31-8b03-7014c2070630"))
        request = mock_http.requests[0]
        assert request["params"]["page_size"] == 15

    def test_update_order_returns_image(self, mock_http):
        """update_order() returns an updated ProductImage."""
        mock_http.set_response(
            "PATCH",
            "/v1/products/{product_id}/images/{Image-Id}/",
            {
                "id": "0bcc247a-61fa-4a95-bab1-21827a824749",
                "image": {
                    "large": "https://media.zid.store/thumbs/d297fb8b/0bcc247a-large.jpg",
                    "small": "https://media.zid.store/thumbs/d297fb8b/0bcc247a-small.jpg",
                    "full_size": "https://media.zid.store/d297fb8b/0bcc247a.jpg",
                    "medium": "https://media.zid.store/thumbs/d297fb8b/0bcc247a-medium.jpg",
                    "thumbnail": "https://media.zid.store/thumbs/d297fb8b/0bcc247a-thumbnail.jpg",
                },
                "alt_text": None,
                "display_order": 3,
            },
        )
        resource = ProductsResource(mock_http)
        image = resource.images.update_order(
            "96d0f5c3-1958-4a31-8b03-7014c2070630",
            "0bcc247a-61fa-4a95-bab1-21827a824749",
            display_order=3,
        )
        assert isinstance(image, ProductImage)
        assert image.display_order == 3
        assert image.id == "0bcc247a-61fa-4a95-bab1-21827a824749"
        request = mock_http.requests[0]
        assert request["method"] == "PATCH"
        assert request["json"]["display_order"] == 3

    def test_update_order_sends_correct_path(self, mock_http):
        """update_order() constructs the correct API path."""
        mock_http.set_response(
            "PATCH",
            "/v1/products/{product_id}/images/{Image-Id}/",
            {
                "id": "img-uuid",
                "image": {
                    "large": "https://example.com/large.jpg",
                    "small": "https://example.com/small.jpg",
                    "full_size": "https://example.com/full.jpg",
                    "medium": "https://example.com/medium.jpg",
                    "thumbnail": "https://example.com/thumb.jpg",
                },
                "alt_text": "Updated",
                "display_order": 1,
            },
        )
        resource = ProductsResource(mock_http)
        resource.images.update_order("prod-123", "img-uuid", display_order=1)
        request = mock_http.requests[0]
        assert request["path"] == "/v1/products/prod-123/images/img-uuid/"

    def test_upload_returns_image(self, mock_http):
        """upload() returns a ProductImage instance."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/images/",
            {
                "id": "59b5fff2-2281-44a4-8bf1-56d9fd1165bb",
                "image": {
                    "full_size": "https://media.zid.store/d297fb8b/59b5fff2.jpg",
                    "medium": "https://media.zid.store/thumbs/d297fb8b/59b5fff2-medium.jpg",
                    "large": "https://media.zid.store/thumbs/d297fb8b/59b5fff2-large.jpg",
                    "small": "https://media.zid.store/thumbs/d297fb8b/59b5fff2-small.jpg",
                    "thumbnail": "https://media.zid.store/thumbs/d297fb8b/59b5fff2-thumb.jpg",
                },
                "alt_text": "test alt text",
                "display_order": 2,
            },
        )
        resource = ProductsResource(mock_http)
        image = resource.images.upload(
            "96d0f5c3-1958-4a31-8b03-7014c2070630",
            image=("test1.jpg", b"fake-image-bytes", "image/jpeg"),
            alt_text="test alt text",
        )
        assert isinstance(image, ProductImage)
        assert image.id == "59b5fff2-2281-44a4-8bf1-56d9fd1165bb"
        assert image.alt_text == "test alt text"
        assert image.display_order == 2
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["data"]["alt_text"] == "test alt text"

    def test_upload_sends_correct_path(self, mock_http):
        """upload() posts to the correct path."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/images/",
            {
                "id": "new-img",
                "image": {
                    "full_size": "https://example.com/full.jpg",
                    "medium": "https://example.com/medium.jpg",
                    "large": "https://example.com/large.jpg",
                    "small": "https://example.com/small.jpg",
                    "thumbnail": "https://example.com/thumb.jpg",
                },
                "alt_text": "alt",
                "display_order": 1,
            },
        )
        resource = ProductsResource(mock_http)
        resource.images.upload(
            "prod-abc",
            image=("img.png", b"bytes", "image/png"),
            alt_text="alt",
        )
        request = mock_http.requests[0]
        assert request["path"] == "/v1/products/prod-abc/images/"

    def test_delete_sends_request(self, mock_http):
        """delete() sends DELETE request to correct path."""
        mock_http.set_response(
            "DELETE",
            "/v1/products/{product_id}/images/{Image-Id}/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.images.delete(
            "96d0f5c3-1958-4a31-8b03-7014c2070630",
            "0bcc247a-61fa-4a95-bab1-21827a824749",
        )
        request = mock_http.requests[0]
        assert request["method"] == "DELETE"
        assert request["path"] == "/v1/products/96d0f5c3-1958-4a31-8b03-7014c2070630/images/0bcc247a-61fa-4a95-bab1-21827a824749/"

    def test_delete_returns_none(self, mock_http):
        """delete() returns None."""
        mock_http.set_response(
            "DELETE",
            "/v1/products/{product_id}/images/{Image-Id}/",
            {},
        )
        resource = ProductsResource(mock_http)
        result = resource.images.delete("prod-123", "img-456")
        assert result is None


from zid.models.product._base import ProductStock, StockLocation


class TestProductStocksSubResource:
    """Tests for ProductStocksSubResource via ProductsResource.stocks."""

    def test_list_returns_stocks(self, mock_http, product_stocks_list_response):
        """list() returns a list of ProductStock instances."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/stocks/",
            product_stocks_list_response,
        )
        resource = ProductsResource(mock_http)
        result = resource.stocks.list("96d0f5c3-1958-4a31-8b03-7014c2070630")
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(s, ProductStock) for s in result)

    def test_list_parses_location(self, mock_http, product_stocks_list_response):
        """list() correctly parses nested location data."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/stocks/",
            product_stocks_list_response,
        )
        resource = ProductsResource(mock_http)
        result = resource.stocks.list("96d0f5c3-1958-4a31-8b03-7014c2070630")
        stock = result[0]
        assert stock.id == "e44bbf6b-c62a-4597-b87f-311fba0e0256"
        assert isinstance(stock.location, StockLocation)
        assert stock.location.id == "8ee590fe-d02d-4c50-9184-f628bb8b115a"
        assert stock.location.type == "PHYSICAL"
        assert stock.available_quantity is None
        assert stock.is_infinite is True

    def test_list_finite_stock(self, mock_http, product_stocks_list_response):
        """list() correctly parses a stock with finite quantity."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/stocks/",
            product_stocks_list_response,
        )
        resource = ProductsResource(mock_http)
        result = resource.stocks.list("96d0f5c3-1958-4a31-8b03-7014c2070630")
        stock = result[1]
        assert stock.id == "0abacb3a-6a43-474d-b1c9-097e95824117"
        assert stock.available_quantity == 25
        assert stock.is_infinite is False

    def test_get_returns_stock(self, mock_http):
        """get() returns a single ProductStock instance."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/stocks/{stock_id}/",
            {
                "id": "e44bbf6b-c62a-4597-b87f-311fba0e0256",
                "location": {
                    "id": "8ee590fe-d02d-4c50-9184-f628bb8b115a",
                    "name": {"ar": "الرياض", "en": "Riyadh"},
                    "type": "PHYSICAL",
                    "full_address": "6137 King Abdul Aziz Branch Rd",
                },
                "available_quantity": None,
                "is_infinite": True,
            },
        )
        resource = ProductsResource(mock_http)
        stock = resource.stocks.get(
            "96d0f5c3-1958-4a31-8b03-7014c2070630",
            "e44bbf6b-c62a-4597-b87f-311fba0e0256",
        )
        assert isinstance(stock, ProductStock)
        assert stock.id == "e44bbf6b-c62a-4597-b87f-311fba0e0256"
        assert stock.is_infinite is True

    def test_get_sends_correct_path(self, mock_http):
        """get() constructs the correct API path."""
        mock_http.set_response(
            "GET",
            "/v1/products/{product_id}/stocks/{stock_id}/",
            {
                "id": "stock-uuid",
                "location": {
                    "id": "loc-uuid",
                    "name": {"en": "Test"},
                    "type": "PHYSICAL",
                    "full_address": "123 Test St",
                },
                "available_quantity": 10,
                "is_infinite": False,
            },
        )
        resource = ProductsResource(mock_http)
        resource.stocks.get("prod-123", "stock-456")
        request = mock_http.requests[0]
        assert request["path"] == "/v1/products/prod-123/stocks/stock-456/"

    def test_create_sends_json(self, mock_http):
        """create() sends the correct JSON payload."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/stocks/",
            {
                "id": "0abacb3a-6a43-474d-b1c9-097e95824117",
                "location": "982a2aac-b9af-44e3-a3e0-51d2faa6b7c2",
                "available_quantity": 3,
                "is_infinite": False,
            },
        )
        resource = ProductsResource(mock_http)
        result = resource.stocks.create(
            "96d0f5c3-1958-4a31-8b03-7014c2070630",
            location="982a2aac-b9af-44e3-a3e0-51d2faa6b7c2",
            available_quantity=3,
            is_infinite=False,
        )
        assert result["id"] == "0abacb3a-6a43-474d-b1c9-097e95824117"
        assert result["available_quantity"] == 3
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"]["location"] == "982a2aac-b9af-44e3-a3e0-51d2faa6b7c2"
        assert request["json"]["available_quantity"] == 3
        assert request["json"]["is_infinite"] is False

    def test_update_sends_patch(self, mock_http):
        """update() sends a PATCH request with the correct payload."""
        mock_http.set_response(
            "PATCH",
            "/v1/products/{product_id}/stocks/{stock_id}/",
            {
                "product_id": "96d0f5c3-1958-4a31-8b03-7014c2070630",
                "location": "8ee590fe-d02d-4c50-9184-f628bb8b115a",
                "quantity": 5,
                "is_infinite": False,
            },
        )
        resource = ProductsResource(mock_http)
        result = resource.stocks.update(
            "96d0f5c3-1958-4a31-8b03-7014c2070630",
            "e44bbf6b-c62a-4597-b87f-311fba0e0256",
            available_quantity=5,
            is_infinite=False,
        )
        assert result["quantity"] == 5
        request = mock_http.requests[0]
        assert request["method"] == "PATCH"
        assert request["json"]["available_quantity"] == 5
        assert request["json"]["is_infinite"] is False

    def test_update_sends_correct_path(self, mock_http):
        """update() constructs the correct API path."""
        mock_http.set_response(
            "PATCH",
            "/v1/products/{product_id}/stocks/{stock_id}/",
            {"product_id": "p1", "location": "l1", "quantity": 10, "is_infinite": False},
        )
        resource = ProductsResource(mock_http)
        resource.stocks.update("prod-123", "stock-456", available_quantity=10)
        request = mock_http.requests[0]
        assert request["path"] == "/v1/products/prod-123/stocks/stock-456/"

    def test_bulk_update_sends_patch(self, mock_http):
        """bulk_update() sends a PATCH request with a list payload."""
        mock_http.set_response(
            "PATCH",
            "/v1/products/{product_id}/stocks/",
            None,
            status=204,
        )
        resource = ProductsResource(mock_http)
        resource.stocks.bulk_update(
            "96d0f5c3-1958-4a31-8b03-7014c2070630",
            [
                {
                    "location": "8ee590fe-d02d-4c50-9184-f628bb8b115a",
                    "available_quantity": 10,
                    "is_infinite": False,
                },
                {
                    "location": "982a2aac-b9af-44e3-a3e0-51d2faa6b7c2",
                    "available_quantity": 20,
                    "is_infinite": False,
                },
            ],
        )
        request = mock_http.requests[0]
        assert request["method"] == "PATCH"
        assert request["path"] == "/v1/products/96d0f5c3-1958-4a31-8b03-7014c2070630/stocks/"
        assert len(request["json"]) == 2


from zid.models.product._base import ProductVariant


class TestProductVariantsSubResource:
    """Tests for ProductVariantsSubResource via ProductsResource.variants."""

    def test_create_returns_product(self, mock_http, variant_create_response):
        """create() returns a Product with variants populated."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/variants/",
            variant_create_response,
        )
        resource = ProductsResource(mock_http)
        product = resource.variants.create(
            "3c58afbb-7b07-4859-b653-b52242a33bb7",
            variants=[
                {
                    "sku": "Z.6.7228299999713898900",
                    "price": 144,
                    "attributes": [
                        {"slug": "اللون", "value": {"ar": "اسود", "en": "Black"}}
                    ],
                    "stocks": [
                        {
                            "available_quantity": 77,
                            "is_infinite": False,
                            "location": "e2629f14-12ad-4ee4-8103-9db7290c4ccc",
                        }
                    ],
                },
                {
                    "sku": "Z.6.8339400000824909011",
                    "price": 144,
                    "attributes": [
                        {"slug": "اللون", "value": {"ar": "ابيض", "en": "White"}}
                    ],
                },
            ],
        )
        assert isinstance(product, Product)
        assert product.id == "3c58afbb-7b07-4859-b653-b52242a33bb7"
        assert product.structure == "parent"
        assert len(product.variants) == 2

    def test_create_variants_are_typed(self, mock_http, variant_create_response):
        """create() returns Product whose variants are ProductVariant instances."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/variants/",
            variant_create_response,
        )
        resource = ProductsResource(mock_http)
        product = resource.variants.create(
            "3c58afbb-7b07-4859-b653-b52242a33bb7",
            variants=[
                {
                    "attributes": [
                        {"slug": "اللون", "value": {"ar": "اسود", "en": "Black"}}
                    ],
                }
            ],
        )
        for variant in product.variants:
            assert isinstance(variant, ProductVariant)
        assert product.variants[0].id == "22a32ae6-6c6c-4904-9e2f-9c3a9373f8f1"
        assert product.variants[0].structure == "child"
        assert product.variants[0].parent_id == "3c58afbb-7b07-4859-b653-b52242a33bb7"
        assert product.variants[1].slug == "en-white"

    def test_create_sends_correct_payload(self, mock_http, variant_create_response):
        """create() sends JSON body with variants array."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/variants/",
            variant_create_response,
        )
        resource = ProductsResource(mock_http)
        variants_payload = [
            {
                "id": "ebd067c3-6c51-4692-9cac-e43118930ec2",
                "is_deleted": False,
                "sku": "Z.1.111111",
                "price": 144,
                "sale_price": None,
                "cost": None,
                "barcode": "Z.1.111111",
                "attributes": [
                    {"slug": "اللون", "value": {"ar": "ابيض", "en": "White"}}
                ],
                "stocks": [
                    {
                        "available_quantity": 44,
                        "is_infinite": False,
                        "location": "e2629f14-12ad-4ee4-8103-9db7290c4ccc",
                    }
                ],
                "weight": {"unit": "kg", "value": None},
            }
        ]
        resource.variants.create(
            "3c58afbb-7b07-4859-b653-b52242a33bb7",
            variants=variants_payload,
        )
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["path"] == "/v1/products/3c58afbb-7b07-4859-b653-b52242a33bb7/variants/"
        assert request["json"]["variants"] == variants_payload

    def test_create_sends_correct_path(self, mock_http, variant_create_response):
        """create() constructs the correct API path."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/variants/",
            variant_create_response,
        )
        resource = ProductsResource(mock_http)
        resource.variants.create(
            "my-product-uuid",
            variants=[{"attributes": [{"slug": "size", "value": {"en": "L"}}]}],
        )
        request = mock_http.requests[0]
        assert request["path"] == "/v1/products/my-product-uuid/variants/"

    def test_create_product_has_options(self, mock_http, variant_create_response):
        """create() response includes options on the parent product."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/variants/",
            variant_create_response,
        )
        resource = ProductsResource(mock_http)
        product = resource.variants.create(
            "3c58afbb-7b07-4859-b653-b52242a33bb7",
            variants=[
                {"attributes": [{"slug": "اللون", "value": {"en": "Black"}}]}
            ],
        )
        assert product.has_options is True
        assert len(product.options) == 1
        assert product.options[0].name == "Color"
        assert "Black" in product.options[0].choices
        assert "White" in product.options[0].choices


from zid.models.product._customization import CustomInputField, CustomOption


class TestProductCustomizationsSubResource:
    """Tests for ProductCustomizationsSubResource via ProductsResource.customizations."""

    def test_create_option_returns_custom_option(self, mock_http):
        """create_option() returns a CustomOption instance."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/custom_options_fields/",
            {
                "id": "a8b0e6ce-6937-4c56-8253-9478d0f28475",
                "type": "CHECKBOX",
                "label": {"ar": "خيار مخصص", "en": "Custom Option"},
                "hint": {"ar": "يرجى اختيار", "en": "Please select"},
                "min_choices": 1,
                "max_choices": 100,
                "can_choose_multiple_options": True,
                "is_published": True,
                "is_required": True,
                "display_order": 2,
                "choices": [
                    {"ar": "قيمة 1", "en": "Value 1", "price": 66.5, "id": "choice-uuid-1"}
                ],
                "visibility_condition": None,
            },
        )
        resource = ProductsResource(mock_http)
        option = resource.customizations.create_option(
            "e0ad7a76-ba42-4c59-94c9-0da600117fbf",
            label={"ar": "خيار مخصص", "en": "Custom Option"},
            hint={"ar": "يرجى اختيار", "en": "Please select"},
            is_published=True,
            is_required=True,
            display_order=2,
            choices=[{"ar": "قيمة 1", "en": "Value 1", "price": 66.5}],
            can_choose_multiple_options=True,
            min_choices=1,
            max_choices=100,
        )
        assert isinstance(option, CustomOption)
        assert option.id == "a8b0e6ce-6937-4c56-8253-9478d0f28475"
        assert option.type == "CHECKBOX"
        assert option.is_published is True
        assert option.is_required is True
        assert option.display_order == 2
        assert len(option.choices) == 1
        assert option.choices[0].price == 66.5

    def test_create_option_sends_correct_payload(self, mock_http):
        """create_option() sends JSON body with all required fields."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/custom_options_fields/",
            {
                "id": "new-option-uuid",
                "type": "DROPDOWN",
                "label": {"ar": "اختيار", "en": "Select"},
                "hint": {"ar": "", "en": ""},
                "min_choices": 0,
                "max_choices": 1,
                "can_choose_multiple_options": False,
                "is_published": True,
                "is_required": False,
                "display_order": 1,
                "choices": [{"ar": "أ", "en": "A", "price": 0}],
                "visibility_condition": None,
            },
        )
        resource = ProductsResource(mock_http)
        resource.customizations.create_option(
            "prod-uuid",
            label={"ar": "اختيار", "en": "Select"},
            is_published=True,
            is_required=False,
            display_order=1,
            choices=[{"ar": "أ", "en": "A", "price": 0}],
        )
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["path"] == "/v1/products/prod-uuid/custom_options_fields/"
        assert request["json"]["label"] == {"ar": "اختيار", "en": "Select"}
        assert request["json"]["is_published"] is True
        assert request["json"]["is_required"] is False
        assert request["json"]["display_order"] == 1
        assert len(request["json"]["choices"]) == 1
        # Optional fields should not be present when not provided
        assert "hint" not in request["json"]
        assert "type" not in request["json"]
        assert "min_choices" not in request["json"]

    def test_update_option_returns_custom_option(self, mock_http):
        """update_option() returns an updated CustomOption instance."""
        mock_http.set_response(
            "PUT",
            "/v1/products/{product_id}/custom_options_fields/{custom_option_field_id}/",
            {
                "id": "a8b0e6ce-6937-4c56-8253-9478d0f28475",
                "type": "CHECKBOX",
                "label": {"ar": "خيار محدث", "en": "Updated Option"},
                "hint": {"ar": "يرجى اختيار الخيار المناسب", "en": "Please select"},
                "min_choices": 1,
                "max_choices": 50,
                "can_choose_multiple_options": True,
                "is_published": True,
                "is_required": False,
                "display_order": 4,
                "choices": [
                    {"ar": "قيمة 1", "en": "Value 1", "price": 66.5, "id": "0908e710-f3fe-4c56-80c0-bd317c8e6f5d"}
                ],
                "visibility_condition": None,
            },
        )
        resource = ProductsResource(mock_http)
        option = resource.customizations.update_option(
            "e0ad7a76-ba42-4c59-94c9-0da600117fbf",
            "a8b0e6ce-6937-4c56-8253-9478d0f28475",
            label={"ar": "خيار محدث", "en": "Updated Option"},
            hint={"ar": "يرجى اختيار الخيار المناسب", "en": "Please select"},
            is_published=True,
            is_required=False,
            display_order=4,
            choices=[
                {"ar": "قيمة 1", "en": "Value 1", "price": 66.5, "id": "0908e710-f3fe-4c56-80c0-bd317c8e6f5d"}
            ],
            can_choose_multiple_options=True,
            min_choices=1,
            max_choices=50,
        )
        assert isinstance(option, CustomOption)
        assert option.id == "a8b0e6ce-6937-4c56-8253-9478d0f28475"
        assert option.label.en == "Updated Option"
        assert option.display_order == 4
        assert option.is_required is False

    def test_update_option_sends_put(self, mock_http):
        """update_option() sends a PUT request to the correct path."""
        mock_http.set_response(
            "PUT",
            "/v1/products/{product_id}/custom_options_fields/{custom_option_field_id}/",
            {
                "id": "field-uuid",
                "type": "DROPDOWN",
                "label": {"ar": "ل", "en": "L"},
                "hint": {"ar": "", "en": ""},
                "min_choices": 0,
                "max_choices": 1,
                "can_choose_multiple_options": False,
                "is_published": False,
                "is_required": False,
                "display_order": 1,
                "choices": [],
                "visibility_condition": None,
            },
        )
        resource = ProductsResource(mock_http)
        resource.customizations.update_option(
            "prod-123",
            "field-456",
            label={"ar": "ل", "en": "L"},
            is_published=False,
            is_required=False,
            display_order=1,
            choices=[],
        )
        request = mock_http.requests[0]
        assert request["method"] == "PUT"
        assert request["path"] == "/v1/products/prod-123/custom_options_fields/field-456/"

    def test_create_input_field_returns_custom_input_field(self, mock_http):
        """create_input_field() returns a CustomInputField instance."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/custom_user_input_fields/",
            {
                "id": "abc123",
                "type": "TEXT",
                "hint": {"en": "Please enter the desired value", "ar": "يرجى إدخال القيمة المطلوبة"},
                "label": {"en": "Custom Text", "ar": "نص مخصص"},
            },
        )
        resource = ProductsResource(mock_http)
        field = resource.customizations.create_input_field(
            "e0ad7a76-ba42-4c59-94c9-0da600117fbf",
            type="TEXT",
            label={"ar": "نص مخصص", "en": "Custom Text"},
            hint={"ar": "يرجى إدخال القيمة المطلوبة", "en": "Please enter the desired value"},
            price="100.00",
        )
        assert isinstance(field, CustomInputField)
        assert field.id == "abc123"
        assert field.type == "TEXT"
        assert field.label.en == "Custom Text"
        assert field.label.ar == "نص مخصص"
        assert field.hint.en == "Please enter the desired value"

    def test_create_input_field_sends_correct_payload(self, mock_http):
        """create_input_field() sends JSON body with correct fields."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/custom_user_input_fields/",
            {
                "id": "new-field",
                "type": "TEXT",
                "hint": None,
                "label": {"en": "Custom Text", "ar": "نص مخصص"},
            },
        )
        resource = ProductsResource(mock_http)
        resource.customizations.create_input_field(
            "prod-uuid",
            type="TEXT",
            label={"ar": "نص مخصص", "en": "Custom Text"},
        )
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["path"] == "/v1/products/prod-uuid/custom_user_input_fields/"
        assert request["json"]["type"] == "TEXT"
        assert request["json"]["label"] == {"ar": "نص مخصص", "en": "Custom Text"}
        # Optional fields should not be present when not provided
        assert "hint" not in request["json"]
        assert "price" not in request["json"]

    def test_create_input_field_with_price(self, mock_http):
        """create_input_field() includes price when provided."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/custom_user_input_fields/",
            {
                "id": "field-with-price",
                "type": "TEXT",
                "hint": {"en": "Enter value", "ar": "أدخل"},
                "label": {"en": "Gift Message", "ar": "رسالة هدية"},
            },
        )
        resource = ProductsResource(mock_http)
        resource.customizations.create_input_field(
            "prod-uuid",
            type="TEXT",
            label={"ar": "رسالة هدية", "en": "Gift Message"},
            hint={"ar": "أدخل", "en": "Enter value"},
            price="50.00",
        )
        request = mock_http.requests[0]
        assert request["json"]["price"] == "50.00"
        assert request["json"]["hint"] == {"ar": "أدخل", "en": "Enter value"}

    def test_delete_option_sends_delete(self, mock_http):
        """delete_option() sends DELETE request to correct path."""
        mock_http.set_response(
            "DELETE",
            "/v1/products/{product_id}/custom_options_fields/{custom_option_field_id}/",
            {},
        )
        resource = ProductsResource(mock_http)
        result = resource.customizations.delete_option(
            "e0ad7a76-ba42-4c59-94c9-0da600117fbf",
            "a8b0e6ce-6937-4c56-8253-9478d0f28475",
        )
        assert result is None
        request = mock_http.requests[0]
        assert request["method"] == "DELETE"
        assert request["path"] == "/v1/products/e0ad7a76-ba42-4c59-94c9-0da600117fbf/custom_options_fields/a8b0e6ce-6937-4c56-8253-9478d0f28475/"


from zid.models.product._notification import (
    NotificationSettings,
    NotificationStats,
    ProductNotification,
)


class TestProductNotificationsSubResource:
    """Tests for ProductNotificationsSubResource via ProductsResource.notifications."""

    def test_list_returns_iterator(self, mock_http, product_notifications_list_response):
        """list() returns a paginated iterator of ProductNotification."""
        mock_http.set_response(
            "GET",
            "/v1/products/notifications/",
            product_notifications_list_response,
        )
        resource = ProductsResource(mock_http)
        result = list(resource.notifications.list())
        assert len(result) == 2
        assert all(isinstance(n, ProductNotification) for n in result)
        assert result[0].id == "0d8f7dc9-423d-4e54-ab47-6c170f4c0d84"
        assert result[1].is_notified is True

    def test_list_with_filters(self, mock_http, product_notifications_list_response):
        """list() passes filter parameters correctly."""
        mock_http.set_response(
            "GET",
            "/v1/products/notifications/",
            product_notifications_list_response,
        )
        resource = ProductsResource(mock_http)
        list(resource.notifications.list(
            q="headphones",
            product_id="a7ad89d0-03e2-430f-b6e4-0624ef05e571",
            page=2,
            page_size=10,
            created_at__gte="2026-01-01T00:00:00Z",
            created_at__lte="2026-12-31T23:59:59Z",
        ))
        request = mock_http.requests[0]
        assert request["params"]["q"] == "headphones"
        assert request["params"]["product_id"] == "a7ad89d0-03e2-430f-b6e4-0624ef05e571"
        assert request["params"]["page"] == 2
        assert request["params"]["page_size"] == 10
        assert request["params"]["created_at__gte"] == "2026-01-01T00:00:00Z"
        assert request["params"]["created_at__lte"] == "2026-12-31T23:59:59Z"

    def test_get_stats(self, mock_http):
        """get_stats() returns NotificationStats."""
        mock_http.set_response(
            "GET",
            "/v1/products/notifications/stats/",
            {
                "total_count": 10,
                "notified_count": 5,
                "purchased_count": 2,
                "purchased_total": 514.50,
            },
        )
        resource = ProductsResource(mock_http)
        stats = resource.notifications.get_stats()
        assert isinstance(stats, NotificationStats)
        assert stats.total_count == 10
        assert stats.notified_count == 5
        assert stats.purchased_count == 2
        assert stats.purchased_total == 514.50

    def test_get_settings(self, mock_http):
        """get_settings() returns NotificationSettings."""
        mock_http.set_response(
            "GET",
            "/v1/products/notifications/settings/",
            {
                "settings": {
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
            },
        )
        resource = ProductsResource(mock_http)
        settings = resource.notifications.get_settings()
        assert isinstance(settings, NotificationSettings)
        assert settings.delay_unit == "hour"
        assert settings.delay_value == 15
        assert settings.email_text.en == "You will be notified when the product is available"
        assert settings.email_title.ar == "المنتج متوفر الآن"
        assert settings.coupon_code is None

    def test_update_settings(self, mock_http):
        """update_settings() sends POST with correct JSON payload."""
        mock_http.set_response(
            "POST",
            "/v1/products/notifications/settings/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.notifications.update_settings(
            delay_unit="minute",
            delay_value=50,
            email_text={"ar": "نص عربي", "en": "English text"},
            email_title={"ar": "عنوان", "en": "Title"},
        )
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"]["delay_unit"] == "minute"
        assert request["json"]["delay_value"] == 50
        assert request["json"]["email_text"] == {"ar": "نص عربي", "en": "English text"}
        assert request["json"]["email_title"] == {"ar": "عنوان", "en": "Title"}

    def test_update_settings_partial(self, mock_http):
        """update_settings() only includes provided fields."""
        mock_http.set_response(
            "POST",
            "/v1/products/notifications/settings/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.notifications.update_settings(delay_unit="day", delay_value=1)
        request = mock_http.requests[0]
        assert request["json"] == {"delay_unit": "day", "delay_value": 1}

    def test_create(self, mock_http):
        """create() sends form data to the correct path."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/notifications/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.notifications.create(
            "a7ad89d0-03e2-430f-b6e4-0624ef05e571",
            email="customer@example.com",
            language="en",
            customer_name="John Doe",
        )
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["path"] == "/v1/products/a7ad89d0-03e2-430f-b6e4-0624ef05e571/notifications/"
        assert request["data"]["email"] == "customer@example.com"
        assert request["data"]["language"] == "en"
        assert request["data"]["customer_name"] == "John Doe"

    def test_create_minimal(self, mock_http):
        """create() with only required email field."""
        mock_http.set_response(
            "POST",
            "/v1/products/{product_id}/notifications/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.notifications.create(
            "prod-uuid",
            email="test@test.com",
        )
        request = mock_http.requests[0]
        assert request["data"] == {"email": "test@test.com"}

    def test_send_email(self, mock_http):
        """send_email() sends form data with required fields."""
        mock_http.set_response(
            "POST",
            "/v1/products/notifications/send/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.notifications.send_email(
            email="customer@example.com",
            customer_name="John Doe",
            product_id="554da609-2f14-427f-9ca5-298d9dea5c1b",
            method="email",
            language="en",
            title="Product Available",
            content="Your product is back in stock!",
        )
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["data"]["email"] == "customer@example.com"
        assert request["data"]["customer_name"] == "John Doe"
        assert request["data"]["product_id"] == "554da609-2f14-427f-9ca5-298d9dea5c1b"
        assert request["data"]["method"] == "email"
        assert request["data"]["language"] == "en"
        assert request["data"]["title"] == "Product Available"
        assert request["data"]["content"] == "Your product is back in stock!"

    def test_send_email_minimal(self, mock_http):
        """send_email() with only required fields."""
        mock_http.set_response(
            "POST",
            "/v1/products/notifications/send/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.notifications.send_email(
            email="test@test.com",
            customer_name="Test",
            product_id="prod-uuid",
            method="email",
        )
        request = mock_http.requests[0]
        assert request["data"] == {
            "email": "test@test.com",
            "customer_name": "Test",
            "product_id": "prod-uuid",
            "method": "email",
        }

    def test_export(self, mock_http):
        """export() sends form data with required fields."""
        mock_http.set_response(
            "POST",
            "/v1/products/notifications/export/",
            {},
        )
        resource = ProductsResource(mock_http)
        resource.notifications.export(
            email="customer@example.com",
            is_notified=True,
        )
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["data"]["email"] == "customer@example.com"
        assert request["data"]["is_notified"] is True

from zid.models.product._attribute import Attribute, AttributePreset, Badge, Metafield


class TestProductAttributesSubResource:
    """Tests for the ProductAttributesSubResource."""

    def test_list_returns_iterator(self, mock_http, attributes_list_response):
        """list() returns a PaginatedIterator of Attribute instances."""
        mock_http.set_response("GET", "/v1/attributes/", attributes_list_response)
        resource = ProductsResource(mock_http)
        result = list(resource.attributes.list())
        assert len(result) == 3
        assert isinstance(result[0], Attribute)
        assert result[0].name == "Color"

    def test_list_with_presets(self, mock_http, attributes_list_response):
        """list() parses nested presets correctly."""
        mock_http.set_response("GET", "/v1/attributes/", attributes_list_response)
        resource = ProductsResource(mock_http)
        result = list(resource.attributes.list())
        attr_with_presets = result[1]
        assert len(attr_with_presets.presets) == 2
        assert isinstance(attr_with_presets.presets[0], AttributePreset)
        assert attr_with_presets.presets[0].value == "Small"

    def test_list_with_pagination_params(self, mock_http, attributes_list_response):
        """list() passes pagination params correctly."""
        mock_http.set_response("GET", "/v1/attributes/", attributes_list_response)
        resource = ProductsResource(mock_http)
        list(resource.attributes.list(page=2, page_size=10))
        request = mock_http.requests[0]
        assert request["params"]["page"] == 2
        assert request["params"]["page_size"] == 10

    def test_get_returns_attribute(self, mock_http, attribute_detail_response):
        """get() returns a single Attribute instance."""
        mock_http.set_response(
            "GET",
            "/v1/attributes/{id}/",
            attribute_detail_response,
        )
        resource = ProductsResource(mock_http)
        attr = resource.attributes.get("cfb5bd3f-bbc5-4439-a171-b2d70e1c0293")
        assert isinstance(attr, Attribute)
        assert attr.id == "cfb5bd3f-bbc5-4439-a171-b2d70e1c0293"
        assert attr.name == "Size"
        assert len(attr.presets) == 3

    def test_list_presets_returns_iterator(self, mock_http, attribute_presets_list_response):
        """list_presets() returns a PaginatedIterator of AttributePreset instances."""
        mock_http.set_response(
            "GET",
            "/v1/attributes/{id}/presets/",
            attribute_presets_list_response,
        )
        resource = ProductsResource(mock_http)
        result = list(
            resource.attributes.list_presets("cfb5bd3f-bbc5-4439-a171-b2d70e1c0293")
        )
        assert len(result) == 3
        assert isinstance(result[0], AttributePreset)
        assert result[0].value == "Small"
        assert result[2].value == "Large"

    def test_update_preset_returns_preset(self, mock_http):
        """update_preset() sends PATCH and returns updated AttributePreset."""
        mock_http.set_response(
            "PATCH",
            "/v1/attributes/{id}/presets/{id}/",
            {
                "id": "4469e2f3-20b5-438b-893d-a22e61d55b7b",
                "slug": "color-6",
                "name": "",
                "value": "Size Size",
                "type": "default",
                "type_value": None,
                "display_order": None,
                "attribute_image_id": None,
                "attribute_id": "cfb5bd3f-bbc5-4439-a171-b2d70e1c0293",
            },
        )
        resource = ProductsResource(mock_http)
        preset = resource.attributes.update_preset(
            "cfb5bd3f-bbc5-4439-a171-b2d70e1c0293",
            "4469e2f3-20b5-438b-893d-a22e61d55b7b",
            value={"ar": "الحجم", "en": "Size Size"},
        )
        assert isinstance(preset, AttributePreset)
        assert preset.value == "Size Size"
        request = mock_http.requests[0]
        assert request["method"] == "PATCH"
        assert request["json"]["value"] == {"ar": "الحجم", "en": "Size Size"}

    def test_list_metafields_returns_iterator(self, mock_http, metafields_list_response):
        """list_metafields() returns a PaginatedIterator of Metafield instances."""
        mock_http.set_response("GET", "/v1/Metafields/", metafields_list_response)
        resource = ProductsResource(mock_http)
        result = list(resource.attributes.list_metafields())
        assert len(result) == 2
        assert isinstance(result[0], Metafield)
        assert result[0].name.en == "Color"
        assert result[0].value.en == "Black"

    def test_create_metafield_returns_metafield(self, mock_http):
        """create_metafield() sends POST and returns a Metafield."""
        mock_http.set_response(
            "POST",
            "/v1/Metafields",
            {
                "id": "new-metafield-uuid",
                "name": {"ar": "اللون", "en": "Color"},
                "slug": "color",
                "value": None,
            },
        )
        resource = ProductsResource(mock_http)
        mf = resource.attributes.create_metafield(
            name={"ar": "اللون", "en": "Color"},
        )
        assert isinstance(mf, Metafield)
        assert mf.id == "new-metafield-uuid"
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"]["name"] == {"ar": "اللون", "en": "Color"}

    def test_list_badges_returns_list(self, mock_http, badges_list_response):
        """list_badges() returns a list of Badge instances."""
        mock_http.set_response("GET", "/v1/badges/", badges_list_response)
        resource = ProductsResource(mock_http)
        badges = resource.attributes.list_badges()
        assert isinstance(badges, list)
        assert len(badges) == 3
        assert isinstance(badges[0], Badge)
        assert badges[0].is_example is True
        assert badges[0].icon is not None
        assert badges[0].icon.code == "discount_percent"

    def test_list_badges_without_icon(self, mock_http, badges_list_response):
        """list_badges() correctly parses badges without icons."""
        mock_http.set_response("GET", "/v1/badges/", badges_list_response)
        resource = ProductsResource(mock_http)
        badges = resource.attributes.list_badges()
        assert badges[1].icon is None
        assert badges[1].body.en == "10% discount"

    def test_update_returns_attribute(self, mock_http):
        """update() sends PATCH and returns updated Attribute."""
        mock_http.set_response(
            "PATCH",
            "/v1/attributes/{id}/",
            {
                "id": "6f637324-a016-4389-a397-44233a13692c",
                "name": "Weight 2",
                "slug": "weight",
                "presets": [],
                "is_extra": True,
                "is_enabled": False,
                "display_order": 1,
                "preset_count": None,
            },
        )
        resource = ProductsResource(mock_http)
        attr = resource.attributes.update(
            "6f637324-a016-4389-a397-44233a13692c",
            name="Weight 2",
            is_extra=True,
            is_enabled=False,
            display_order=1,
        )
        assert isinstance(attr, Attribute)
        assert attr.name == "Weight 2"
        assert attr.is_extra is True
        assert attr.is_enabled is False
        request = mock_http.requests[0]
        assert request["method"] == "PATCH"
        assert request["json"]["name"] == "Weight 2"

    def test_delete_sends_request(self, mock_http):
        """delete() sends DELETE request."""
        mock_http.set_response("DELETE", "/v1/attributes/{id}/", None)
        resource = ProductsResource(mock_http)
        resource.attributes.delete("1f258e6a-4433-46f0-aa8a-3bc987839b69")
        request = mock_http.requests[0]
        assert request["method"] == "DELETE"
        assert "/v1/attributes/1f258e6a-4433-46f0-aa8a-3bc987839b69/" in request["path"]

    def test_create_preset_returns_preset(self, mock_http):
        """create_preset() sends POST and returns AttributePreset."""
        mock_http.set_response(
            "POST",
            "/v1/attributes/{id}/presets/",
            {
                "id": "4469e2f3-20b5-438b-893d-a22e61d55b7b",
                "slug": "color-6",
                "name": "",
                "value": "color",
                "type": "default",
                "type_value": None,
                "display_order": None,
                "attribute_image_id": None,
                "attribute_id": "cfb5bd3f-bbc5-4439-a171-b2d70e1c0293",
            },
        )
        resource = ProductsResource(mock_http)
        preset = resource.attributes.create_preset(
            "cfb5bd3f-bbc5-4439-a171-b2d70e1c0293",
            value={"ar": "اللون", "en": "color"},
        )
        assert isinstance(preset, AttributePreset)
        assert preset.id == "4469e2f3-20b5-438b-893d-a22e61d55b7b"
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"]["value"] == {"ar": "اللون", "en": "color"}

    def test_delete_preset_sends_request(self, mock_http):
        """delete_preset() sends DELETE request."""
        mock_http.set_response("DELETE", "/v1/attributes/{id}/presets/{id}/", None)
        resource = ProductsResource(mock_http)
        resource.attributes.delete_preset(
            "cfb5bd3f-bbc5-4439-a171-b2d70e1c0293",
            "4469e2f3-20b5-438b-893d-a22e61d55b7b",
        )
        request = mock_http.requests[0]
        assert request["method"] == "DELETE"
        assert "/v1/attributes/cfb5bd3f-bbc5-4439-a171-b2d70e1c0293/presets/4469e2f3-20b5-438b-893d-a22e61d55b7b/" in request["path"]

    def test_create_returns_attribute(self, mock_http):
        """create() sends POST and returns new Attribute."""
        mock_http.set_response(
            "POST",
            "/v1/attributes/",
            {
                "id": "6f637324-a016-4389-a397-44233a13692c",
                "name": "Weight",
                "slug": "weight",
                "presets": [],
                "is_extra": False,
                "is_enabled": True,
                "display_order": None,
                "preset_count": None,
            },
        )
        resource = ProductsResource(mock_http)
        attr = resource.attributes.create(
            name="Weight",
            slug="weight",
            is_enabled=True,
        )
        assert isinstance(attr, Attribute)
        assert attr.id == "6f637324-a016-4389-a397-44233a13692c"
        assert attr.name == "Weight"
        assert attr.slug == "weight"
        request = mock_http.requests[0]
        assert request["method"] == "POST"
        assert request["json"]["name"] == "Weight"
        assert request["json"]["slug"] == "weight"
        assert request["json"]["is_enabled"] is True
        assert "is_extra" not in request["json"]

    def test_create_minimal(self, mock_http):
        """create() with only required name field."""
        mock_http.set_response(
            "POST",
            "/v1/attributes/",
            {
                "id": "new-attr-uuid",
                "name": "Color",
                "slug": "color",
                "presets": [],
                "is_extra": False,
                "is_enabled": True,
                "display_order": None,
                "preset_count": None,
            },
        )
        resource = ProductsResource(mock_http)
        resource.attributes.create(name="Color")
        request = mock_http.requests[0]
        assert request["json"] == {"name": "Color"}
