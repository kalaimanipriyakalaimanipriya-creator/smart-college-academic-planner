from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

# --------------------------------------------------
# Flask App Configuration
# --------------------------------------------------
app = Flask(__name__)
app.secret_key = "smart_timetable_secret"

DB_NAME = "database.db"

# --------------------------------------------------
# Database Connection Helper
# --------------------------------------------------
def get_db():
    return sqlite3.connect(DB_NAME)

# --------------------------------------------------
# Database Initialization (SAFE & REUSABLE)
# --------------------------------------------------
def init_db():
    db = get_db()

    # Create tables from schema.sql
    with open("database/schema.sql", "r") as f:
        db.executescript(f.read())

    cur = db.cursor()

    # Insert default users only if table is empty
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("staff", "staff123", "staff")
        )
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("student", "student123", "student")
        )

    db.commit()
    db.close()

# --------------------------------------------------
# Login Route (Staff / Student)
# --------------------------------------------------
@app.route("/academic-planner/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )
        result = cur.fetchone()
        db.close()

        if result:
            session["role"] = result[0]
            if result[0] == "staff":
                return redirect("/staff")
            else:
                return redirect("/student")

    return render_template("login.html")

# --------------------------------------------------
# Staff Dashboard – Add Subjects
# --------------------------------------------------
@app.route("/staff", methods=["GET", "POST"])
def staff_dashboard():
    if request.method == "POST":
        department = "BSc IT"
        semester = request.form["semester"]
        subject = request.form["subject"]
        subject_type = request.form["type"]
        hours = request.form["hours"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO subjects
            (department, semester, subject_name, subject_type, hours_per_week)
            VALUES (?, ?, ?, ?, ?)
            """,
            (department, semester, subject, subject_type, hours)
        )
        db.commit()
        db.close()

    return render_template("staff_dashboard.html")

# --------------------------------------------------
# Timetable Generation Logic
# --------------------------------------------------
@app.route("/generate/<int:semester>")
def generate_timetable(semester):
    department = "BSc IT"

    db = get_db()
    cur = db.cursor()

    # Clear old timetable
    cur.execute(
        "DELETE FROM timetable WHERE department=? AND semester=?",
        (department, semester)
    )

    # Fetch subjects
    cur.execute(
        """
        SELECT subject_name, subject_type, hours_per_week
        FROM subjects
        WHERE department=? AND semester=?
        """,
        (department, semester)
    )
    subjects = cur.fetchall()

    days = ["Day1", "Day2", "Day3", "Day4", "Day5", "Day6"]
    day_index = 0
    period = 1

    for subject, s_type, hours in subjects:

        if s_type == "lab":
            # Lab = 2 continuous periods
            cur.execute(
                "INSERT INTO timetable VALUES (NULL,?,?,?,?,?)",
                (department, semester, days[day_index], period, subject)
            )
            cur.execute(
                "INSERT INTO timetable VALUES (NULL,?,?,?,?,?)",
                (department, semester, days[day_index], period + 1, subject)
            )
            period += 2

        else:
            # Theory subjects
            for _ in range(int(hours)):
                cur.execute(
                    "INSERT INTO timetable VALUES (NULL,?,?,?,?,?)",
                    (department, semester, days[day_index], period, subject)
                )
                period += 1

        # Move to next day if periods exceed 5
        if period > 5:
            period = 1
            day_index += 1
            if day_index >= len(days):
                break

    db.commit()
    db.close()

    return redirect("/student")

# --------------------------------------------------
# Student Timetable View
# --------------------------------------------------
@app.route("/student", methods=["GET", "POST"])
def student_view():
    timetable = None

    # Period → Time mapping
    time_slots = {
        1: "10:00 - 10:50",
        2: "10:50 - 11:40",
        3: "11:40 - 12:30",
        4: "1:30 - 2:30",
        5: "2:30 - 3:30"
    }

    if request.method == "POST":
        semester = request.form["semester"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            SELECT day, period, subject_name
            FROM timetable
            WHERE semester=?
            ORDER BY day, period
            """,
            (semester,)
        )
        rows = cur.fetchall()
        db.close()

        # Add time slot to each row
        timetable = []
        for day, period, subject in rows:
            time = time_slots.get(period, "N/A")
            timetable.append((day, time, subject))

    return render_template("student_view.html", timetable=timetable)


# Add this anywhere in app.py
@app.context_processor
def inject_user():
    # This makes 'current_user' available in all your HTML templates
    user_role = session.get('role')
    return dict(current_user_role=user_role)

# --------------------------------------------------
# App Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    init_db()          # ALWAYS ensure DB & tables exist
    app.run(debug=True)
