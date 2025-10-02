"""
News fetching service.

This module encapsulates calls to NewsAPI (or other sources), simple caching
and insertion into the DB via db.crud in future iterations.
"""
from typing import List, Dict, Any, Optional, Tuple
import os
import time
import asyncio
import requests


class NewsService:
    """Simple NewsAPI client with in-memory caching.

    - Loads API key from the environment variable NEWSAPI_KEY.
    - Provides an async fetch_articles method that uses requests in a thread
      to avoid blocking the event loop.
    - Caches results in-memory with a TTL to reduce external calls.
    """

    BASE_URL = "https://newsapi.org/v2/top-headlines"

    def __init__(self, api_key: Optional[str] = None, cache_ttl: int = 300):
        self.api_key = api_key or os.environ.get("NEWSAPI_KEY")
        self.cache_ttl = cache_ttl
        # cache: key -> (timestamp, data)
        self._cache: Dict[Tuple[str, int], Tuple[float, List[Dict[str, Any]]]] = {}

    def _cache_key(self, category: str, page_size: int) -> Tuple[str, int]:
        return (category or "", page_size)

    def _is_cached(self, key: Tuple[str, int]) -> bool:
        entry = self._cache.get(key)
        if not entry:
            return False
        ts, _ = entry
        return (time.time() - ts) < self.cache_ttl

    async def fetch_articles(self, category: str = "", page_size: int = 20) -> List[Dict[str, Any]]:
        """Fetch top headlines from NewsAPI for a category or free-text query.

        This method is async but runs the blocking HTTP request in a thread.
        Returns a list of article dicts as returned by NewsAPI.
        """
        if not self.api_key:
            # No API key configured — return empty list and let caller decide how to handle
            return []

        key = self._cache_key(category, page_size)
        if self._is_cached(key):
            return self._cache[key][1]

        params = {"apiKey": self.api_key, "pageSize": page_size}
        # If category looks like a general term, map to q; else use category param
        if category:
            # NewsAPI supports both 'category' (like business, sports) and 'q' for search.
            # We'll use 'q' for general queries and 'category' for recognized categories.
            recognized_categories = {"business", "entertainment", "general", "health", "science", "sports", "technology"}
            if category.lower() in recognized_categories:
                params["category"] = category.lower()
            else:
                params["q"] = category

        # Run blocking request in thread
        try:
            resp = await asyncio.to_thread(requests.get, self.BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            articles = data.get("articles", []) if isinstance(data, dict) else []
        except Exception:
            # On any error, return empty list. Caller can raise HTTP errors if desired.
            articles = []

        # Cache and return
        self._cache[key] = (time.time(), articles)
        return articles


# module-level singleton for convenience
_default_service: Optional[NewsService] = None


def get_news_service() -> NewsService:
    global _default_service
    if _default_service is None:
        _default_service = NewsService()
    return _default_service
