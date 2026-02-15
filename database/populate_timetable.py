def populate_timetable(cursor):
    cursor.execute("SELECT id FROM departments WHERE name='BSc IT'")
    dept_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM subjects WHERE subject_name='Programming in C'")
    subject_id = cursor.fetchone()[0]

    timetable_entries = [
        (dept_id, 1, "Monday", 1, subject_id, None),
        (dept_id, 1, "Monday", 2, subject_id, None)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO timetable
        (department_id, semester, day, period, subject_id, staff_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, timetable_entries)
