"""
API routes package initializer.

This package exposes the route modules so they can be included in the main app.
"""
from . import articles, recommend, feedback

__all__ = ["articles", "recommend", "feedback"]
