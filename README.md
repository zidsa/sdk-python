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
    authorization="Bearer abc123...",
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
    authorization="Bearer abc123...",
    store_token="xyz789...",
    refresh_token="refresh-token",
    client_id="48",
    client_secret="your-secret",
    redirect_uri="https://yourapp.com/callback",
    on_tokens_refreshed=save_tokens,
)
```

When a request fails with 401, the SDK will automatically refresh tokens and retry.

## Resources

### Orders

```python
# List orders (paginated)
for order in client.orders.list():
    print(order.id, order.order_status.code)

# Filter by status
for order in client.orders.list(order_status="new"):
    print(order.id)

# Get full order details with products
for order in client.orders.list(payload_type="default"):
    print(order.products)

# Get a specific order
order = client.orders.get(12345)

# Update order status
client.orders.update_status(12345, order_status="preparing")

# Get credit notes
credit_notes = client.orders.list_credit_notes(12345)
```

### Customers

```python
# List customers
for customer in client.customers.list():
    print(customer.name, customer.email)

# Get a specific customer
customer = client.customers.get(12345)
```

### Locations (Multi-Inventory)

```python
# List inventory locations
for location in client.locations.list():
    print(location.name, location.is_default)

# Get a specific location
location = client.locations.get("location-uuid")

# Create a location
location = client.locations.create(
    name="Warehouse 2",
    city_id=123,
    address="123 Main St",
)

# Update stock
client.locations.update_stock(
    location_id="location-uuid",
    products=[{"product_id": 1, "quantity": 100}],
)
```

### Abandoned Carts

```python
# List abandoned carts
for cart in client.abandoned_carts.list():
    print(cart.id, cart.customer_name)

# Get cart details
cart = client.abandoned_carts.get(12345)
```

### Reverse Orders (Returns/Refunds)

```python
# List return reasons
reasons = client.reverse_orders.list_reasons()

# Create a reverse order
reverse = client.reverse_orders.create(
    order_id=12345,
    products=[{"product_id": 1, "quantity": 1}],
)
```

### Delivery Options

```python
# List delivery options
for option in client.delivery_options.list():
    print(option.id, option.name)
```

### Payment Methods

```python
# List payment methods
methods = client.payment_methods.list()
for method in methods:
    print(method.code, method.name)
```

### Store Profile

```python
# Get store profile
profile = client.stores.get_profile()
print(profile.store.name)

# Get VAT settings
vat = client.stores.get_vat_settings()
```

### Geography (Countries & Cities)

```python
# List countries where store operates
countries = client.geography.list_operating()

# List all countries
for country in client.geography.list_all():
    print(country.name)

# List cities by country
cities = client.geography.list_by_country(country_id=1)
```

### Webhooks

```python
# List webhooks
webhooks = client.webhooks.list()

# Create a webhook
webhook = client.webhooks.create(
    event="order.create",
    target_url="https://example.com/webhook",
    original_id="my-app-id",
)

# Delete a webhook
client.webhooks.delete(original_id="my-app-id")
```

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
        base_delay=1.0,             # Initial delay (seconds)
        max_delay=60.0,             # Maximum delay between retries
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