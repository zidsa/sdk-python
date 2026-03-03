"""Webhooks resource for the Zid SDK."""

from __future__ import annotations

from typing import Any

from zid.models.webhook import Webhook, WebhookConditions
from zid.resources.base import BaseResource


class WebhooksResource(BaseResource):
    """Resource for managing webhook subscriptions.

    Webhooks allow you to receive real-time notifications
    when specific events occur in the store.
    """

    def list(self) -> list[Webhook]:
        """List all webhook subscriptions.

        Returns:
            List of webhook subscriptions.

        Example:
            ```python
            webhooks = client.webhooks.list()
            for webhook in webhooks:
                print(f"{webhook.event}: {webhook.target_url}")
            ```
        """
        response = self._get("/v1/managers/webhooks")
        data = response.get("data", [])
        return [Webhook.model_validate(item) for item in data]

    def create(
        self,
        event: str,
        target_url: str,
        original_id: str | int,
        conditions: WebhookConditions | dict[str, Any] | None = None,
    ) -> Webhook:
        """Create a new webhook subscription.

        Args:
            event: The event type to subscribe to (e.g., "order.create",
                "order.status.update", "category.create").
            target_url: The URL that will receive webhook payloads.
            original_id: Unique identifier for the app (App ID or MD5 hash).
            conditions: Optional conditions to filter events. Only applicable
                for "order.create" and "order.status.update" events.

        Returns:
            The created webhook subscription.

        Example:
            ```python
            webhook = client.webhooks.create(
                event="order.create",
                target_url="https://example.com/webhook",
                original_id="my-app-id",
            )
            print(f"Created webhook: {webhook.id}")

            # With conditions (for order events)
            webhook = client.webhooks.create(
                event="order.status.update",
                target_url="https://example.com/webhook",
                original_id="my-app-id",
                conditions={"status": "delivered"},
            )
            ```
        """
        payload: dict[str, Any] = {
            "event": event,
            "target_url": target_url,
            "original_id": original_id,
        }

        if conditions is not None:
            if isinstance(conditions, WebhookConditions):
                payload["conditions"] = conditions.model_dump(exclude_none=True)
            else:
                payload["conditions"] = conditions

        response = self._create("/v1/managers/webhooks", json=payload)
        return Webhook.model_validate(response)

    def delete(self, original_id: str | int) -> bool:
        """Delete a webhook subscription by original ID.

        Args:
            original_id: The original ID used when creating the webhook
                (App ID or MD5 hash).

        Returns:
            True if deletion was successful.

        Example:
            ```python
            success = client.webhooks.delete(original_id="my-app-id")
            if success:
                print("Webhook deleted")
            ```
        """
        self._delete("/v1/managers/webhooks", params={"original_id": str(original_id)})
        return True

    def delete_by_subscriber(self, subscriber: str) -> bool:
        """Delete all webhooks for a subscriber.

        Note: This endpoint is deprecated by Zid.

        Args:
            subscriber: The subscriber ID (MD5 hash assigned on creation).

        Returns:
            True if deletion was successful.

        Example:
            ```python
            success = client.webhooks.delete_by_subscriber(
                subscriber="your-subscriber-id-here"
            )
            if success:
                print("All webhooks for subscriber deleted")
            ```
        """
        self._delete(f"/v1/managers/webhooks/subscribers/{subscriber}")
        return True
