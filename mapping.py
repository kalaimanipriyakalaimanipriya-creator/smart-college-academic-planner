from flask import render_template, request, flash, jsonify
from db import get_db, query_db
import sqlite3


def mapping(app):

    @app.route('/mapping', methods=['GET', 'POST'])
    def staff_mapping():
        
        if request.method == 'GET':
                staff_list = query_db("SELECT * FROM staff")
                flash("Staff table retrieve successfully!", "success")
                
                subject_list = query_db("SELECT * FROM subjects")
                flash("subjects table retrieve successfully!", "success")
        
        if request.method == 'POST':
            staff_id = request.form['staff_id']
            subject_id = request.form['subject_id']
            department = request.form['department']
            semester = request.form['semester']

        try:
            # query_db("""
            #     INSERT INTO staff_subject_map 
            #     (staff_id, subject_id)
            #     VALUES (?, ?)
            # """, (staff_id, subject_id))

            flash("Mapping saved successfully!", "success")

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
            staff_list=staff_list,
            subject_list=subject_list,
            mappings=mappings
        )   
