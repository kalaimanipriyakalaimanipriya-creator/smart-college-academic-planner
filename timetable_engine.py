# timetable_engine.py

def generate_smart_timetable(query_db, semester, department):

    days = ["Day-1", "Day-2", "Day-3", "Day-4", "Day-5"]
    max_periods = 5

    # Clear old timetable
    query_db(
        "DELETE FROM timetable WHERE department=? AND semester=?",
        (department, semester)
    )

    subjects = query_db("""
        SELECT s.id, s.subject_name, s.subject_type, s.hours_per_week,
               m.staff_id
        FROM subjects s
        LEFT JOIN staff_subject_map m ON s.id = m.subject_id
        WHERE s.department=? AND s.semester=?
    """, (department, semester))

    timetable = {
        day: {p: None for p in range(1, max_periods + 1)}
        for day in days
    }

    staff_busy = {day: {p: set() for p in range(1, max_periods+1)} for day in days}
    subject_daily_count = {sub[0]: {day: 0 for day in days} for sub in subjects}

    # ---- SMART LOGIC HERE ----
    # (Place labs + theory logic here exactly as given earlier)

    # ---- SAVE ----
    for day in days:
        for period in range(1, max_periods + 1):
            cell = timetable[day][period]
            if cell:
                sub_id, staff_id = cell

                query_db("""
                    INSERT INTO timetable
                    (department, semester, day, period, subject_id, staff_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (department, semester, day, period, sub_id, staff_id))

    return True
