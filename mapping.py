from flask import render_template, request, flash, jsonify
from db import get_db, query_db
import sqlite3


def mapping(app):

    @app.route('/mapping', methods=['GET', 'POST'])
    def staff_mapping():
        db = get_db()
        selected_department = ""
        selected_semester = ""
        selected_staff = ""
        selected_subject = ""
        
        if request.method == 'GET':
            staff_list = query_db("SELECT * FROM staff")
            subject_list = query_db("SELECT * FROM subjects")
        
        if request.method == 'POST':
            selected_staff      = request.form['staff_id']
            selected_subject    = request.form['subject_id']
            selected_department = request.form['department']
            selected_semester   = request.form['semester']

        try:
            query_db("""
                INSERT INTO staff_subject_map 
                (staff_id, subject_id)
                VALUES (?, ?)
            """, (selected_staff, selected_subject))

            flash("Mapping saved successfully!", "success")
            
             # Always fetch filtered data based on selected values
            subject_query = "SELECT * FROM subjects WHERE 1=1"
            subject_params = []

            if selected_department:
                subject_query += " AND department = ?"
                subject_params.append(selected_department)

            if selected_semester:
                subject_query += " AND semester = ?"
                subject_params.append(selected_semester)

            subjects = db.execute(subject_query, subject_params).fetchall()

            staff_query = "SELECT * FROM staff WHERE 1=1"
            staff_params = []

            if selected_department:
                staff_query += " AND department = ?"
                staff_params.append(selected_department)

            staff = db.execute(staff_query, staff_params).fetchall()


        except sqlite3.IntegrityError:
            flash("This mapping already exists!", "error")

        staff_list = query_db("SELECT id, name FROM staff")
        subject_list = query_db("""
            SELECT id, subject_name, department, semester 
            FROM subjects
        """)

        mappings = query_db("""
            SELECT s.name, sub.subject_name, sub.department, sub.semester
            FROM staff_subject_map m
            JOIN staff s ON m.staff_id = s.id
            JOIN subjects sub ON m.subject_id = sub.id
        """)

        return render_template(
            "staff/mapping.html",
            staff_list          =staff_list,
            subject_list        = subject_list,
            selected_department = selected_department,
            selected_semester   = selected_semester,
            selected_staff      = selected_staff,
            selected_subject    = selected_subject,
            mappings            = mappings
        )   
