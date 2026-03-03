# Changelog

All notable changes to `zid-client` will be documented in this file.

## [0.1.0] - 2026-03-03

### Added
- Initial release of the Zid Python SDK
- `ZidClient` — main entry point with support for all resources
- Resources: Orders, Customers, Locations, Abandoned Carts, Reverse Orders,
  Delivery Options, Payment Methods, Stores, Geography, Webhooks,
  Coupons, Bundle Offers, Loyalty
- Automatic pagination via `PaginatedIterator` — iterate across pages transparently
- OAuth token auto-refresh on 401 responses
- Retry logic with exponential backoff and jitter for transient errors (5xx)
- Rate limit handling — auto-wait on 429 with `Retry-After` support
- Full type annotations with `py.typed` marker (PEP 561)
- Pydantic v2 models for all API responses
- Exception hierarchy: `ZidError`, `ZidAPIError`, `ZidAuthenticationError`,
  `ZidAuthorizationError`, `ZidNotFoundError`, `ZidValidationError`,
  `ZidRateLimitError`, `ZidServerError`, `ZidConnectionError`
- Context manager support (`with ZidClient(...) as client`)
- Python 3.10, 3.11, 3.12, 3.13 support
