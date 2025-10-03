"""
Recommendation routes: return personalized article lists.

Endpoints:
- POST / to request a personalized batch of recommended articles for a user

Next steps: wire to services.recommender_service.recommend_for_user
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.models.schemas import RecommendRequest, RecommendResponse
from app.services.recommender_service import recommend_for_user

router = APIRouter()


@router.post("/", response_model=RecommendResponse)
async def recommend(payload: RecommendRequest):
    """Return recommended articles for the requesting user."""
    try:
        articles = await recommend_for_user(payload.user_id, num_items=payload.num_items, context=payload.context)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")
    return RecommendResponse(articles=articles, meta={"num_returned": len(articles)})
