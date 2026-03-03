"""Payment methods resource for the Zid SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING

from zid.models.payment_method import PaymentMethod
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class PaymentMethodsResource(BaseResource):
    """Resource for retrieving store payment methods.

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # List all payment methods
        methods = client.payment_methods.list()
        for method in methods:
            print(f"{method.name}: {method.code} (enabled={method.enabled})")
        ```
    """

    token_header: str = "X-Manager-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the payment methods resource."""
        super().__init__(client)
        self._base_path = "/v1/managers/store/payment-methods"

    def list(self) -> list[PaymentMethod]:
        """List all payment methods for the store.

        Returns:
            List of PaymentMethod instances.

        Example:
            ```python
            methods = client.payment_methods.list()
            for method in methods:
                status = "enabled" if method.enabled else "disabled"
                print(f"{method.name} ({status})")
            ```
        """
        response = self._get(self._base_path)
        # Response structure: {"code": "...", "payload": [...]}
        payload = response.get("payload", [])
        return [PaymentMethod.model_validate(item) for item in payload]
