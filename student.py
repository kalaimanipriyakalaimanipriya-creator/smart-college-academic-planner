from flask import jsonify, render_template, request
from db import query_db

def student_routes(app):

    @app.route("/student", methods=["GET", "POST"])
    def student_view():
        data = request.get_json()
        print('printing incomoing data: ', data)
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
            
            selected_department = data.get("department_map")
            selected_semester   = int(data.get("semester_map"))
            # Check types before executing
            print(f"DEBUG: semester type: {type(selected_semester)}, value: {selected_semester}")
            print(f"DEBUG: department type: {type(selected_department)}, value: {selected_department}")

            searched = True
            rows = query_db("""
                    SELECT 
                        t.day, 
                        t.period, 
                        s.subject_name
                    FROM timetable t
                    JOIN subjects s ON t.subject_id = s.id
                WHERE CAST(t.semester AS INTEGER)=?
                AND  t.department=?
                ORDER BY day, period
            """, (selected_semester, selected_department))

            print('rigth after DB call VIew TT')
            print(rows)

            # 2. Handle Empty Case
            if not rows:
                print(f"No records found for Sem: {selected_semester}, Dept: {selected_department}")
                return jsonify({
                    "grid": grid, 
                    "success": True, 
                    "message": "No timetable data found." 
                })

            # 1. Initialize the grid with empty strings
            days = ["DAY-1", "DAY-2", "DAY-3", "DAY-4", "DAY-5"]
            grid = {d: {str(p): "" for p in range(1, 6)} for d in days}

            # 2. Process rows using column names (MUST MATCH SQL SELECT)
            for row in rows:
                # Use .upper() and strip() to ensure "Day-1" becomes "DAY-1"
                db_day = str(row['day']).upper().strip()
                db_period = str(row['period']).strip()
                subj_name = row['subject_name']

                # Debug each row to see why it's missing the grid
                # print(f"Checking row: {db_day} | {db_period} | {subj_name}")

                if db_day in grid:
                    grid[db_day][db_period] = subj_name
                else:
                    print(f"FAIL: {db_day} not found in grid keys: {list(grid.keys())}")

            print(f"FINAL GRID: {grid}")

            return jsonify({"success": True,
                            "grid": grid,
                            "time_map": time_map,
                            "searched": searched,
                            })
        
        return render_template(
            "student_view.html",
            time_map = time_map,
            searched = searched
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
