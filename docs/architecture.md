# Architecture Overview

This document describes the high-level architecture of news-navigator.

Components:

- Frontend (Streamlit): user-facing app that fetches articles and submits feedback.
- Backend (FastAPI): provides API endpoints for articles, recommendations and feedback. Contains ML logic (embeddings, bandit) and DB persistence.
- Database (SQLite): stores articles, feedback and bandit state.

Flow:
1. Frontend requests articles from Backend (/api/articles).
2. Users interact and provide feedback (POST /api/feedback).
3. Feedback is persisted and used to update the BanditAgent.
4. Recommendations are served via bandit + optional embedding similarity (POST /api/recommend).

Database schema (simplified ERD):

- articles(id PK, title, description, url, source)
- feedback(id PK, user_id, article_id FK->articles.id, category, reward, metadata, timestamp)
- bandit_state(arm PK, count, value)

Data flow description:
- Article ingestion: NewsService fetches articles from NewsAPI and may persist them to `articles`.
- Recommendation: RecommenderService selects a category via BanditAgent and filters candidate articles; embeddings may refine similarity-based ranking.
- Feedback loop: Frontend sends feedback; backend persists to `feedback` and updates `bandit_state` to improve future recommendations.

API endpoints overview:
- GET /api/articles?category=... -> list articles
- GET /api/articles/{id} -> get article
- POST /api/recommend -> request recommendations for user
- POST /api/feedback -> submit feedback event
- GET /api/feedback/stats -> aggregated feedback per category

Deployment:
- Backend: Deploy to Render using `Procfile` and `requirements.txt`.
- Frontend: Deploy to HuggingFace Spaces as a Streamlit app using `frontend/requirements.txt`.

Diagram (ASCII):

Frontend (Streamlit)
        |
        v
Backend (FastAPI) <-> SQLite DB
        ^
        |
   External API (NewsAPI)

