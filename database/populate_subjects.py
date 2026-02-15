def populate_subjects(cursor):
    cursor.execute("SELECT id FROM departments WHERE name='BSc IT'")
    dept_id = cursor.fetchone()[0]

    subjects = [
        (dept_id, 1, "Programming in C", "theory", 4),
        (dept_id, 1, "Digital Computer Fundamentals", "theory", 4),
        (dept_id, 1, "Mathematics I", "theory", 4),
        (dept_id, 1, "English I", "theory", 3),
        (dept_id, 1, "Environmental Studies", "theory", 3),
        (dept_id, 1, "C Programming Lab", "lab", 4),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO subjects
        (department_id, semester, subject_name, subject_type, hours_per_week)
        VALUES (?, ?, ?, ?, ?)
    """, subjects)
