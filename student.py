from flask import render_template, request
from db import query_db

def student_routes(app):

    @app.route("/student", methods=["GET", "POST"])
    def student_view():

        time_map = {
            1: "10:00-10:50",
            2: "10:50-11:40",
            3: "11:40-12:30",
            4: "1:30-2:30",
            5: "2:30-3:30"
        }
        grid = {}
        searched = False
        
        if request.method == "POST":
            searched = True
            rows = query_db("""
                SELECT day, period, subject_name
                FROM timetable
                WHERE semester=?
                AND department=?
                ORDER BY day, period
            """, (request.form["semester"],request.form["department"]))

            days = ["DAY-1", "DAY-2", "DAY-3", "DAY-4", "DAY-5"]
            periods = [1, 2, 3, 4, 5]

            # 🔹 create empty grid
            grid = {day: {p: "" for p in periods} for day in days}
            
            # days = ["Day-1", "Day-2", "Day-3", "Day-4", "Day-5"]
            # periods = [1, 2, 3, 4, 5, 6]

            # grid = {}

            # for day in days:
            #     grid[day] = {}
            #     for period in periods:
            #         grid[day][period] = ""

            # 🔹 fill grid
            for day, period, subject in rows:
                day = day.upper()
                grid[day][period] = subject

        return render_template(
            "student_view.html",
            grid     = grid,
            time_map = time_map,
            searched = searched,
            mapping = mapping
        )
    
    # def student_view_V1():
    #     timetable = None
    #     time_map = {
    #         1: "10:00-10:50",
    #         2: "10:50-11:40",
    #         3: "11:40-12:30",
    #         4: "1:30-2:30",
    #         5: "2:30-3:30"
    #     }

    #     if request.method == "POST":
    #         rows = query_db("""
    #             SELECT day, period, subject_name
    #             FROM timetable
    #             WHERE semester=?
    #             OR department=?
    #             ORDER BY day, period
    #         """, (request.form["semester"], request.form["department"]))

    #         timetable = [(d, time_map[p], s) for d, p, s in rows]

    #     return render_template("student_view.html", timetable=timetable)
