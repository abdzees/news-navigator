import os
import requests

API_URL = os.environ.get('API_URL', 'http://127.0.0.1:8000/api')


def fetch_articles(query: str):
    try:
        r = requests.get(f"{API_URL}/articles", params={"category": query})
        r.raise_for_status()
        return r.json()
    except Exception:
        return []


def recommend_for_user(user_id: str, num_items: int = 10):
    try:
        payload = {"user_id": user_id, "num_items": num_items}
        r = requests.post(f"{API_URL}/recommend", json=payload)
        r.raise_for_status()
        return r.json().get('articles', [])
    except Exception:
        return []


def send_feedback(user_id: str, article_id: int, reward: float):
    try:
        payload = {"user_id": user_id, "article_id": article_id, "reward": reward}
        r = requests.post(f"{API_URL}/feedback", json=payload)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def get_feedback_stats():
    try:
        r = requests.get(f"{API_URL}/feedback/stats")
        r.raise_for_status()
        return r.json()
    except Exception:
        return []
