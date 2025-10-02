"""
Utility helpers used across the application.

Add functions for text normalization, caching helpers, and any small utilities
that are useful in multiple modules.
"""
from typing import Any


def safe_get(d: dict, key: str, default: Any = None):
    """Safe dictionary access helper."""
    return d.get(key, default)
