"""
Pydantic schemas for request/response bodies and DB models.

Add and expand fields as the DB schema becomes concrete.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class ArticleOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None


class RecommendRequest(BaseModel):
    user_id: str
    num_items: int = 10
    context: Optional[Dict[str, Any]] = None


class RecommendResponse(BaseModel):
    articles: List[ArticleOut]
    meta: Dict[str, Any]


class FeedbackIn(BaseModel):
    user_id: str
    article_id: int
    reward: float  # e.g. click=1, skip=0, like=1.0, partial=0.5
    metadata: Optional[Dict[str, Any]] = None


class FeedbackOut(BaseModel):
    success: bool
    message: Optional[str] = None
