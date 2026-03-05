"""Product customizations sub-resource for the Zid SDK.

Manages custom option fields (checkbox/dropdown selectors) and custom
user input fields (free-text, number, etc.) on products.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from zid.models.product._customization import CustomInputField, CustomOption
from zid.resources.base import BaseResource

if TYPE_CHECKING:
    from zid.http import HTTPClient


class ProductCustomizationsSubResource(BaseResource):
    """Sub-resource for managing product customization fields.

    Provides methods to create and update custom option fields
    (checkbox/dropdown) and custom user input fields (text, number, etc.).

    Example:
        ```python
        client = ZidClient(authorization="token", store_token="store-token")

        # Create a custom option (dropdown/checkbox)
        option = client.products.customizations.create_option(
            "product-uuid",
            label={"ar": "خيار مخصص", "en": "Custom Option"},
            is_published=True,
            is_required=False,
            display_order=1,
            choices=[{"ar": "قيمة 1", "en": "Value 1", "price": 10}],
        )

        # Create a custom input field
        field = client.products.customizations.create_input_field(
            "product-uuid",
            type="TEXT",
            label={"ar": "نص مخصص", "en": "Custom Text"},
        )
        ```
    """

    token_header: str = "Access-Token"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the customizations sub-resource.

        Args:
            client: HTTP client for making API requests.
        """
        super().__init__(client)

    def create_option(
        self,
        product_id: str,
        *,
        label: dict[str, str],
        is_published: bool,
        is_required: bool,
        display_order: int,
        choices: list[dict[str, Any]],
        hint: dict[str, str] | None = None,
        type: str | None = None,
        min_choices: int | None = None,
        max_choices: int | None = None,
        can_choose_multiple_options: bool | None = None,
    ) -> CustomOption:
        """Create a custom option field on a product.

        Custom options present customers with predefined choices
        (checkbox or dropdown) during purchase. Each choice can
        carry an additional price.

        Args:
            product_id: The unique identifier (UUID) of the product.
            label: Localized display name (``{"ar": "...", "en": "..."}``).
            is_published: Whether the option is visible to customers.
            is_required: Whether the customer must select a choice.
            display_order: Position relative to other custom options.
            choices: List of choice dicts, each with ``ar``, ``en``,
                and optional ``price`` keys.
            hint: Localized hint/tooltip text (``{"ar": "...", "en": "..."}``).
            type: Option type (``"CHECKBOX"`` or ``"DROPDOWN"``). Auto-determined
                from ``can_choose_multiple_options`` if omitted.
            min_choices: Minimum number of choices the customer must select.
            max_choices: Maximum number of choices the customer can select.
            can_choose_multiple_options: If ``True``, type is CHECKBOX;
                if ``False``, type is DROPDOWN. Defaults to ``True``.

        Returns:
            The newly created CustomOption instance.

        Raises:
            ZidValidationError: If required fields are missing or invalid.

        Example:
            ```python
            option = client.products.customizations.create_option(
                "product-uuid",
                label={"ar": "خيار مخصص", "en": "Custom Option"},
                hint={"ar": "اختر", "en": "Choose"},
                is_published=True,
                is_required=True,
                display_order=2,
                choices=[
                    {"ar": "قيمة 1", "en": "Value 1", "price": 66.5},
                    {"ar": "قيمة 2", "en": "Value 2", "price": 0},
                ],
                can_choose_multiple_options=True,
                min_choices=1,
                max_choices=100,
            )
            print(option.id, option.type)
            ```
        """
        data: dict[str, Any] = {
            "label": label,
            "is_published": is_published,
            "is_required": is_required,
            "display_order": display_order,
            "choices": choices,
        }
        if hint is not None:
            data["hint"] = hint
        if type is not None:
            data["type"] = type
        if min_choices is not None:
            data["min_choices"] = min_choices
        if max_choices is not None:
            data["max_choices"] = max_choices
        if can_choose_multiple_options is not None:
            data["can_choose_multiple_options"] = can_choose_multiple_options

        path = f"/v1/products/{product_id}/custom_options_fields/"
        response = self._create(path, json=data)
        return CustomOption.model_validate(response)

    def update_option(
        self,
        product_id: str,
        field_id: str,
        *,
        label: dict[str, str],
        is_published: bool,
        is_required: bool,
        display_order: int,
        choices: list[dict[str, Any]],
        hint: dict[str, str] | None = None,
        type: str | None = None,
        min_choices: int | None = None,
        max_choices: int | None = None,
        can_choose_multiple_options: bool | None = None,
    ) -> CustomOption:
        """Update an existing custom option field.

        Replaces the option's data entirely with the new payload.

        Args:
            product_id: The unique identifier (UUID) of the product.
            field_id: The unique identifier (UUID) of the custom option field.
            label: Localized display name (``{"ar": "...", "en": "..."}``).
            is_published: Whether the option is visible to customers.
            is_required: Whether the customer must select a choice.
            display_order: Position relative to other custom options.
            choices: List of choice dicts, each with ``ar``, ``en``,
                and optional ``price`` and ``id`` keys.
            hint: Localized hint/tooltip text (``{"ar": "...", "en": "..."}``).
            type: Option type (``"CHECKBOX"`` or ``"DROPDOWN"``).
            min_choices: Minimum number of choices the customer must select.
            max_choices: Maximum number of choices the customer can select.
            can_choose_multiple_options: If ``True``, type is CHECKBOX;
                if ``False``, type is DROPDOWN.

        Returns:
            The updated CustomOption instance.

        Raises:
            ZidNotFoundError: If the product or option field does not exist.
            ZidValidationError: If the payload is invalid.

        Example:
            ```python
            option = client.products.customizations.update_option(
                "product-uuid",
                "option-field-uuid",
                label={"ar": "خيار محدث", "en": "Updated Option"},
                is_published=True,
                is_required=False,
                display_order=4,
                choices=[
                    {"ar": "قيمة 1", "en": "Value 1", "price": 66.5,
                     "id": "choice-uuid"},
                ],
            )
            ```
        """
        data: dict[str, Any] = {
            "label": label,
            "is_published": is_published,
            "is_required": is_required,
            "display_order": display_order,
            "choices": choices,
        }
        if hint is not None:
            data["hint"] = hint
        if type is not None:
            data["type"] = type
        if min_choices is not None:
            data["min_choices"] = min_choices
        if max_choices is not None:
            data["max_choices"] = max_choices
        if can_choose_multiple_options is not None:
            data["can_choose_multiple_options"] = can_choose_multiple_options

        path = f"/v1/products/{product_id}/custom_options_fields/{field_id}/"
        response = self._update(path, json=data, method="PUT")
        return CustomOption.model_validate(response)

    def delete_option(self, product_id: str, field_id: str) -> None:
        """Delete a custom option field from a product.

        Args:
            product_id: The unique identifier (UUID) of the product.
            field_id: The unique identifier (UUID) of the custom option field.

        Returns:
            None (HTTP 204 on success).

        Raises:
            ZidNotFoundError: If the product or option field does not exist.

        Example:
            ```python
            client.products.customizations.delete_option(
                "product-uuid",
                "option-field-uuid",
            )
            ```
        """
        path = f"/v1/products/{product_id}/custom_options_fields/{field_id}/"
        self._delete(path)

    def create_input_field(
        self,
        product_id: str,
        *,
        type: str,
        label: dict[str, str],
        hint: dict[str, str] | None = None,
        price: str | None = None,
    ) -> CustomInputField:
        """Create a custom user input field on a product.

        Input fields collect free-form data from customers at purchase
        time (e.g., engraving text, gift message, special instructions).

        Args:
            product_id: The unique identifier (UUID) of the product.
            type: Input field type (e.g., ``"TEXT"``).
            label: Localized field label (``{"ar": "...", "en": "..."}``).
            hint: Localized hint/helper text (``{"ar": "...", "en": "..."}``).
            price: Price associated with this input field (e.g., ``"100.00"``).

        Returns:
            The newly created CustomInputField instance.

        Raises:
            ZidValidationError: If required fields are missing or invalid.

        Example:
            ```python
            field = client.products.customizations.create_input_field(
                "product-uuid",
                type="TEXT",
                label={"ar": "نص مخصص", "en": "Custom Text"},
                hint={"ar": "أدخل النص", "en": "Enter text"},
                price="100.00",
            )
            print(field.id, field.type)
            ```
        """
        data: dict[str, Any] = {
            "type": type,
            "label": label,
        }
        if hint is not None:
            data["hint"] = hint
        if price is not None:
            data["price"] = price

        path = f"/v1/products/{product_id}/custom_user_input_fields/"
        response = self._create(path, json=data)
        return CustomInputField.model_validate(response)
