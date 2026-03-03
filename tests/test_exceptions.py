"""Unit tests for exception handling.

Tests that HTTP errors are correctly mapped to SDK exceptions.
"""

import pytest

from zid.exceptions import (
    ZidError,
    ZidAPIError,
    ZidAuthenticationError,
    ZidAuthorizationError,
    ZidNotFoundError,
    ZidValidationError,
    ZidRateLimitError,
    ZidServerError,
    ZidConnectionError,
)
from zid.resources.customers import CustomersResource
from zid.resources.orders import OrdersResource


class TestExceptionHierarchy:
    """Tests for exception class hierarchy."""
    
    def test_all_exceptions_inherit_from_zid_error(self):
        """All SDK exceptions inherit from ZidError."""
        assert issubclass(ZidAPIError, ZidError)
        assert issubclass(ZidAuthenticationError, ZidAPIError)
        assert issubclass(ZidAuthorizationError, ZidAPIError)
        assert issubclass(ZidNotFoundError, ZidAPIError)
        assert issubclass(ZidValidationError, ZidAPIError)
        assert issubclass(ZidRateLimitError, ZidAPIError)
        assert issubclass(ZidServerError, ZidAPIError)
        assert issubclass(ZidConnectionError, ZidError)
    
    def test_api_error_has_status_code(self):
        """ZidAPIError includes status code."""
        error = ZidAPIError("Test error", status_code=400)
        assert error.status_code == 400
        assert error.message == "Test error"
    
    def test_validation_error_has_field_errors(self):
        """ZidValidationError includes field-level errors."""
        error = ZidValidationError(
            message="Validation failed",
            errors={"email": ["Invalid email format"]},
        )
        assert error.errors == {"email": ["Invalid email format"]}
    
    def test_rate_limit_error_has_retry_after(self):
        """ZidRateLimitError includes retry-after."""
        error = ZidRateLimitError(message="Too many requests", retry_after=60)
        assert error.retry_after == 60


class TestCustomersExceptionHandling:
    """Tests for Customers resource exception handling."""
    
    def test_get_nonexistent_raises_not_found(self, mock_http, error_404):
        """Getting nonexistent customer raises ZidNotFoundError."""
        mock_http.set_response("GET", "/v1/managers/store/customers/99999", error_404, status=404)
        
        resource = CustomersResource(mock_http)
        
        with pytest.raises(ZidNotFoundError) as exc_info:
            resource.get(99999)
        
        assert exc_info.value.status_code == 404
    
    def test_invalid_auth_raises_authentication_error(self, mock_http, error_401):
        """Invalid auth raises ZidAuthenticationError."""
        mock_http.set_response("GET", "/v1/managers/store/customers", error_401, status=401)
        
        resource = CustomersResource(mock_http)
        
        with pytest.raises(ZidAuthenticationError) as exc_info:
            list(resource.list())
        
        assert exc_info.value.status_code == 401
    
    def test_forbidden_raises_authorization_error(self, mock_http, error_403):
        """Forbidden access raises ZidAuthorizationError."""
        mock_http.set_response("GET", "/v1/managers/store/customers", error_403, status=403)
        
        resource = CustomersResource(mock_http)
        
        with pytest.raises(ZidAuthorizationError) as exc_info:
            list(resource.list())
        
        assert exc_info.value.status_code == 403


class TestOrdersExceptionHandling:
    """Tests for Orders resource exception handling."""
    
    def test_get_nonexistent_order_raises_not_found(self, mock_http, error_404):
        """Getting nonexistent order raises ZidNotFoundError."""
        mock_http.set_response("GET", "/v1/managers/store/orders/{id}/view", error_404, status=404)
        
        resource = OrdersResource(mock_http)
        
        with pytest.raises(ZidNotFoundError):
            resource.get(99999)
    
    def test_invalid_status_update_raises_validation_error(self, mock_http, error_422):
        """Invalid status update raises ZidValidationError."""
        mock_http.set_response(
            "POST",
            "/v1/managers/store/orders/{id}/change-order-status",
            error_422,
            status=422,
        )
        
        resource = OrdersResource(mock_http)
        
        with pytest.raises(ZidValidationError):
            resource.update_status(123, order_status="invalid_status")
    
    def test_rate_limit_raises_rate_limit_error(self, mock_http, error_429):
        """Rate limiting raises ZidRateLimitError."""
        mock_http.set_response("GET", "/v1/managers/store/orders", error_429, status=429)
        
        resource = OrdersResource(mock_http)
        
        with pytest.raises(ZidRateLimitError):
            list(resource.list())
    
    def test_server_error_raises_server_error(self, mock_http, error_500):
        """Server errors raise ZidServerError."""
        mock_http.set_response("GET", "/v1/managers/store/orders", error_500, status=500)
        
        resource = OrdersResource(mock_http)
        
        with pytest.raises(ZidServerError) as exc_info:
            list(resource.list())
        
        assert exc_info.value.status_code == 500


class TestExceptionStringRepresentation:
    """Tests for exception __str__ methods."""
    
    def test_api_error_str_includes_status(self):
        """API error string includes status code."""
        error = ZidAPIError("Something went wrong", status_code=400)
        assert "400" in str(error)
        assert "Something went wrong" in str(error)
    
    def test_validation_error_str_includes_fields(self):
        """Validation error string includes field errors."""
        error = ZidValidationError(
            message="Validation failed",
            errors={"email": ["Invalid format"]},
        )
        assert "email" in str(error)
    
    def test_rate_limit_error_str_includes_retry(self):
        """Rate limit error string includes retry-after."""
        error = ZidRateLimitError(message="Too many requests", retry_after=30)
        assert "30" in str(error)
