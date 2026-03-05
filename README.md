# Zid Python SDK

A Python client for the [Zid](https://zid.sa) e-commerce platform API.

## Installation

```bash
pip install zid-client
```

Requires Python 3.10+.

## Quick Start

```python
from zid import ZidClient

# Initialize the client with your OAuth tokens
client = ZidClient(
    authorization="your-partner-token",
    store_token="store-access-token",
)

# List orders
for order in client.orders.list():
    print(order.id, order.order_status.code)

# Get a specific customer
customer = client.customers.get(12345)
print(customer.name, customer.email)
```

## Authentication

The SDK uses OAuth 2.0 tokens obtained through Zid's OAuth flow:

- `authorization`: Your partner/app token (the `Authorization` value from OAuth callback)
- `store_token`: Store-level access token (the `access_token` from OAuth callback)

### Basic Setup

```python
client = ZidClient(
    authorization="abc123...",
    store_token="xyz789...",
)
```

### With Automatic Token Refresh

Configure the client to automatically refresh expired tokens:

```python
def save_tokens(auth):
    """Persist new tokens to your database."""
    db.update_tokens(
        store_token=auth.store_token,
        refresh_token=auth.refresh_token,
        authorization=auth.authorization,
    )

client = ZidClient(
    authorization="abc123...",
    store_token="xyz789...",
    refresh_token="refresh-token",
    client_id="48",
    client_secret="your-secret",
    redirect_uri="https://yourapp.com/callback",
    on_tokens_refreshed=save_tokens,
)
```

When a request fails with 401, the SDK will automatically refresh tokens and retry.

## Features

- 13 resources, 50+ typed Pydantic models with full IDE autocomplete
- Composable sub-resources (e.g. `client.products.images`, `client.products.variants`)
- Automatic pagination across cursor-based and offset/limit APIs
- Auto token refresh with a callback to persist new credentials
- Retry with exponential backoff, jitter, and rate limit handling
- Dict-style access on models (`order["id"]` works alongside `order.id`)
- `.raw` property on every model to access undocumented API fields
- Automatic camelCase ↔ snake_case field mapping
- Lazy resource initialization — resources are created on first access

## Resources

### Products

```python
# List products
for product in client.products.list():
    print(product.id, product.name)

# CRUD
product = client.products.get("product-uuid")
product = client.products.create(name="Wireless Headphones", price=257, sku="WH-1000XM5")
product = client.products.update("product-uuid", price=79.99)
client.products.delete("product-uuid")

# Sub-resources
images = client.products.images.list("product-uuid")
client.products.images.upload("product-uuid", image=("photo.jpg", b"...", "image/jpeg"), alt_text="Front view")
client.products.variants.create("product-uuid", variants=[{"sku": "WH-BLK", "price": 257, "attributes": [...]}])
stocks = client.products.stocks.list("product-uuid")
categories = client.products.categories.list()
notifications = client.products.notifications.list(product_id="product-uuid")
```

### Orders

```python
# List orders (paginated, filterable)
for order in client.orders.list():
    print(order.id, order.order_status.code)

for order in client.orders.list(order_status="new", payload_type="default"):
    print(order.id, order.products)

# Get, update status, credit notes
order = client.orders.get(12345)
client.orders.update_status(12345, order_status="preparing")
credit_notes = client.orders.list_credit_notes(12345)

# Create a draft order (requires customer, consignee, products, shipping, payment)
order = client.orders.create(
    currency_code="SAR",
    customer={"full_name": "John Doe", "mobile_country_code": "966", "mobile_number": "500000000"},
    consignee={
        "contact": {"full_name": "John Doe", "mobile_country_code": "966", "mobile_number": "500000000"},
        "address": {"line_1": "King Fahd Road", "city_name": "Riyadh", "country_code": "SA"},
    },
    products=[{"sku": "PROD-SKU-123", "quantity": 1}],
    shipping_method={"type": "delivery", "id": 432480},
    payment_method={"id": 555224},
)
```

### Customers

```python
# List customers
for customer in client.customers.list():
    print(customer.name, customer.email)

# Get a specific customer
customer = client.customers.get(12345)
```

### Other Resources

| Resource | Accessor | Key Methods |
|---|---|---|
| Coupons | `client.coupons` | `list()`, `get(id)`, `create(...)`, `delete(id)` |
| Locations | `client.locations` | `list()`, `get(id)`, `create(...)`, `update(...)`, `update_stock(id, items)` |
| Abandoned Carts | `client.abandoned_carts` | `list()`, `get(cart_uuid)` |
| Reverse Orders | `client.reverse_orders` | `create(...)`, `list_reasons()`, `refund(...)`, `create_waybill(...)` |
| Delivery Options | `client.delivery_options` | `list()` |
| Payment Methods | `client.payment_methods` | `list()` |
| Store Profile | `client.stores` | `get_profile()`, `get_vat_settings()` |
| Geography | `client.geography` | `list_operating_countries()`, `list_all_countries()`, `list_cities(country_id)` |
| Webhooks | `client.webhooks` | `list()`, `create(event, target_url, original_id)`, `delete(original_id)` |
| Bundle Offers | `client.bundle_offers` | `list()` |
| Loyalty | `client.loyalty` | `get_status()`, `get_program()`, `get_customer_summary(customer_id)`, `adjust_customer_points(...)` |

All list methods return a `PaginatedIterator`. All resources have full docstrings — use your IDE's autocomplete or `help()` for parameter details.

## Pagination

List methods return a `PaginatedIterator` that handles pagination automatically:

```python
# Iterate through all pages transparently
for order in client.orders.list():
    print(order.id)

# Get total count without iterating
orders = client.orders.list()
print(f"Total orders: {len(orders)}")

# Control page size
for order in client.orders.list(per_page=100):
    print(order.id)

# Convenience methods
latest = client.orders.list(order_status="new").first()
top_5 = client.products.list().take(5)
all_customers = client.customers.list().to_list()
```

## Error Handling

The SDK raises specific exceptions for different error types:

```python
from zid import (
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

try:
    customer = client.customers.get(99999)
except ZidNotFoundError:
    print("Customer not found")
except ZidAuthenticationError as e:
    print(f"Auth failed: {e.error_code}")
except ZidRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except ZidValidationError as e:
    print(f"Validation errors: {e.errors}")
except ZidAPIError as e:
    print(f"API error {e.status_code}: {e.message}")
except ZidConnectionError:
    print("Network error")
```

### Exception Hierarchy

- `ZidError` — Base exception
  - `ZidAPIError` — API returned an error response
    - `ZidAuthenticationError` — 401 Unauthorized
    - `ZidAuthorizationError` — 403 Forbidden
    - `ZidNotFoundError` — 404 Not Found
    - `ZidValidationError` — 400/422 Validation errors
    - `ZidRateLimitError` — 429 Too Many Requests
    - `ZidServerError` — 5xx Server errors
  - `ZidConnectionError` — Network failures
  - `AuthError` — Invalid auth configuration
  - `TokenRefreshError` — Token refresh failed

## Context Manager

Use the client as a context manager to ensure proper cleanup:

```python
with ZidClient(authorization="...", store_token="...") as client:
    orders = list(client.orders.list())
# Connection is automatically closed
```

## Configuration

```python
client = ZidClient(
    authorization="...",
    store_token="...",
    base_url="https://api.zid.sa",  # Default
    timeout=30.0,                    # Request timeout in seconds
    language="en",                   # Accept-Language header (en/ar)
    auto_refresh=True,               # Auto-refresh tokens on 401
)
```

## Retry & Rate Limit Handling

The SDK automatically retries failed requests with exponential backoff:

```python
from zid import ZidClient, RetryConfig

# Default behavior: 3 retries with exponential backoff
client = ZidClient(authorization="...", store_token="...")

# Custom retry configuration
client = ZidClient(
    authorization="...",
    store_token="...",
    retry=RetryConfig(
        max_retries=5,              # Number of retry attempts
        base_delay=0.5,             # Initial delay (seconds)
        max_delay=30.0,             # Maximum delay between retries
        retry_on_rate_limit=True,   # Auto-wait on 429 responses
        max_rate_limit_wait=120.0,  # Max seconds to wait for rate limit
    ),
)

# Disable retries entirely
client = ZidClient(
    authorization="...",
    store_token="...",
    retry=RetryConfig(max_retries=0),
)
```

The retry logic handles:
- Server errors (500, 502, 503, 504) with exponential backoff + jitter
- Rate limits (429) by waiting for the `Retry-After` duration
- Connection errors and timeouts

## License

MIT