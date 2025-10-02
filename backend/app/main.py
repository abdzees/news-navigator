"""
Entry point for the backend FastAPI application.

This module creates the FastAPI app, includes routers and defines startup/shutdown
hooks. Replace placeholder logic with real initialization (DB, models, embeddings,
external API clients) during Stage 2.
"""

from dotenv import load_dotenv
# Load .env from the working directory (e.g. backend/.env). This allows setting
# NEWSAPI_KEY and other secrets without committing them to the repo.
load_dotenv()

from fastapi import FastAPI

# Import routers (module structure is prepared in api.routes)
from app.api.routes import articles, recommend, feedback

app = FastAPI(title="news-navigator-backend", version="0.1.0")

# Include route modules
app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
app.include_router(recommend.router, prefix="/api/recommend", tags=["recommend"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["feedback"])


@app.on_event("startup")
async def on_startup():
    """Initialize DB connections, ML models and external API clients here."""
    # TODO: initialize database (app.state.db), load embeddings model, bandit state
    # Example: app.state.db = await database.connect()
    pass


@app.on_event("shutdown")
async def on_shutdown():
    """Clean up resources on shutdown."""
    # TODO: close DB connections, persist model state, etc.
    pass


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
