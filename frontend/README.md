# Frontend (Streamlit) for News Navigator

This frontend runs with Streamlit and communicates with the backend API using the `API_URL` environment variable.

Run locally:

1. Create venv and install dependencies
   python -m venv .venv
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force; .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt

2. Ensure `frontend/.env` contains API_URL pointing to the backend, then run:
   $env:API_URL = "http://127.0.0.1:8000/api"; streamlit run app.py
