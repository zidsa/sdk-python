"""Product notifications sub-resource for the Zid SDK.

Manages availability notifications — customers subscribing to be
notified when out-of-stock products become available again.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.product._notification import (
    NotificationSettings,
    NotificationStats,
    ProductNotification,
)
from zid.pagination import PaginatedIterator
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class ProductNotificationsSubResource(BaseResource):
    """Sub-resource for managing product availability notifications.

    Provides methods to list, create, and manage notifications that
    alert customers when out-of-stock products become available.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all notifications
        for notification in client.products.notifications.list():
            print(notification.customer.email, notification.is_notified)

        # Get notification stats
        stats = client.products.notifications.get_stats()
        print(stats.total_count, stats.purchased_count)

        # Get notification settings
        settings = client.products.notifications.get_settings()
        print(settings.delay_unit, settings.delay_value)
        ```
    """

    token_header: str = "Access-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the notifications sub-resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)
        self._base_path = "/v1/products/notifications"

    def list(
        self,
        *,
        q: str | None = None,
        product_id: str | None = None,
        created_at__gte: str | None = None,
        created_at__lte: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        **kwargs: Any,
    ) -> PaginatedIterator[ProductNotification]:
        """List availability notifications with pagination and filtering.

        Args:
            q: Search by product name (partial or full match).
            product_id: Filter by product UUID.
            created_at__gte: Include notifications created on or after
                this datetime (ISO 8601 format).
            created_at__lte: Include notifications created on or before
                this datetime (ISO 8601 format).
            page: Page number (1-indexed).
            page_size: Number of items per page.
            **kwargs: Additional query parameters.

        Returns:
            Paginated iterator yielding ProductNotification instances.

        Example:
            ```python
            # List all notifications for a specific product
            for n in client.products.notifications.list(
                product_id="a7ad89d0-03e2-430f-b6e4-0624ef05e571",
            ):
                print(n.customer.name, n.is_notified)

            # Filter by date range
            for n in client.products.notifications.list(
                created_at__gte="2026-01-01T00:00:00Z",
                created_at__lte="2026-12-31T23:59:59Z",
            ):
                print(n.created_at)
            ```
        """
        params: dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if product_id is not None:
            params["product_id"] = product_id
        if created_at__gte is not None:
            params["created_at__gte"] = created_at__gte
        if created_at__lte is not None:
            params["created_at__lte"] = created_at__lte
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        params.update(kwargs)

        return self._list(
            f"{self._base_path}/",
            ProductNotification.model_validate,
            params=params if params else None,
            results_key="results",
        )

    def get_stats(self) -> NotificationStats:
        """Retrieve statistics on availability notifications.

        Returns:
            NotificationStats with total, notified, purchased counts
            and total purchase value.

        Example:
            ```python
            stats = client.products.notifications.get_stats()
            print(f"Total: {stats.total_count}")
            print(f"Notified: {stats.notified_count}")
            print(f"Purchased: {stats.purchased_count}")
            print(f"Revenue: {stats.purchased_total}")
            ```
        """
        response = self._get(f"{self._base_path}/stats/")
        return NotificationStats.model_validate(response)

    def get_settings(self) -> NotificationSettings:
        """Retrieve current settings for availability notifications.

        Returns:
            NotificationSettings with delay, email template, and coupon
            configuration.

        Example:
            ```python
            settings = client.products.notifications.get_settings()
            print(settings.delay_unit, settings.delay_value)
            print(settings.email_title.en)
            ```
        """
        response = self._get(f"{self._base_path}/settings/")
        return NotificationSettings.model_validate(response["settings"])

    def update_settings(
        self,
        *,
        delay_unit: str | None = None,
        delay_value: int | None = None,
        email_text: dict[str, str] | None = None,
        email_title: dict[str, str] | None = None,
    ) -> None:
        """Save settings for availability notifications.

        Args:
            delay_unit: Time unit for notification delay
                (``"minute"``, ``"hour"``, or ``"day"``).
            delay_value: Delay value before sending the notification.
            email_text: Localized email body template
                (``{"ar": "...", "en": "..."}``). Supports placeholders:
                ``{customer_name}``, ``{product_name}``, ``{product_url}``.
            email_title: Localized email subject template
                (``{"ar": "...", "en": "..."}``). Supports placeholders:
                ``{product_name}``, ``{store_name}``.

        Returns:
            None (HTTP 201 on success).

        Example:
            ```python
            client.products.notifications.update_settings(
                delay_unit="hour",
                delay_value=2,
                email_title={"ar": "المنتج متوفر", "en": "Product available"},
                email_text={
                    "ar": "عزيزنا {customer_name}، {product_name} متوفر الآن",
                    "en": "Dear {customer_name}, {product_name} is back in stock",
                },
            )
            ```
        """
        data: dict[str, Any] = {}
        if delay_unit is not None:
            data["delay_unit"] = delay_unit
        if delay_value is not None:
            data["delay_value"] = delay_value
        if email_text is not None:
            data["email_text"] = email_text
        if email_title is not None:
            data["email_title"] = email_title

        self._create(f"{self._base_path}/settings/", json=data)

    def create(
        self,
        product_id: str,
        *,
        email: str,
        language: str | None = None,
        name: str | None = None,
        phone: str | None = None,
        customer_id: str | None = None,
        customer_phone_number: str | None = None,
        customer_name: str | None = None,
    ) -> None:
        """Subscribe to an availability notification for a product.

        Signs up a customer to receive an email when the specified
        product becomes available again.

        Args:
            product_id: The unique identifier (UUID) of the product.
            email: Email address of the customer (required).
            language: Language preference (``"ar"`` or ``"en"``).
            name: Name of the subscriber.
            phone: Phone number of the subscriber.
            customer_id: ID of an existing customer.
            customer_phone_number: Phone number of the customer.
            customer_name: Name of the customer.

        Returns:
            None (HTTP 201 on success).

        Raises:
            ZidNotFoundError: If the product does not exist.
            ZidValidationError: If required fields are missing.

        Example:
            ```python
            client.products.notifications.create(
                "a7ad89d0-03e2-430f-b6e4-0624ef05e571",
                email="customer@example.com",
                language="en",
                customer_name="John Doe",
            )
            ```
        """
        data: dict[str, Any] = {"email": email}
        if language is not None:
            data["language"] = language
        if name is not None:
            data["name"] = name
        if phone is not None:
            data["phone"] = phone
        if customer_id is not None:
            data["customer_id"] = customer_id
        if customer_phone_number is not None:
            data["customer_phone_number"] = customer_phone_number
        if customer_name is not None:
            data["customer_name"] = customer_name

        self._client.post(
            f"/v1/products/{product_id}/notifications/",
            data=data,
            token_header=self.token_header,
        )

    def send_email(
        self,
        *,
        email: str,
        customer_name: str,
        product_id: str,
        method: str,
        language: str | None = None,
        content: str | None = None,
        title: str | None = None,
    ) -> None:
        """Manually send an availability notification email.

        Args:
            email: Email address of the recipient.
            customer_name: Name of the customer.
            product_id: UUID of the product.
            method: Notification method (e.g., ``"email"``).
            language: Language preference (``"ar"`` or ``"en"``).
            content: Email body content.
            title: Email subject/title.

        Returns:
            None (HTTP 201 on success).

        Raises:
            ZidValidationError: If required fields are missing.

        Example:
            ```python
            client.products.notifications.send_email(
                email="customer@example.com",
                customer_name="John Doe",
                product_id="554da609-2f14-427f-9ca5-298d9dea5c1b",
                method="email",
                language="en",
                title="Product Available",
                content="Your product is back in stock!",
            )
            ```
        """
        data: dict[str, Any] = {
            "email": email,
            "customer_name": customer_name,
            "product_id": product_id,
            "method": method,
        }
        if language is not None:
            data["language"] = language
        if content is not None:
            data["content"] = content
        if title is not None:
            data["title"] = title

        self._client.post(
            f"{self._base_path}/send/",
            data=data,
            token_header=self.token_header,
        )

    def export(
        self,
        *,
        email: str,
        is_notified: bool,
    ) -> None:
        """Export availability notifications data.

        Args:
            email: Email address of the customer to filter by.
            is_notified: Filter by notification status.

        Returns:
            None (HTTP 204 on success).

        Example:
            ```python
            client.products.notifications.export(
                email="customer@example.com",
                is_notified=True,
            )
            ```
        """
        data: dict[str, Any] = {
            "email": email,
            "is_notified": is_notified,
        }

        self._client.post(
            f"{self._base_path}/export/",
            data=data,
            token_header=self.token_header,
        )
