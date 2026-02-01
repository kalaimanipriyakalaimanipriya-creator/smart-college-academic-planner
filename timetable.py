from flask import redirect
from db import query_db

def timetable_routes(app):

    @app.route("/generate/v1/<int:semester>")
    def generate_timetable_v1(semester):
        department = "BSc IT"
        days = ["Day1", "Day2", "Day3", "Day4", "Day5"]

        query_db(
            "DELETE FROM timetable WHERE department=? AND semester=?",
            (department, semester)
        )

        subjects = query_db("""
            SELECT subject_name, subject_type, hours_per_week
            FROM subjects WHERE department=? AND semester=?
        """, (department, semester))

        period, day = 1, 0
        for subject, s_type, hours in subjects:
            repeat = 2 if s_type == "lab" else int(hours)
            for _ in range(repeat):
                query_db(
                    "INSERT INTO timetable VALUES (NULL,            ?,?,?,?,?)",
                    (department, semester, days[day], period, subject)
                )
                period += 1
                if period > 5:
                    period, day = 1, day + 1

        return redirect("/student")
    
    @app.route("/generate/<int:semester>")
    def generate_timetable(semester):
        department = "BSc IT"
        days = ["Day-1", "Day-2", "Day-3", "Day-4", "Day-5", "Day-6"]
        max_periods = 5

        # Clear old timetable
        query_db(
            "DELETE FROM timetable WHERE department=? AND semester=?",
            (department, semester)
        )

        # Fetch subjects
        subjects = query_db("""
            SELECT subject_name, subject_type, hours_per_week
            FROM subjects
            WHERE department=? AND semester=?
        """, (department, semester))

        # Timetable structure
        timetable = {
            day: {p: None for p in range(1, max_periods + 1)}
            for day in days
        }

        # Separate labs and theory
        labs = []
        theory = []

        for name, s_type, hours in subjects:
            if s_type.lower() == "lab":
                labs.append((name, 2))  # lab = 2 periods
            else:
                theory.append((name, int(hours)))

        # -------------------------------
        # Step 1: Place LABS
        # -------------------------------
        day_index = 0
        for lab, duration in labs:
            placed = False
            while not placed and day_index < len(days):
                day = days[day_index]
                for p in range(1, max_periods):
                    if timetable[day][p] is None and timetable[day][p+1] is None:
                        timetable[day][p] = lab
                        timetable[day][p+1] = lab
                        placed = True
                        break
                day_index += 1

        # -------------------------------
        # Step 2: Place THEORY subjects
        # -------------------------------
        for subject, hours in theory:
            day_pointer = 0
            while hours > 0 and day_pointer < len(days):
                day = days[day_pointer]

                # Avoid repeating same subject on same day
                if subject in timetable[day].values():
                    day_pointer += 1
                    continue

                for p in range(1, max_periods + 1):
                    if timetable[day][p] is None:
                        timetable[day][p] = subject
                        hours -= 1
                        break

                day_pointer += 1

        # -------------------------------
        # Step 3: Save to DB
        # -------------------------------
        for day in days:
            for period in range(1, max_periods + 1):
                subject = timetable[day][period]
                if subject:
                    query_db(
                        "INSERT INTO timetable VALUES (NULL,?,?,?,?,?)",
                        (department, semester, day, period, subject)
                    )

        return redirect("/student")

