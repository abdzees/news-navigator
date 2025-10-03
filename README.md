# news-navigator

Personalized news recommender using RL bandits and NLP embeddings.

Structure:
- backend/: FastAPI backend, ML logic, DB
- frontend/: Streamlit UI

Quickstart (dev):
1. Start backend
   cd backend
   .\run.ps1

2. Start frontend
   cd frontend
   .\run.ps1 start

Deployment notes:
- Backend intended for Render: include `backend/Procfile` and `requirements.txt`.
- Frontend intended for HuggingFace Spaces: include `frontend/requirements.txt` and `frontend/README.md`.

Architecture and docs in /docs
