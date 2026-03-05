"""Products resource package for the Zid SDK.

Exports the main ProductsResource class which provides core product CRUD
and acts as the entry point for product sub-resources.
"""

from zid.resources.products._base import ProductsResource

__all__ = [
    "ProductsResource",
]

# Sub-resources will be wired here
