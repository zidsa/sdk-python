"""Base model class for all Zid SDK models."""

from types import UnionType
from typing import Any, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, model_validator
from pydantic.alias_generators import to_camel

__all__ = ["BaseModel"]


def _expects_list(type_hint: Any) -> bool:
    """Check if a type annotation expects a list value."""
    origin = get_origin(type_hint)
    if origin is list:
        return True
    if origin in (Union, UnionType):
        # Check union members (e.g., list[X] | None)
        return any(_expects_list(arg) for arg in get_args(type_hint) if arg is not type(None))
    return False


class BaseModel(PydanticBaseModel):
    """Base model with common configuration for all Zid SDK models.

    Features:
    - Automatic snake_case to camelCase alias generation
    - Extra fields are preserved (access via .raw property)
    - Supports both attribute access (model.field) and dict-style access (model["field"])
    - Validates by field name and alias
    - Concise __repr__ for readable debugging
    - Smart empty list handling (coerces [] to None only for non-list fields)
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="allow",  # Preserve extra fields for .raw access
        from_attributes=True,
        ser_json_timedelta="iso8601",
        validate_default=True,
    )

    @model_validator(mode="before")
    @classmethod
    def _coerce_empty_lists_to_none(cls, data: Any) -> Any:
        """Coerce empty lists to None only for fields that expect objects.

        The Zid API returns [] instead of null for some optional nested objects.
        This converts [] to None only when the field expects an object, preserving
        empty lists for fields that actually expect list types.
        """
        if not isinstance(data, dict):
            return data

        data = data.copy()  # This so we don't muatate the origian input.
        hints = get_type_hints(cls)
        for key, value in data.items():
            if value == [] and key in hints and not _expects_list(hints[key]):
                data[key] = None

        return data

    @property
    def raw(self) -> dict[str, Any]:
        """Access extra fields from the API response not defined in the model.

        Returns:
            Dictionary of extra fields returned by the API.

        Example:
            >>> order.raw["some_undocumented_field"]
        """
        return self.model_extra or {}

    def __getitem__(self, key: str) -> Any:
        """Enable dict-style access to model fields.

        Args:
            key: Field name (snake_case)

        Returns:
            The field value

        Raises:
            KeyError: If the field does not exist
        """
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def __repr__(self) -> str:
        """Concise repr showing key identifiers only."""
        id_fields = ["id", "code", "name", "invoice_number", "sku"]
        parts = []
        for field in id_fields:
            val = getattr(self, field, None)
            if val is not None:
                parts.append(f"{field}={val!r}")
        # Fallback: show first 3 non-None fields
        if not parts:
            for key, val in self.model_dump(exclude_none=True).items():
                if len(parts) >= 3:
                    break
                if not isinstance(val, (dict, list)):
                    parts.append(f"{key}={val!r}")
        return f"{self.__class__.__name__}({', '.join(parts)})"

