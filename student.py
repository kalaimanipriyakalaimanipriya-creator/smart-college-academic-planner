from flask import render_template, request
from db import query_db

def student_routes(app):

    @app.route("/student", methods=["GET", "POST"])
    def student_view():
        timetable = None
        time_map = {
            1: "10:00-10:50",
            2: "10:50-11:40",
            3: "11:40-12:30",
            4: "1:30-2:30",
            5: "2:30-3:30"
        }

        if request.method == "POST":
            rows = query_db("""
                SELECT day, period, subject_name
                FROM timetable
                WHERE semester=?
                ORDER BY day, period
            """, (request.form["semester"],))

            timetable = [(d, time_map[p], s) for d, p, s in rows]

        return render_template("student_view.html", timetable=timetable)
