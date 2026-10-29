# Student Management System (Flask + SQLite)

Working student dashboard with **200 fictional sample students**. Supports search, add, edit and delete.

## Run locally (Windows)
1. Extract this ZIP, open the extracted project folder.
2. Open a terminal in that folder.
3. Run `py -m pip install -r requirements.txt`
4. Run `py app.py`
5. Open http://127.0.0.1:5000/

## Deploy on Render
- Push the extracted project files to a GitHub repository.
- Create a Render **Web Service** (Python).
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Visit the Render service URL, not `/api/students`, to see the dashboard.

Note: SQLite files on Render's ephemeral filesystem can reset on redeployment/restart. For persistent edits, attach a persistent disk and configure the DB path, or use managed PostgreSQL. The packaged database includes 200 fictional records on first deployment.
