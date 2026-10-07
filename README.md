# Student Management System — MDM Teacher Assessment

## Selected Aim
**Aim 3 — Student Management System**

A full-stack CRUD web application for adding, viewing, searching, updating and deleting student records.

## Technology
- Frontend: HTML5, CSS3, JavaScript
- Backend: Python Flask
- Database: SQLite
- Frontend tooling: Node.js / npm (optional development tooling)

## Features
- Add student records
- View all records
- Search by name, roll number or class
- Update existing records
- Delete records
- Duplicate roll-number validation
- Marks range validation (0–100)
- Indian 10-digit mobile-number validation
- Dynamic Fetch/AJAX updates without page reload
- REST-style GET, POST, PUT and DELETE endpoints
- SQLite persistent storage
- Responsive interface

## Run locally

### 1. Create a virtual environment
Windows:
`python -m venv venv`
`venv\Scripts\activate`

### 2. Install dependencies
`pip install -r requirements.txt`

### 3. Start the application
`python app.py`

Open:
`http://127.0.0.1:5000`

The SQLite database is created automatically on first run.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/students | List/search students |
| POST | /api/students | Add a student |
| PUT | /api/students/<id> | Update a student |
| DELETE | /api/students/<id> | Delete a student |

## Project structure

student_management_system/
├── app.py
├── requirements.txt
├── package.json
├── README.md
├── report.docx
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
