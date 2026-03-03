"""Pytest configuration and shared fixtures."""

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import httpx
import pytest

from zid import ZidClient
from zid.http import HTTPClient


FIXTURES_DIR = Path(__file__).parent / "fixtures"


# =============================================================================
# Fixture Loading Helpers
# =============================================================================

def load_fixture(name: str) -> dict[str, Any]:
    """Load a JSON fixture file."""
    path = FIXTURES_DIR / f"{name}.json"
    if not path.exists():
        pytest.skip(f"Fixture {name}.json not found - run capture_fixtures.py first")
    return json.loads(path.read_text())


# =============================================================================
# Mock HTTP Client
# =============================================================================

class MockHTTPClient:
    """Mock HTTP client for unit tests."""
    
    def __init__(self):
        self.responses: dict[str, Any] = {}
        self.requests: list[dict] = []
    
    def set_response(self, method: str, path: str, response: Any, status: int = 200):
        """Set a mock response for a specific request."""
        key = f"{method}:{path}"
        self.responses[key] = {"data": response, "status": status}
    
    def get(self, path: str, *, params: dict | None = None, **kwargs) -> Any:
        return self._request("GET", path, params=params)
    
    def post(self, path: str, *, json: dict | None = None, data: dict | None = None, **kwargs) -> Any:
        return self._request("POST", path, json=json, data=data)
    
    def delete(self, path: str, **kwargs) -> Any:
        return self._request("DELETE", path)
    
    def _request(self, method: str, path: str, json: dict | None = None, data: dict | None = None, **kwargs) -> Any:
        self.requests.append({"method": method, "path": path, "json": json, "data": data, **kwargs})
        
        key = f"{method}:{path}"
        if key in self.responses:
            resp = self.responses[key]
            if resp["status"] >= 400:
                self._raise_error(resp["status"], resp["data"])
            return resp["data"]
        
        # Check for pattern matches (e.g., /orders/123/view)
        for resp_key, resp in self.responses.items():
            resp_method, resp_path = resp_key.split(":", 1)
            if resp_method == method and self._path_matches(resp_path, path):
                if resp["status"] >= 400:
                    self._raise_error(resp["status"], resp["data"])
                return resp["data"]
        
        raise ValueError(f"No mock response for {method} {path}")
    
    def _path_matches(self, pattern: str, path: str) -> bool:
        """Simple pattern matching for paths with IDs."""
        pattern_parts = pattern.split("/")
        path_parts = path.split("/")
        if len(pattern_parts) != len(path_parts):
            return False
        for p, a in zip(pattern_parts, path_parts):
            if p.startswith("{") and p.endswith("}"):
                continue  # Wildcard
            if p != a:
                return False
        return True
    
    def _raise_error(self, status: int, data: dict):
        from zid.exceptions import (
            ZidAuthenticationError,
            ZidAuthorizationError,
            ZidNotFoundError,
            ZidValidationError,
            ZidRateLimitError,
            ZidServerError,
        )
        
        message = data.get("message", "Error")
        
        if status == 401:
            raise ZidAuthenticationError(message=message, body=data)
        elif status == 403:
            raise ZidAuthorizationError(message=message, body=data)
        elif status == 404:
            raise ZidNotFoundError(message=message, body=data)
        elif status in (400, 422):
            raise ZidValidationError(message=message, body=data)
        elif status == 429:
            raise ZidRateLimitError(message=message, body=data)
        elif status >= 500:
            raise ZidServerError(message=message, status_code=status, body=data)


@pytest.fixture
def mock_http():
    """Provide a mock HTTP client."""
    return MockHTTPClient()


# =============================================================================
# Fixtures for Models
# =============================================================================

@pytest.fixture
def customer_list_response():
    """Load customers list fixture."""
    return load_fixture("customers_list")


@pytest.fixture
def customer_detail_response():
    """Load customer detail fixture."""
    return load_fixture("customer_detail")


@pytest.fixture
def orders_list_response():
    """Load orders list fixture."""
    return load_fixture("orders_list")


@pytest.fixture
def orders_list_default_response():
    """Load orders list with default payload fixture."""
    return load_fixture("orders_list_default")


@pytest.fixture
def order_detail_response():
    """Load order detail fixture."""
    return load_fixture("order_detail")


@pytest.fixture
def coupons_list_response():
    """Load coupons list fixture."""
    return load_fixture("coupons_list")


@pytest.fixture
def coupon_detail_response():
    """Load coupon detail fixture."""
    return load_fixture("coupon_detail")


@pytest.fixture
def bundle_offers_list_response():
    """Load bundle offers list fixture."""
    return load_fixture("bundle_offers_list")


@pytest.fixture
def loyalty_program_response():
    """Load loyalty program fixture."""
    return load_fixture("loyalty_program")


@pytest.fixture
def loyalty_customer_response():
    """Load loyalty customer fixture."""
    return load_fixture("loyalty_customer")


# =============================================================================
# Error Response Fixtures
# =============================================================================

@pytest.fixture
def error_401():
    """Authentication error response."""
    return {
        "message": "Unauthenticated",
        "error_code": "ERROR_SESSION_INVALID",
    }


@pytest.fixture
def error_403():
    """Authorization error response."""
    return {
        "message": "Permission denied",
        "error_code": "ERROR_FORBIDDEN",
    }


@pytest.fixture
def error_404():
    """Not found error response."""
    return {
        "message": "Resource not found",
    }


@pytest.fixture
def error_422():
    """Validation error response."""
    return {
        "message": "Validation failed",
        "order_status": ["Invalid status value"],
    }


@pytest.fixture
def error_429():
    """Rate limit error response."""
    return {
        "message": "Too many requests",
    }


@pytest.fixture
def error_500():
    """Server error response."""
    return {
        "message": "Internal server error",
    }
