from flask import render_template, request, flash, jsonify
from db import get_db, query_db
import sqlite3

def admin_routes(app):

    @app.route("/storeTotal", methods=["POST"])
    def store_total():

        data = request.get_json()
        total = data.get("total")
        item = data.get("value")   # student / staff / department ...

        column_map = {
            "student": "total_student",
            "staff": "total_staff",
            "department": "total_department",
            "course": "total_course",
            "placement": "total_placement"
        }

        if item not in column_map:
            return jsonify({"message": "Invalid item"}), 400

        column = column_map[item]

        db = get_db()
        db.execute(f"""
            UPDATE college_overview
            SET {column} = ?
            WHERE id = 1
        """, (total,))
        db.commit()

        return jsonify({"message": "Updated successfully"})