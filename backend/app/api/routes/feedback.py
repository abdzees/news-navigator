"""
Feedback routes: receive user feedback (clicks, likes, skips) used to update
bandit/learning components.

Endpoints:
- POST / to submit feedback for an article shown to a user

Next steps: implement services.feedback_service.process_feedback to update
bandit state and persist feedback to DB.
"""
from fastapi import APIRouter

from app.models.schemas import FeedbackIn, FeedbackOut

router = APIRouter()


@router.post("/", response_model=FeedbackOut)
async def submit_feedback(payload: FeedbackIn):
    """Receive feedback events from the frontend (placeholder)."""
    # TODO: call services.feedback_service.process_feedback(payload)
    return FeedbackOut(success=True)
