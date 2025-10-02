"""
Articles routes: fetching and listing articles.

Placeholder endpoints are provided for:
- GET / to list cached/latest articles
- GET /{article_id} to retrieve a single article

Next steps: integrate with services/news_service.py to fetch and cache articles
from NewsAPI and persist them via db.crud.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import ArticleOut
from app.services.news_service import get_news_service

router = APIRouter()


@router.get("/", response_model=List[ArticleOut])
async def list_articles(category: Optional[str] = Query(None, description="Category name or free-text query"), page_size: int = Query(20, ge=1, le=100)):
    """Return a list of recent articles fetched from NewsAPI.

    If no API key is configured the service returns an empty list. Articles are
    mapped to the ArticleOut schema and assigned synthetic IDs (position in the
    returned list). Persisting articles to the DB and stable IDs will be added
    in a later stage.
    """
    service = get_news_service()
    articles = await service.fetch_articles(category or "", page_size)

    results: List[ArticleOut] = []
    for i, a in enumerate(articles):
        source = None
        src = a.get("source")
        if isinstance(src, dict):
            source = src.get("name")
        results.append(ArticleOut(
            id=i + 1,
            title=a.get("title") or "",
            description=a.get("description"),
            url=a.get("url"),
            source=source,
        ))

    return results


@router.get("/{article_id}", response_model=ArticleOut)
async def get_article(article_id: int):
    """Return a single article by id (placeholder)."""
    # TODO: fetch from db.crud.get_article(article_id)
    raise HTTPException(status_code=404, detail="Article not found")
