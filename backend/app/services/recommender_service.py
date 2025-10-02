"""
Recommendation business logic using the BanditAgent.
"""
from typing import List, Dict, Any

from app.models.bandit import get_bandit_agent
from app.db import crud


class RecommenderService:
    def __init__(self, arms=None, epsilon: float = 0.1):
        self.agent = get_bandit_agent(arms=arms, epsilon=epsilon)

    def recommend(self, user_id: str, num_items: int = 10, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Return a list of recommended article dicts.

        This simplistic implementation selects a category from the bandit, then
        returns up to `num_items` most recent articles that contain the category
        string in their title or source. Real implementation should use
        embeddings/contextual bandits and proper filtering.
        """
        category = self.agent.select_arm()
        candidates = crud.list_articles()
        # filter candidates by simple substring match
        filtered = [a for a in candidates if category.lower() in ((a.get("title") or "").lower() + (a.get("source") or "").lower())]
        # fallback: if not enough articles for the category, just return top N
        if len(filtered) < num_items:
            filtered = candidates[:num_items]
        else:
            filtered = filtered[:num_items]

        return filtered


# async wrapper used by API routes
async def recommend_for_user(user_id: str, num_items: int = 10, context: Dict[str, Any] = None):
    svc = RecommenderService()
    return svc.recommend(user_id=user_id, num_items=num_items, context=context)
