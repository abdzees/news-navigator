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

