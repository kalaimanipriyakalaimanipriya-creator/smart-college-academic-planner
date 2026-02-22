from flask import render_template, request, redirect, session, url_for, flash, jsonify
from db import query_db, get_db
from utils.security import hash_password
# import sqlite3

def staff_routes(app):

    @app.route("/staff", methods=["GET", "POST"])
    def staff_dashboard():
        # if session.get("role") != "staff":
        #     return redirect(url_for("login"))

        if request.method == "POST":
            query_db("""
                INSERT INTO subjects
                (department, semester, subject_name, subject_type, hours_per_week)
                VALUES (?,?,?,?,?)
            """, (
                request.form["department"],
                request.form["semester"],
                request.form["subject"],
                request.form["type"],
                request.form["hours"]
            ))

        return render_template("staff/staff_dashboard.html")

    @app.route("/dashboard", methods=["GET", "POST"])
    def dashboard():
        return render_template("dashboard.html")
    
    @app.route("/staff/check-availability", methods=["POST"])
    def check_staff_availability():
        data = request.get_json()
        email = data.get("email", "").lower()
        username = data.get("username", "").lower()
        
        print("username " , username)
        print("email " , email);

        user = query_db(
            "SELECT id FROM staff WHERE email = ? OR username = ?",
            (email, username),
            one=True
        )

        if user:
            return jsonify({"exists": True})
        else:
            return jsonify({"exists": False})
        
    @app.route("/staff/forgot-password", methods=["POST"])
    def forgot_password():
        username = request.form("username").lower()
        
        print("username " , username)

        user = query_db(
            "SELECT id FROM staff WHERE email = ? OR username = ?",
            (username),
            one=True
        )

        if user:
            return jsonify({"exists": True})
        else:
            return jsonify({"exists": False})
        
        
    @app.route("/staff/filter-staff-by-dept", methods=["POST"])
    def filter_staff_by_dept():
        data = request.get_json()
        department = data.get("department")

        db = get_db()
        staff = db.execute(
            "SELECT id, name FROM staff WHERE department = ?",
            (department,)
        ).fetchall()

        staff_list = [
            {"id": row["id"], "name": row["name"]}
            for row in staff
        ]

        return jsonify(staff_list)
    
    @app.route("/staff/filter-subject-by-staff", methods=["POST"])
    def filter_subject_by_staff():
        data = request.get_json()
        staff_id = data.get("staff_id")

        db = get_db()

        # Get department from staff table
        staff = db.execute(
            "SELECT department FROM staff WHERE id = ?",
            (staff_id,)
        ).fetchone()

        if not staff:
            return jsonify([])

        department = staff["department"]

        subjects = db.execute(
            """
            SELECT id, subject_name, semester
            FROM subjects
            WHERE department = ?
            ORDER BY semester
            """,
            (department,)
        ).fetchall()

        subject_list = [
            {
                "id": row["id"],
                "subject_name": row["subject_name"],
                "semester": row["semester"]
            }
            for row in subjects
        ]

        return jsonify(subject_list)
    
    @app.route("/filter-data", methods=["POST"])
    def filter_data():

        data = request.get_json()

        semester = data.get("semester")
        department = data.get("department")

        db = get_db()

        # ----------------------
        # Build Subject Query
        # ----------------------
        subject_query = "SELECT id, subject_name, semester FROM subjects WHERE 1=1"
        subject_params = []

        if department:
            subject_query += " AND department = ?"
            subject_params.append(department)

        if semester:
            subject_query += " AND semester = ?"
            subject_params.append(semester)

        subjects = db.execute(subject_query, subject_params).fetchall()

        subject_list = [
            {
                "id": row["id"],
                "subject_name": row["subject_name"],
                "semester": row["semester"]
            }
            for row in subjects
        ]

        # ----------------------
        # Build Staff Query
        # ----------------------
        staff_query = "SELECT id, name FROM staff WHERE 1=1"
        staff_params = []

        if department:
            staff_query += " AND department = ?"
            staff_params.append(department)

        staff = db.execute(staff_query, staff_params).fetchall()

        staff_list = [
            {"id": row["id"], "name": row["name"]}
            for row in staff
        ]

        return jsonify({
            "subjects": subject_list,
            "staff": staff_list
        })
