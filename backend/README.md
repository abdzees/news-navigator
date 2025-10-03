Backend skeleton for news-navigator.

This folder contains a FastAPI backend scaffold including:
- API routes in app/api/routes
- Core configuration in app/core
- Models for bandits and embeddings in app/models
- Services to orchestrate news fetching, recommendations and feedback
- Simple SQLite DB utilities in app/db

Next steps:
- Implement services using NewsAPI and SentenceTransformers
- Switch DB code to async (SQLModel/SQLAlchemy) for production
- Add tests and CI

# Backend quickstart

1. Create venv and install deps:
   python -m venv .venv
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force; .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt

2. Create .env from .env.example and add NEWSAPI_KEY.
3. Run the backend:
   .\run.ps1

Deployment to Render:
- Ensure `Procfile` exists (provided).
- Set necessary environment variables (NEWSAPI_KEY, DATABASE_URL) in Render.
- Use `uvicorn app.main:app` as the web process.
