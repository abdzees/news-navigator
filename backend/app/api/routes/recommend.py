"""
Recommendation routes: return personalized article lists.

Endpoints:
- POST / to request a personalized batch of recommended articles for a user

Next steps: wire to services.recommender_service.recommend_for_user
"""
from fastapi import APIRouter
from typing import Dict, Any

from app.models.schemas import RecommendRequest, RecommendResponse

router = APIRouter()


@router.post("/", response_model=RecommendResponse)
async def recommend(payload: RecommendRequest):
    """Return recommended articles for the requesting user (placeholder)."""
    # TODO: use services.recommender_service.recommend_for_user(payload.user_id, ...)
    return RecommendResponse(articles=[], meta={})
