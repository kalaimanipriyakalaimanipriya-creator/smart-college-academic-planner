def populate_staff(cursor):
    cursor.execute("SELECT id FROM departments WHERE name='BSc IT'")
    dept_id = cursor.fetchone()[0]

    staff = [
        ("Arun Kumar", "arun@college.edu", "arun", "pass123", dept_id, "Assistant Professor"),
        ("Meena Devi", "meena@college.edu", "meena", "pass123", dept_id, "Associate Professor")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO staff
        (name, email, username, password, department_id, designation)
        VALUES (?, ?, ?, ?, ?, ?)
    """, staff)
