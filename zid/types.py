"""Shared type definitions for the Zid SDK."""

from typing import Any, Protocol, TypeVar, runtime_checkable

__all__ = [
    "JSONDict",
    "Headers",
    "QueryParams",
    "ModelT",
    "Serializable",
    "Deserializable",
    "OptionalStr",
    "OptionalInt",
    "OptionalFloat",
    "OptionalBool",
]

# Type aliases for common structures
JSONDict = dict[str, Any]
"""A dictionary representing JSON data."""

Headers = dict[str, str]
"""HTTP headers dictionary."""

QueryParams = dict[str, str | int | float | bool | None]
"""Query parameters for HTTP requests."""

# TypeVar for generic model typing
ModelT = TypeVar("ModelT")
"""Generic type variable for model classes."""


@runtime_checkable
class Serializable(Protocol):
    """Protocol for objects that can be serialized to a dictionary."""

    def model_dump(self, *, exclude_unset: bool = False) -> JSONDict:
        """Serialize the model to a dictionary."""
        ...


@runtime_checkable
class Deserializable(Protocol):
    """Protocol for objects that can be deserialized from a dictionary."""

    @classmethod
    def model_validate(cls, data: JSONDict) -> "Deserializable":
        """Deserialize a dictionary to a model instance."""
        ...


# Optional field handling
OptionalStr = str | None
OptionalInt = int | None
OptionalFloat = float | None
OptionalBool = bool | None
