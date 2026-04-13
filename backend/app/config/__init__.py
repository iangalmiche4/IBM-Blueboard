"""
Configuration package
"""

from app.config.api import DEFAULT_LIMIT, DEFAULT_SKIP, MAX_LIMIT, MIN_LIMIT
from app.config.settings import settings

__all__ = ["DEFAULT_LIMIT", "DEFAULT_SKIP", "MAX_LIMIT", "MIN_LIMIT", "settings"]
