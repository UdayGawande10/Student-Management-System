from flask import Flask, request, jsonify, render_template
import sqlite3
from pathlib import Path
import re

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "students.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            class_name TEXT NOT NULL,
            marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100),
            contact TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Seed only when the table is empty, so the application looks populated on first run.
    count = conn.execute("SELECT COUNT(*) AS c FROM students").fetchone()["c"]
    if count == 0:
        sample = [
            ("Aarav Patil", "B1/01", "B.Tech CSE", 82, "9876543210"),
            ("Riya Sharma", "B1/02", "B.Tech CSE", 91, "9123456780"),
            ("Kabir Joshi", "B1/03", "B.Tech CSE", 76, "9988776655"),
        ]
        conn.executemany(
            "INSERT INTO students (name, roll_no, class_name, marks, contact) VALUES (?, ?, ?, ?, ?)",
            sample,
        )
    conn.commit()
    conn.close()


def validate_student(data):
    required = ["name", "roll_no", "class_name", "marks", "contact"]
    for field in required:
        if field not in data or str(data[field]).strip() == "":
            return f"{field.replace('_', ' ').title()} is required."

    name = str(data["name"]).strip()
    roll_no = str(data["roll_no"]).strip()
    class_name = str(data["class_name"]).strip()
    contact = str(data["contact"]).strip()

    try:
        marks = float(data["marks"])
    except (TypeError, ValueError):
        return "Marks must be a number."

    if len(name) < 2:
        return "Name must contain at least 2 characters."
    if len(roll_no) > 30:
        return "Roll number is too long."
    if not 0 <= marks <= 100:
        return "Marks must be between 0 and 100."
    if not re.fullmatch(r"[6-9]\d{9}", contact):
        return "Contact must be a valid 10-digit Indian mobile number."

    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/api/students")
def list_students():
    query = request.args.get("q", "").strip()
    conn = get_db()
    if query:
        like = f"%{query}%"
        rows = conn.execute(
            """
            SELECT id, name, roll_no, class_name, marks, contact
            FROM students
            WHERE name LIKE ? OR roll_no LIKE ? OR class_name LIKE ?
            ORDER BY id DESC
            """,
            (like, like, like),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, name, roll_no, class_name, marks, contact FROM students ORDER BY id DESC"
        ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.post("/api/students")
def add_student():
    data = request.get_json(silent=True) or {}
    error = validate_student(data)
    if error:
        return jsonify({"error": error}), 400

    conn = get_db()
    try:
        cur = conn.execute(
            """
            INSERT INTO students (name, roll_no, class_name, marks, contact)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                data["name"].strip(),
                data["roll_no"].strip(),
                data["class_name"].strip(),
                float(data["marks"]),
                data["contact"].strip(),
            ),
        )
        conn.commit()
        student_id = cur.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Roll number already exists."}), 409

    row = conn.execute(
        "SELECT id, name, roll_no, class_name, marks, contact FROM students WHERE id = ?",
        (student_id,),
    ).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


@app.put("/api/students/<int:student_id>")
def update_student(student_id):
    data = request.get_json(silent=True) or {}
    error = validate_student(data)
    if error:
        return jsonify({"error": error}), 400

    conn = get_db()
    try:
        cur = conn.execute(
            """
            UPDATE students
            SET name = ?, roll_no = ?, class_name = ?, marks = ?, contact = ?
            WHERE id = ?
            """,
            (
                data["name"].strip(),
                data["roll_no"].strip(),
                data["class_name"].strip(),
                float(data["marks"]),
                data["contact"].strip(),
                student_id,
            ),
        )
        if cur.rowcount == 0:
            conn.close()
            return jsonify({"error": "Student not found."}), 404
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Roll number already exists."}), 409

    row = conn.execute(
        "SELECT id, name, roll_no, class_name, marks, contact FROM students WHERE id = ?",
        (student_id,),
    ).fetchone()
    conn.close()
    return jsonify(dict(row))


@app.delete("/api/students/<int:student_id>")
def delete_student(student_id):
    conn = get_db()
    cur = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({"error": "Student not found."}), 404
    return jsonify({"message": "Student deleted successfully."})


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
