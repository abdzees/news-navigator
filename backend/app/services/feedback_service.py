"""
Feedback processing service.

This implementation stores feedback in the DB (via db.crud) and updates the
BanditAgent estimates. The mapping from article_id -> category is naive and
should be replaced with a proper metadata-driven mapping.
"""
from typing import Dict, Any

from app.db import crud
from app.models.bandit import get_bandit_agent


async def process_feedback(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process a feedback event with keys: user_id, article_id, reward, metadata.

    Returns a small policy summary including the updated estimated values.
    """
    user_id = event.get("user_id")
    article_id = event.get("article_id")
    reward = float(event.get("reward", 0.0))
    metadata = event.get("metadata")

    if not user_id or article_id is None:
        raise ValueError("user_id and article_id are required in feedback event")

    # persist feedback
    crud.insert_feedback(user_id=user_id, article_id=article_id, reward=reward, metadata=str(metadata) if metadata else None)

    # Map article to a category for bandit update. This is a naive approach:
    # try reading metadata['category'], else fall back to simple mapping.
    category = None
    if isinstance(metadata, dict):
        category = metadata.get("category")

    if not category:
        # simple heuristic: map common keywords to arms
        # In real system, the article row should have a category field.
        art = None
        try:
            art = crud.get_article(article_id)
        except Exception:
            art = None
        title = (art.get("title") if art else "") or ""
        title_l = title.lower()
        for arm in ["technology", "business", "politics", "sports", "science", "health", "entertainment"]:
            if arm in title_l:
                category = arm
                break
    if not category:
        # default to 'general' if nothing matches
        category = "general"

    # update bandit
    agent = get_bandit_agent()
    agent.update(category, reward)

    # return policy summary
    return {"updated_arm": category, "estimates": agent.values}
