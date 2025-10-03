"""
Feedback routes: receive user feedback (clicks, likes, skips) used to update
bandit/learning components.

Endpoints:
- POST / to submit feedback for an article shown to a user
- GET /stats to retrieve feedback statistics

Next steps: implement services.feedback_service.process_feedback to update
bandit state and persist feedback to DB.
"""
from fastapi import APIRouter, HTTPException

from app.models.schemas import FeedbackIn, FeedbackOut
from app.services.feedback_service import process_feedback
from app.db import crud

router = APIRouter()


@router.post("/", response_model=FeedbackOut)
async def submit_feedback(payload: FeedbackIn):
    """Receive feedback events from the frontend and update bandit state."""
    try:
        summary = await process_feedback(payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process feedback")

    return FeedbackOut(success=True, message=f"Updated bandit arm {summary.get('updated_arm')}")


@router.get('/stats')
async def feedback_stats():
    """Retrieve feedback statistics."""
    try:
        stats = crud.get_feedback_stats()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch feedback stats")
    return stats
