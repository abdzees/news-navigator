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
